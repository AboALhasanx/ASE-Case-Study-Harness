# Chapter 7 — Software Reliability

**Source:** `knowledge/Ch07_Software_Reliability.pdf`, PDF pages 1–85 (printed pages 307–363).

## Concepts and source locations

- Reliability basics: operational conditions, failures versus faults, environment, and uses of reliability studies (PDF pp. 1–18; §§7.1–7.1.5).
- Product quality models: McCall, Boehm, and ISO 9126 (pp. 19–32; §§7.2.1–7.2.3).
- Reliability models: basic execution-time, logarithmic Poisson execution-time, calendar-time component, Jelinski–Moranda, and bug-seeding models (pp. 33–60; §§7.3.1–7.3.5).
- Process maturity and quality assurance: Capability Maturity Model (CMM) and ISO-9000/ISO-9001 discussion (pp. 61–74; §§7.4–7.5).

## Case-study questions

1. What operational profile and environment are evidenced for the target? Which users, inputs, workloads, and conditions are missing?
2. What public evidence exists about observed failures, defects, fixes, and reliability-related testing? What is the reporting bias?
3. Which product-quality factors can be evaluated from repository artifacts, and which require runtime/user evidence not available here?
4. Is there sufficient failure-time or execution data to fit a reliability model? If not, which model-based claims must remain unavailable?
5. What process practices (reviews, CI, release controls, defect tracking, documented procedures) are observable? Can they support any carefully bounded maturity discussion?

## Evidence and method

- Define the reliability claim before analysis: probability of failure-free operation under a specified environment/time, failure intensity, or another explicit quantity.
- Capture target version, runtime environment, workload/operational profile, observation duration, failure definition, and data-collection method for any empirical estimate.
- Use issue/commit/test/release evidence to build a traceable failure-and-fix sample. State search terms, date range, inclusion rules, duplicate handling, and known reporting gaps.
- Apply quantitative reliability models only when their required inputs and assumptions are met. Preserve the dataset and calculations; otherwise mark the estimate **Not available**.
- Map quality attributes to observable evidence (tests, static analysis, interfaces, documentation, supported environments), and describe indirect proxies as proxies.
- For CMM/ISO topics, report observed practices and evidence only. Do not certify or score the project as conformant without an authorized, complete assessment against a specific standard/version.

## Pitfalls and limits

- A fault in source code is not the same as an observed failure during operation.
- GitHub issues are a selected, incomplete sample, not a complete operational failure log.
- Test counts, stars, release frequency, or absence of reported defects do not establish reliability.
- Reliability depends on a defined environment and workload; avoid an unqualified “reliable/unreliable” conclusion.
- Process maturity frameworks assess organizational practices and evidence; public repository artifacts may be incomplete and cannot establish an audit result.
- Keep the source's historical standards/models distinct from current standards or current project claims.

## Reviewer checklist

- [ ] Reliability measure, environment, time/workload, and failure definition are explicit.
- [ ] Failures and faults are not conflated.
- [ ] Data source, sampling window, collection method, and missing-data limits are recorded.
- [ ] Reliability models are used only with supported inputs and assumptions.
- [ ] Quality-factor evaluations cite observable evidence and identify proxies.
- [ ] CMM/ISO observations are not mislabeled as certification or formal conformance.
- [ ] Conclusions and limitations are proportionate to the evidence.
