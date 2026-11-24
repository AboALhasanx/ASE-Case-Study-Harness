# Chapter 9 — Software Maintenance

**Source:** `knowledge/Ch09.pdf` (33 PDF pages; printed text begins at p. 459). The source discusses maintenance after operation/release and the evidence available in project history.

## Concepts and source locations

- Maintenance definition and the four categories—corrective, adaptive, perfective, preventive: PDF pp. 1–5 (printed pp. 459–463).
- Maintenance process and process models: PDF pp. 6–11 (printed pp. 464–469).
- Maintenance cost/effort estimation: PDF pp. 12–14 (printed pp. 470–472).
- Regression testing and change impact: PDF pp. 15–17 (printed pp. 473–475).
- Reverse engineering and software re-engineering: PDF pp. 18–24 (printed pp. 476–482).
- Configuration management and documentation: PDF pp. 25–30 (printed pp. 483–488).

## Case-study questions

1. What evidence shows that the selected system changed over time, and which releases/commits fall in the study window?
2. How do representative changes relate to the four maintenance categories? Are any changes ambiguous or mixed?
3. What change-control, version/configuration-management, documentation, or regression-test practices can be observed?
4. What evidence exists for maintenance effort or cost? If the repository does not expose it, what can be estimated—and under which explicit assumptions?

## Evidence and method

- Pin a date range or release interval and define a sampling method before selecting commits/issues (for example, stratified samples by release or a fixed systematic interval).
- Record commit SHA/date, changed paths, linked issue/PR, release notes, tests affected, and the evidence supporting each classification.
- Assign a primary category only when the change rationale supports it; allow multiple labels, **Mixed**, or **Unclassified** with a reason. A commit message alone may not establish intent.
- For change impact, trace affected components and related tests/docs using repository history and code references. Record commands and the exact revision used.
- Distinguish observed history from inferred category, and distinguish any model-based estimate from the project's actual reported maintenance cost.

## Pitfalls and reviewer checklist

- Do not equate all commits after a release with maintenance; justify the operational/release boundary.
- Avoid cherry-picking dramatic bug fixes; disclose the sampling frame and missing history.
- Do not infer developer motives or actual costs from code churn alone.
- Verify commit links, dates, sample counts, classification rationale, and regression-test claims.
- Report repository limitations (squashed history, missing issues, private work, or incomplete release notes) and their impact on conclusions.
