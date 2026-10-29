# AI Loop Skill: local preflight

This record covers local package checks and the documented control-flow example. The machine-readable report is in [local-check-results.json](../evals/local-check-results.json).

## Scope

The package check inspects required files, skill metadata, README heading order, the assistant setup heading, interface invocation, relative links, portable navigation, the evaluator JSON example, and pseudocode syntax.

The control-flow check runs the exact Python example from [SKILL.md](../SKILL.md) with synthetic adapters. It checks success, feedback propagation, iteration caps, best-attempt retention, no-progress detection, terminal escalation, risk precedence, and invalid iteration limits.

## Results

| Check suite | Recorded result | What the result covers |
|---|---|---|
| Package preflight | 9/9 passed | Required files, metadata, heading order, setup, invocation, relative links, portable navigation, JSON example, and pseudocode syntax |
| Synthetic loop control flow | 9/9 passed | Selected branches of the documented example using controlled local adapters |

The checks ran with Python 3.11.15. The saved JSON record contains the actual UTC run time, per-check results, and fingerprints of the checked skill and scripts. Both commands exited with status 0 and made no model calls. No assistant installation or live model comparison was performed as part of this run.

## Reproduction

From the repository root:

```bash
python scripts/check_package.py
python evals/check_loop_model.py
```

Both commands print JSON and exit nonzero on failure. Neither writes files or contacts a service. The control-flow check executes this repository's inspected example with synthetic functions; review that example before executing a modified copy.

## Interpretation

These checks cover package integrity and selected branches of an illustrative loop. They do not establish model quality, evaluator accuracy, factual correctness, cost savings, assistant discovery, or production behavior. Timeouts, tool budgets, permissions, and error handling belong in the consuming application.

Use [the benchmark protocol](benchmark-protocol.md) for the next model comparison. Preserve this record when adding later results.
