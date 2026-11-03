"""Issue #32: benchmark report with Run 1/2/3 and per-scenario pass rates."""

from pathlib import Path

from benchmark.report import render
from benchmark.schema import ResultsFile, Run, ScenarioResult

SNAPSHOT = Path(__file__).parent / "snapshots" / "benchmark_report.md"
SCENARIOS = [
    ("B1", "Basic"),
    ("B2", "Moderate"),
    ("B3", "Intermediate"),
    ("B4", "Advanced"),
    ("B5", "Most complex"),
]


def result(scenario_id, label, passed=True, prompts=2, reason=None,
           category=None, informational=False):
    return ScenarioResult(
        id=scenario_id,
        label=label,
        informational=informational,
        passed=passed,
        promptCount=prompts,
        failureReason=None if passed else reason,
        failureCategory=None if passed else category,
        behaviorExpected="asked",
        behaviorObserved="asked",
        behaviorOk=True,
    )


def run(number, failures=None):
    failures = failures or {}
    return Run(run=number, official=number == 1, results=[
        result(sid, label, *failures[sid]) if sid in failures
        else result(sid, label)
        for sid, label in SCENARIOS
    ])


def results_file(*runs):
    return ResultsFile(
        model="claude-sonnet-5-5",
        promptVersion="test-1",
        commitSha="abc1234",
        timestamp="2026-11-03T12:00:00+00:00",
        provider="claude",
        runs=list(runs),
    )


KAYLA_OFF = (False, 2, "Kayla's share off by $0.01", "tax/tip")


def test_five_of_five_passes():
    markdown = render(results_file(run(1)))

    assert "| Run 1 (official) | 5/5 (100%) | PASS |" in markdown
    assert "**PASS** against the 90% target" in markdown


def test_four_of_five_is_eighty_percent_and_fails():
    markdown = render(results_file(run(1, {"B3": KAYLA_OFF})))

    assert "| Run 1 (official) | 4/5 (80%) | FAIL |" in markdown
    assert "**FAIL** against the 90% target" in markdown
    assert "❌ 2 prompts, Kayla's share off by $0.01" in markdown


def test_scenario_passing_two_of_three_runs_is_flaky():
    markdown = render(results_file(
        run(1), run(2, {"B3": KAYLA_OFF}), run(3),
    ))

    assert "| B3 Intermediate ⚠ |" in markdown
    assert "| B1 Basic |" in markdown  # stable rows have no marker


def test_missing_run_column_is_handled():
    markdown = render(results_file(run(1), run(2)))

    assert "| Run 1 (official) | Run 2 | Run 3 |" in markdown.replace(" | Behavior (Run 1)", "")
    assert "| Run 3 | not run | — |" in markdown
    assert "| B1 Basic | ✅ 2 prompts | ✅ 2 prompts | — |" in markdown


def test_failure_categories_group():
    markdown = render(results_file(
        run(1, {"B3": KAYLA_OFF, "B5": (False, 5, "prompt limit", "prompt limit")}),
        run(2, {"B3": KAYLA_OFF}),
    ))

    assert "| tax/tip | 2 |" in markdown
    assert "| prompt limit | 1 |" in markdown


def test_shows_model_prompt_version_and_commit():
    markdown = render(results_file(run(1)))

    assert "`claude-sonnet-5-5`" in markdown
    assert "`test-1`" in markdown
    assert "`abc1234`" in markdown
    assert "Run 1 is the **official** run" in markdown


def test_threshold_note_explains_single_run_math():
    markdown = render(results_file(run(1)))

    assert "passes 90% only at 5/5 (4/5 is 80%)" in markdown
    assert "≥ 14/15" in markdown


def test_informational_cases_excluded_from_pass_rate():
    first = run(1)
    first.results.append(result("MESSY-1", "x", passed=False, reason="r",
                                category="participants", informational=True))

    markdown = render(results_file(first))

    assert "| Run 1 (official) | 5/5 (100%) | PASS |" in markdown
    assert "## Informational cases (not counted)" in markdown


def test_markdown_snapshot():
    markdown = render(results_file(
        run(1, {"B3": KAYLA_OFF}),
        run(2),
        run(3, {"B5": (False, 5, "prompt limit: no final preview within 5 prompts", "prompt limit")}),
    ))

    assert markdown == SNAPSHOT.read_text(encoding="utf-8")
