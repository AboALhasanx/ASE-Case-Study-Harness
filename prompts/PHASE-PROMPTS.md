# Per-phase prompts

Use a phase prompt only after reading `AGENTS.md`, `GOALS.md`, `PLANS.md`, `config.yaml`, and `docs/COURSE-MATERIALS.md`.

## Phase 0 — Bootstrap

Inventory the local course materials, RAG index, workspace, and available analysis tools. Use Chapters 1–9 as the core scope and Chapter 10 as supplemental when relevant. Ask for no setup preferences.

## Phase 1 — Course knowledge map

For each in-scope chapter, extract a concise concept-to-evidence map from the provided material. Record chapter/section/page locators and paraphrase rather than reproduce. Note unreadable pages and uncertain mappings.

## Phase 2 — Target baseline

Use the supplied repository URL. Automatically fetch its default branch, pin the HEAD commit and retrieval time, inspect project purpose/license/history/tests, and derive a feasible analysis boundary. Do not ask the user to pick a revision or scope. Do not replace an inaccessible target with an example project.

## Analysis phases

For each phase in `PLANS.md`, state the question, method, evidence collected, findings, limits, and next step. Save a checkpoint and continue automatically. Link every material claim to an evidence-log entry. Clearly distinguish a test plan from an executed test and a reconstructed requirement from an original requirement.

## Independent critique

Review one phase without rewriting its conclusion first. List unsupported claims, missing evidence, arithmetic issues, citation gaps, and scope overreach with exact references. The lead agent resolves each item and records the disposition.
