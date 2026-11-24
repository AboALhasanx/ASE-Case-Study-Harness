# Chapter 3 — Software Requirements: Analysis and Specifications

**Source:** `knowledge/Ch3.pdf` (99 PDF pages). Page numbers below refer to the page index inside the PDF; cite the exact relevant subsection/page when applying a concept.

## Concepts to apply

| Topic | Source locator | Case-study use |
|---|---|---|
| Requirements engineering process and current practice | PDF pp. 1–6; §§3.1–3.1.2 | Reconstruct only requirements supported by public docs, behavior, tests, or issue discussions; do not claim these are the original private requirements. |
| Functional vs. non-functional; user vs. system requirements; interfaces | PDF pp. 6–8; §§3.2.1–3.2.3 | Classify externally visible capabilities separately from quality attributes and interface constraints. Keep user-level language distinct from technical detail. |
| Feasibility studies | PDF pp. 8–9; §§3.3.1–3.3.2 | Assess technical, operational, economic, schedule, or related feasibility only for the bounded case-study question and available evidence. |
| Elicitation techniques: interviews, brainstorming, FAST, QFD, use cases | PDF pp. 9–19; §§3.4.1–3.4.5 | For a retrospective OSS study, use public issue/discussion/user documentation as traces, not as a substitute for direct stakeholder interviews. Mark unobserved stakeholder needs unavailable. |
| Analysis models: DFDs, data dictionaries, ER diagrams, prototyping | PDF pp. 19–33; §§3.5.1–3.5.4 | Derive diagrams from observed interfaces, data schemas, and behavior; label reconstructed models and cite each element. |
| SRS nature, quality characteristics, organization, and examples | PDF pp. 33–95; §§3.6 onward | Produce a concise reconstructed SRS with unique IDs, source traceability, testable wording, and explicit uncertainty. Select only relevant template parts; don’t imply historical authenticity. |

## Questions for the case study

- Who are the evidenced user classes and external systems? Which stakeholders are absent from public sources?
- Which functional capabilities can be traced to documentation, UI/API behavior, tests, or maintained issue discussions?
- Which non-functional concerns are explicitly specified or can be tested safely in a local, isolated environment?
- Can representative workflows be modeled with use cases, DFD/data dictionary, or ER diagrams using evidence from the target?
- Are reconstructed requirements clear, consistent, bounded, and verifiable? Which remain inferred or unknown?

## Evidence to collect

- README/user guides, API and interface docs, examples, schemas/migrations, tests, UI routes or command interfaces.
- Issues/discussions only as dated reports or requests; distinguish a request from an accepted requirement and a fix from proof of user need.
- For each requirement: ID, statement, class (functional/non-functional/interface), evidence link and locator, status/confidence, rationale, and verification idea.

## Method

Create a traceability matrix linking source artifacts → reconstructed requirement/use case → analysis model or test idea. Keep user requirements concise and implementation-independent; put observed technical details in system requirements or evidence notes. Draw models only from identified evidence, and mark missing details rather than filling them in. Cite PDF page(s) for theory separately from target evidence.

## Common pitfalls

- Presenting a reconstructed SRS as the original project SRS.
- Converting every GitHub issue into a requirement regardless of status or acceptance.
- Calling a quality attribute verified because the code contains a related setting or label.
- Drawing detailed DFD/ERD elements from assumptions rather than observed flows/schema.
- Copying a long SRS template wholesale when the evidence and scope support only a smaller subset.

## Reviewer checklist

- [ ] Every requirement has a stable ID, type, status, source, and verification idea.
- [ ] User needs, system behavior, and design choices are kept distinct.
- [ ] Open/closed issue state and date are preserved when issue records are cited.
- [ ] Diagrams show provenance or mark reconstructed/uncertain elements.
- [ ] SRS claims are testable or explicitly qualified.
- [ ] Private/original requirements are marked **Not available** when unsupported.
