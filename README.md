# ASE-Harness

Reusable, evidence-driven harness for studying an open-source software system through the Advanced Software Engineering course.

## Purpose

Each student provides one open-source repository URL. The harness then analyzes that repository through the course lifecycle: requirements, planning, design, metrics, reliability and quality, testing, and maintenance. It derives the target revision and practical study scope from the repository and runs to completion without intermediate questions or approvals. The harness uses Codex as the agent runtime; it does not require an API key, an external orchestrator, or a custom multi-agent program.

The case study is an engineering review of an existing system. It is not a claim that this team developed that system.

## Start here

1. Open this repository folder in Codex.
2. Start the goal below and provide the target repository URL. That is the only required input.
3. The agent pins the current default-branch commit, derives the scope from the repository, uses the course RAG index, and completes every phase automatically. If the Codex version does not support `/goal`, give the same instruction in chat.

```text
/goal Execute the complete software engineering case study defined in this repository.
Read AGENTS.md, GOALS.md, PLANS.md, config.yaml, and docs/COURSE-MATERIALS.md.
Target repository URL: <paste URL here>
If the URL is missing, ask me only for it. Do not ask follow-up questions.
Fetch the default branch, pin its current commit, derive the study scope, and finish every phase without approvals.
Use the course RAG index and verify cited PDF pages.
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

The final package includes an editable `.docx` report and `.pptx` seminar, plus their source files and evidence. Install dependencies with `python -m pip install -r requirements.txt`. The agent follows [`docs/WORD-GENERATION.md`](docs/WORD-GENERATION.md), [`docs/SLIDES-GENERATION.md`](docs/SLIDES-GENERATION.md), and [`docs/DEVELOPMENT-PLAN.md`](docs/DEVELOPMENT-PLAN.md), then renders and checks each page and slide when a renderer is available. Missing tools or visual checks are reported explicitly.

## Course materials and repository access

The owner confirmed permission to share the provided course PDFs for this project. They are included in `knowledge/` and remain attributed course materials; their inclusion does not make them openly licensed. Respect any course-specific use limits, and respect the target project's license when quoting or copying its code and documents.

See `docs/COURSE-MATERIALS.md` for the verified inventory and chapter mapping. The core study covers Chapters 1–9; Chapter 10, Software Certification, is used as supplemental analysis when relevant.

## Fast course-material retrieval

The repo includes a local SQLite FTS5 index of page-addressable PDF passages in `knowledge/index/ase_knowledge.sqlite3`. Search it with `python scripts/search_knowledge.py "your topic"`; results include source PDF and page number. Rebuild it after changing the PDFs with `python scripts/build_knowledge_index.py`. Retrieval is lexical BM25 and requires no API key or model download. Confirm any cited passage in the original PDF page, especially for diagrams and tables.

## Suggested target systems

The shared planning conversation mentioned Kanboard, BookStack, Flask, and Snipe-IT as examples only. The agent analyzes the URL you provide. If it is inaccessible, it records the limitation and completes whatever safe static analysis is possible rather than silently substituting a different project.

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
