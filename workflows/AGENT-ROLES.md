# Bounded multi-agent roles

Use these roles only after the target repository and revision are approved. The coordinator owns scope, integration, citations, and final conclusions. Keep delegation bounded and independent; use sequential work when subagents are unavailable.

| Role | Independent task | Required output | Review boundary |
|---|---|---|---|
| Requirements analyst | Reconstruct observable requirements from docs, behavior, issues, and tests | SRS rows with source IDs and confidence | Do not state reconstructed requirements as original intent |
| Design/metrics analyst | Inspect architecture and calculate selected reproducible metrics | Design notes and metric worksheet with raw results | Declare tools, versions, scope, and definitions |
| Testing analyst | Inventory tests and run only approved, safe, bounded checks | Test plan and exact execution record | Separate proposed, executed, blocked, and failed |
| Maintenance analyst | Sample commits/issues and classify change types | Sample method and evidence-linked change table | Include ambiguous cases and sampling limits |
| Critic | Challenge another phase's evidence, arithmetic, coverage, and claims | Findings list with exact references | Critique first; do not silently rewrite source evidence |

The lead agent reconciles overlapping results and resolves conflicts against primary evidence. Prefer at most three concurrent subagents to control context and usage. Never delegate access-token handling or actions against live services.
