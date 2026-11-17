"""Ask for everything missing in one turn instead of one fact per prompt.

Live red-team retests used 4 of the 5 prompts on questions asked one at
a time (each pizza's price, then each pizza's split). The pipeline also
showed only the first of the model's open questions and dropped the rest.
"""

from backend.config import SYSTEM_PROMPT
from backend.llm import FakeLlmClient
from backend.pipeline import parse_turn


ROSTER = ["Sarah", "Kayla", "Rui"]


def with_questions(*questions):
    return {
        "description": "Pizza",
        "payer": None,
        "items": [
            {
                "name": "Pizza",
                "quantity": 1,
                "unitPrice": None,
                "participants": {"mode": "all", "names": []},
            }
        ],
        "charges": [],
        "statedTotal": None,
        "openQuestions": [{"field": f"q{i}", "question": q} for i, q in enumerate(questions)],
    }


def run(raw, text="we got pizzas"):
    return parse_turn(
        llm=FakeLlmClient([raw]),
        conversation=[{"role": "user", "content": text}],
        roster=ROSTER,
        current_user="Kayla",
    )


def test_all_open_questions_are_asked_together():
    result = run(with_questions(
        "What did the first pizza cost?",
        "What did the second pizza cost?",
        "How should each pizza be split?",
    ))

    assert result == {
        "type": "question",
        "question": (
            "What did the first pizza cost? What did the second pizza cost? "
            "How should each pizza be split?"
        ),
    }


def test_single_open_question_is_unchanged():
    result = run(with_questions("What did the pizza cost?"))

    assert result == {"type": "question", "question": "What did the pizza cost?"}


def test_duplicate_and_blank_questions_are_dropped():
    result = run(with_questions(
        "What did the pizza cost?",
        "  ",
        "what did the pizza cost?",
        "Who shared it?",
    ))

    assert result["question"] == "What did the pizza cost? Who shared it?"


def test_repeated_batch_still_triggers_the_loop_guard():
    questions = ("What did the pizza cost?", "Who shared it?")
    batched = "What did the pizza cost? Who shared it?"

    result = parse_turn(
        llm=FakeLlmClient([with_questions(*questions)]),
        conversation=[
            {"role": "user", "content": "we got pizza"},
            {"role": "assistant", "content": batched},
            {"role": "user", "content": "hmm"},
        ],
        roster=ROSTER,
        current_user="Kayla",
    )

    assert result["question"] == f"I still need this before I can show a preview: {batched}"


def test_system_prompt_asks_for_missing_facts_together():
    assert "ask for all of them in one question" in SYSTEM_PROMPT
    assert "Do not ask one fact per turn" in SYSTEM_PROMPT


def test_system_prompt_keeps_weights_on_the_items_they_were_given_for():
    """Live B4 failure: nights for the house were applied to every item."""
    assert "Apply weights only to the items the user tied them to" in SYSTEM_PROMPT
    assert "don't spread them over every item yourself" in SYSTEM_PROMPT
