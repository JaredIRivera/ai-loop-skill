# AI Loop Skill: loop design brief

Complete this brief before implementing a workflow. Use [the skill](../SKILL.md) to choose the smallest architecture that meets the task. Definitions are in [the glossary](glossary.md).

## Reusable brief

```text
TASK AND USER
Who needs the output, and what decision or action will it support?

INPUTS
Required context:
Optional context:
Missing-input behavior:
Data sensitivity and retention limits:

OUTPUT CONTRACT
Required content:
Format and length:
Forbidden content or actions:
Evidence required for factual claims:

SUCCESS CRITERIA
List observable pass/fail requirements. Identify which require human review.

ARCHITECTURE
Why a direct prompt is insufficient:
Generator role:
Evaluator role and validation tools:
Refiner role, if separate:
Tools and permissions for each role:

EVALUATION
Rubric, weights, and threshold:
Critical failures that override a passing score:
Specific feedback format:
How original requirements are rechecked:

LIMITS
Maximum complete cycles:
Maximum elapsed time:
Maximum model and tool calls:
Maximum spend, if applicable:
No-progress rule:
Repeated-failure rule:

ESCALATION
Human decision triggers:
Missing context or permission triggers:
Result returned when blocked or capped:
Authorized resumption procedure:

LOGGING
Record inputs, draft versions, evidence, feedback, decisions, and final status.
Exclude secrets and unnecessary personal data.
Define storage location, access, and retention.

COMPARISON
Strong single-response baseline:
Representative cases and held-out cases:
Fixed scoring and acceptance rule:
Measurements: quality, safety, human correction, all calls, time, and cost.
```

## Example completed limits

For a draft-only support response workflow:

- Maximum three complete draft/evaluation cycles, including the initial draft.
- Read-only access to the supplied approved policy.
- Stop before any external message or account change.
- Stop if a required policy is absent or contradictory.
- Stop if the same failed criterion remains after two revisions.
- Return the best draft with failed criteria and evidence gaps when the cap is reached.

These are planning choices for the example. An application must enforce its actual time, cost, tool, and permission limits. The sample does not grant permission to connect to an account or send a message.
