# AI Loop Skill: benchmark protocol

Use this plan to determine whether iteration improves a specific workflow enough to justify its cost. It is a protocol, not a claim of results. Technical terms are defined in [the glossary](glossary.md).

## Compare equivalent tasks

| Condition | Definition |
|---|---|
| A: baseline | A strong single-response prompt with the same task, context, permitted tools, and output requirements |
| B: bounded loop | The proposed generator/evaluator workflow with a fixed rubric and explicit stop conditions |

Select representative cases before testing. Include ordinary successes, missing context, contradictory sources, misleading input, and relevant approval boundaries. Reserve a separate held-out set. Small screening sets can reveal failures but cannot establish production reliability.

Use the same final-answer checks in both conditions. Include all generator, evaluator, refiner, and retry calls when reporting the loop's cost. A comparison between a weak baseline and a carefully tuned loop does not isolate the value of iteration.

## Hold conditions constant

Record provider, exact model or snapshot, settings, output limits, tools, permissions, prompts, instruction version, dates, and case identifiers. Alternate execution order and use repeated trials where output variation matters. Keep test data separate from development examples.

Define rubrics, scoring rules, critical failures, and the promotion rule before viewing results. Prefer deterministic checks for calculations, code, and structure; use blinded human review for open-ended quality where practical. For factual tasks, inspect source support and contradictions.

## Record measurements

For every case and condition, record:

- Final requirement checks, unsupported claims, and safety or authorization failures.
- Evaluator false passes and false failures against external checks or human review.
- Number of drafts, model calls, tool calls, retries, and escalation reason.
- Total tokens when reported, elapsed time, actual billed cost when available, and missing telemetry.
- Human correction required before the output is usable.
- Whether required facts or constraints were lost during revision.
- Exact inputs, outputs, and relevant evidence after removing unnecessary sensitive information.

Separate observed data from estimates and missing measurements. A successful local control-flow test says nothing about the quality of a live evaluator's judgments.

## Score quality and safety

Define acceptance criteria for the actual use case. At minimum, require no new critical safety or authorization failure and preserve required correctness and output structure. Decide the acceptable tradeoff between quality, time, cost, and human correction before testing.

For a draft-only support pilot, a possible rule is: all policy claims supported, all mandatory steps included, no unauthorized send action, and a human reviewer considers the draft usable. The loop must improve a predefined quality or correction measure enough to justify its added time and cost. This is an example rule, not a universal threshold.

Inspect errors by case. Report uncertainty and model variation. Do not change scoring after seeing a failure and present the revised score as the original result.

## Report the result

Show baseline and loop results side by side, including failures, escalation, all calls, total time, total cost, and human correction. Explain which findings are observed, estimated, or not measured. Identify whether the evaluator's checks cover the actual risks.

Use a separate output location to preserve the repository's local check record. A live test requires the intended model account, appropriate data permissions, and an authorized usage budget. No live runner or credentials are included in this package.
