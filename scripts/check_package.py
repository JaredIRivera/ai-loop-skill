"""Check the portable skill package without network access or file writes."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HEADINGS = [
    "What you can accomplish",
    "Quick start",
    "Working examples",
    "How it works and design choices",
    "Recorded results",
    "Running checks and experiments",
    "Project status and next decisions",
    "Glossary",
]
REQUIRED_FILES = [
    "README.md", "SKILL.md", "SPEC.md", "RELEASE_NOTES.md",
    "agents/openai.yaml", "references/glossary.md",
    "references/loop-design-brief.md", "references/benchmark-protocol.md",
    "references/evidence.md", "references/source-notes.md",
    "references/preflight-2026-10-28.md", "scripts/check_package.py",
    "evals/check_loop_model.py", "evals/local-check-results.json",
]


def run_checks() -> dict:
    checks = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    record("required_files", not missing, "All required files present" if not missing else str(missing))
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    frontmatter = skill.split("---", 2)[1] if skill.startswith("---\n") else ""
    metadata_ok = all(value in frontmatter for value in (
        "name: ai-loop-skill", "description:", "license: MIT", 'version: "1.0"'
    ))
    record("skill_metadata", metadata_ok, "Required installed skill identifiers and license metadata")
    headings = re.findall(r"^## (.+)$", readme, flags=re.MULTILINE)
    record("readme_section_order", headings == EXPECTED_HEADINGS, "Compared all H2 headings against presentation reference")
    record("assistant_setup_heading", "### Use the skill in your assistant" in readme, "Installation subsection present")
    interface = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    record("interface_invocation", "$ai-loop-skill" in interface, "Interface default prompt retains skill invocation")

    broken_links = []
    checked_links = 0
    for document in sorted(ROOT.rglob("*.md")):
        text = document.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            resolved = (document.parent / relative).resolve()
            checked_links += 1
            if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                broken_links.append(f"{document.relative_to(ROOT).as_posix()}: {target}")
    record("relative_links", not broken_links, f"Checked {checked_links} local links; failures: {broken_links}")
    record("portable_skill_navigation", "[[" not in skill and "Parent branch:" not in skill, "No private wiki navigation remains in the skill")

    json_examples = re.findall(r"```json\n(.*?)\n```", skill, flags=re.DOTALL)
    try:
        example = json.loads(json_examples[0])
        expected = {
            "passed", "confidence", "scores", "failed_criteria", "evidence_checked",
            "feedback", "requires_human", "high_risk", "stop_reason",
        }
        schema_ok = (
            len(json_examples) == 1 and set(example) == expected
            and type(example["passed"]) is bool
            and type(example["requires_human"]) is bool
            and type(example["high_risk"]) is bool
            and isinstance(example["scores"], dict)
            and all(type(score) is int and 0 <= score <= 5 for score in example["scores"].values())
            and isinstance(example["failed_criteria"], list)
            and isinstance(example["evidence_checked"], list)
        )
    except (IndexError, ValueError, KeyError, TypeError):
        schema_ok = False
    record("evaluator_json_example", schema_ok, "Example parses and retains required fields and score range")

    python_blocks = re.findall(r"```python\n(.*?)\n```", skill, flags=re.DOTALL)
    try:
        parsed = ast.parse(python_blocks[0])
        syntax_ok = len(python_blocks) == 1 and any(
            isinstance(node, ast.FunctionDef) and node.name == "run_loop" for node in parsed.body
        )
    except (IndexError, SyntaxError):
        syntax_ok = False
    record("pseudocode_syntax", syntax_ok, "Illustrative function parses; application adapters are supplied only by tests")

    return {
        "suite": "package-preflight",
        "scope": "Package structure and examples; no model evaluation",
        "model_calls": 0,
        "passed": sum(check["passed"] for check in checks),
        "total": len(checks),
        "checks": checks,
    }


if __name__ == "__main__":
    report = run_checks()
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["passed"] == report["total"] else 1)
