"""Structural validator for the Track 1 Day 23 submission.

This script checks presence and traceability structure. It does not claim to
automatically prove semantic product correctness.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    path = ROOT / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def check(condition: bool, label: str, failures: list[str]) -> None:
    if not condition:
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    required_files = [
        "README.md",
        "metrics-pack.md",
        "ai-support-log.md",
        "gate-audit.md",
        "submission-checklist.md",
        "mentor-defense.md",
        "scripts/validate_submission.py",
    ]
    for name in required_files:
        check((ROOT / name).is_file(), f"missing file: {name}", failures)

    readme = read("README.md")
    pack = read("metrics-pack.md")
    ai_log = read("ai-support-log.md")

    required_sections = [
        "## 00 — Dự án, persona, core job",
        "## 01 — Core Action Card",
        "## 02 — Action Nature Card + kết luận cadence",
        "## 03 — Metric System",
        "## 04 — Retention Definition",
        "## 05 — Product Loop",
        "## 06 — Tracking nhanh",
        "## 07 — Revision",
    ]
    for section in required_sections:
        check(section in pack, f"missing required section: {section}", failures)

    for criterion in [
        "Near core value",
        "Repeatable",
        "Observable",
        "Meaningful",
        "Influenceable",
    ]:
        check(criterion in pack, f"missing self-check criterion: {criterion}", failures)

    for item in ["Unit", "Cohort entry", "Return event", "Window", "Threshold", "Segment"]:
        check(item in pack, f"retention component absent: {item}", failures)

    for item in ["Start event", "Activation event", "Time window"]:
        check(item in pack, f"activation component absent: {item}", failures)

    for item in [
        "North Star Metric (NSM)",
        "Leading indicators",
        "Counter-metrics",
        "Product Loop",
        "Metric Hypothesis",
        "Acceptance criteria",
        "Metric ↔ event traceability matrix",
    ]:
        check(item in pack, f"missing metric/tracking section: {item}", failures)

    contract_section = pack.split("### Acceptance criteria", 1)[0]
    unique_events = set(
        re.findall(
            r"^\|\s+\x60(fraud_case_[a-z_]+|fraud_evidence_[a-z_]+)\x60\s+\|",
            contract_section,
            flags=re.MULTILINE,
        )
    )
    check(
        4 <= len(unique_events) <= 8,
        f"tracking event count is {len(unique_events)}, expected 4–8",
        failures,
    )
    for event in [
        "fraud_case_assigned",
        "fraud_case_review_started",
        "fraud_evidence_completed",
        "fraud_case_resolved",
        "fraud_case_reopened",
        "fraud_case_reversed",
    ]:
        check(event in unique_events, f"missing core event: {event}", failures)

    acceptance_count = len(re.findall(r"\*\*AC\d+\s+—", pack))
    check(acceptance_count >= 2, f"acceptance criteria count is {acceptance_count}", failures)
    check(
        "Computable?" in pack and "YES" in pack,
        "traceability matrix is absent or has no YES evidence",
        failures,
    )
    check(
        "Student decision: METRIC HYPOTHESIS = A" in pack,
        "metric hypothesis is not student-confirmed",
        failures,
    )
    check(
        "Student decision: CADENCE = A" in pack,
        "cadence is not student-confirmed",
        failures,
    )
    check(
        "Student decision: CORE ACTION = A" in pack,
        "core action is not student-confirmed",
        failures,
    )

    for prompt in [
        "## AI đã giúp tôi ở đâu?",
        "## AI sai, hời hợt hoặc đề xuất metric sai nature ở đâu?",
        "## Tôi đã tự sửa hoặc quyết định lại điều gì?",
    ]:
        check(prompt in ai_log, f"AI Support Log prompt absent: {prompt}", failures)
    check(
        "student" in ai_log.lower() and "AI" in ai_log,
        "AI Support Log lacks authorship/compliance evidence",
        failures,
    )
    check("metrics-pack.md" in readme, "README lacks Metrics Pack link", failures)

    submission_text = "\n".join(read(name) for name in required_files if name != "scripts/validate_submission.py")
    forbidden_unresolved = [
        "TODO",
        "TBD",
        "FIXME",
        "[fill here]",
        "STUDENT CONFIRMATION REQUIRED",
    ]
    for token in forbidden_unresolved:
        check(token not in submission_text, f"unresolved token found: {token}", failures)

    if failures:
        print("STRUCTURAL VALIDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("STRUCTURAL VALIDATION: PASS")
    print(f"Files checked: {len(required_files)}")
    print(f"Unique tracking events: {len(unique_events)}")
    print(f"Acceptance criteria: {acceptance_count}")
    print("Note: semantic correctness remains a human audit responsibility.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
