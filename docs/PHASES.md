# Phase map and acceptance gates

This map turns the course-wide case study into small, reviewable steps. Each team phase should leave a short durable record under `case-studies/<team-slug>/` (for example `case-studies/team-a/context/phase-00-bootstrap/`), not only a chat summary. Use concise findings plus links to raw evidence. Do not commit private student notes or restricted course material to a shared remote.

## 0 — Bootstrap and scope

**Do:** Load the supplied chapter inventory, RAG index, and available tools. Use Chapters 1–9 as the core scope and Chapter 10 as a supplemental lens when relevant. Derive defaults from the repository and do not ask the user for scope or tool preferences.

**Artifacts:** initial shared inventory in `docs/COURSE-MATERIALS.md`; team-specific project state, decisions, and progress under `case-studies/<team-slug>/context/`.

**Gate:** Materials and defaults are accounted for automatically; unavailable or unclear items are logged without pausing.

## 1 — Course knowledge map

**Do:** Extract concepts, definitions, methods, and relevant caveats from each in-scope chapter. For each candidate analysis, record its chapter/section/page locator, the evidence needed from the target system, and whether it is observed, inferred, or estimated. Keep chapter summaries concise and paraphrased; do not reproduce textbook pages.

**Artifacts:** `knowledge/` chapter map, chapter guides, and a concept-to-evidence matrix. Team-specific notes may be kept under `case-studies/<team-slug>/context/`.

**Gate:** Every in-scope chapter is represented and the matrix makes clear which claims can be tested against repository evidence. Record OCR or page-number uncertainty.

## 2 — Target repository baseline

**Do:** Use the repository URL provided by the user. Run `python scripts/prepare_target.py <repository-url>` to clone and write the manifest, or resume an existing matching study without overwriting it; see `docs/TARGET-BASELINE.md`. Pin the exact HEAD commit and retrieval time. Infer the study question from the repository purpose and inspect its license, history, documentation, tests, and safe setup. Derive a practical boundary from repository size; do not ask the user to choose a revision or scope. Never substitute a suggested project for an inaccessible URL.

**Artifacts:** `case-studies/<team-slug>/context/target-manifest.md`, with URL, default branch, exact commit, retrieval time, scope, exclusions, and rationale.

**Gate:** The supplied URL, default branch, exact commit, retrieval time, inferred boundary, and access limits are recorded. Continue without an approval pause.

## 3 — Repository baseline and reproducibility

**Do:** Record upstream URL, license, release/tag/commit SHA, repository structure, languages, setup instructions, and relevant dependency/tool versions. Attempt only safe, local, documented setup steps. Skip commands that could affect live services, external accounts, or user data, and record why. Capture command, environment summary, date, and result for checks that are run; protect secrets and personal paths.

**Artifacts:** `case-studies/<team-slug>/evidence/repository-manifest.md`, `case-studies/<team-slug>/evidence/setup-log.md`, raw outputs or stable references.

**Gate:** Another student can identify the exact studied revision and understand what did and did not run. A failed setup is documented as a limitation, never reported as a passing test.

## 4 — Lifecycle and requirements (course lifecycle and requirements chapters)

**Do:** Trace releases, commits, issues, roadmap, and documentation to infer the development model. Reconstruct only requirements supported by externally visible behavior, docs, tests, or issues. Give each requirement an ID, source, rationale, confidence, and verification idea.

**Artifacts:** lifecycle analysis; requirements/SRS draft; traceability matrix under `case-studies/<team-slug>/`.

**Gate:** Facts about project history are observed; lifecycle model is explicitly an inference. Reconstructed requirements are distinguished from original author requirements, which may be unavailable.

## 5 — Planning and design

**Do:** Apply course planning concepts to the bounded case study. If estimating hypothetical project effort/cost, state model, inputs, assumptions, ranges, and why this is not the original project's actual cost. Analyze architecture and design from code/docs; cite paths/lines and distinguish direct structure from interpretation.

**Artifacts:** planning and risk note; architecture/context diagrams; design observations under `case-studies/<team-slug>/`.

**Gate:** Estimates are labelled **Estimated**, assumptions are visible, and no unobservable developer intent is stated as fact.

## 6 — Metrics and quality/reliability

**Do:** Choose metrics relevant to the course and repository. Define each metric, unit, scope, formula/tool/version, exclusions, command, and raw result. Review quality/reliability evidence such as tests, defect history, CI, and releases; repository activity alone is not proof of reliability.

**Artifacts:** metrics worksheet/report and raw machine-readable results where practical; quality/reliability evidence table under `case-studies/<team-slug>/`.

**Gate:** Calculations can be reproduced and manually spot-checked. Claims do not exceed what the sample or available evidence supports.

## 7 — Testing and certification

**Do:** Map the target's test levels/types and evaluate representative cases. Run safe tests if setup permits; save exact commands and outcomes. If not, label cases as designed/proposed and report execution as unavailable. Connect certification concepts to documented criteria or standards only where sources support the connection; do not claim the software is certified based on a superficial comparison.

**Artifacts:** test inventory, test plan/cases, execution record, certification discussion with primary-source citations when applicable, under `case-studies/<team-slug>/`.

**Gate:** Executed tests, static inspection, and proposed tests are clearly separated. A certification conclusion states scope, criteria, and limitations or remains undetermined.

## 8 — Maintenance and evolution

**Do:** Define a sampling window and selection method for commits/issues/releases. Classify representative changes as corrective, adaptive, perfective, or preventive only with a linked change and rationale; allow ambiguous/unclassifiable. Avoid cherry-picking only dramatic examples.

**Artifacts:** sample method, commit/change table, maintenance analysis under `case-studies/<team-slug>/`.

**Gate:** Each classification has evidence and reasoning. Sample limitations and ambiguous cases are reported.

## 9 — Verification and critique

**Do:** Use a second reviewer/agent when available to challenge evidence, formulas, chapter coverage, source quality, contradictions, and overclaims. Compare conclusions against raw evidence and correct the source artifact, not just the narrative. Build a structured ledger of claims and evidence and run `scripts/check_evidence.py` as described in `docs/EVIDENCE-CHECK.md`; enumerate deliverable claims from the actual report and slides. This structural check cannot verify factual support or discover omitted claims, so perform the independent source review too. Sequential self-review is the fallback. Do not wait for a human to approve the critique.

**Artifacts:** `case-studies/<team-slug>/validation/findings-review.md`, citation/evidence ledger, issue list, correction log.

**Gate:** Every important conclusion has a traceable basis; calculations have checks; contradictions and open questions are resolved or disclosed; all gaps have a next action. Log remaining limits and continue to final packaging.

## 10 — Final report, seminar, and viva

**Do:** Assemble an academic report, seminar deck, supporting SRS/design/metrics/testing/maintenance artifacts, evidence repository, and viva questions from verified outputs. Include methodology, limitations, AI-use disclosure according to instructor rules, and reproducibility notes. The proposed sizes (30–50 report pages and 15–25 slides) are optional targets from the conversation, not requirements.

**Artifacts:** English editable Word report (`.docx`) and English editable PowerPoint (`.pptx`), their source files, English viva material and final evidence index under `case-studies/<team-slug>/deliverables/`. Add a separate Arabic presenter script mapped to every slide and include the narration in speaker notes when supported. Follow `docs/DEVELOPMENT-PLAN.md` and the generator guides.

**Gate:** Report, visible slides, citations, diagrams and viva are in English and agree with the evidence ledger. The Arabic presenter script covers each slide and retains its meaning; check that speaker notes are preserved and Arabic is legible. Every chart/table can be traced to data; references are checked; viva material tests understanding rather than memorization. Open and render both files when tooling is available, inspect all pages/slides for legibility, clipping, overflow and alignment, fix defects, and repeat. Record any unavailable format or visual inspection explicitly as incomplete; do not claim a successful review without evidence.

## Evidence record minimum

For each nontrivial finding, record:

| Field | What to capture |
|---|---|
| ID | Stable finding or requirement ID |
| Claim | One testable statement |
| Status | Observed, Inferred, Estimated, Not available, or unresolved |
| Source | Course page/section, source path and lines, commit/issue, command output, or external source |
| Method | How the evidence was found or value calculated |
| Confidence/limits | Sampling, missing data, ambiguity, and assumptions |
| Review | Reviewer and outcome, or pending |

Prefer primary evidence: the exact source revision, project documentation, test output, release/issue/commit records, and the provided course materials. Keep snapshots or hashes for sources that may change. External sources support context; they do not override what the chosen revision shows.
