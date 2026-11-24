# Chapter 8 — Software Testing

**Source:** `knowledge/Ch08_Software_Testing.pdf` (153 PDF pages; printed text begins at p. 365). Use the PDF page locator as the stable source reference and include the printed page where readable.

## Concepts and source locations

- Testing strategy, test objectives, and limits of exhaustive testing: PDF pp. 1–4 (printed pp. 365–368).
- Fault/error/failure terminology, test cases, verification vs. validation, and alpha/beta testing: PDF pp. 4–8 (printed pp. 368–372).
- Functional test design, including boundary-value and related input-selection methods: PDF pp. 8–49 (printed pp. 372–413).
- Structural testing and control-flow coverage: PDF pp. 50–120 (printed pp. 414–484).
- Testing levels, validation, debugging, and testing tools: PDF pp. 121–153 (printed pp. 485–517).

## Case-study questions

1. What test levels and test types are visible in the target repository, and where are they defined?
2. Which representative user-visible behaviors have existing tests, and what expected outcomes do those tests assert?
3. What gaps appear when a small, justified sample of requirements or code paths is compared with test coverage?
4. Can a safe, isolated subset of tests run on the pinned revision? If not, which setup constraint prevents execution?

## Evidence and method

- Inventory test directories, test framework/configuration, CI workflows, and documented test commands at the pinned commit.
- Select cases using a stated rule (for example, one core workflow plus one boundary/error case); connect each case to a source requirement, user documentation, or clearly labelled reconstructed requirement.
- Record test ID, preconditions, inputs, expected result, command, environment/tool version, actual output, and source revision. Link test-file paths/lines and CI runs where available.
- Label tests as **Executed**, **Inspected**, or **Proposed**. Save failed setup output as a setup limitation; it is not a test result.
- For a test-design exercise, use relevant course techniques such as boundary-value analysis, equivalence classes, or structural coverage, and show the selected inputs and rationale. Avoid claiming completeness from a small sample.

## Pitfalls and reviewer checklist

- Do not treat test count or a green CI badge as proof that the system is defect-free or reliable.
- Separate verification of artifacts from execution-based validation; report the exact scope of each.
- Confirm that expected results have an independent basis and are not invented from observed implementation behavior alone.
- Check that every claimed execution has a reproducible command, revision, environment, and captured outcome.
- Check sample-selection bias, test data safety, coverage definitions, and limitations; do not run tests against a live service or real user data.
