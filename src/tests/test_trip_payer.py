"""Multi-payer trips: no top-level payer needed when every item has one.

Found in a live B4 run: the model set paidBy on every item and left the
top-level payer empty, and the app asked "Who paid for this expense?"
even though the prompt said who paid for each item.
"""

from backend.llm import FakeLlmClient
from backend.pipeline import parse_turn


ROSTER = ["Sarah", "Kayla", "Rui"]


def item(name, price, names=(), mode="only", **extra):
    return {
        "name": name,
        "quantity": 1,
        "unitPrice": price,
        "participants": {"mode": mode, "names": list(names)},
        **extra,
    }


def b4_items():
    return [
        item("House", "840.00", mode="all", paidBy="ME", weights=[
            {"name": "ME", "weight": 3},
            {"name": "Rui", "weight": 3},
            {"name": "Kayla", "weight": 1},
        ]),
        item("Groceries", "120.00", mode="all", paidBy="Rui"),
        item("Transportation", "90.00", ["ME", "Kayla"], paidBy="Kayla"),
    ]


def parsed(items, payer=None, charges=()):
    return {
        "description": "Trip",
        "payer": payer,
        "items": items,
        "charges": list(charges),
        "statedTotal": None,
        "openQuestions": [],
    }


def run(raw):
    return parse_turn(
        llm=FakeLlmClient([raw]),
        conversation=[{"role": "user", "content": "trip"}],
        roster=ROSTER,
        current_user="Sarah",
    )


def by_name(entries):
    return {entry["name"]: entry["cents"] for entry in entries}


def test_every_item_has_a_payer_so_no_question():
    result = run(parsed(b4_items()))

    assert result["type"] == "preview", result.get("question")
    preview = result["preview"]
    assert by_name(preview["shares"]) == {"Sarah": 44500, "Kayla": 20500, "Rui": 40000}
    assert by_name(preview["paid"]) == {"Sarah": 84000, "Kayla": 9000, "Rui": 12000}


def test_main_payer_is_whoever_paid_the_most():
    result = run(parsed(b4_items()))

    assert result["preview"]["payer"] == "Sarah"


def test_still_asks_when_an_item_has_no_payer():
    items = b4_items()
    del items[1]["paidBy"]

    result = run(parsed(items))

    assert result["type"] == "question"
    assert result["question"] == "Who paid for this expense?"


def test_still_asks_when_tax_or_tip_has_no_payer():
    # Charges are paid by the main payer, so it must be known.
    tip = {"kind": "tip", "amount": "10.00", "percent": None, "method": "equal"}

    result = run(parsed(b4_items(), charges=[tip]))

    assert result["type"] == "question"
    assert result["question"] == "Who paid for this expense?"


def test_explicit_payer_still_wins():
    result = run(parsed(b4_items(), payer="Rui"))

    assert result["preview"]["payer"] == "Rui"
