# Chapter 1 — Introduction to Software Engineering

**Source:** `knowledge/Ch1.pdf` (19 PDF pages). Page numbers below refer to the page index inside the PDF.

## Concepts to apply

| Topic | Source locator | Case-study use |
|---|---|---|
| Software crisis, software failures, and the limits of a single “silver bullet” | PDF pp. 1–4; §§1.1–1.1.2 | Frame a concrete engineering question and avoid claiming that one tool or practice alone proves quality. Historical examples in the notes are context, not evidence about the selected system. |
| Software engineering objective and definitions | PDF p. 4; §1.2 | Evaluate the system as a product built and maintained through a process, with quality, requirements, time, and cost concerns. |
| Program vs. software; documentation and operating procedures | PDF pp. 4–6; §§1.2.2–1.2.3 | Inventory source, docs, deployment/setup instructions, and operating guidance; don’t equate repository code with the complete product. |
| Software process, process improvement, and software characteristics | PDF pp. 6–11; §§1.2.3–1.3 | Look for recurring development/release practices and characteristics that affect evolution. Describe only what repository artifacts show. |
| Software myths and terminology: deliverable, milestone, product/process, metrics, effort/productivity, module/component, generic/custom | PDF pp. 11–15; §§1.4–1.5.7 | Use terms consistently. A commit count is not a productivity measure; a GitHub release is only a candidate milestone until its role is established. |
| Management concerns: people, product, process, and project | PDF pp. 15–16; §1.6 | Organize the context around project goals, contributors, process evidence, and product characteristics; avoid inferring private management decisions. |

## Questions for the case study

- What user or organizational problem does the target appear to address, and what evidence supports that description?
- What constitutes the software product in this case: code, documentation, setup/deployment procedures, and operational components?
- Which product and process characteristics are observable in the repository, and which remain unknown?
- What evidence suggests a recurring engineering process or improvement practice? What evidence would be needed before making that claim?

## Evidence to collect

- Project README, user/developer documentation, release notes, supported deployment or operating procedures.
- Repository structure and contribution guidance; dated releases, issue/PR and commit samples where later phases permit.
- Explicitly stated project goals, supported platforms, audience, and license, with source location and access date.

## Method

Define a short system profile from primary project artifacts. Separate **Observed** repository facts from **Inferred** context and **Not available** items. Keep course examples and definitions cited as course theory; never transfer a historical failure or statistic from the notes to the target.

## Common pitfalls

- Calling a source-code repository the entire software product without checking docs, operations, dependencies, or deployment material.
- Treating terminology as measured evidence: commits, contributors, and LOC alone do not establish productivity, quality, or process maturity.
- Claiming original requirements, budget, staffing decisions, or management intent without a source.

## Reviewer checklist

- [ ] System purpose is paraphrased from a cited primary project source.
- [ ] Product boundary includes relevant documentation and operating/deployment information.
- [ ] Observations, inferences, and unknowns are clearly labeled.
- [ ] No course historical example is presented as a target-system finding.
- [ ] Product/process/effort/metric terminology is used consistently.
