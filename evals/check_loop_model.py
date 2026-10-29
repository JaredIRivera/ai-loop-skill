"""Exercise SKILL.md's illustrative loop with synthetic in-process adapters.

This tests the bundled control flow, not a model or production integration.
The only executed text is the inspected Python example in this repository.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def exercise(evaluations: list[dict], limit: int) -> tuple[object, dict]:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)\n```", text, flags=re.DOTALL)
    if len(blocks) != 1:
        raise ValueError("Expected one documented loop example")
    state = {"calls": 0, "feedback": [], "escalations": 0}

    def generator(goal, context, feedback):
        state["calls"] += 1
        state["feedback"].append(feedback)
        return f"draft-{state['calls']}"

    def evaluator(draft, rubric, validation_tools):
        defaults = dict(
            passed=False, requires_human=False, high_risk=False,
            no_progress=False, feedback="Fix the missing criterion", score=0,
        )
        defaults.update(evaluations[min(state["calls"] - 1, len(evaluations) - 1)])
        return SimpleNamespace(**defaults)

    def choose_best(best, draft, evaluation):
        if best is None or evaluation.score > best["score"]:
            return {"draft": draft, "score": evaluation.score}
        return best

    def escalate_to_human(draft, evaluation):
        state["escalations"] += 1
        return {"status": "escalated", "draft": draft}

    namespace = {
        "generator": generator,
        "evaluator": evaluator,
        "choose_best": choose_best,
        "no_meaningful_progress": lambda evaluation: evaluation.no_progress,
        "escalate_to_human": escalate_to_human,
        "best_attempt_with_caveats": lambda best, evaluation: {"status": "incomplete", "best": best},
    }
    exec(compile(blocks[0], "SKILL.md:Core Loop Model", "exec"), namespace)
    result = namespace["run_loop"]("synthetic goal", {}, {}, [], limit)
    return result, state


def run_checks() -> dict:
    checks = []

    def case(name, operation):
        try:
            operation()
            checks.append({"name": name, "passed": True})
        except Exception as exc:
            checks.append({"name": name, "passed": False, "error": f"{type(exc).__name__}: {exc}"})

    def first_pass():
        result, state = exercise([{"passed": True}], 3)
        assert result == "draft-1" and state["calls"] == 1

    def revision_pass():
        result, state = exercise([{"feedback": "Use the approved window"}, {"passed": True}], 3)
        assert result == "draft-2" and state["calls"] == 2
        assert state["feedback"] == [None, "Use the approved window"]

    def iteration_cap():
        result, state = exercise([{"score": 4}, {"score": 2}], 3)
        assert state["calls"] == 3
        assert result == {"status": "incomplete", "best": {"draft": "draft-1", "score": 4}}

    def no_progress():
        result, state = exercise([{"no_progress": True}], 3)
        assert result["status"] == "incomplete" and state["calls"] == 1

    def human_escalation():
        result, state = exercise([{"requires_human": True}], 3)
        assert result["status"] == "escalated"
        assert state["calls"] == 1 and state["escalations"] == 1

    def risk_overrides_success():
        result, state = exercise([{"passed": True, "high_risk": True}], 3)
        assert result["status"] == "escalated"
        assert state["calls"] == 1 and state["escalations"] == 1

    def invalid_limit(value):
        try:
            exercise([{}], value)
        except ValueError as exc:
            assert str(exc) == "max_iterations must be a positive integer"
            return
        raise AssertionError("Invalid limit was accepted")

    case("success_stops_after_first_cycle", first_pass)
    case("revision_receives_feedback_and_stops_on_success", revision_pass)
    case("iteration_cap_preserves_best_attempt", iteration_cap)
    case("no_progress_stops_early", no_progress)
    case("human_escalation_is_terminal", human_escalation)
    case("risk_overrides_passing_quality_score", risk_overrides_success)
    case("zero_iteration_limit_rejected", lambda: invalid_limit(0))
    case("negative_iteration_limit_rejected", lambda: invalid_limit(-1))
    case("boolean_iteration_limit_rejected", lambda: invalid_limit(True))

    return {
        "suite": "synthetic-loop-control-flow",
        "scope": "Documented example with synthetic adapters; no model judgments",
        "model_calls": 0,
        "passed": sum(check["passed"] for check in checks),
        "total": len(checks),
        "checks": checks,
    }


if __name__ == "__main__":
    report = run_checks()
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["passed"] == report["total"] else 1)
