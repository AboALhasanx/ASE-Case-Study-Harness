"""Regression coverage for Markdown table fidelity in Word reports."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document
from docx.shared import Inches
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_report.py"


class ReportTables(unittest.TestCase):
    def run_report(self, text, destination=None, force=False):
        source = self.directory / "source.md"
        output = destination or self.directory / "report.docx"
        source.write_text(text, encoding="utf-8")
        command = [sys.executable, str(SCRIPT), str(source), "-o", str(output)]
        if force:
            command.append("--force")
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        return result, output

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def test_escaped_pipes_and_backslashes_remain_in_correct_cells(self):
        source = (
            "# Report\n\n"
            "| Requirement | Description |\n"
            "| --- | --- |\n"
            r"| R1 | A \| B |" "\n"
            r"| R2 | C:\\folder\\file |" "\n"
            r"| R3 | Ends with \|" "\n"
            r"| R4 | \\\| |" "\n"
            r"| R5 | path\name |" "\n"
            "| R6 | |\n"
        )
        result, output = self.run_report(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        table = Document(output).tables[0]
        self.assertEqual(len(table.columns), 2)
        self.assertEqual([row.cells[1].text for row in table.rows], [
            "Description", "A | B", r"C:\folder\file", "Ends with |", r"\|", r"path\name", ""
        ])

    def test_mismatched_body_row_is_rejected_without_replacing_output(self):
        output = self.directory / "report.docx"
        original = b"existing file must survive"
        output.write_bytes(original)
        source = "# Report\n\n| One | Two |\n| --- | --- |\n| A | B | C |\n"
        result, _ = self.run_report(source, output, force=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("line 5: table row has 3 cells; expected 2", result.stderr)
        self.assertEqual(output.read_bytes(), original)

    def test_mismatched_separator_is_rejected_without_output(self):
        source = "# Report\n\n| One | Two |\n| --- | --- | --- |\n| A | B |\n"
        result, output = self.run_report(source)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("line 4: table separator has 3 cells; expected 2", result.stderr)
        self.assertFalse(output.exists())

    def test_relative_image_has_caption_alt_and_fits_page(self):
        figures = self.directory / "figures"
        figures.mkdir()
        Image.new("RGB", (600, 1800), "white").save(figures / "diagram.png")
        result, output = self.run_report("# Report\n\n![Architecture evidence E-01](figures/diagram.png)\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        doc = Document(output)
        self.assertEqual(len(doc.inline_shapes), 1)
        shape = doc.inline_shapes[0]
        section = doc.sections[0]
        self.assertLessEqual(shape.width, section.page_width - section.left_margin - section.right_margin)
        self.assertLessEqual(shape.height, section.page_height - section.top_margin - section.bottom_margin - Inches(0.8))
        self.assertLessEqual(shape.height, Inches(6.0))
        self.assertAlmostEqual(shape.height / shape.width, 3, places=3)
        self.assertEqual(shape._inline.docPr.get("descr"), "Architecture evidence E-01")
        self.assertIn("Architecture evidence E-01", [p.text for p in doc.paragraphs])

    def test_missing_remote_and_escaping_images_do_not_replace_existing_output(self):
        output = self.directory / "report.docx"
        original = b"existing file must survive"
        for image in ("missing.png", "https://example.org/a.png", "../outside.png"):
            with self.subTest(image=image):
                output.write_bytes(original)
                result, _ = self.run_report(f"# Report\n\n![Evidence]({image})\n", output, force=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("line 3:", result.stderr)
                self.assertEqual(output.read_bytes(), original)

    def test_inline_image_is_rejected(self):
        result, output = self.run_report("# Report\n\nText ![Evidence](diagram.png)\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("standalone", result.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
