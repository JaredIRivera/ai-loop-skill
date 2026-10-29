---
name: ai-loop-skill
description: "Use when designing, prompting, evaluating, or implementing AI loops, loop engineering, agent loops, evaluator-optimizer workflows, reflect-refine loops, reflection loops, maker-checker agents, tool-verified agents, or agentic workflows that generate, evaluate, revise, and repeat until success or a stop condition."
license: MIT
metadata:
  version: "1.0"
  research_basis: "Based on official guidance from Anthropic, OpenAI, AWS, LangGraph, Microsoft, Google Research, and academic work on Self-Refine, Reflexion, ReAct, Tree of Thoughts, and LLM self-correction limits."
---
# AI Loop Skill

## When to Use This Skill

Use this skill when the user wants help with:

- Designing a loop-based AI workflow, agent, prompt, or automation.
- Writing prompts for loop engineering, agent loops, evaluator-optimizer workflows, reflection loops, reflect-refine loops, or maker-checker systems.
- Reducing manual back-and-forth by having an AI draft, evaluate, revise, and repeat.
- Adding success criteria, rubrics, stop conditions, validation, logging, and human escalation to an AI workflow.
- Comparing one-shot prompting against a looped agent approach.
- Debugging loops that waste tokens, drift from the goal, hallucinate, repeat, or take unsafe actions.

Do not use this skill for simple one-shot tasks where a direct answer, single prompt, or short edit is sufficient. Looping adds cost, latency, and failure modes, so it should be used only when measurable quality improvement or reduced manual review justifies the overhead.

## Research-Backed Principles

Base every recommendation on these findings:

1. **Treat looping as a workflow pattern, not magic prompting.** A loop is a controlled process: generate, evaluate, give feedback, revise, and stop. Anthropic describes this as an evaluator-optimizer workflow, AWS describes generator/evaluator/refiner reflect-refine loops, LangGraph implements this with generator and evaluator nodes plus conditional edges, and Microsoft AutoGen uses coder/reviewer reflection loops.

2. **Prefer loops only when success criteria are clear.** Evaluator-optimizer workflows work best when there is a clear definition of success and feedback can be made specific. If the user cannot define “good,” first help them define a rubric instead of starting the loop.

3. **Do not rely on vague self-reflection for correctness.** Academic surveys and self-correction studies find that prompted self-correction often fails or worsens reasoning when the model has no external feedback. For factual, technical, legal, medical, financial, or operational tasks, require external validation when possible.

4. **Use external validation whenever possible.** Strong validation signals include code tests, linters, type checks, schema validators, calculators, retrieval checks, citations, database queries, policy engines, dry runs, monitoring data, and human review.

5. **Separate generation and evaluation when quality matters.** Use a distinct evaluator prompt, model, agent, tool, or rubric. A separate evaluator reduces role confusion and makes it easier to inspect failures.

6. **Always include stop conditions.** Set maximum iterations, maximum tool calls, timeout, no-progress detection, confidence thresholds, and escalation rules. Never recommend unlimited loops.

7. **Log the loop.** Capture drafts, evaluations, feedback, tool outputs, iteration count, cost/latency indicators, final status, and reasons for escalation. OpenAI’s eval guidance emphasizes traces and graders for diagnosing agent workflows.

8. **Human approval is mandatory for high-risk actions.** Any loop that can send messages, spend money, modify records, delete files, change production systems, access sensitive data, or make irreversible decisions needs approval gates.

## Core Loop Model

Use this illustrative Python-style pseudocode as a control-flow model. The generator, evaluator, selection, progress, and escalation functions are application-defined adapters, not supplied services. It demonstrates a bounded iteration count and a terminal escalation path. A consuming application must also enforce timeouts, tool-call budgets, permissions, and safe error handling.

```python
def run_loop(goal, context, rubric, validation_tools, max_iterations):
    if type(max_iterations) is not int or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")

    feedback = None
    best_attempt = None

    for iteration in range(1, max_iterations + 1):
        draft = generator(goal, context, feedback)
        evaluation = evaluator(draft, rubric, validation_tools)
        best_attempt = choose_best(best_attempt, draft, evaluation)

        if evaluation.requires_human or evaluation.high_risk:
            return escalate_to_human(draft, evaluation)

        if evaluation.passed:
            return draft

        if no_meaningful_progress(evaluation):
            break

        feedback = evaluation.feedback

    return best_attempt_with_caveats(best_attempt, evaluation)
```

## Architecture Selection

Choose the smallest loop architecture that can satisfy the user’s need.

### Single-Agent Self-Check Loop

Use for low-risk writing cleanup, formatting, brainstorming refinement, or simple consistency checks. Keep the loop short and do not use it to verify factual or technical correctness.

Controls:

- Maximum 1 to 2 revisions.
- Explicit checklist.
- Final caveat if correctness is not externally verified.

### Two-Agent Generator/Evaluator Loop

Use for higher-quality writing, QA, code review, policy checking, research coverage checks, or support response review.

Controls:

- Separate generator and evaluator instructions.
- Structured evaluator output.
- Maximum 2 to 5 iterations.
- Clear pass/fail threshold.

### Generator/Evaluator/Refiner Loop

Use when creation, critique, and rewriting benefit from specialization, such as long-form reports, proposal writing, customer support macros, or brand-sensitive writing.

Controls:

- Evaluator feedback must be concise and actionable.
- Refiner must preserve original requirements.
- Final evaluator must compare output against original context, not only the previous draft.

### Tool-Verified Loop

Use for coding, calculations, research verification, structured data, policy checks, QA, and operations.

Controls:

- Use objective tools as the main evaluator whenever possible.
- Never claim success unless validation passes.
- If validation cannot run, return a caveat and next step.
- Require approval before external side effects.

### Multi-Agent Orchestrator Loop

Use only when the task genuinely requires specialization, tool separation, security boundaries, parallel work, or complex state. Avoid adding agents merely to make the system sound advanced.

Controls:

- Define each agent’s role, inputs, outputs, tools, and permissions.
- Use least-privilege access.
- Include checkpoints, audit logs, and context compaction.
- Escalate if agents disagree or repeat without progress.

## Loop Design Procedure

Follow this procedure when building or advising on an AI loop:

1. **Classify the task.** Determine whether the user needs writing/editing, coding, research, QA, customer support, operations, or another workflow.

2. **Decide whether a loop is justified.** Recommend a one-shot prompt if the task is simple, low-risk, and easy to complete directly. Recommend a loop if quality matters, first drafts are likely to be incomplete, and evaluation is feasible.

3. **Define success criteria.** Convert the user’s goal into observable acceptance criteria. Include output format, required content, forbidden content, quality bar, and evidence requirements.

4. **Create a measurable rubric.** Use pass/fail and 0 to 5 scoring where helpful. Include feedback fields that force specificity.

5. **Pick the validation signal.** Prefer external validation. If no external validation exists, make limitations explicit and use human review for important decisions.

6. **Set stop conditions.** Include maximum iterations, maximum time, maximum tool calls, no-progress detection, repeated-failure handling, low-confidence escalation, and high-risk approval.

7. **Design the prompts or agents.** Separate generator, evaluator, and refiner roles when quality matters. Keep evaluator instructions stricter than generator instructions.

8. **Specify logging.** Record inputs, drafts, feedback, validation results, decisions, and final caveats.

9. **Test against a baseline.** Compare one-shot prompting versus looped prompting on representative examples. Track quality, revision count, token cost, latency, failure rate, and human correction rate.

10. **Report tradeoffs honestly.** State whether the loop improved quality enough to justify added cost, latency, and risk.

## Reusable Loop Prompt Template

Use or adapt this template:

```text
You are a loop-based AI agent. Complete the task by generating, evaluating,
revising, and stopping under explicit controls.

TASK
{{task}}

CONTEXT
{{context}}

TOOLS
{{available_tools}}

SUCCESS CRITERIA
The task is successful only if:
{{success_criteria}}

EVALUATION RUBRIC
Evaluate each draft using:
{{evaluation_rubric}}

MAXIMUM ITERATIONS
{{max_iterations}}

STOP CONDITIONS
Stop when:
1. The evaluator returns passed = true.
2. The loop reaches max_iterations.
3. Required context, data, tools, or permissions are missing.
4. The system detects low confidence, repeated failure, or no meaningful progress.
5. The task requires a high-risk external action.

HUMAN ESCALATION RULES
Escalate when:
{{human_escalation_rules}}

LOOP PROCEDURE
For each iteration:
1. Generate or revise the draft using the goal, context, and prior feedback.
2. Evaluate using the rubric and available validation tools.
3. If passed, return the final output.
4. If failed, produce specific feedback and revise.
5. If max_iterations is reached, return the best attempt with caveats.

FINAL OUTPUT FORMAT
{{final_output_format}}
```

## Evaluator Output Schema

Prefer structured evaluator output:

```json
{
  "passed": true,
  "confidence": "high",
  "scores": {
    "criterion_1": 5,
    "criterion_2": 4
  },
  "failed_criteria": [],
  "evidence_checked": [
    "tests",
    "citations",
    "schema",
    "policy"
  ],
  "feedback": "Specific, actionable revision instructions.",
  "requires_human": false,
  "high_risk": false,
  "stop_reason": "passed"
}
```

## Domain Playbooks

### Coding

Use generate -> test -> debug -> retest. Require external validation such as unit tests, type checks, linters, compilers, or sandbox execution. Do not claim success unless validation passes.

### Research

Use search -> synthesize -> coverage check -> more search. Require citations, source quality checks, contradiction checks, and explicit known gaps. Never invent citations or fill evidence gaps with speculation.

### Writing and Editing

Use draft -> editorial critique -> revision. Evaluate audience fit, clarity, structure, specificity, tone, completeness, and brand/style compliance. For factual claims, add source verification.

### QA

Use generate cases -> run/check -> refine. Evaluate coverage, edge cases, reproducibility, expected outcomes, and failure clarity.

### Customer Support

Use draft response -> policy/tone/factual check -> revise or escalate. Validate against knowledge base, account context, support policy, privacy rules, and approval thresholds.

### Operations Agents

Use plan -> dry run -> validate -> seek approval -> execute -> monitor. Require approval for destructive, financial, permission-changing, production, or external communication actions.

## Anti-Patterns to Prevent

Reject or redesign loops that include:

- “Keep going until perfect” with no definition of perfect.
- Unlimited iterations or no stop conditions.
- Vague self-grading such as “check if this is good.”
- No external validation for factual, technical, or high-risk tasks.
- Autonomous external actions without approval.
- Multi-agent orchestration without meaningful specialization.
- Repeated revisions that only rephrase without improving measurable criteria.
- Context growth that causes the loop to forget the original task.
- Hidden failures where the agent claims success without showing validation.

## Evaluation Plan for Loop Effectiveness

When asked whether a loop works, recommend a controlled comparison:

1. Build a representative benchmark set.
2. Run a strong one-shot prompt baseline.
3. Run the looped workflow on the same tasks.
4. Track quality score, accuracy, test pass rate, citation validity, policy compliance, human correction rate, iteration count, token cost, tool calls, latency, escalation rate, and failure modes.
5. Use blind human review when possible.
6. Report whether the quality improvement is worth the added cost and latency.

## Research Basis to Mention When Needed

Use these source-backed points in explanations:

- Anthropic frames evaluator-optimizer as one LLM call generating while another evaluates and returns feedback in a loop.
- AWS describes reflect-refine loops with generator, evaluator, and optimizer/refiner agents that repeat until success, approval, or retry limits.
- LangGraph implements evaluator-optimizer as generator and evaluator nodes with conditional routing back to generation.
- OpenAI emphasizes traces, evals, guardrails, exit conditions, and human intervention for reliable agents.
- Microsoft warns that multi-agent systems add token, context, coordination, and debugging overhead, and recommends iteration caps and instrumentation.
- Self-Refine and Reflexion show how feedback and reflection can improve outputs without model weight updates.
- ReAct shows the value of action-observation loops for tool-using agents.
- Academic self-correction surveys warn that intrinsic self-correction is unreliable without external feedback.

## Final Recommendation Pattern

When advising the user, end with a practical recommendation:

- Use a loop if the task is important, iterative, and evaluable.
- Avoid a loop if one strong prompt is enough.
- Always include success criteria, a rubric, max iterations, validation, logging, and escalation.
- State clearly that loops improve process reliability but do not guarantee correctness.
