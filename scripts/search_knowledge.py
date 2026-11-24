#!/usr/bin/env python3
"""Search the course knowledge index and return page-addressable evidence."""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "knowledge" / "index" / "ase_knowledge.sqlite3"

# Keep common connective words out of OR queries: they occur on nearly every
# page and can crowd out matches on the actual course concept.
STOPWORDS = set("""a an and are as at be been being but by can could did do does for
from had has have how i if in into is it its may might must of on or our should
that the their them then there these they this to was we were what when where
which who why will with would you your""".split())
QUESTION_MARKER = re.compile(r"(?:\?|\b\d+(?:\.\d+)*\s*[.)])")
INSTRUCTIONAL_MARKER = re.compile(
    r"\b(?:definition|defined as|refers to|is the process|is a technique|"
    r"consists of|therefore|because|for example|in contrast|the objective)\b",
    re.IGNORECASE,
)


def rerank_score(bm25_score: float, text: str) -> float:
    """Apply a small, transparent preference for explanatory prose over exercises."""
    questions = len(QUESTION_MARKER.findall(text))
    # BM25 scores are negative, with more relevant passages closer to -infinity.
    # Add a modest penalty only when the chunk looks strongly question-led.
    question_penalty = min(2.0, max(0, questions - 1) * 0.35)
    explanation_credit = 0.2 if INSTRUCTIONAL_MARKER.search(text) else 0.0
    return bm25_score + question_penalty - explanation_credit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Natural-language or keyword query")
    parser.add_argument("-k", "--top-k", type=int, default=6, help="Maximum results (default: 6)")
    parser.add_argument("--source", help="Limit to a PDF filename, e.g. Ch6.pdf")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX, help="SQLite index path")
    args = parser.parse_args()
    if args.top_k < 1 or args.top_k > 50:
        parser.error("--top-k must be between 1 and 50")
    if not args.index.is_file():
        print(f"Knowledge index not found: {args.index}\nBuild it with scripts/build_knowledge_index.py", file=sys.stderr)
        return 2

    terms = re.findall(r"[\w]+", args.query, flags=re.UNICODE)
    terms = [term for term in terms if term.casefold() not in STOPWORDS]
    if not terms:
        print("Query has no searchable terms after common-word filtering; add a course concept or synonym.")
        return 0
    # Quote each token and OR them to keep FTS syntax safe and favor broad recall.
    match_query = " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)
    sql = """
        SELECT source, page, chunk_no, text,
               snippet(chunks_fts, 0, '[', ']', ' … ', 24),
               bm25(chunks_fts) AS score
        FROM chunks_fts
        WHERE chunks_fts MATCH ?
    """
    parameters: list[object] = [match_query]
    if args.source:
        sql += " AND source = ?"
        parameters.append(args.source)
    # Retrieve a wider lexical candidate set so the lightweight prose-quality
    # adjustment can reorder candidates without changing the index/schema.
    sql += " ORDER BY score LIMIT ?"
    parameters.append(min(500, max(args.top_k * 8, 40)))

    try:
        with sqlite3.connect(f"file:{args.index.resolve().as_posix()}?mode=ro", uri=True) as db:
            rows = db.execute(sql, parameters).fetchall()
    except sqlite3.OperationalError as exc:
        print(f"Search failed: {exc}", file=sys.stderr)
        return 2
    if not rows:
        print("No matching course passages found.")
        return 0
    rows.sort(key=lambda row: rerank_score(row[5], row[3]))
    rows = rows[:args.top_k]
    print(f"Top {len(rows)} passages (FTS5 BM25 with modest explanatory-prose reranking; lexical retrieval)\n")
    for rank, (source, page, chunk_no, text, excerpt, score) in enumerate(rows, start=1):
        adjusted = rerank_score(score, text)
        print(f"{rank}. [{source}, p. {page}] chunk {chunk_no} | adjusted score {adjusted:.4f} (BM25 {score:.4f})")
        print(f"   {excerpt}\n")
    print("Use the PDF page cited above to confirm context before relying on a passage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
