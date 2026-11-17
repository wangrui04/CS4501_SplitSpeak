"""Issue #55: tie each payer and price to the user's own words.

The #49 checks prove a value was typed somewhere, not that it was typed
for that item. The model now quotes the words behind each item's payer
and price and each charge's amount, and code checks the quote:

- A quote that isn't in the user's messages word for word (paraphrased)
  is ignored; the older checks still apply.
- A word-for-word quote that contradicts the value is rejected, and the
  app asks instead.
"""

import json
from pathlib import Path

from backend.config import SYSTEM_PROMPT
from backend.grounding import evidence_question, ground_payer_evidence
from backend.llm import PARSED_EXPENSE_SCHEMA, FakeLlmClient
from backend.pipeline import parse_turn
from backend.schemas import ParsedExpense


ROSTER = ["Sarah", "Kayla", "Rui"]
ROOT = Path(__file__).resolve().parents[1]


def item(name, price, names=(), mode="only", quantity=1, **extra):
    return {
        "name": name,
        "quantity": quantity,
        "unitPrice": price,
        "participants": {"mode": mode, "names": list(names)},
        **extra,
    }


def charge(kind, amount=None, percent=None, evidence=None):
    return {
        "kind": kind,
        "amount": amount,
        "percent": percent,
        "method": "proportional",
        "amountEvidence": evidence,
    }


def parsed(items, payer=None, charges=()):
    return {
        "description": "Dinner",
        "payer": payer,
        "items": items,
        "charges": list(charges),
        "statedTotal": None,
        "openQuestions": [],
    }


def run(raw, text, current_user="Kayla"):
    return parse_turn(
        llm=FakeLlmClient([raw]),
        conversation=[{"role": "user", "content": text}],
        roster=ROSTER,
        current_user=current_user,
    )


# ------------------------------------------------------------------ schema


def test_evidence_fields_are_optional():
    data = parsed([item("Pizza", "10")], charges=[charge("tax", amount="1")])
    del data["charges"][0]["amountEvidence"]

    expense = ParsedExpense.model_validate(data)

    assert expense.items[0].priceEvidence is None
    assert expense.items[0].payerEvidence is None
    assert expense.charges[0].amountEvidence is None


def test_llm_schema_lists_evidence_fields_as_optional():
    defs = PARSED_EXPENSE_SCHEMA["$defs"]

    for model, field in (("Item", "priceEvidence"), ("Item", "payerEvidence"), ("Charge", "amountEvidence")):
        assert field in defs[model]["properties"], field
        assert field not in defs[model].get("required", []), field


# ------------------------------------------------------------ price quotes

PIZZAS = "nachos 18 pizza 36 and margs 12 each"


def test_matching_price_quote_passes():
    data = parsed([item("Pizza", "36", mode="all", priceEvidence="pizza 36")])

    assert evidence_question(data, [PIZZAS]) is None


def test_quote_is_matched_ignoring_case_and_spacing():
    data = parsed([item("Pizza", "36", mode="all", priceEvidence="Pizza   36")])

    assert evidence_question(data, [PIZZAS]) is None


def test_paraphrased_quote_is_ignored():
    data = parsed([item("Pizza", "36", mode="all", priceEvidence="the pizza cost thirty-six")])

    assert evidence_question(data, [PIZZAS]) is None


def test_price_quote_with_another_items_number_is_rejected():
    data = parsed([item("Pizza", "36", mode="all", priceEvidence="nachos 18")])

    assert evidence_question(data, [PIZZAS]) == "How much was Pizza?"


def test_price_quote_may_state_the_unit_price_or_the_total():
    each = item("Margarita", "12", mode="all", quantity=2, priceEvidence="margs 12 each")
    total = item("Drinks", "10", mode="all", quantity=2, priceEvidence="drinks were 20")

    assert evidence_question(parsed([each]), [PIZZAS]) is None
    assert evidence_question(parsed([total]), ["drinks were 20"]) is None


# ----------------------------------------------------------- charge quotes

CHARGES = "tax 9 tip 18 split those proportionally"


def test_matching_charge_quotes_pass():
    data = parsed(
        [item("Food", "60", mode="all")],
        charges=[charge("tax", "9", evidence="tax 9"), charge("tip", "18", evidence="tip 18")],
    )

    assert evidence_question(data, ["food 60. " + CHARGES]) is None


def test_swapped_tax_and_tip_are_rejected():
    data = parsed(
        [item("Food", "60", mode="all")],
        charges=[charge("tax", "18", evidence="tip 18"), charge("tip", "9", evidence="tax 9")],
    )

    assert evidence_question(data, ["food 60. " + CHARGES]) == "How much was the tax?"


def test_shared_charge_quote_uses_the_number_nearest_its_word():
    good = parsed(
        [item("Food", "60", mode="all")],
        charges=[
            charge("tax", "9", evidence="tax 9 tip 18"),
            charge("tip", "18", evidence="tax 9 tip 18"),
        ],
    )
    swapped = parsed(
        [item("Food", "60", mode="all")],
        charges=[charge("tax", "18", evidence="tax 9 tip 18")],
    )

    assert evidence_question(good, ["food 60. " + CHARGES]) is None
    assert evidence_question(swapped, ["food 60. " + CHARGES]) == "How much was the tax?"


def test_number_after_the_word_wins_a_tie():
    text = "tax was $6 and tip was 14.40"
    data = parsed(
        [item("Food", "60", mode="all")],
        charges=[
            charge("tax", "6", evidence="tax was $6 and tip was 14.40"),
            charge("tip", "14.40", evidence="tax was $6 and tip was 14.40"),
        ],
    )

    assert evidence_question(data, ["food 60. " + text]) is None


def test_percent_charge_needs_a_percent_in_its_quote():
    good = parsed([item("Food", "40", mode="all")], charges=[charge("tip", percent="18", evidence="tip was 18%")])
    bad = parsed([item("Food", "40", mode="all")], charges=[charge("tip", amount="18", evidence="tip was 18%")])
    text = "food 40, tip was 18%"

    assert evidence_question(good, [text]) is None
    assert evidence_question(bad, [text]) == "How much was the tip?"


# ------------------------------------------------------------ payer quotes

TWO_PIZZAS = "Sarah bought a $10 pizza and I ate 2/3 of it. Rui bought a $20 pizza and shared it evenly."


def test_payer_quote_for_another_item_is_rejected():
    data = parsed([item("Pizza", "10", ["ME", "Sarah"], paidBy="Rui", payerEvidence="Rui bought a $20 pizza")])

    grounded, fired = ground_payer_evidence(data, [TWO_PIZZAS], "Kayla")

    assert grounded["items"][0]["paidBy"] is None
    assert fired == ["payer_evidence"]


def test_payer_quote_naming_someone_else_is_rejected():
    data = parsed([item("Pizza", "10", ["ME", "Sarah"], paidBy="Rui", payerEvidence="Sarah bought a $10 pizza")])

    grounded, _ = ground_payer_evidence(data, [TWO_PIZZAS], "Kayla")

    assert grounded["items"][0]["paidBy"] is None


def test_matching_payer_quote_is_kept():
    data = parsed([item("Pizza", "10", ["ME", "Sarah"], paidBy="Sarah", payerEvidence="Sarah bought a $10 pizza")])

    grounded, fired = ground_payer_evidence(data, [TWO_PIZZAS], "Kayla")

    assert grounded["items"][0]["paidBy"] == "Sarah"
    assert fired == []


def test_first_person_payer_quote_is_kept():
    data = parsed([item("Lodging", "600", mode="all", paidBy="ME", payerEvidence="i paid 600 lodging")])

    grounded, _ = ground_payer_evidence(data, ["i paid 600 lodging"], "Sarah")

    assert grounded["items"][0]["paidBy"] == "ME"


def test_paraphrased_payer_quote_is_ignored():
    data = parsed([item("Pizza", "10", ["ME"], paidBy="Rui", payerEvidence="Rui got the first pizza")])

    grounded, fired = ground_payer_evidence(data, [TWO_PIZZAS], "Kayla")

    assert grounded["items"][0]["paidBy"] == "Rui"
    assert fired == []


# ----------------------------------------------------------------- pipeline


def test_misattributed_pizza_asks_who_paid_for_it():
    items = [
        item("Pizza", "10", ["ME", "Sarah"], paidBy="Rui", payerEvidence="Rui bought a $20 pizza"),
        item("Pizza", "20", mode="all", paidBy="Rui", payerEvidence="Rui bought a $20 pizza"),
    ]

    result = run(parsed(items), TWO_PIZZAS)

    assert result == {"type": "question", "question": "Who paid for Pizza ($10)?"}


def test_swapped_charges_ask_through_the_pipeline():
    raw = parsed(
        [item("Food", "60", mode="all")],
        payer="ME",
        charges=[charge("tax", "18", evidence="tip 18"), charge("tip", "9", evidence="tax 9")],
    )

    result = run(raw, "i paid 60 for food. " + CHARGES)

    assert result == {"type": "question", "question": "How much was the tax?"}


# ------------------------------------------------------- prompt and fixtures


def test_system_prompt_asks_for_exact_quotes():
    assert "priceEvidence" in SYSTEM_PROMPT
    assert "payerEvidence" in SYSTEM_PROMPT
    assert "amountEvidence" in SYSTEM_PROMPT
    assert "exact words" in SYSTEM_PROMPT


def official_preview_fixtures():
    fixtures = json.loads((ROOT / "backend" / "fixtures" / "llm_fixtures.json").read_text())["responses"]
    texts = {
        turn["text"]
        for path in (ROOT / "benchmark" / "scenarios" / "official").glob("*.json")
        for turn in json.loads(path.read_text())["turns"]
    }
    return {text: fx for text, fx in fixtures.items() if text in texts and not fx["openQuestions"]}


def test_official_fixtures_quote_every_price_and_charge():
    fixtures = official_preview_fixtures()
    assert len(fixtures) == 6

    for text, fixture in fixtures.items():
        for entry in fixture["items"]:
            assert entry.get("priceEvidence"), (text[:30], entry["name"])
            if entry.get("paidBy"):
                assert entry.get("payerEvidence"), (text[:30], entry["name"])
        for entry in fixture["charges"]:
            assert entry.get("amountEvidence"), (text[:30], entry["kind"])
