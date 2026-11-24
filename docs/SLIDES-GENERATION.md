# Generating editable case-study slides

`scripts/generate_slides.py` creates a standard 16:9 PowerPoint deck from a small
JSON or Markdown file. Text, shapes, citations, and slide numbers are native PowerPoint
objects and remain editable. The output starts with a cover, followed by one slide for
each input slide. Content is not fact-checked by the generator: verify every claim and
source against the evidence ledger before presenting.

Keep visible slide content and citations in English. Provide an Arabic presenter narration for each slide in a separate `arabic-presenter-script.md` and in the slide's `notes` field. The narration should explain the same evidence without adding unsupported claims. Inspect the notes in a presentation application to confirm Arabic legibility; notes are not visible to the audience in the slide view.

## Install

From the repository root, install the runtime dependencies:

```powershell
python -m pip install -r requirements.txt
```

The generator uses `python-pptx` in the environment used to generate the presentation.

## Run

```powershell
python scripts/generate_slides.py path\to\seminar.json --output path\to\seminar.pptx
python scripts/generate_slides.py path\to\seminar.md --output path\to\seminar.pptx
# Replace an existing deck only when intended
python scripts/generate_slides.py path\to\seminar.json --output path\to\seminar.pptx --force
```

Input is UTF-8. The output directory is created if needed. The CLI exits non-zero and
prints a concise error for malformed input or missing dependencies.
Existing output files are protected by default; pass `--force` to replace one.

## JSON format

```json
{
  "title": "A case study of Project X",
  "subtitle": "Evidence and limitations at commit abc123",
  "slides": [
    {
      "title": "Study boundary",
      "section": "Scope",
      "body": "Review of the repository snapshot identified in the baseline manifest.",
      "bullets": [
        "Observed: the study uses the pinned repository commit.",
        "Unknown: production behavior was not available for inspection."
      ],
      "citations": ["Baseline manifest, commit abc123", "README.md, Installation"],
      "notes": "Explain how the selected boundary was derived from the repository."
    },
    {
      "title": "Lifecycle evidence",
      "layout": "section",
      "section": "Chapter 2",
      "bullets": ["Describe the evidence before classifying the process model."],
      "citations": ["docs/CONTRIBUTING.md, Development workflow"]
    }
  ]
}
```

`title` and a non-empty `slides` array are required. Set `cover_notes` in JSON for the Arabic narration of the automatically created cover slide; set each content slide's `notes` for its narration. Markdown input cannot express cover notes, so use JSON when a cover narration must be embedded. Each slide needs a `title` and may
include `body`, `bullets` (array of strings), `section`, `citations` (string or array),
`notes`, and `layout`. Layout is `content` by default; `section` gives the slide a pale
background for a chapter divider. `notes` are added to the PowerPoint speaker notes
where supported by the installed `python-pptx` version. Citations are also printed on
the slide so that the evidence trail remains visible in exported or printed views.

To keep the generated layout readable, validation limits the deck title to 70
characters, subtitle to 150, slide title to 55, body to 240, and each slide to five
bullets of at most 220 characters each. Estimated bullet text is capped at seven lines
per slide. Each slide may have up to six citations and 350 combined citation characters;
speaker notes are capped at 4,000 characters. If a limit is reached, shorten the wording
or split the material across slides. These are layout limits, not limits on the case
study's underlying evidence or report.

## Markdown format

Use one H1 for the deck title, optional plain text beneath it for the subtitle, and one
H2 for each slide. Top-level `-` bullets become editable bullet paragraphs. Use the
literal `Citations:` and `Notes:` labels to direct following lines to the source footer
and speaker notes respectively.

```markdown
# A case study of Project X
Evidence and limitations at commit abc123

## Study boundary
Review of the repository snapshot identified in the baseline manifest.
- Observed: the study uses the pinned repository commit.
- Unknown: production behavior was not available for inspection.
Citations:
- Baseline manifest, commit abc123
- README.md, Installation
Notes:
Explain how the selected boundary was derived from the repository.

## Lifecycle evidence
- Describe the evidence before classifying the process model.
Citations:
- docs/CONTRIBUTING.md, Development workflow
```

Markdown produces the same content-slide layout as JSON. Use JSON when you need a
section divider or more structured generation from another tool.

## Design and evidence guidance

- The deck uses a restrained teal and slate palette, wide margins, a 16:9 canvas, and
  editable native text and shapes. Keep the source wording concise so slide text stays
  readable at presentation size.
- A useful case-study sequence is: question and scope, target baseline, lifecycle and
  requirements, planning and design, metrics and quality, testing, maintenance,
  synthesis, limitations, and references. Adapt it to the findings rather than filling
  slides to match a fixed template.
- Label claims as Observed, Inferred, Estimated, or Unknown where their status could be
  unclear. Cite material evidence on the same slide using stable paths, line/section
  references, commit IDs, commands and captured results, or dated external sources.
- Avoid placing several dense paragraphs on a slide. Split them or shorten wording;
  inspect the exported deck in PowerPoint or LibreOffice before presenting. The helper
  does not automatically validate claim support, optimal text fit, or academic rules.
