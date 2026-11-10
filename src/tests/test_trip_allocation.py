"""Multi-payer, weighted, refund, and pooled tax/tip allocation.

These are the upstream features the five benchmark scenarios need
(see docs/benchmarks.md). Expected values come from the answer keys.
"""

import pytest
from hypothesis import given, strategies as st

from backend.allocation import (
    allocate_charges,
    allocate_items,
    WeightsMismatchError,
)
from backend.validator import validate


ROSTER = ["Sarah", "Kayla", "Rui"]


def item(name, price, names, mode="only", quantity=1, **extra):
    return {
        "name": name,
        "quantity": quantity,
        "unitPrice": price,
        "participants": {"mode": mode, "names": names},
        **extra,
    }


def weights(**by_name):
    return [{"name": name, "weight": w} for name, w in by_name.items()]


def by_roster(shares):
    return {name: shares[name] for name in ROSTER}


# Weighted splits

def test_weighted_item_splits_by_nights():
    # B4 house: 840 over nights 3 / 3 / 1.
    result = allocate_items(
        [item("House", "840.00", [], mode="all",
              weights=weights(ME=3, Rui=3, Kayla=1))],
        "Sarah", ROSTER, "Sarah",
    )

    assert by_roster(result["shares"]) == {
        "Sarah": 36000, "Kayla": 12000, "Rui": 36000,
    }


def test_weighted_item_twice_as_much():
    result = allocate_items(
        [item("Dinner", "120.00", ["ME", "Rui"],
              weights=weights(ME=1, Rui=2), paidBy="Rui")],
        "Sarah", ROSTER, "Sarah",
    )

    assert result["shares"]["Sarah"] == 4000
    assert result["shares"]["Rui"] == 8000
    assert result["shares"]["Kayla"] == 0


def test_weights_must_match_participants():
    with pytest.raises(WeightsMismatchError):
        allocate_items(
            [item("House", "90.00", ["ME", "Rui"],
                  weights=weights(ME=1, Kayla=2))],
            "Sarah", ROSTER, "Sarah",
        )


def test_weighted_remainder_cents_still_sum():
    result = allocate_items(
        [item("Cabin", "100.00", [], mode="all",
              weights=weights(Sarah=1, Kayla=1, Rui=1))],
        "Kayla", ROSTER, "Sarah",
    )

    assert sum(result["shares"].values()) == 10000
    # Leftover cent goes to the item's payer when they share it.
    assert result["shares"]["Kayla"] == 3334


# Per-item payers

def test_items_paid_by_different_people():
    # B4: Sarah 840 house, Rui 120 groceries, Kayla 90 transport.
    result = allocate_items(
        [
            item("House", "840.00", [], mode="all",
                 weights=weights(ME=3, Rui=3, Kayla=1)),
            item("Groceries", "120.00", [], mode="all", paidBy="Rui"),
            item("Transportation", "90.00", ["ME", "Kayla"],
                 paidBy="Kayla"),
        ],
        "Sarah", ROSTER, "Sarah",
    )

    assert by_roster(result["shares"]) == {
        "Sarah": 44500, "Kayla": 20500, "Rui": 40000,
    }
    assert by_roster(result["paid"]) == {
        "Sarah": 84000, "Kayla": 9000, "Rui": 12000,
    }
    assert result["totalCents"] == 105000
    assert result["lineItems"][1]["paidBy"] == "Rui"


def test_item_payer_me_resolves_to_current_user():
    result = allocate_items(
        [item("Taxi", "60.00", ["Rui"], mode="all_except", paidBy="ME")],
        "Sarah", ROSTER, "Kayla",
    )

    assert result["paid"]["Kayla"] == 6000


def test_unknown_item_payer_rejected():
    from backend.allocation import UnknownNameError

    with pytest.raises(UnknownNameError):
        allocate_items(
            [item("Taxi", "60.00", [], mode="all", paidBy="Aly")],
            "Sarah", ROSTER, "Sarah",
        )


# Refunds

def test_refund_reduces_cost_and_counts_as_negative_paid():
    # B5 lodging: 600 paid by Sarah, 100 refunded to Sarah, 3/3/2 nights.
    result = allocate_items(
        [item("Lodging", "600.00", [], mode="all",
              weights=weights(ME=3, Rui=3, Kayla=2),
              refund={"amount": "100.00", "recipient": "ME"})],
        "Sarah", ROSTER, "Sarah",
    )

    assert by_roster(result["shares"]) == {
        "Sarah": 18750, "Kayla": 12500, "Rui": 18750,
    }
    assert result["paid"]["Sarah"] == 50000
    assert result["totalCents"] == 50000
    assert result["lineItems"][0]["refundCents"] == 10000


def test_refund_larger_than_item_rejected():
    # match= makes sure the refund check raised, not a later check.
    with pytest.raises(ValueError, match="Refund is larger"):
        allocate_items(
            [item("Lodging", "50.00", [], mode="all",
                  refund={"amount": "60.00", "recipient": "ME"})],
            "Sarah", ROSTER, "Sarah",
        )


def test_b5_full_corrected_allocation():
    result = allocate_items(
        [
            item("Lodging", "600.00", [], mode="all",
                 weights=weights(ME=3, Rui=3, Kayla=2),
                 refund={"amount": "100.00", "recipient": "ME"}),
            item("Dinner", "120.00", ["ME", "Rui"], paidBy="Rui",
                 weights=weights(ME=1, Rui=2)),
            item("Taxi", "60.00", ["Rui"], mode="all_except",
                 paidBy="Kayla"),
        ],
        "Sarah", ROSTER, "Sarah",
    )

    assert by_roster(result["shares"]) == {
        "Sarah": 25750, "Kayla": 15500, "Rui": 26750,
    }
    assert by_roster(result["paid"]) == {
        "Sarah": 50000, "Kayla": 6000, "Rui": 12000,
    }


# Pooled tax + tip

def test_b2_proportional_tax_and_tip():
    allocation = allocate_items(
        [
            item("Rui meal", "18.00", ["Rui"]),
            item("Sarah meal", "24.00", ["ME"]),
            item("Kayla meal", "30.00", ["Kayla"]),
        ],
        "Sarah", ROSTER, "Sarah",
    )
    result = allocate_charges(
        [
            {"kind": "tax", "amount": "6.00", "percent": None,
             "method": "proportional"},
            {"kind": "tip", "amount": "14.40", "percent": None,
             "method": "proportional"},
        ],
        allocation, "Sarah", ROSTER,
    )

    assert by_roster(result["shares"]) == {
        "Sarah": 3080, "Kayla": 3850, "Rui": 2310,
    }
    assert result["paid"] == {"Sarah": 9240, "Kayla": 0, "Rui": 0}


def test_b3_pooled_tax_and_tip_matches_key_to_the_cent():
    # Allocating tax and tip separately gives Sarah 28.28 / Kayla 24.22.
    # Pooling them into one proportional allocation matches the key.
    allocation = allocate_items(
        [
            item("Nachos", "18.00", ["ME", "Rui"]),
            item("Pizza", "36.00", ["Rui", "Kayla"]),
            item("Margarita", "12.00", ["Kayla"], mode="all_except",
                 quantity=2),
        ],
        "Sarah", ROSTER, "Sarah",
    )
    result = allocate_charges(
        [
            {"kind": "tax", "amount": "9.00", "percent": None,
             "method": "proportional"},
            {"kind": "tip", "amount": "18.00", "percent": None,
             "method": "proportional"},
        ],
        allocation, "Sarah", ROSTER,
    )

    assert by_roster(result["shares"]) == {
        "Sarah": 2827, "Kayla": 2423, "Rui": 5250,
    }
    assert result["totalCents"] == 10500
    assert result["chargeAllocations"][0]["kinds"] == ["tax", "tip"]
    assert result["chargeAllocations"][0]["amountCents"] == 2700


def test_mixed_methods_pool_separately():
    allocation = {
        "totalCents": 3000,
        "shares": {"Sarah": 0, "Kayla": 2000, "Rui": 1000},
        "lineItems": [],
    }
    result = allocate_charges(
        [
            {"kind": "tax", "amount": "3.00", "percent": None,
             "method": "proportional"},
            {"kind": "fee", "amount": "3.00", "percent": None,
             "method": "equal"},
        ],
        allocation, "Sarah", ROSTER,
    )

    assert [group["method"] for group in result["chargeAllocations"]] == [
        "proportional", "equal",
    ]
    assert result["shares"] == {"Sarah": 0, "Kayla": 2350, "Rui": 1250}


@given(
    prices=st.lists(st.integers(min_value=1, max_value=50000),
                    min_size=1, max_size=4),
    nights=st.lists(st.integers(min_value=1, max_value=9),
                    min_size=3, max_size=3),
    refund_pct=st.integers(min_value=0, max_value=100),
)
def test_hypothesis_paid_and_shares_balance(prices, nights, refund_pct):
    items = []
    for index, cents in enumerate(prices):
        refund = cents * refund_pct // 100
        items.append(item(
            f"Item {index}", f"{cents // 100}.{cents % 100:02d}", [],
            mode="all",
            paidBy=ROSTER[index % 3],
            weights=weights(**dict(zip(ROSTER, nights))),
            refund=(
                {"amount": f"{refund // 100}.{refund % 100:02d}",
                 "recipient": ROSTER[(index + 1) % 3]}
                if refund else None
            ),
        ))

    result = allocate_items(items, "Sarah", ROSTER, "Sarah")

    assert sum(result["shares"].values()) == result["totalCents"]
    assert sum(result["paid"].values()) == result["totalCents"]


# Validator coverage for the new fields

def base_parsed(**item_extra):
    return {
        "description": "Trip",
        "payer": "Sarah",
        "items": [item("House", "90.00", [], mode="all", **item_extra)],
        "charges": [],
        "statedTotal": None,
        "openQuestions": [],
    }


def good_allocation():
    return {
        "totalCents": 9000,
        "shares": {"Sarah": 3000, "Kayla": 3000, "Rui": 3000},
        "paid": {"Sarah": 9000, "Kayla": 0, "Rui": 0},
    }


def test_validator_accepts_balanced_payments():
    assert validate(base_parsed(), good_allocation(), ROSTER)["ok"]


def test_validator_rejects_payments_that_do_not_sum():
    allocation = good_allocation()
    allocation["paid"]["Sarah"] = 8000

    result = validate(base_parsed(), allocation, ROSTER)

    assert not result["ok"]
    assert result["errors"][0]["code"] == "PAYMENTS_DONT_SUM"


def test_validator_rejects_unknown_item_payer():
    result = validate(base_parsed(paidBy="Allie"), good_allocation(), ROSTER)

    assert not result["ok"]
    assert result["errors"][0]["code"] == "UNKNOWN_NAME"


def test_validator_rejects_unknown_weight_name():
    result = validate(
        base_parsed(weights=weights(Sarah=1, Allie=2)),
        good_allocation(),
        ROSTER,
    )

    assert not result["ok"]
    assert result["errors"][0]["code"] == "UNKNOWN_NAME"


def test_validator_rejects_refund_larger_than_item():
    result = validate(
        base_parsed(refund={"amount": "95.00", "recipient": "Sarah"}),
        good_allocation(),
        ROSTER,
    )

    assert not result["ok"]
    assert result["errors"][0]["code"] == "INVALID_REFUND"


def test_validator_accepts_stated_total_before_refund():
    parsed = base_parsed(refund={"amount": "30.00", "recipient": "Sarah"})
    parsed["statedTotal"] = "90.00"
    allocation = {
        "totalCents": 6000,
        "shares": {"Sarah": 2000, "Kayla": 2000, "Rui": 2000},
        "paid": {"Sarah": 6000, "Kayla": 0, "Rui": 0},
    }

    assert validate(parsed, allocation, ROSTER)["ok"]
