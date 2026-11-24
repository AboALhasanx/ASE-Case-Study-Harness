# ASE Case Study Harness memory

## 2026-11-24 — URL-only autonomous case study
- Context: The owner wants classmates to provide a target repository URL and receive the full case study without follow-up questions or per-phase approvals.
- Fact: Derive the default-branch HEAD, repo-name-plus-SHA slug, study question, scope, and safe analysis boundary from the target repository. Use Chapters 1–9 as core; Chapter 10 is a relevant supplemental lens. Retrieve course theory first from the SQLite FTS5/BM25 index and verify source PDF pages.
- Verify: Check `AGENTS.md`, `PROMPTS.md`, `PLANS.md`, `config.yaml`, and `docs/PHASES.md`; each should request only the repository URL and continue automatically.
