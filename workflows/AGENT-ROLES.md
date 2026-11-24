# Bounded multi-agent roles

Use these roles after the user provides the target URL and the coordinator pins its default-branch HEAD. The coordinator derives scope from the repository and owns integration, citations, and final conclusions. Keep delegation bounded and independent; use sequential work when subagents are unavailable. Roles do not wait for human approval between phases.

| Role | Independent task | Required output | Review boundary |
|---|---|---|---|
| Requirements analyst | Reconstruct observable requirements from docs, behavior, issues, and tests | SRS rows with source IDs and confidence | Do not state reconstructed requirements as original intent |
| Design/metrics analyst | Inspect architecture and calculate selected reproducible metrics | Design notes and metric worksheet with raw results | Declare tools, versions, scope, and definitions |
| Testing analyst | Inventory tests and run only local, safe, bounded checks | Test plan and exact execution record | Separate proposed, executed, skipped, blocked, and failed |
| Maintenance analyst | Sample commits/issues and classify change types | Sample method and evidence-linked change table | Include ambiguous cases and sampling limits |
| Critic | Challenge another phase's evidence, arithmetic, coverage, and claims | Findings list with exact references | Critique first; do not silently rewrite source evidence |

The lead agent reconciles overlapping results and resolves conflicts against primary evidence. Prefer at most three concurrent subagents to control context and usage. Never delegate access-token handling or actions against live services. If a required input is missing, the lead asks only for the repository URL; other unknowns are recorded as limitations or derived from repository evidence.
