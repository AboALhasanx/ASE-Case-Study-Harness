# Student prompts

## Start a case study

Read `AGENTS.md`, `GOALS.md`, `PLANS.md`, `config.yaml`, and `docs/COURSE-MATERIALS.md` first. The only required input is the target repository URL. If I have not provided it, ask only for the URL. After I provide it, automatically fetch the default branch, pin its current HEAD commit, derive a suitable study question and boundary from the repository, and continue all phases without asking me to approve the plan or intermediate results.

For course theory, search the local index first with `python scripts/search_knowledge.py "<concepts>"`. Use the result's PDF and page locator, then verify the relevant original page before making a sourced claim. The index is lexical BM25, not a semantic embedding model; include synonyms or the chapter's terminology when searching.

Conduct the case study phase by phase using the local course RAG index, original course materials, and evidence rules in this repository. Save outputs under `case-studies/<team-slug>/`. After each phase, write a checkpoint and continue automatically. Do not fabricate facts, metrics, tests, history, estimates, citations, or sources. Label every claim Observed, Inferred, Estimated, or Not Available. Separate course concepts from evidence about the target system.

Use a small number of bounded specialist subagents when the current Codex environment supports them. Delegate independent analysis tasks with explicit inputs and outputs; otherwise work sequentially. Run an independent critique and check calculations and evidence references internally. If evidence is unavailable, access is denied, or execution could affect a third-party system, use a safe fallback, disclose the limitation, and continue all independent work. Do not ask for credentials or intermediate approval.
