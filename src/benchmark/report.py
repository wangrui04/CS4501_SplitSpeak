"""Markdown report: one row per scenario, one column per run."""

from __future__ import annotations

from collections import Counter

from benchmark.schema import FAILURE_CATEGORIES, ResultsFile

THRESHOLD = 0.90
RUN_COLUMNS = 3


def _cell(result) -> str:
    if result is None:
        return "—"
    prompts = f"{result.promptCount} prompt{'s' if result.promptCount != 1 else ''}"
    if result.passed:
        return f"✅ {prompts}"
    return f"❌ {prompts}, {result.failureReason}"


def _rate(results) -> tuple[int, int]:
    return sum(r.passed for r in results), len(results)


def _pct(passed: int, total: int) -> str:
    return f"{passed}/{total} ({passed / total:.0%})" if total else "n/a"


def render(results: ResultsFile) -> str:
    runs = {run.run: run for run in results.runs}
    columns = max(RUN_COLUMNS, max(runs, default=0))

    scenario_order = []
    for run in results.runs:
        for result in run.results:
            if result.id not in [s[0] for s in scenario_order]:
                scenario_order.append((result.id, result.label, result.informational))

    def lookup(run_number, scenario_id):
        run = runs.get(run_number)
        if run is None:
            return None
        return next((r for r in run.results if r.id == scenario_id), None)

    lines = [
        "# Benchmark Report",
        "",
        f"- Model: `{results.model}`",
        f"- Provider: `{results.provider}`",
        f"- Prompt version: `{results.promptVersion}`",
        f"- Commit: `{results.commitSha}`",
        f"- Run at: {results.timestamp}",
        "",
        "Run 1 is the **official** run. ⚠ marks a scenario whose result differs across runs.",
        "",
        "| Scenario | " + " | ".join(
            f"Run {n}{' (official)' if n == 1 else ''}" for n in range(1, columns + 1)
        ) + " | Behavior (Run 1) |",
        "| --- | " + " | ".join("---" for _ in range(columns)) + " | --- |",
    ]

    for scenario_id, label, informational in scenario_order:
        if informational:
            continue
        cells = [lookup(n, scenario_id) for n in range(1, columns + 1)]
        outcomes = {c.passed for c in cells if c is not None}
        flaky = " ⚠" if len(outcomes) > 1 else ""
        first = cells[0]
        behavior = "—"
        if first is not None:
            mark = "✅" if first.behaviorOk else "⚠"
            behavior = f"{mark} expected {first.behaviorExpected}, {first.behaviorObserved}"
        lines.append(
            f"| {scenario_id} {label}{flaky} | "
            + " | ".join(_cell(c) for c in cells)
            + f" | {behavior} |"
        )

    lines += ["", "## Pass rates", "", "| Run | Passed | Result |", "| --- | --- | --- |"]
    overall_passed = overall_total = 0
    official_rate = None
    for n in range(1, columns + 1):
        run = runs.get(n)
        if run is None:
            lines.append(f"| Run {n} | not run | — |")
            continue
        passed, total = _rate([r for r in run.results if not r.informational])
        overall_passed += passed
        overall_total += total
        ok = total and passed / total >= THRESHOLD
        if n == 1:
            official_rate = (passed, total, ok)
        lines.append(f"| Run {n}{' (official)' if n == 1 else ''} | {_pct(passed, total)} | {'PASS' if ok else 'FAIL'} |")
    lines.append(f"| Overall | {_pct(overall_passed, overall_total)} | — |")

    lines += ["", "## Threshold", ""]
    if official_rate:
        passed, total, ok = official_rate
        lines.append(
            f"**{'PASS' if ok else 'FAIL'}** against the 90% target: Run 1 passed {_pct(passed, total)}."
        )
    lines += [
        "",
        "With 5 scenarios, a single automated run passes 90% only at 5/5 (4/5 is 80%). "
        "This report is supporting evidence. The official result is the 15-attempt human "
        "session in `docs/alpha-results.md` (3 testers × 5 scenarios, ≥ 14/15 to pass).",
    ]

    failures = Counter(
        r.failureCategory
        for run in results.runs
        for r in run.results
        if not r.passed and not r.informational
    )
    lines += ["", "## Failures by category", ""]
    if not failures:
        lines.append("No failures.")
    else:
        lines += ["| Category | Failures |", "| --- | ---: |"]
        for category in FAILURE_CATEGORIES:
            if failures.get(category):
                lines.append(f"| {category} | {failures[category]} |")

    informational = [
        (run.run, r) for run in results.runs for r in run.results if r.informational
    ]
    if informational:
        lines += [
            "",
            "## Informational cases (not counted)",
            "",
            "| Run | Case | Result |",
            "| --- | --- | --- |",
        ]
        for number, result in informational:
            lines.append(f"| {number} | {result.id} {result.label} | {_cell(result)} |")

    return "\n".join(lines) + "\n"
