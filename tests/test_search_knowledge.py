"""Regression checks for lexical course retrieval without external data."""
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "search_knowledge.py"


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.index = Path(self.tmp.name) / "index.sqlite3"
        with sqlite3.connect(self.index) as db:
            db.execute("CREATE VIRTUAL TABLE chunks_fts USING fts5(text, source UNINDEXED, page UNINDEXED, chunk_no UNINDEXED)")
            db.execute("INSERT INTO chunks_fts VALUES(?,?,?,?)", (
                "Multiple choice questions: maintenance (a) corrective (b) adaptive (c) preventive?", "Ch09.pdf", 30, 1))
            db.execute("INSERT INTO chunks_fts VALUES(?,?,?,?)", (
                "Software maintenance includes corrective adaptive and preventive maintenance activities.", "Ch09.pdf", 5, 1))
            db.execute("INSERT INTO chunks_fts VALUES(?,?,?,?)", (
                "Testing identifies defects in software.", "Ch08.pdf", 3, 1))
        db.close()

    def tearDown(self):
        self.tmp.cleanup()

    def search(self, query, *args):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), query, "--index", str(self.index), *args],
                              capture_output=True, text=True, encoding="utf-8", env=env, check=True).stdout

    def test_arabic_terminology_returns_page_reference(self):
        text = self.search("ما هي أنواع صيانة البرمجيات", "--source", "Ch09.pdf")
        self.assertIn("صيانة → maintenance", text)
        self.assertIn("[Ch09.pdf, p. 5]", text)
        self.assertNotIn("[Ch08.pdf", text)

    def test_explanatory_passage_beats_multiple_choice(self):
        text = self.search("corrective adaptive preventive maintenance", "--source", "Ch09.pdf")
        self.assertLess(text.index("[Ch09.pdf, p. 5]"), text.index("[Ch09.pdf, p. 30]"))

    def test_unmapped_query_reports_limit_and_stopwords_are_safe(self):
        self.assertIn("Arabic vocabulary expansion is limited", self.search("موضوع غير معروف"))
        self.assertIn("no searchable terms", self.search("the and why"))

    def test_mixed_query_and_diacritics(self):
        text = self.search("صِيَانَة corrective", "--top-k", "1")
        self.assertIn("[Ch09.pdf, p. 5]", text)


if __name__ == "__main__":
    unittest.main()
