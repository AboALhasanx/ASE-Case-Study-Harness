# Chapter 6 — Software Metrics

**Source:** `knowledge/Ch6.pdf`, PDF pages 1–58 (printed pages 250–307).

## Concepts and source locations

- Metric purpose, definition, application areas, implementation problems, and metric categories (PDF pp. 1–5).
- Token-count / Halstead measures: operator and operand counts, vocabulary/length, volume, level or difficulty, effort, time, and language level (pp. 5–15).
- Data-structure measures: amount and use of data, live variables, module weakness, and data sharing (pp. 15–33).
- Information-flow measures and model variants (pp. 34–37).
- Object-oriented measures: size, coupling, cohesion, and inheritance (pp. 38–45).
- Use-case and web-engineering measures (pp. 46–48); analysis, statistical interpretation, data problems, and application practices (pp. 48–52).

## Case-study questions

1. Which metrics can be calculated reproducibly from the selected revision and are relevant to the study question?
2. For a representative module, what complexity, size, data-use, or dependency metrics can be calculated, and how do they vary across the chosen sample?
3. For an object-oriented system, which class measures (for example, method count/complexity, coupling, cohesion, inheritance depth or children) are meaningful under the source definitions?
4. Are any measures based on documentation or use cases rather than source code? What assumptions affect the result?
5. What can the measured sample support, and what cannot be generalized to the whole project?

## Evidence and method

- Start with a measurement question and define the metric, unit, formula, inclusion/exclusion rules, aggregation, and interpretation before collecting values.
- Pin the target revision and select a representative sample using stated criteria (for example, core production modules stratified by subsystem). Exclude generated/vendor code only with a documented rule.
- Record tool name/version, command, environment, inputs, raw result, and date. Preserve raw machine-readable output when possible.
- For manual or source-defined counts, publish the counting convention and show a worked example that another reviewer can repeat.
- Recalculate a sample independently and check totals, denominators, and units. Distinguish observed counts from model-based estimates.
- Consult the cited chapter pages for the exact formulas and assumptions before applying Halstead, live-variable, information-flow, OO, use-case, or web metrics.

## Pitfalls and limits

- A metric is an operationalized measure, not a direct proxy for quality or developer productivity.
- Different parsers, language constructs, generated files, and counting rules can change results. State the exact rule set.
- The chapter's textbook formulas and worked examples may depend on assumptions that do not transfer directly to modern languages or repositories.
- Do not compare systems unless scopes, tools, versions, and definitions are comparable.
- Outliers, small samples, and missing project context may dominate summary statistics; report distributions and limitations, not only averages.
- Do not claim a threshold is good/bad unless an appropriate, cited benchmark supports it.

## Reviewer checklist

- [ ] Each metric has a definition, formula, unit, scope, and stated interpretation.
- [ ] Revision, sample selection, exclusions, tool/version, commands, and date are recorded.
- [ ] Raw values and at least one independently checked calculation are available.
- [ ] Estimates are distinguished from direct counts.
- [ ] Claims do not exceed the sample or evidence.
- [ ] Chapter page references and target evidence references are separate and traceable.
