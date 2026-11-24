# ASE-Harness

Reusable, evidence-driven harness for studying an open-source software system through the Advanced Software Engineering course.

## Purpose

Each student team selects one open-source target and prepares a case study spanning the course lifecycle: requirements, planning, design, metrics, reliability and quality, testing, and maintenance. The harness uses Codex as the agent runtime; it does not require an API key, an external orchestrator, or a custom multi-agent program.

The case study is an engineering review of an existing system. It is not a claim that this team developed that system.

## Start here

1. Open this repository folder in Codex.
2. Read `AGENTS.md`, `GOALS.md`, and `PLANS.md`.
3. Set the target repository and scope in `context/PROJECT.md` (or answer the agent's setup questions).
4. Start the goal with the command below. If the Codex version does not support `/goal`, ask the agent to execute one phase at a time and persist progress after each phase.

```text
/goal Execute the complete software engineering case study defined in this repository.
Read AGENTS.md, GOALS.md, PLANS.md, config.yaml, and docs/COURSE-MATERIALS.md.
Ask me to select a target open-source repository if none is configured.
Use specialized subagents for independent analysis when supported; otherwise work sequentially.
Follow the evidence-driven phases, verify claims, and revise unsupported findings.
Generate the academic report, seminar materials, evidence index, and viva preparation.
Persist progress after every phase. Never fabricate evidence. Report unresolved blockers.
```

For a one-phase run, use `prompts/PHASE-PROMPTS.md` and name the phase.

## What a completed study contains

- A scoped, reproducible system profile and source snapshot reference.
- Findings mapped to course concepts, each linked to evidence.
- Clearly labeled measurements, estimates, assumptions, and limitations.
- An academic report, seminar outline/slides, evidence index, and viva questions grounded in the evidence.
- A progress log that lets another team member resume the work.

See `PLANS.md` for phases and `GOALS.md` for completion criteria. Study outputs belong under `case-studies/<team-slug>/` in the team's working copy. Do not commit secrets, credentials, or unrelated personal data.

## Course materials and repository access

The owner confirmed permission to share the provided course PDFs for this project. They are included in `knowledge/` and remain attributed course materials; their inclusion does not make them openly licensed. Respect any course-specific use limits, and respect the target project's license when quoting or copying its code and documents.

See `docs/COURSE-MATERIALS.md` for the verified inventory and chapter mapping. The core study covers Chapters 1–9; Chapter 10, Software Certification, remains supplementary pending instructor confirmation.

## Fast course-material retrieval

The repo includes a local SQLite FTS5 index of page-addressable PDF passages in `knowledge/index/ase_knowledge.sqlite3`. Search it with `python scripts/search_knowledge.py "your topic"`; results include source PDF and page number. Rebuild it after changing the PDFs with `python scripts/build_knowledge_index.py`. Retrieval is lexical BM25 and requires no API key or model download. Confirm any cited passage in the original PDF page, especially for diagrams and tables.

## Suggested target systems

The shared planning conversation suggested Kanboard as the first candidate, with BookStack, Flask, and Snipe-IT as alternatives. These are suggestions only. The team must verify the target is reachable, open-source, and manageable in scope before locking it in. No target is configured in this starter repository.

## Working principles

- Evidence first: cite paths, line numbers, commit IDs, issue/PR URLs, test output, and dates where available.
- Separate observed facts from inference and estimates.
- Use a bounded review loop. Fix gaps that materially affect acceptance criteria; do not loop without a concrete reason.
- Keep the student responsible for checking and understanding results, especially before submission or viva.
- Use parallel agents only for independent tasks and reconcile their findings centrally.

## Repository map

- `AGENTS.md` — persistent instructions for Codex.
- `GOALS.md` — objective, scope, and acceptance criteria.
- `PLANS.md` — ordered, resumable workflow.
- `prompts/` — compact launch and phase prompts.
- `knowledge/` — supplied PDFs and course material guide.
- `knowledge/index/` — generated local RAG retrieval database.
- `chapter-guides/` — chapter-to-evidence guidance.
- `context/` — target configuration, decisions, and progress.
- `templates/` — claim and evidence log templates.
- `workflows/AGENT-ROLES.md` — bounded multi-agent work split and reviewer role.
- `validation/` — acceptance rules and critique checklist.
