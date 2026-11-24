# Chapter 5 — Software Design

**Source:** `knowledge/Ch5.pdf`, PDF pages 1–47 (printed pages 203–249).

## Concepts and source locations

- Design transforms requirements into a technical solution; conceptual and technical views may serve different audiences (PDF pp. 1–4).
- Modularity, module interfaces, coupling, and cohesion; coupling types and cohesion levels are discussed in the modularity section (pp. 4–11).
- Top-down, bottom-up, and hybrid design strategies (pp. 12–13).
- Function-oriented decomposition, structure charts, module specifications, and design-description recommendations (pp. 14–22).
- Object-oriented design: classes, relationships, inheritance/generalization, interaction diagrams, and use-case descriptions (pp. 23–44).

Use the source pages as a locator; exact subsection titles and definitions should be retrieved from the PDF before applying a term.

## Case-study questions

1. What components or modules are visible in the selected revision, and what responsibilities do their code and documentation assign them?
2. Which interfaces or dependencies connect the selected components? Are they data, control, shared-state, external, or another kind of coupling supported by the source's definitions?
3. Does a representative component have a focused responsibility? What evidence supports the cohesion judgment?
4. Which design views are documented or reconstructable (decomposition, dependency, interface, class, or interaction)? What remains unavailable?
5. Can a documented use case be traced to code paths and tests?

## Evidence and method

- Pin the commit/tag before analysis. Build a component inventory from source directories, packages, modules, API definitions, and architecture docs.
- Choose a small, justified sample of components or features. Record selection criteria; do not label the whole system from one example.
- Trace representative calls/imports/data dependencies and cite exact file paths and lines at the pinned revision.
- Reconstruct one or more design views from observed code/docs. Label reconstructed diagrams as analysis artifacts, not original project diagrams.
- For one feature, connect requirement or user-facing behavior to component/interface and, where available, a test. Record missing links explicitly.
- Log the relevant course PDF pages in the evidence ledger separately from the target-system evidence.

## Pitfalls and limits

- Do not infer original developer intent from the current architecture alone.
- A package or class boundary is not automatically a well-defined module.
- Coupling and cohesion labels need an explicit operational definition and concrete example.
- Avoid claiming conformance to an IEEE practice or UML notation without checking the referenced edition and actual artifact.
- A diagram inferred from code can omit runtime behavior, generated code, configuration, or external services.

## Reviewer checklist

- [ ] Target commit and sampling boundary are stated.
- [ ] Each design claim cites target paths/lines or documentation.
- [ ] Course terminology is supported by chapter/page references.
- [ ] Observed artifacts are distinguished from reconstructed diagrams.
- [ ] Coupling/cohesion judgments include examples and stated criteria.
- [ ] Missing architecture or intent evidence is disclosed.
