# Student prompts

## Start a case study

Read `AGENTS.md`, `GOALS.md`, `PLANS.md`, `config.yaml`, and `docs/COURSE-MATERIALS.md` first. Then ask me for the target open-source repository URL, the revision or date range to study, and the agreed scope. Do not clone or analyze a target until those choices are recorded in `config.yaml` and I approve the analysis plan.

Conduct the case study phase by phase using the course materials and the evidence rules in this repository. Save outputs under `case-studies/<team-slug>/`. At the end of each phase, summarize findings, evidence, limitations, and open questions, then wait for my approval before continuing. Do not fabricate facts, metrics, tests, history, estimates, citations, or sources. Label every claim Observed, Inferred, Estimated, or Not Available. Separate course concepts from evidence about the target system.

Use a small number of bounded specialist subagents only when the current Codex environment supports them. Delegate independent analysis tasks with explicit inputs and outputs; otherwise work sequentially. A reviewer must check calculations and evidence references before a phase is accepted. Stop when evidence is unavailable, permission is missing, or execution could affect a third-party system.
