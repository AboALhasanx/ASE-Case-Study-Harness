# GOALS.md — case-study objective and acceptance criteria

## Objective

Produce a reproducible academic case study that evaluates one selected open-source software system through the Advanced Software Engineering course. The team acts as an independent reviewer. Codex can coordinate bounded analysis tasks and preserve progress; the team remains responsible for validation and presentation.

## Scope

Cover the nine course chapters with the following initial mapping. Verify exact chapter titles and terminology against the supplied course materials before finalizing the analysis:

| Chapter | Initial topic | Case-study application |
| --- | --- | --- |
| 1 | Introduction to Software Engineering | System context, users, problem, purpose, and case-study question |
| 2 | Software Life Cycle Models | Evidence-based account of the development process and lifecycle model(s) |
| 3 | Requirements Analysis and Specifications | Reconstructed requirements and traceability to system evidence |
| 4 | Software Project Planning | Planning approach, effort/cost/time estimates, assumptions, and risks |
| 5 | Software Design | Architecture, components, interfaces, coupling/cohesion, and design evidence |
| 6 | Software Metrics | Reproducible measurements with definitions, tools, scope, and limitations |
| 7 | Software Reliability and Quality | Quality/reliability evaluation using available observable evidence |
| 8 | Software Testing | Test inventory and, where feasible, bounded test execution with recorded results |
| 9 | Software Maintenance | Change history, maintenance patterns, defects, and evolution evidence |

This is a review, not a rebuild of the target. Do not promise claims that cannot be established from repository artifacts or safe local checks. Keep the target-system scope feasible for a student seminar.

## Acceptance criteria

A case study is complete only when:

1. **Target is pinned:** URL, owner/project, selected commit/tag or snapshot date, license, study boundary, and any exclusions are recorded.
2. **All chapters are addressed:** every chapter has a question, analysis, evidence, and an explicit limitation or a reason it is not applicable.
3. **Claims are traceable:** every material finding has a stable evidence reference in the evidence ledger; no orphaned conclusions remain.
4. **Methods are reproducible:** commands, tool/version, environment, dates, and relevant outputs are recorded for measurements and tests.
5. **Uncertainty is visible:** facts, inferences, estimates, and unknowns are distinguished; estimates show assumptions; conflicting evidence is discussed.
6. **Independent review is done:** a critic pass checks coverage, arithmetic, citations, scope, and unsupported language; issues are resolved or listed as open limitations.
7. **Deliverables are present:** editable academic Word report (`.docx`), editable seminar presentation (`.pptx`), their source files, evidence index, progress/decision log, and viva questions with evidence-grounded answers. Student-facing material is English; provide an Arabic presenter script mapped slide by slide and embed it in speaker notes when supported. If a generator or renderer is unavailable, provide source material and explicitly report the missing deliverable or verification; do not mark it complete.
8. **Review and learning support are present:** an independent critic pass checks the final claims, and the viva materials explain the methods and limitations so students can verify and learn from the work. The harness completes without waiting for sign-off.

## Out of scope for the starter

- Building or modifying the target system as the main deliverable.
- A custom agent orchestration service, API integration, vector database, or external memory server.
- Automatically submitting or publishing the academic work.
- Treating a generated report as proof without human verification.

## Stop conditions

The only routine input request is the target repository URL. If it is missing, ask for that URL only. For inaccessible repositories, risky checks, or unsupported claims, continue independent work and record the blocker, fallback method, and next action in the final report; do not ask for credentials or phase approvals.
