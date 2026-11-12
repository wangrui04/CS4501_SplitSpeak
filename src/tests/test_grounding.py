"""Issue #49: check the LLM's payer, prices, and charges against the user's text.

The LLM can misread a message ("everyone pays for their own food" as
three payers) or invent an amount. These checks use only what the user
typed, so a wrong reading becomes a question instead of a preview.
"""

import logging
import re
from pathlib import Path

import pytest

from backend import config
from backend.grounding import (
    amount_question,
    charge_question,
    ground_payers,
    user_texts,
)
from backend.llm import FakeLlmClient
from backend.pipeline import parse_turn


ROSTER = ["Sam", "Lee", "Jordan"]
SCENARIOS = Path(__file__).resolve().parents[1] / "benchmark" / "scenarios" / "official"


def item(name, price, names=(), mode="only", quantity=1, **extra):
    return {
        "name": name,
        "quantity": quantity,
        "unitPrice": price,
        "participants": {"mode": mode, "names": list(names)},
        **extra,
    }


def charge(kind, amount=None, percent=None, method="proportional"):
    return {"kind": kind, "amount": amount, "percent": percent, "method": method}


def parsed(items, payer=None, charges=()):
    return {
        "description": "Dinner",
        "payer": payer,
        "items": items,
        "charges": list(charges),
        "statedTotal": None,
        "openQuestions": [],
    }


def user(*texts):
    return [{"role": "user", "content": text} for text in texts]


# ---------------------------------------------------------------- user_texts


def test_user_texts_ignores_assistant_messages():
    conversation = [
        {"role": "user", "content": "lunch 20"},
        {"role": "assistant", "content": "Who paid? Sam paid $99?"},
        {"role": "user", "content": "i paid"},
    ]

    assert user_texts(conversation) == ["lunch 20", "i paid"]


# -------------------------------------------------------------------- payer


@pytest.mark.parametrize(
    "text",
    [
        "i paid for lunch",
        "I covered it",
        "im the one who paid",
        "paid by me",
        "i got the bill",
        "I picked up the check",
    ],
)
def test_signed_in_user_payer_is_grounded_by_first_person(text):
    data, fired = ground_payers(parsed([], payer="ME"), [text], "Sam")

    assert data["payer"] == "ME"
    assert fired == []


def test_signed_in_user_by_name_counts_as_me():
    data, _ = ground_payers(parsed([], payer="Sam"), ["i paid"], "Sam")

    assert data["payer"] == "Sam"


@pytest.mark.parametrize(
    "text",
    [
        "Lee paid for lunch",
        "lee covered everything",
        "it was paid by Lee",
        "Lee picked up the tab",
        "lee bought the groceries",
    ],
)
def test_named_payer_is_grounded(text):
    data, fired = ground_payers(parsed([], payer="Lee"), [text], "Sam")

    assert data["payer"] == "Lee"
    assert fired == []


@pytest.mark.parametrize(
    "text",
    [
        "lunch with Lee was 20",
        "Lee got a burger. i paid",
        "everyone pays for their own food, Lee too",
        "im Lee",
    ],
)
def test_payer_not_tied_to_a_payment_word_is_cleared(text):
    data, fired = ground_payers(parsed([], payer="Lee"), [text], "Sam")

    assert data["payer"] is None
    assert fired == ["payer"]


def test_ungrounded_me_is_cleared():
    data, fired = ground_payers(parsed([], payer="ME"), ["Lee and I had lunch"], "Sam")

    assert data["payer"] is None
    assert fired == ["payer"]


def test_per_item_payers_are_checked_one_by_one():
    items = [
        item("Burger", "20", ["ME"], paidBy="ME"),
        item("Salad", "25", ["Lee"], paidBy="Lee"),
        item("Pasta", "30", ["Jordan"], paidBy="Jordan"),
    ]
    text = "i paid 20 for my burger and Lee paid 25 for a salad. jordan had pasta 30"

    data, fired = ground_payers(parsed(items), [text], "Sam")

    assert [it["paidBy"] for it in data["items"]] == ["ME", "Lee", None]
    assert fired == ["item_payer"]


def test_ground_payers_does_not_mutate_or_change_amounts():
    original = parsed([item("Burger", "20", ["Lee"], paidBy="Lee")], payer="Lee")

    data, _ = ground_payers(original, ["burger 20"], "Sam")

    assert original["payer"] == "Lee"
    assert original["items"][0]["paidBy"] == "Lee"
    assert data["items"][0]["unitPrice"] == "20"


# ------------------------------------------------------------------ amounts


@pytest.mark.parametrize(
    ("text", "price"),
    [
        ("lunch was 6", "6"),
        ("lunch was $6", "6.00"),
        ("lunch was 6.00", "6"),
        ("lunch was $14.40", "14.4"),
        ("lunch was 1,200", "1200"),
    ],
)
def test_item_price_in_any_number_format_is_grounded(text, price):
    assert amount_question(parsed([item("Lunch", price, mode="all")]), [text]) is None


def test_quantity_times_unit_price_is_grounded():
    data = parsed([item("Drinks", "10", mode="all", quantity=2)])

    assert amount_question(data, ["two drinks for 20"]) is None


def test_invented_item_price_asks():
    data = parsed([item("Lunch", "45", mode="all")])

    assert amount_question(data, ["lunch was 40"]) == "How much was Lunch?"


def test_invented_tax_amount_asks():
    data = parsed([item("Lunch", "40", mode="all")], charges=[charge("tax", amount="3.20")])

    assert amount_question(data, ["lunch was 40, plus tax"]) == "How much was the tax?"


def test_percent_tip_is_grounded_by_percent_sign_or_word():
    data = parsed([item("Lunch", "40", mode="all")], charges=[charge("tip", percent="18")])

    assert amount_question(data, ["lunch 40. tip was 18%"]) is None
    assert amount_question(data, ["lunch 40. tip was 18 percent"]) is None


def test_percent_tip_needs_the_user_to_say_percent():
    data = parsed([item("Lunch", "40", mode="all")], charges=[charge("tip", percent="18")])

    assert amount_question(data, ["lunch 40. tip was 18"]) == "How much was the tip?"


def test_dollar_charge_is_not_grounded_by_a_percent():
    data = parsed([item("Lunch", "40", mode="all")], charges=[charge("tip", amount="18")])

    assert amount_question(data, ["lunch 40. tip was 18%"]) == "How much was the tip?"


def test_refund_amount_must_be_typed():
    refund = {"amount": "30", "recipient": "ME"}
    data = parsed([item("Hotel", "300", mode="all", refund=refund)])

    assert amount_question(data, ["hotel 300, got some money back"]) == (
        "How much was the refund on Hotel?"
    )
    assert amount_question(data, ["hotel 300, got 30 back"]) is None


# ------------------------------------------------------------------ charges


def test_tax_and_tip_mentioned_but_missing_asks():
    data = parsed([item("Lunch", "40", mode="all")])

    assert charge_question(data, ["lunch was 40 and we left a tip and paid tax"]) == (
        "How much were the tax and tip, and should they be split equally or "
        "proportionally? If they were already included, say so."
    )


def test_only_the_missing_charge_is_asked_about():
    data = parsed([item("Lunch", "40", mode="all")], charges=[charge("tax", amount="4")])

    assert charge_question(data, ["lunch 40, tax 4, and a tip"]) == (
        "How much was the tip, and should it be split equally or "
        "proportionally? If it was already included, say so."
    )


@pytest.mark.parametrize(
    "text",
    [
        "lunch was 40 including tax and tip",
        "the total already includes tax and tip",
        "lunch was 40, tax and tip included",
        "40 with tax and tip",
        "no tax and no tip",
        "lunch was 40, no tip",
        "40 after tax and tip",
        "lunch 40 with no extra tax or tip",
    ],
)
def test_included_or_none_phrasing_needs_no_charges(text):
    data = parsed([item("Lunch", "40", mode="all")])

    assert charge_question(data, [text]) is None


def test_no_mention_needs_no_charges():
    assert charge_question(parsed([item("Lunch", "40", mode="all")]), ["lunch 40"]) is None


# ----------------------------------------------------------------- pipeline


def run(raw, *texts, current_user="Sam"):
    return parse_turn(
        llm=FakeLlmClient([raw]),
        conversation=user(*texts),
        roster=ROSTER,
        current_user=current_user,
    )


def own_meals(paid_by_each):
    return [
        item("My meal", "20", ["ME"], paidBy="ME" if paid_by_each else None),
        item("Lee's meal", "25", ["Lee"], paidBy="Lee" if paid_by_each else None),
        item("Jordan's meal", "30", ["Jordan"], paidBy="Jordan" if paid_by_each else None),
    ]


OWN_FOOD = (
    "Dinner was me, Lee, and Jordan; my meal was 20, Lee's 25, Jordan's 30, "
    "everyone pays for their own food"
)


def test_misread_per_meal_payers_ask_who_paid():
    result = run(parsed(own_meals(paid_by_each=True)), OWN_FOOD)

    assert result == {"type": "question", "question": "Who paid for this expense?"}


def test_follow_up_i_paid_allows_the_preview():
    result = run(parsed(own_meals(paid_by_each=False), payer="ME"), OWN_FOOD, "I paid")

    assert result["type"] == "preview", result.get("question")
    assert result["preview"]["payer"] == "Sam"


def test_hallucinated_payer_asks_who_paid():
    raw = parsed([item("Lunch", "40", mode="all")], payer="Lee")

    result = run(raw, "lunch for the three of us was 40, all included")

    assert result == {"type": "question", "question": "Who paid for this expense?"}


def test_hallucinated_tax_asks_for_the_tax():
    raw = parsed(
        [item("Lunch", "40", mode="all")],
        payer="ME",
        charges=[charge("tax", amount="3.20")],
    )

    result = run(raw, "i paid 40 for lunch plus tax, split evenly")

    assert result == {"type": "question", "question": "How much was the tax?"}


def test_dropped_tip_asks_how_to_handle_it():
    raw = parsed([item("Lunch", "40", mode="all")], payer="ME")

    result = run(raw, "i paid 40 for lunch and left a tip, split evenly")

    assert result["type"] == "question"
    assert result["question"].startswith("How much was the tip")


def test_grounded_message_still_previews():
    raw = parsed(
        [item("Lunch", "40", mode="all")],
        payer="ME",
        charges=[charge("tip", percent="18")],
    )

    result = run(raw, "i paid 40 for lunch. tip was 18%, split it proportionally")

    assert result["type"] == "preview", result.get("question")
    assert result["preview"]["totalCents"] == 4720


def test_fired_check_is_logged_without_user_text(caplog):
    raw = parsed([item("Lunch", "40", mode="all")], payer="Lee")

    with caplog.at_level(logging.INFO, logger="splitwise.grounding"):
        run(raw, "lunch secretphrase 40, all included")

    assert "payer" in caplog.text
    assert "secretphrase" not in caplog.text


# ---------------------------------------------------------------- word lists


def test_word_lists_live_in_config():
    assert config.GROUNDING_PAYMENT_WORDS
    assert config.GROUNDING_INCLUDED_WORDS
    assert config.GROUNDING_NONE_WORDS
    assert config.GROUNDING_COVERED_AFTER_WORDS


def test_word_lists_do_not_copy_benchmark_phrasing():
    """No grounding pattern may be a multi-word phrase from a benchmark prompt."""
    import json

    prompts = [
        turn["text"].lower()
        for path in SCENARIOS.glob("*.json")
        for turn in json.loads(path.read_text())["turns"]
    ]
    phrases = (
        list(config.GROUNDING_PAYMENT_WORDS)
        + list(config.GROUNDING_INCLUDED_WORDS)
        + list(config.GROUNDING_NONE_WORDS)
        + list(config.GROUNDING_COVERED_AFTER_WORDS)
        + list(config.GROUNDING_PAYER_FILLER_WORDS)
    )
    for phrase in phrases:
        if len(phrase.split()) < 2:
            continue
        for prompt in prompts:
            assert not re.search(rf"\b{re.escape(phrase)}\b", prompt), phrase
