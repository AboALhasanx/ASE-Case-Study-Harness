# Workflow overview

The case study advances through the phases in `PLANS.md` without interactive approval gates. The only required input is a target repository URL. The agent pins the default-branch HEAD, derives the study scope, and continues automatically. Keep each team's work isolated under `case-studies/<team-slug>/` and preserve a resumable checkpoint after every phase. If a check is unsafe or unavailable, log the limitation and continue independent analysis.
