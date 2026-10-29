# AI Loop Skill: glossary

| Term | Meaning in this project |
|---|---|
| AI loop | A workflow that generates an output, evaluates it, uses feedback, and repeats under explicit limits |
| Generator | The role or component that produces a draft |
| Evaluator | A tool, person, model, or combination that checks the draft against requirements |
| Refiner | The role or component that revises a draft using specific feedback |
| Rubric | Named criteria and a defined scoring or pass/fail rule |
| Validation signal | Evidence used to check a requirement, such as a test result, source passage, calculation, or schema check |
| External validation | A check beyond the generating model's own unsupported judgment |
| Iteration | One complete generation and evaluation cycle in the core example |
| Stop condition | An explicit reason to end a loop, such as success, budget exhaustion, missing input, or no progress |
| Escalation | Stopping autonomous work and returning an issue that needs an authorized human decision |
| No-progress detection | A rule that identifies repeated or unchanged failures so the loop can stop |
| Baseline | The comparison condition, usually a strong single-response prompt with equivalent inputs and tools |
| Held-out case | An example reserved for evaluation rather than used to develop the workflow |
| Preflight | A local check before a more costly or consequential experiment |
| Synthetic adapter | A small test substitute for a component; it returns controlled data instead of calling a model or service |
| Pseudocode | An illustrative description of program logic; its application-specific parts still need implementation |
| Fingerprint | A calculated hash, here SHA-256, used to identify a file's exact bytes |
| Trace | A record of inputs, outputs, checks, decisions, and actions across a workflow |

Return to [the README](../README.md) or [the specification](../SPEC.md).
