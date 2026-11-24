"""Regression checks for the standalone Master Studio slide builder."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

from pptx import Presentation

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'master_studio' / 'seminar_deck_builder.py'
spec = importlib.util.spec_from_file_location('seminar_deck_builder', SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SlideBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def build(self, text):
        source, target = self.root / 'deck.md', self.root / 'deck.pptx'
        source.write_text(text, encoding='utf-8')
        builder.build(source, target)
        return Presentation(target)

    def test_frontmatter_and_paginate_in_content_are_not_confused(self):
        prs = self.build('---\nmarp: true\npaginate: true\n---\n# First\n'
                         'Important explanation with paginate: 5 pages.\n---\n# Second\n- finding\n')
        self.assertEqual(len(prs.slides), 2)
        texts = [' '.join(shape.text for shape in s.shapes if shape.has_text_frame) for s in prs.slides]
        self.assertIn('paginate: 5 pages', texts[0])
        self.assertIn('Second', texts[1])

    def test_indented_bullets_keep_hierarchy_and_symbols(self):
        prs = self.build('# Findings\n- Parent → next\n  - Child ✓\n')
        paragraphs = [p for s in prs.slides[0].shapes if s.has_text_frame
                      for p in s.text_frame.paragraphs if 'Child' in p.text]
        self.assertEqual(len(paragraphs), 1)
        self.assertEqual(paragraphs[0].level, 1)
        self.assertIn('✓', paragraphs[0].text)
        self.assertTrue(any('→' in s.text for s in prs.slides[0].shapes if s.has_text_frame))

    def test_notes_keep_separator_and_arabic(self):
        prs = self.build('# Findings\n- Result\n::: notes\nشرح بالعربي\n---\nتفصيل\n:::\n')
        self.assertEqual(len(prs.slides), 1)
        notes = prs.slides[0].notes_slide.notes_text_frame.text
        self.assertIn('شرح بالعربي\n---\nتفصيل', notes)

    def test_inline_comment_does_not_discard_content(self):
        prs = self.build('# Findings\n- Claim <!-- private comment --> continues\n')
        texts = ' '.join(shape.text for shape in prs.slides[0].shapes if shape.has_text_frame)
        self.assertIn('Claim  continues', texts)
        self.assertNotIn('private comment', texts)

    def test_unclosed_notes_raise_before_output(self):
        source = self.root / 'bad.md'
        source.write_text('# Findings\n::: notes\nUnclosed\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unclosed speaker notes'):
            builder.build(source, self.root / 'bad.pptx')
        self.assertFalse((self.root / 'bad.pptx').exists())

    def test_fenced_code_rejected_before_splitting_on_separator(self):
        source = self.root / 'fenced.md'
        source.write_text('# Findings\n```text\n---\nimportant\n```\n', encoding='utf-8')
        target = self.root / 'fenced.pptx'
        with self.assertRaisesRegex(ValueError, 'Fenced code blocks are unsupported'):
            builder.build(source, target)
        self.assertFalse(target.exists())


if __name__ == '__main__':
    unittest.main()
