"""Issue #31: benchmark runner for the five benchmark scenarios."""

import json
import re
from pathlib import Path

import pytest

from backend.llm import FIXTURES_PATH, FakeLlmClient
from backend.settlement import compute_settlement
from benchmark.benchmark import BenchmarkRefused, run_benchmark, write_results
from benchmark.comparator import compare, describe
from benchmark.runner import run_scenario
from benchmark.schema import Expected, ResultsFile, Scenario, load_scenarios


DOCS = Path(__file__).resolve().parents[2] / "docs" / "benchmarks.md"
FIXTURES = json.loads(FIXTURES_PATH.read_text())["responses"]
OFFICIAL = {s.id: s for s in load_scenarios("official")}


def turn_fixture(scenario_id, turn):
    return FIXTURES[OFFICIAL[scenario_id].turns[turn].text]


def b4_expected():
    return OFFICIAL["B4"].expected


def preview_for(expected: Expected):
    return {
        "shares": [{"name": n, "cents": c} for n, c in expected.shares.items()],
        "paid": [{"name": n, "cents": c} for n, c in expected.paid.items()],
        "settlement": {"transfers": [
            {"from": t.from_, "to": t.to, "cents": t.cents}
            for t in expected.settlement
        ]},
    }


# Comparator

def test_exact_match_passes():
    assert compare(b4_expected(), preview_for(b4_expected()), 2) == []


def test_one_cent_off_share_names_the_field():
    preview = preview_for(b4_expected())
    preview["shares"][1]["cents"] += 1

    mismatches = compare(b4_expected(), preview, 2)

    assert [m.field for m in mismatches] == ["shares.Kayla"]
    assert "share off by $0.01" in describe(mismatches)


def test_wrong_settlement_direction_fails():
    preview = preview_for(b4_expected())
    preview["settlement"]["transfers"][0] = {
        "from": "Sarah", "to": "Rui", "cents": 28000,
    }

    assert [m.field for m in compare(b4_expected(), preview, 2)] == ["settlement"]


def test_wrong_amount_paid_fails():
    preview = preview_for(b4_expected())
    preview["paid"] = [{"name": "Sarah", "cents": 105000}]

    fields = {m.field for m in compare(b4_expected(), preview, 2)}

    assert {"paid.Sarah", "paid.Rui", "paid.Kayla"} <= fields


def test_correct_result_but_six_prompts_fails():
    mismatches = compare(b4_expected(), preview_for(b4_expected()), 6)

    assert [m.field for m in mismatches] == ["promptCount"]


# Runner flow (scripted fake LLM, no API calls)

def test_b1_preview_after_turn_one_is_done_in_one_prompt():
    llm = FakeLlmClient([turn_fixture("B1", 0)])

    result = run_scenario(OFFICIAL["B1"], llm)

    assert result.passed
    assert result.promptCount == 1
    assert len(llm.calls) == 1


def test_if_asked_turn_not_sent_after_a_preview():
    # If the bot previews B4 right away, turn 2 (if_asked) is skipped.
    # B4's first message states every payer and price, so the final
    # extraction passes the grounding checks (#49) on turn 1. (B2's
    # turn 1 never says who paid, so it now correctly asks first.)
    llm = FakeLlmClient([turn_fixture("B4", 1)])

    result = run_scenario(OFFICIAL["B4"], llm)

    assert len(llm.calls) == 1
    assert result.promptCount == 1
    assert result.behaviorOk is False  # B4 should have asked first


def test_b5_always_correction_sent_after_preview():
    llm = FakeLlmClient([
        turn_fixture("B5", 0),  # preview
        turn_fixture("B5", 1),  # question about the refund
        turn_fixture("B5", 2),  # corrected preview
    ])

    result = run_scenario(OFFICIAL["B5"], llm)

    assert [entry["type"] for entry in result.transcript] == [
        "preview", "question", "preview",
    ]
    assert result.promptCount == 3
    assert result.passed, result.failureReason
    assert result.behaviorOk


def test_question_with_no_turns_left_runs_out_of_script():
    question = turn_fixture("B1", 0) | {
        "openQuestions": [{"field": "payer", "question": "Who paid?"}],
    }
    result = run_scenario(OFFICIAL["B1"], FakeLlmClient([question]))

    assert not result.passed
    assert result.failureReason == "ran out of script"


def test_unresolved_response_fails_the_run():
    result = run_scenario(OFFICIAL["B1"], FakeLlmClient([]))

    assert not result.passed
    assert result.failureReason.startswith("unresolved")


def test_wrong_split_reports_mismatch():
    wrong = json.loads(json.dumps(turn_fixture("B1", 0)))
    # A misread the grounding checks (#49) can't catch: 96 was typed, but
    # the model read two dinners instead of one.
    wrong["items"][0]["quantity"] = 2
    wrong["statedTotal"] = None

    result = run_scenario(OFFICIAL["B1"], FakeLlmClient([wrong]))

    assert not result.passed
    assert "share off by" in result.failureReason
    assert result.failureCategory == "multiple payers"  # paid is also off


def test_fixture_extraction_reproduces_every_answer_key():
    results = run_benchmark(
        runs=1, provider="fake", include_informational=True,
        env={}, progress=lambda _: None,
    )

    failures = [
        (r.id, r.failureReason)
        for r in results.runs[0].results
        if not r.passed
    ]
    assert failures == []


def test_results_file_validates_against_schema(tmp_path):
    results = run_benchmark(runs=2, provider="fake", env={}, progress=lambda _: None)

    path = write_results(results, tmp_path)
    loaded = ResultsFile.model_validate_json(path.read_text())

    assert [run.official for run in loaded.runs] == [True, False]
    assert {r.id for r in loaded.runs[0].results} == set(OFFICIAL)
    assert loaded.promptVersion and loaded.commitSha and loaded.timestamp


def test_informational_cases_excluded_by_default():
    results = run_benchmark(runs=1, provider="fake", env={}, progress=lambda _: None)

    assert not any(r.informational for r in results.runs[0].results)


def test_refuses_live_run_in_ci():
    with pytest.raises(BenchmarkRefused, match="CI"):
        run_benchmark(provider="claude", env={"CI": "true", "ANTHROPIC_API_KEY": "x"})


def test_refuses_live_run_without_key():
    with pytest.raises(BenchmarkRefused, match="ANTHROPIC_API_KEY"):
        run_benchmark(provider="claude", env={})


# Scenario files

def test_five_official_scenarios_labeled_by_difficulty():
    assert [(s.id, s.label) for s in OFFICIAL.values()] == [
        ("B1", "Basic"),
        ("B2", "Moderate"),
        ("B3", "Intermediate"),
        ("B4", "Advanced"),
        ("B5", "Most complex"),
    ]
    assert all(s.signedInAs == "Sarah" and not s.informational for s in OFFICIAL.values())


def test_legacy_and_informational_scenarios_are_informational():
    for scenario in load_scenarios("legacy", "informational"):
        assert scenario.informational, scenario.id


@pytest.mark.parametrize("scenario_id", sorted(OFFICIAL))
def test_answer_key_sanity(scenario_id):
    """Catch typos in the hand-typed answer keys."""
    expected = OFFICIAL[scenario_id].expected

    assert sum(expected.shares.values()) == sum(expected.paid.values())

    settlement = compute_settlement(
        [{
            "payments": [{"name": n, "cents": c} for n, c in expected.paid.items()],
            "shares": [{"name": n, "cents": c} for n, c in expected.shares.items()],
        }],
        ["Sarah", "Kayla", "Rui"],
    )
    assert sorted((t["from"], t["to"], t["cents"]) for t in settlement["transfers"]) == sorted(
        t.key() for t in expected.settlement
    )


def docs_prompts():
    text = DOCS.read_text()
    sections = re.split(r"^## (B\d) ", text, flags=re.M)[1:]
    return {
        scenario_id: re.findall(
            r"Turn \d \(`(always|if_asked)`[^)]*\):\n\n```text\n(.*?)\n```",
            body, flags=re.S,
        )
        for scenario_id, body in zip(sections[0::2], sections[1::2])
    }


def test_scenario_prompts_match_docs_verbatim():
    documented = docs_prompts()

    assert set(documented) == set(OFFICIAL)
    for scenario_id, scenario in OFFICIAL.items():
        assert [(t.send, t.text) for t in scenario.turns] == documented[scenario_id]


def test_system_prompt_does_not_leak_benchmark_amounts():
    """The prompt's examples must not contain the benchmark's own numbers."""
    from backend.config import SYSTEM_PROMPT

    prompt_numbers = set(re.findall(r"\d+(?:\.\d+)?", SYSTEM_PROMPT))
    for scenario in OFFICIAL.values():
        for turn in scenario.turns:
            for number in re.findall(r"\d+(?:\.\d+)?", turn.text):
                if len(number.replace(".", "")) >= 2:
                    assert number not in prompt_numbers, (scenario.id, number)


    # Distinctive phrasing and weights from the official scenarios.
    lowered = SYSTEM_PROMPT.lower()
    for term in ["marg", "fairly", "twice as much", "[3, 3, 1]", "[3, 3, 2]", "[1, 2]"]:
        assert term not in lowered, term


def test_system_prompt_asks_to_confirm_a_full_plan():
    from backend.config import SYSTEM_PROMPT

    assert "restate the complete interpretation" in SYSTEM_PROMPT
    assert 'do not ask an open "either/or"' in SYSTEM_PROMPT


def test_system_prompt_requires_a_stated_payer():
    from backend.config import SYSTEM_PROMPT

    assert "Only set payer" in SYSTEM_PROMPT
    assert "only identifies who they are, not who paid" in SYSTEM_PROMPT
    assert "leave payer null" in SYSTEM_PROMPT


def test_scenario_requires_expected_or_question():
    with pytest.raises(ValueError):
        Scenario.model_validate({
            "id": "X", "label": "x",
            "turns": [{"text": "hi", "send": "always"}],
        })
