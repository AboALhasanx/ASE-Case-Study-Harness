# Active case study configuration

The only user-supplied field is the repository URL. If it is absent, ask for that URL and nothing else. After receiving it, automatically populate all remaining fields from the repository and these defaults.

- Target repository URL: (user input)
- Default branch and fetched HEAD commit: (auto-detect and pin)
- Retrieval timestamp: (automatic)
- Project/team slug: (derive from repository name and short HEAD SHA)
- License: (inspect repository evidence; label unknown if unavailable)
- Study question and boundary: (derive from README, docs, source, tests, and history)
- Exclusions and sampling: (derive from repository size and available evidence; explain in the report)
- Execution boundary: read-only by default; only local, bounded, non-destructive checks

Do not ask the user to choose a revision, team slug, study question, chapter scope, or phase approval. Store the completed target manifest and decisions under `case-studies/<team-slug>/context/`.
