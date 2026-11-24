# Execution plan

This plan builds and then uses the ASE-Harness: a reusable, evidence-led workflow for studying one open-source software system through the Advanced Software Engineering course. It is designed for Codex as the agent runtime; a custom orchestrator, API key, or always-on loop is not required.

The harness must support both specialized subagents when the current Codex environment offers them and a sequential fallback. Work is resumable: save each phase's scope, evidence, decisions, and open questions before moving on. See [`docs/PHASES.md`](docs/PHASES.md) for phase artifacts and acceptance gates.

## Operating rules

1. Treat the course materials as the academic baseline. Use the local SQLite retrieval index to locate relevant passages quickly, then confirm the source PDF page and cite chapter and section/page; flag uncertain mappings for human review.
2. Separate **Observed** (directly evidenced), **Inferred** (reasoned from evidence), and **Estimated** (model-based approximation) claims. Use **Not available** when a fact cannot be established.
3. Every material claim must point to a source: a course-material location, source file and line, commit/issue/PR, test output, or stable external reference. Record retrieval date for sources that may change.
4. Never invent source history, requirements, costs, metrics, test outcomes, citations, or author intent. Mark an unverified result as pending rather than filling the gap.
5. A failed setup or unavailable dependency does not count as a runtime test. Continue with explicitly labelled static or historical analysis when useful.
6. Do not modify the target system as part of an audit unless the team explicitly approves an experiment. Keep generated work and test data separate from upstream source.
7. The team reviews the conclusions and can explain them. AI-assisted analysis does not replace authorship, instructor rules, or viva preparation.
8. Keep iteration bounded: each cycle names a finding, evidence gap, or failed check; make a targeted correction; rerun the relevant check; log the outcome. Stop when gates pass or report the blocker and next action.

## Phase sequence

| Phase | Purpose | Exit gate |
|---|---|---|
| 0. Bootstrap | Confirm course scope, available materials, tool limits, and workspace privacy. | Inventory recorded; no source or permission ambiguity is hidden. |
| 1. Course knowledge | Build a chapter map and evidence rules from the provided material. | All relevant chapters mapped to concepts, source locations, and candidate analyses; gaps noted. |
| 2. Target screening | Compare candidate open-source systems for scope, access, history, tests, documentation, and runnable setup. | Team selects one target and a bounded version/commit; suitability rationale is recorded. |
| 3. Repository baseline | Capture provenance, license, release/commit, structure, build instructions, and an initial reproducibility check. | Baseline manifest and environment/setup outcome are saved; operational limits are explicit. |
| 4. Lifecycle and requirements | Analyze development evidence and reconstruct requirements with traceability. | Lifecycle classification is labelled inference; each reconstructed requirement links to evidence and confidence. |
| 5. Planning and design | Apply project-planning concepts and inspect architecture/design. | Estimates are labelled and assumptions shown; design claims cite code/docs/diagrams. |
| 6. Metrics and quality | Calculate selected code metrics and evaluate quality/reliability evidence. | Metric definitions, scope, tools, commands, raw outputs, and limitations are recorded and reproducible. |
| 7. Testing and certification | Inspect test strategy, run feasible checks, evaluate certification concepts only where evidence supports them. | Test cases and actual outcomes are distinguished from proposals; no unsupported certification claim. |
| 8. Maintenance | Examine a representative, justified sample of changes/issues and classify maintenance. | Sample method and commit links are recorded; classifications include rationale and uncertainty. |
| 9. Synthesis and verification | Cross-check coverage, calculations, citations, contradictions, and limitations. | Independent critique completed; material findings traced to evidence; unresolved items disclosed. |
| 10. Final package | Produce report, seminar, supporting artifacts, and viva preparation. | Deliverables agree with verified findings and pass the checklist in `docs/PHASES.md`. |

Phases may be revisited when evidence changes. Do not skip a gate silently. When a gate cannot be passed, preserve completed work, describe the blocker, and propose the smallest next action.

## Starting prompt

```text
Read AGENTS.md, GOALS.md, and PLANS.md. Inspect the course-material inventory.
Ask me to select a target open-source repository if none is configured. Screen
candidate repositories before recommending one. Work phase by phase, save
evidence and decisions after each phase, and stop at each acceptance gate for
review when the decision affects scope or assumptions. Use specialized
subagents for independent work when available; otherwise work sequentially.
Never fabricate evidence. Continue until the goals are met or report a concrete
blocker and next action.
```
