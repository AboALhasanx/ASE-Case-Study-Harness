# Development plan for case-study deliverables

## Objective

From one repository URL, produce an evidence-backed case study with an editable academic Word report and a clear, editable PowerPoint presentation. Preserve the source documents and evidence so a student can understand, check, and revise the result.

## Workstreams

1. **Deliverable contract:** require a `.docx`, a `.pptx`, source files, an evidence ledger, and a final quality report. Separate missing evidence or tooling from completed work.
2. **Document generation:** convert a reviewed Markdown report into a consistent academic Word document with page layout, hierarchy, tables, references, and page numbers. Keep sources traceable.
3. **Presentation generation:** build a 16:9 editable presentation from structured evidence-backed content. Use concise slide text, readable contrast, source references, and speaker notes where supported.
4. **Course retrieval:** improve ranking for explanatory passages and preserve page references. Record limitations and retain the source PDF as the final authority.
5. **Quality gate:** render Word and slides to page images when a renderer is available; inspect all pages for clipping, legibility, breaks, contrast, and factual alignment with the evidence ledger. Fix issues and re-render. Record any unavailable verification as an explicit limitation rather than declaring it passed.
6. **Pilot:** run a complete study on a real open-source project after a target URL is provided; audit the resulting artifacts and refine the harness from actual failures. A small synthetic fixture checks tooling but cannot replace this pilot.

## Completion criteria

- No questions after the target URL under normal conditions; derive and record revision and study boundary.
- Every material conclusion is traceable, and all nine core chapters have coverage or an explicit limitation.
- Word and presentation files open, are editable, and agree with the verified source materials.
- All student-facing content is English. Supply Arabic presenter narration for each slide as a separate script and in PowerPoint notes when supported.
- Final output includes a review log covering both evidence and visual inspection; missing rendering tools or inaccessible sources are disclosed.
- Documented commands and dependencies let another student reproduce the files without API keys.

On Windows with Microsoft Office, `scripts/master_studio/office_to_pdf.py --engine com --no-qa` provides faithful PDF previews for visual inspection. See `scripts/master_studio/README.md` for prerequisites and limitations; an automated text QA result alone is not visual review. The copied seminar builder supports evidence images and speaker notes as an alternative presentation path.
