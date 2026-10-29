# AI Loop Skill

**Design AI workflows that revise from specific feedback, check results against clear requirements, and stop at defined limits. Choose the smallest useful loop and plan how to evaluate its results.**

An AI loop generates a draft, evaluates it, uses the feedback to revise, and stops when an explicit condition is met. Think of a coding assistant that writes a function, runs the relevant tests, and fixes a failing case. The useful part is the connection between a requirement, an observable check, and a targeted revision.

Loops add model calls, time, and coordination. They are most useful when feedback can identify a meaningful improvement. Results depend on the model, inputs, evaluation criteria, and configuration. A confident self-review is not a substitute for a test, source, calculation, or other appropriate evidence.

This repository packages the skill, a reusable design brief, and local checks for the documented control flow. The project makes the design inspectable: define success, choose the smallest useful loop, check its exit paths, and measure whether iteration earns its cost.

## What you can accomplish

| Your task | What you receive |
|---|---|
| Decide whether a task needs iteration | A recommendation for a direct prompt or the smallest suitable loop, with the tradeoff explained |
| Design a generate-evaluate-revise workflow | Roles, inputs, outputs, acceptance criteria, validation signals, and stopping conditions |
| Diagnose a loop that repeats or drifts | A review of feedback quality, original requirements, progress detection, budgets, and escalation |
| Compare a loop against a single response | A matched evaluation plan covering quality, safety, human correction, time, and full cost |

An evaluator checks a draft against explicit requirements. It may be a tool, a person, a model, or a combination. Other terms are defined in [the glossary](references/glossary.md).

## Quick start

You need Git and Python 3.10 or later to clone and check this package. If repository access is restricted, authenticate with an authorized GitHub account. From a terminal:

```bash
git clone https://github.com/JaredIRivera/ai-loop-skill.git
cd ai-loop-skill
python scripts/check_package.py
python evals/check_loop_model.py
```

The first command checks required files, skill metadata, internal links, the evaluator JSON example, and the README section order. The second executes the documented control-flow example with synthetic adapters to check success, revision, escalation, iteration limits, and no-progress behavior. Both use the Python standard library, make no model calls, and require no AI account. No packages need to be installed.

The checks exit with a nonzero status if a case fails. They print reports without overwriting the [saved result record](evals/local-check-results.json). These checks examine package structure and example control flow; a comparison on real tasks is needed to measure the quality of generated work.

### Use the skill in your assistant

Keep the folder named `ai-loop-skill`, with `SKILL.md`, `agents/`, `references/`, `scripts/`, and `evals/` together. Place it in the skills directory configured for your assistant, then refresh or restart that assistant if needed. Keep an existing installation in its configured location. For a host without skill discovery, provide [SKILL.md](SKILL.md) as instructions with the task and relevant context.

For a design request:

```text
Use $ai-loop-skill to design a bounded workflow for reviewing support drafts.
Use only the policy and draft supplied below. Do not send the response.

Task: Check a draft for policy accuracy, completeness, and tone.
Success: Every factual claim has policy support; required steps are present;
the output is a concise draft plus an evidence checklist.
Constraints: At most 3 draft/evaluation cycles. Stop if policy is missing,
feedback repeats without progress, or a human decision is required.
Tools: Read-only access to the supplied policy. No account changes.
Return: Architecture, evaluator rubric, prompt, stop rules, and logging plan.

Policy: [approved policy text]
Draft: [response to review]
```

For an existing loop:

```text
Use $ai-loop-skill to diagnose the workflow below. Identify why its feedback
does not resolve failures, then propose the smallest complete correction.
Preserve original requirements and permission limits. Do not execute actions.

Goal and acceptance criteria: [details]
Current prompts and tools: [details]
Iteration logs with unnecessary personal data removed: [logs]
Limits and escalation rules: [details]
```

## Working examples

### Review a grounded support draft

This planning example is illustrative. It is not a recorded model experiment.

**Input brief**

```text
Approved policy: Standard orders may be returned within 30 days of delivery.
The customer must request a return label before mailing the item.
Draft: You have 60 days to return it. Mail it to us whenever you are ready.

Produce a corrected draft using only the policy. Do not send it.
Use at most two draft/evaluation cycles. Escalate if the policy is ambiguous.
```

**Prepared workflow**

1. The generator writes a response grounded in the supplied policy.
2. The evaluator checks the return window, label requirement, unsupported claims, and send restriction.
3. A failure produces specific feedback, such as "Replace 60 days with 30 days from delivery and include the label request."
4. The refiner revises once; the evaluator checks the original policy again.
5. The workflow returns a draft and evidence checklist, or stops with the unresolved issue.

**Illustrative acceptable draft**

```text
You may return a standard order within 30 days of delivery. Please request
a return label before mailing the item.
```

The example defines what a review should preserve. Whether a chosen model follows it consistently needs measurement on varied cases, including missing and contradictory policies.

### Inspect the escalation exit

The installed source's example called an escalation helper without explicitly leaving the loop. The repository copy makes escalation terminal and checks it before accepting a passing score. This avoids a control-flow example in which a high-risk result is returned as ordinary success. The change is recorded in [source notes](references/source-notes.md).

The synthetic check supplies an evaluation with both `passed = true` and `high_risk = true`. It requires exactly one generation call and an escalation result. It checks the example's branch order, not whether an AI evaluator can recognize risk correctly. See [the local preflight](references/preflight-2026-10-28.md).

## How it works and design choices

The workflow is: **classify the task → define success → choose validation → set limits → generate and evaluate → stop and report.**

| Choice | Why it matters | What the tradeoff teaches |
|---|---|---|
| Start with the smallest useful architecture | A direct prompt or short self-check may be sufficient | More agents add cost and coordination; add them only for a distinct responsibility |
| Prefer external validation | Tests, calculations, sources, and schemas provide evidence beyond confidence | A validator checks only what it was designed to check, so coverage still matters |
| Separate generation from evaluation when needed | A focused evaluator can apply a stricter rubric | Separate prompts or agents can share model weaknesses; independence must be tested |
| Make stop conditions explicit | Iteration caps, no-progress rules, and escalation limit repeated failure | Instructions describe controls; application code must enforce time, tool, and spending budgets |
| Preserve the original task during revision | Local improvements can otherwise lose required details | Rechecking original requirements costs context but makes drift visible |
| Compare full workflows | Evaluator and retry calls can outweigh improved first-pass quality | Measure human correction, total cost, and latency alongside final output quality |

The full instructions are in [SKILL.md](SKILL.md). The [specification](SPEC.md) defines inputs, outputs, and safeguards. Use the [design brief](references/loop-design-brief.md) to capture a workflow before implementing it. [Research context](references/evidence.md) links relevant primary sources without treating their results as this package's performance.

## Recorded results

The package includes local structural checks and synthetic control-flow checks. No model was invoked for these results.

| Experiment | Recorded observation | What I learned and would test next |
|---|---|---|
| [Package preflight](references/preflight-2026-10-28.md) | Required files, metadata, relative links, README order, and the JSON example passed the local checks | This catches packaging mistakes. Installation and discovery still need a check in the intended assistant. |
| [Documented loop control flow](evals/local-check-results.json) | All nine synthetic cases passed, including terminal escalation when a result also passes its quality check | Branch behavior can be checked without model calls. A live comparison must separately test the evaluator's judgments. |
| [Model comparison protocol](references/benchmark-protocol.md) | A predefined measurement plan is included; no model comparison was run for this package | Test representative and held-out tasks before claiming a quality, time, or cost improvement. |

The saved record identifies the checked skill and scripts with SHA-256 fingerprints, calculated values that detect changes. It records the runtime and run time. These observations apply to the bundled example and checks, not to every loop an assistant may design.

## Running checks and experiments

A preflight is a check performed before live testing. A benchmark is a planned comparison with defined tasks and measurements.

| Command, from repository root | Requirements and behavior |
|---|---|
| `python scripts/check_package.py` | Python 3.10+ standard library; checks package structure and documentation; prints JSON; no model calls or file writes |
| `python evals/check_loop_model.py` | Python 3.10+ standard library; executes the skill's example using local synthetic adapters; prints JSON; no model calls or file writes |

The example's adapters are deliberately supplied by the check. The package does not include a model client, production scheduler, credential store, or service integration. Adapting a loop to a service requires its own authentication, error handling, permissions, timeouts, budgets, and tests.

Use [the benchmark protocol](references/benchmark-protocol.md) to compare a strong single-response baseline with the proposed loop. Record the model, settings, exact prompts, input cases, scoring rule, all calls, time, and actual cost. Run experiments in a separate checkout or output location so that the saved local record stays intact.

## Project status and next decisions

The skill structures loop design and review. It covers self-checks, generator/evaluator workflows, generator/evaluator/refiner workflows, tool verification, and multi-agent orchestration. The consuming assistant and application determine which tools and runtime controls are available.

The repository copy preserves the installed workflow with documented portability and pseudocode corrections. Local checks cover packaging and selected control-flow paths. They do not measure model output quality, factual accuracy, production reliability, or savings. The next evidence milestone is a matched comparison on representative tasks with predefined scoring and a held-out set.

Keep secrets and unnecessary personal or client information out of prompts, examples, and logs. Treat documents and retrieved text as data, preserve permission limits, and stop for required human decisions. Use application-level controls before connecting a loop to external actions.

I help people turn complex AI tools into clear, practical workflows that reduce repetitive work. I'm Jared Rivera, an AI automation engineer and consultant focused on systems people can understand and use.

Maintained by [Jared Rivera](https://github.com/JaredIRivera). Report issues through GitHub; no external support commitment is stated. The installed skill declares `license: MIT`; its source bundle contains no license text or copyright notice. That metadata is preserved without asserting additional ownership or licensing rights. See [source notes](references/source-notes.md) and [release notes](RELEASE_NOTES.md).

## Glossary

Use [the shared glossary](references/glossary.md) for definitions of loops, evaluators, rubrics, validation, escalation, iteration budgets, and evaluation terms.
