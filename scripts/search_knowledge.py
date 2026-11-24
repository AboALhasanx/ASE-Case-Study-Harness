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
    if not terms:
        parser.error("query must contain at least one searchable word")
    # Quote each token and OR them to keep FTS syntax safe and favor broad recall.
    match_query = " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)
    sql = """
        SELECT source, page, chunk_no,
               snippet(chunks_fts, 0, '[', ']', ' … ', 24),
               bm25(chunks_fts) AS score
        FROM chunks_fts
        WHERE chunks_fts MATCH ?
    """
    parameters: list[object] = [match_query]
    if args.source:
        sql += " AND source = ?"
        parameters.append(args.source)
    sql += " ORDER BY score LIMIT ?"
    parameters.append(args.top_k)

    try:
        with sqlite3.connect(f"file:{args.index.resolve().as_posix()}?mode=ro", uri=True) as db:
            rows = db.execute(sql, parameters).fetchall()
    except sqlite3.OperationalError as exc:
        print(f"Search failed: {exc}", file=sys.stderr)
        return 2
    if not rows:
        print("No matching course passages found.")
        return 0
    print(f"Top {len(rows)} passages (SQLite FTS5 BM25; lexical retrieval)\n")
    for rank, (source, page, chunk_no, excerpt, score) in enumerate(rows, start=1):
        print(f"{rank}. [{source}, p. {page}] chunk {chunk_no} | score {score:.4f}")
        print(f"   {excerpt}\n")
    print("Use the PDF page cited above to confirm context before relying on a passage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
