# Tools copied from Master Studio

These utilities were copied from `90_Shared_Toolbox/tools` in the Master Studio project. The project's Apache License 2.0 is included in this directory. This copy is modified: the Office converter does not dismiss other Office windows' dialogs, rejects existing output paths, and no longer treats ordinary Cambria as a math font; the seminar builder checks missing/multiple images and protects existing outputs.

## Seminar with images and speaker notes

`seminar_deck_builder.py` builds an editable PPTX from slide blocks separated by `---`. It accepts one image per content slide and a `::: notes` block. Requires `python-pptx` and Pillow. For a sample syntax see the module's opening documentation.

```text
python scripts/master_studio/seminar_deck_builder.py deck.md -o deck.pptx
```

This is an additional visual option; inspect every slide for overflow, verify all sources, and do not rely on it to check citations or layout. It does not support more than one image on a slide or images on title slides. Its input is distinct from the JSON/Markdown schema of `scripts/generate_slides.py`.

## Office preview PDFs

```text
python scripts/master_studio/office_to_pdf.py report.docx -o report-preview.pdf --engine com --no-qa
python scripts/master_studio/office_to_pdf.py slides.pptx -o slides-preview.pdf --engine com --no-qa
```

Windows COM requires Microsoft Office and `pywin32`; this preserves Office's layout. The optional Chromium fallback needs `playwright`, a browser, `mammoth` and `python-pptx`; it reconstructs an approximation, especially for slides, and must not be used as proof of Office layout fidelity. The optional automated PDF text QA needs PyMuPDF and may reject valid slides with little text; it is not a visual inspection. `--no-qa` skips that gate, so inspect the exported PDF pages separately. Existing output paths are rejected.

## Diagram rendering

`diagram_forge.py` renders a self-contained HTML/SVG diagram to PNG using Playwright and a locally installed Chromium-compatible browser. Install `playwright` and its browser as needed; the script can also discover common desktop browsers.

```text
python scripts/master_studio/diagram_forge.py diagram.html diagram.png --width 1080 --scale 2
```

Use trusted, self-contained input and review the generated diagram. This is a raster image for evidence and presentations, not an editable PowerPoint diagram.

Master Studio's semantic index is coupled to its private local source manifest, folders and an E5 model cache. It was not copied as a working drop-in index; the harness's local FTS index remains available. A portable semantic retrieval integration requires its own model/dependency and source-provenance setup.
