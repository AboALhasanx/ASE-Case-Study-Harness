# Evidence ledger structural check

Run `python scripts/check_evidence.py path/to/ledger.json`. The command exits 0 for structurally consistent data, 1 for validation errors, and 2 for unreadable or malformed JSON. It uses only the Python standard library.

```json
{
  "evidence": [
    {"id": "E-01", "source": "README.md at commit abc123, section Usage"}
  ],
  "claims": [
    {"id": "C-01", "claim": "The README documents setup.", "status": "Observed", "evidence": ["E-01"]},
    {"id": "C-02", "claim": "Actual operating cost", "status": "Not Available", "evidence": [], "limitation": "No cost records were found."}
  ],
  "deliverable_claims": ["C-01", "C-02"]
}
```

Use exact statuses `Observed`, `Inferred`, `Estimated`, and `Not Available`. Evidence and claim IDs must be unique in their own lists. Each evidence item needs a source locator. All claims need text and an evidence array; observed, inferred, and estimated claims require at least one existing evidence ID. Not Available claims need an explicit limitation. The `deliverable_claims` array must be non-empty, every ID listed there must resolve to a claim, and duplicate IDs in the list are rejected.

Populate `deliverable_claims` from the report and slides, including claims marked unavailable. The checker cannot independently discover missing claims in documents or prove that a source exists, supports a claim, has been interpreted correctly, or is sufficient. An evidence reviewer must still inspect source locations, calculations, dates, assumptions, and the actual deliverables.
