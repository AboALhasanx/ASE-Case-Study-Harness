# Word report generation

The harness authors reports in Markdown so the evidence and citations remain easy to review in Git. Generate a shareable Word document from a completed report with:

```powershell
python -m pip install python-docx
python scripts/generate_report.py case-studies/<team-slug>/report.md
```

By default, the DOCX is written beside the Markdown file with the same base name. Set a destination explicitly with `--output` (or `-o`):

```powershell
python scripts/generate_report.py case-studies/<team-slug>/report.md --output case-studies/<team-slug>/deliverables/final-report.docx
```

An existing output is preserved: the command stops with an error if the destination already exists. Pass `--force` only when you intend to replace it.

The generator uses only the Python standard library and `python-docx`. It does not fetch sources, rewrite claims, infer missing report content, or replace the Markdown source. Its compact Markdown reader supports headings (levels 1–6), paragraphs, bold and italic spans, inline code, links, ordered and unordered lists, fenced code blocks, and simple pipe tables. Before writing the DOCX it checks for unsupported images, footnotes, nested lists, block quotes, embedded HTML, and aligned pipe tables, then fails with a line-specific message. This prevents these constructs from being silently dropped or misrepresented. Convert them to a supported form before running the generator; images and footnotes can also be added directly in Word after conversion. More complex constructs may need similar simplification.

The output uses Cambria body text, a clear heading ladder, readable margins and spacing, shaded repeating table headers, a running report title, and a centered footer with page numbering. Inspect the finished DOCX in Word or LibreOffice before submission, especially tables and page breaks. The Markdown report remains the source of truth and should be checked for evidence traceability and course-specific requirements.

For command options, run `python scripts/generate_report.py --help`.
