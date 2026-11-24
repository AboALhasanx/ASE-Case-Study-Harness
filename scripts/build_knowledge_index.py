#!/usr/bin/env python3
"""Build a local SQLite FTS5 index over course PDFs, preserving page citations."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "knowledge"
DEFAULT_OUTPUT = ROOT / "knowledge" / "index" / "ase_knowledge.sqlite3"
CHUNK_CHARS = 1800
OVERLAP_CHARS = 240


def normalize(text: str) -> str:
    text = (text.replace("\x00", " ").replace("\u00ad", "")
            .replace("\ufffd", " "))
    return re.sub(r"\s+", " ", text).strip()


def chunks(text: str):
    """Yield overlapping character windows, preferring word boundaries."""
    start = 0
    while start < len(text):
        end = min(start + CHUNK_CHARS, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start + CHUNK_CHARS // 2, end)
            if boundary > start:
                end = boundary
        part = text[start:end].strip()
        if part:
            yield part
        if end == len(text):
            break
        start = max(end - OVERLAP_CHARS, start + 1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                        help="Folder containing source PDFs (default: knowledge/)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="SQLite database path (default: knowledge/index/ase_knowledge.sqlite3)")
    args = parser.parse_args()

    pdfs = sorted(p for p in args.source.glob("*.pdf") if p.is_file())
    if not pdfs:
        print(f"No PDF files found in {args.source}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = args.output.with_name(args.output.name + ".tmp")
    if temporary_output.exists():
        temporary_output.unlink()

    connection = sqlite3.connect(temporary_output)
    try:
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        connection.execute("""
            CREATE TABLE chunks (
                id INTEGER PRIMARY KEY,
                source TEXT NOT NULL,
                page INTEGER NOT NULL,
                chunk_no INTEGER NOT NULL,
                text TEXT NOT NULL,
                UNIQUE(source, page, chunk_no)
            )
        """)
        connection.execute("""
            CREATE VIRTUAL TABLE chunks_fts USING fts5(
                text, source UNINDEXED, page UNINDEXED, chunk_no UNINDEXED,
                tokenize='unicode61 remove_diacritics 2'
            )
        """)
        total_pages = 0
        total_chunks = 0
        empty_text_pages: list[str] = []
        digest = hashlib.sha256()

        with connection:
            for pdf in pdfs:
                digest.update(pdf.name.encode("utf-8"))
                digest.update(pdf.read_bytes())
                reader = PdfReader(str(pdf))
                if reader.is_encrypted:
                    raise ValueError(f"Encrypted PDF cannot be indexed: {pdf.name}")
                for page_number, page in enumerate(reader.pages, start=1):
                    total_pages += 1
                    text = normalize(page.extract_text() or "")
                    if not text:
                        empty_text_pages.append(f"{pdf.name}:p.{page_number}")
                    for chunk_number, part in enumerate(chunks(text), start=1):
                        cursor = connection.execute(
                            "INSERT INTO chunks(source,page,chunk_no,text) VALUES(?,?,?,?)",
                            (pdf.name, page_number, chunk_number, part),
                        )
                        connection.execute(
                            "INSERT INTO chunks_fts(rowid,text,source,page,chunk_no) VALUES(?,?,?,?,?)",
                            (cursor.lastrowid, part, pdf.name, page_number, chunk_number),
                        )
                        total_chunks += 1

            metadata = {
                "schema_version": "1",
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "source_pdf_count": str(len(pdfs)),
                "source_page_count": str(total_pages),
                "indexed_chunk_count": str(total_chunks),
                "source_sha256": digest.hexdigest(),
                "retrieval": "SQLite FTS5 BM25 (lexical)",
                "pages_without_extractable_text": json.dumps(empty_text_pages, ensure_ascii=False),
            }
            connection.executemany("INSERT INTO metadata(key,value) VALUES(?,?)", metadata.items())
        print(f"Indexed {len(pdfs)} PDFs, {total_pages} pages, {total_chunks} chunks")
        print(f"Pages without extractable text: {len(empty_text_pages)}")
        print(f"Database: {args.output}")
        print(f"Source SHA-256: {digest.hexdigest()}")
    finally:
        connection.close()
    temporary_output.replace(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
