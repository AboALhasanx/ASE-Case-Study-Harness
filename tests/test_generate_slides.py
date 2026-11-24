"""Regression checks for speaker notes in generated presentations."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pptx import Presentation

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'generate_slides.py'
spec = importlib.util.spec_from_file_location('generate_slides', SCRIPT)
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class SlideNotesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_arabic_notes_and_english_sources_survive_round_trip(self):
        source = self.root / 'source.json'
        target = self.root / 'deck.pptx'
        source.write_text(json.dumps({
            'title': 'Evidence review',
            'cover_notes': 'أهلاً بكم في عرض دراسة الحالة',
            'slides': [{'title': 'Findings', 'bullets': ['The evidence'],
                        'notes': 'هذا شرح للطلبة\nونذكر الاستنتاج',
                        'citations': ['E-01: README.md']}],
        }, ensure_ascii=False), encoding='utf-8')
        run = subprocess.run([sys.executable, str(SCRIPT), str(source), '-o', str(target)],
                             capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(run.returncode, 0, run.stderr)
        deck = Presentation(target)
        self.assertIn('أهلاً بكم', deck.slides[0].notes_slide.notes_text_frame.text)
        self.assertEqual(deck.slides[0].notes_slide.notes_text_frame.paragraphs[0]._p.pPr.get('rtl'), '1')
        slide = deck.slides[1]
        notes = slide.notes_slide.notes_text_frame
        self.assertIn('هذا شرح للطلبة\nونذكر الاستنتاج', notes.text)
        self.assertIn('E-01: README.md', notes.text)
        arabic = [p for p in notes.paragraphs if 'هذا شرح' in p.text]
        self.assertEqual(len(arabic), 1)
        self.assertEqual(arabic[0]._p.pPr.get('rtl'), '1')
        self.assertIn('E-01: README.md', ' '.join(s.text for s in slide.shapes if s.has_text_frame))

    def test_markdown_notes_remain_arabic(self):
        parsed = generator.parse_markdown('# Report\n## Finding\n- Evidence\nNotes:\nشرح باللغة العربية\n')
        self.assertEqual(parsed['slides'][0]['notes'], 'شرح باللغة العربية')
        target = self.root / 'deck.pptx'
        generator.build_presentation(parsed, target)
        self.assertIn('شرح باللغة العربية', Presentation(target).slides[1].notes_slide.notes_text_frame.text)

    def test_unavailable_speaker_notes_raise_and_do_not_disappear(self):
        class UnsupportedSlide:
            @property
            def notes_slide(self):
                raise NotImplementedError('notes unavailable')

        with self.assertRaisesRegex(ValueError, 'Speaker notes cannot be embedded'):
            generator.add_notes(UnsupportedSlide(), 'شرح بالعربي', [])

    def test_unavailable_notes_without_content_are_not_needed(self):
        class UnsupportedSlide:
            @property
            def notes_slide(self):
                raise NotImplementedError('notes unavailable')

        self.assertIsNone(generator.add_notes(UnsupportedSlide(), '', []))


if __name__ == '__main__':
    unittest.main()
