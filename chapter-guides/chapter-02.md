# Chapter 2 — Software Life Cycle Models

**Source:** `knowledge/Ch2.pdf` (20 PDF pages). Page numbers below refer to the page index inside the PDF.

## Concepts to apply

| Topic | Source locator | Case-study use |
|---|---|---|
| Life cycle, development process, and Build-and-Fix | PDF pp. 1–2; §2.1 | Use as a comparison model, not a label for a project merely because its process documentation is sparse. |
| Waterfall phases and artifacts | PDF pp. 2–4; §2.2 | Compare the stated sequence of requirements, design, implementation/unit test, integration/system test, and operation/maintenance against actual evidence. |
| Incremental models: iterative enhancement and RAD | PDF pp. 4–6; §§2.3.1–2.3.2 | Look for staged releases and feedback; a sequence of versions alone does not prove a particular model. |
| Evolutionary models: prototyping and spiral | PDF pp. 6–9; §§2.4.1–2.4.2 | Search for evidence of prototypes, repeated user feedback, and explicit risk analysis. Keep risk-driven spiral classification cautious. |
| Unified Process phases and work products | PDF pp. 9–15; §§2.5.1–2.5.2 | Look for lifecycle stages and work products; don’t assume terminology maps one-to-one to public GitHub milestones. |
| Model selection: requirements, team status, user involvement, project type and risk | PDF pp. 15–17; §2.6 | Use these dimensions to explain which model best fits the observable constraints, and identify missing private/team evidence. |

## Questions for the case study

- What lifecycle evidence is available across releases, requirements documents, design docs, tests, deployment, maintenance, and retirement/deprecation?
- Which model, if any, best explains the observed process? What competing explanation fits the same evidence?
- Is there evidence of incremental delivery, user feedback, prototyping, or risk-driven iteration?
- Which selection factors from §2.6 are visible, and which (team experience, user access, project constraints) are not public?

## Evidence to collect

- Version tags/releases, changelog entries, issue and pull-request timelines, roadmap or contribution process.
- Design/specification docs, test suites and CI workflows, user feedback channels, deprecation/maintenance statements.
- A small defined time window and representative sample; record query/filter and sample counts.

## Method

Build a dated lifecycle timeline from cited artifacts. State a candidate model as **Inferred**, list supporting and conflicting observations, and name unavailable evidence. Explain how the model-selection factors inform the interpretation; do not equate a release cadence with a lifecycle model.

## Common pitfalls

- Inferring Waterfall from ordered release notes or Agile from frequent commits.
- Assigning a Unified Process phase based solely on the name of a GitHub milestone.
- Treating lack of published planning documents as evidence that no planning took place.
- Ignoring survivorship bias in a history sample or the gap between public artifacts and private team practice.

## Reviewer checklist

- [ ] Lifecycle claim is explicitly labeled **Inferred**.
- [ ] Timeline citations point to immutable tags/commits or dated project records.
- [ ] At least one alternative interpretation and its limitations are considered.
- [ ] Team/user/risk factors are not asserted without evidence.
- [ ] Sample window and selection method are reproducible.
