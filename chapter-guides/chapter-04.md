# Chapter 4 — Software Project Planning

**Source:** `knowledge/Ch4.pdf` (64 PDF pages). Page numbers below refer to the page index inside the PDF.

## Concepts to apply

| Topic | Source locator | Case-study use |
|---|---|---|
| Planning activities and size estimation | PDF pp. 1–12; §4.1 | Define the case-study scope first. Measure the selected code snapshot with explicit LOC rules, or estimate functional size only where requirements evidence supports it. |
| LOC and function points | PDF pp. 3–12; §§4.1.1–4.1.2 | Explain language dependence and counting convention for LOC. Function points require user-visible inputs, outputs, inquiries, logical files and external interface files; label counts reconstructed. |
| Cost estimation and model types | PDF pp. 12–14; §§4.2–4.3 | Distinguish measured project facts from an illustrative estimate for reproducing the bounded work. State model and inputs. |
| COCOMO, COCOMO II and project modes | PDF pp. 14–43; §§4.4–4.5.3 | Use only if size and calibration assumptions are defensible. Show formulas, selected mode/drivers, intermediate values, and sensitivity/range; do not report an estimate as actual project cost. |
| Putnam resource-allocation model and time/cost trade-off | PDF pp. 43–56; §§4.6–4.6.5 | Use as course theory or a clearly qualified comparison; public repository evidence rarely supplies enough calibrated inputs for a reliable original-project estimate. |
| Software risk and risk management activities | PDF pp. 56–60; §§4.7–4.7.3 | Create a case-study risk register with probability/impact rationale, exposure if supported, mitigation/monitoring, and owner. Separate research risks from risks the target team faced. |

## Questions for the case study

- What is the bounded work and deliverable set for this student case study, and what assumptions/exclusions define it?
- Which size measure is meaningful for the target revision? Can the counting rules be reproduced?
- Is there enough defensible input for a course estimation model? If not, which inputs are unavailable and why should the estimate be withheld?
- What risks threaten the study (setup, inaccessible history, sampling bias, time, tool/resource limits), and how will they be managed?

## Evidence to collect

- Target revision, language inventory, source boundaries, and machine-readable count output where applicable.
- Documented system functions and data/interface examples if constructing a function-point estimate.
- Estimation formula, model version/source, parameter choices, conversion assumptions, and arithmetic worksheet.
- For the student project, agreed scope, task breakdown, schedule constraints, tools/resources, and a risk register.

## Method

Separate two different estimands: (1) a prospective estimate for the student case-study work, based on its defined tasks/resources; and (2) any hypothetical estimate of target-system development, which should be omitted unless inputs are credible. Mark all estimates **Estimated**. Include ranges or sensitivity when assumptions materially affect results. For LOC, state file filters, generated/vendor exclusions, comment/blank policy, and tool version. For function points, show every function-type count and complexity rationale.

## Common pitfalls

- Treating code size as a historical estimate of the effort or cost that produced the target.
- Applying COCOMO with guessed KLOC, mode, multipliers, or current salaries and presenting precision as accuracy.
- Mixing code size, function points, calendar time, and person-months without explaining conversions.
- Counting generated, vendored, test, or documentation files without a declared scope.
- Listing risks without owners, indicators, response actions, or evidence-based prioritization.

## Reviewer checklist

- [ ] The estimate answers a stated question and uses a named model.
- [ ] Inputs, units, formulas, assumptions, exclusions, and calculation steps are visible.
- [ ] LOC/FPA boundary and counting rules are repeatable.
- [ ] Estimates are never represented as observed original project data.
- [ ] Sensitivity/uncertainty is reported where assumptions dominate.
- [ ] Risks distinguish the case study from the target team's unobserved project risks.
