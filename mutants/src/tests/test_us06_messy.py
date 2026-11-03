"""Issue #25: US-06 messy language and typo handling.

The live-LLM versions of these cases are informational benchmark
scenarios (src/benchmark/scenarios/legacy/us-06.json and
informational/messy-*.json). Here the LLM is the scripted fixture
client, so these tests check the pipeline's side of the contract: it
honors questions, never previews a guessed value, and computes the
right split once the details are in.
"""

import pytest

from backend.llm import FixtureLlmClient
from benchmark.runner import run_scenario
from benchmark.schema import SCENARIO_DIR, load_scenarios


US06 = next(s for s in load_scenarios("legacy") if s.id == "US-06")
MESSY = [s for s in load_scenarios("informational") if s.id.startswith("MESSY")]
QUESTION_CASES = [
    s for s in load_scenarios("legacy", "informational")
    if s.behavior.mustEndWithQuestion
]


def test_us06_scenario_file_exists():
    assert (SCENARIO_DIR / "legacy" / "us-06.json").exists()
    assert US06.turns[0].text == (
        "I paid for dinr. Me and Kayla shared nachoes for $16. "
        "Riu got 2 drnks for $5 each. Split the rest evenly."
    )


def test_us06_two_turns_asks_about_the_rest_then_splits():
    result = run_scenario(US06, FixtureLlmClient())

    first = result.transcript[0]
    assert first["type"] == "question"
    assert "the rest" in first["assistant"]

    assert result.passed, result.failureReason
    assert result.promptCount == 2


def test_us06_final_split_matches_key():
    assert US06.expected.shares == {"Sarah": 800, "Kayla": 800, "Rui": 1000}
    assert sum(US06.expected.shares.values()) == 2600
    assert US06.expected.paid == {"Sarah": 2600, "Kayla": 0, "Rui": 0}


def test_five_to_eight_messy_informational_cases():
    assert 5 <= len(MESSY) <= 8
    assert all(s.informational for s in MESSY)
    texts = " ".join(t.text for s in MESSY for t in s.turns)
    assert "kayla n i split pizza 24" in texts
    assert "rui had double" in texts


@pytest.mark.parametrize("scenario", MESSY, ids=lambda s: s.id)
def test_messy_cases_with_fixture_extraction(scenario):
    result = run_scenario(scenario, FixtureLlmClient())

    assert result.passed, result.failureReason


@pytest.mark.parametrize("scenario", QUESTION_CASES, ids=lambda s: s.id)
def test_no_preview_from_a_guessed_value(scenario):
    result = run_scenario(scenario, FixtureLlmClient())

    assert [entry["type"] for entry in result.transcript] == ["question"]
    assert result.passed
