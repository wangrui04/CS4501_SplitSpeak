"""Issue #28: net settlement and group balances API."""

import pytest
from fastapi.testclient import TestClient
from hypothesis import given, strategies as st

from backend.database import create_database, seed_database
from backend.main import create_app
from backend.repository import save_expense
from backend.settlement import compute_settlement, member_balances


ROSTER = ["Sarah", "Kayla", "Rui"]


def expense(paid, shares):
    return {
        "payments": [
            {"name": name, "cents": cents} for name, cents in paid.items()
        ],
        "shares": [
            {"name": name, "cents": cents} for name, cents in shares.items()
        ],
    }


def transfers(result):
    return [(t["from"], t["to"], t["cents"]) for t in result["transfers"]]


# Benchmark keys as test vectors

def test_b1_equal_dinner():
    result = compute_settlement(
        [expense({"Sarah": 9600}, {"Sarah": 3200, "Rui": 3200, "Kayla": 3200})],
        ROSTER,
    )

    assert result["error"] is None
    assert sorted(transfers(result)) == [
        ("Kayla", "Sarah", 3200), ("Rui", "Sarah", 3200),
    ]


def test_b2_moderate():
    result = compute_settlement(
        [expense({"Sarah": 9240},
                 {"Sarah": 3080, "Rui": 2310, "Kayla": 3850})],
        ROSTER,
    )

    assert transfers(result) == [
        ("Kayla", "Sarah", 3850), ("Rui", "Sarah", 2310),
    ]


def test_b3_intermediate():
    result = compute_settlement(
        [expense({"Sarah": 10500},
                 {"Sarah": 2827, "Rui": 5250, "Kayla": 2423})],
        ROSTER,
    )

    assert transfers(result) == [
        ("Rui", "Sarah", 5250), ("Kayla", "Sarah", 2423),
    ]


def test_b4_multi_payer_is_net_not_pairwise():
    # Pairwise would say Kayla owes Rui $40; net settlement does not.
    result = compute_settlement(
        [expense({"Sarah": 84000, "Rui": 12000, "Kayla": 9000},
                 {"Sarah": 44500, "Rui": 40000, "Kayla": 20500})],
        ROSTER,
    )

    assert transfers(result) == [
        ("Rui", "Sarah", 28000), ("Kayla", "Sarah", 11500),
    ]


def test_b5_refund_counts_as_negative_paid():
    result = compute_settlement(
        [{
            "payments": [
                {"name": "Sarah", "cents": 60000},
                {"name": "Sarah", "cents": -10000},
                {"name": "Rui", "cents": 12000},
                {"name": "Kayla", "cents": 6000},
            ],
            "shares": [
                {"name": "Sarah", "cents": 25750},
                {"name": "Rui", "cents": 26750},
                {"name": "Kayla", "cents": 15500},
            ],
        }],
        ROSTER,
    )

    assert transfers(result) == [
        ("Rui", "Sarah", 14750), ("Kayla", "Sarah", 9500),
    ]


def test_two_creditors():
    result = compute_settlement(
        [
            expense({"Sarah": 10000}, {"Rui": 10000}),
            expense({"Kayla": 5000}, {"Rui": 5000}),
        ],
        ROSTER,
    )

    assert transfers(result) == [
        ("Rui", "Sarah", 10000), ("Rui", "Kayla", 5000),
    ]


def test_ties_broken_by_roster_order():
    result = compute_settlement(
        [expense({"Sarah": 3000}, {"Sarah": 1000, "Kayla": 1000, "Rui": 1000})],
        ROSTER,
    )

    # Kayla and Rui owe the same; Kayla comes first in the roster.
    assert transfers(result)[0][0] == "Kayla"


def test_legacy_single_payer_shape_still_works():
    result = compute_settlement(
        [{
            "payer": "Sarah",
            "totalCents": 3000,
            "shares": [
                {"name": "Sarah", "cents": 1000},
                {"name": "Kayla", "cents": 1000},
                {"name": "Rui", "cents": 1000},
            ],
        }],
        ROSTER,
    )

    assert {n["name"]: n["netCents"] for n in result["nets"]} == {
        "Sarah": 2000, "Kayla": -1000, "Rui": -1000,
    }


def test_unbalanced_input_returns_error_and_no_transfers():
    result = compute_settlement(
        [expense({"Sarah": 3000}, {"Kayla": 1000, "Rui": 1000})],
        ROSTER,
    )

    assert result["error"] == "UNBALANCED"
    assert result["transfers"] == []


def test_empty_group_is_all_zero():
    result = compute_settlement([], ROSTER)

    assert result["transfers"] == []
    assert all(n["netCents"] == 0 for n in result["nets"])


@st.composite
def balanced_nets(draw):
    size = draw(st.integers(min_value=2, max_value=6))
    values = draw(st.lists(
        st.integers(min_value=-100000, max_value=100000),
        min_size=size - 1, max_size=size - 1,
    ))
    return values + [-sum(values)]


@given(nets=balanced_nets())
def test_property_transfers_settle_everyone(nets):
    roster = [f"P{index}" for index in range(len(nets))]
    expenses = [
        expense({name: net}, {}) if net > 0 else expense({}, {name: -net})
        for name, net in zip(roster, nets)
        if net
    ]

    first = compute_settlement(expenses, roster)
    second = compute_settlement(expenses, roster)

    balance = dict(zip(roster, nets))
    for transfer in first["transfers"]:
        assert transfer["cents"] > 0
        assert transfer["from"] != transfer["to"]
        balance[transfer["from"]] += transfer["cents"]
        balance[transfer["to"]] -= transfer["cents"]

    assert all(value == 0 for value in balance.values())
    assert len(first["transfers"]) <= len(roster) - 1
    assert first == second


def test_member_balances_relative_to_session_user():
    result = compute_settlement(
        [expense({"Sarah": 84000, "Rui": 12000, "Kayla": 9000},
                 {"Sarah": 44500, "Rui": 40000, "Kayla": 20500})],
        ROSTER,
    )

    as_kayla = member_balances(result, "Kayla", ROSTER)

    assert as_kayla["balances"] == [
        {"name": "Sarah", "cents": -11500, "status": "you owe"},
        {"name": "Rui", "cents": 0, "status": "settled up"},
    ]
    assert as_kayla["summary"] == {
        "totalBalance": -11500, "youOwe": 11500, "youAreOwed": 0,
    }


# API

@pytest.fixture
def db():
    connection = create_database(":memory:")
    seed_database(connection)
    yield connection
    connection.close()


def login(db, name):
    client = TestClient(create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
    ))
    client.post("/api/session", json={"name": name})
    return client


def save_b4(db):
    save_expense(db, {
        "groupId": 1,
        "description": "Trip",
        "payer": "Sarah",
        "totalCents": 105000,
        "payments": [
            {"name": "Sarah", "cents": 84000},
            {"name": "Rui", "cents": 12000},
            {"name": "Kayla", "cents": 9000},
        ],
        "shares": [
            {"name": "Sarah", "cents": 44500},
            {"name": "Kayla", "cents": 20500},
            {"name": "Rui", "cents": 40000},
        ],
        "source": "ai",
        "createdBy": "Sarah",
    })


def test_api_group_summary_as_sarah(db):
    save_b4(db)

    body = login(db, "Sarah").get("/api/groups/1").json()

    assert body["members"] == ROSTER
    assert body["summary"] == {
        "totalBalance": 39500, "youOwe": 0, "youAreOwed": 39500,
    }
    assert [(t["from"], t["to"], t["cents"]) for t in body["transfers"]] == [
        ("Rui", "Sarah", 28000), ("Kayla", "Sarah", 11500),
    ]
    assert {n["name"]: n["netCents"] for n in body["nets"]} == {
        "Sarah": 39500, "Kayla": -11500, "Rui": -28000,
    }


def test_api_group_summary_as_kayla(db):
    save_b4(db)

    body = login(db, "Kayla").get("/api/groups/1").json()

    assert body["summary"]["youOwe"] == 11500
    assert {b["name"]: b["status"] for b in body["balances"]} == {
        "Sarah": "you owe", "Rui": "settled up",
    }


def test_api_empty_group_is_all_zero(db):
    body = login(db, "Sarah").get("/api/groups/1").json()

    assert body["summary"] == {
        "totalBalance": 0, "youOwe": 0, "youAreOwed": 0,
    }
    assert body["transfers"] == []
    assert all(b["status"] == "settled up" for b in body["balances"])


def test_saved_payments_round_trip(db):
    save_b4(db)

    expenses = login(db, "Sarah").get("/api/groups/1/expenses").json()

    assert expenses[0]["payments"] == [
        {"name": "Sarah", "cents": 84000},
        {"name": "Kayla", "cents": 9000},
        {"name": "Rui", "cents": 12000},
    ]


def test_payments_must_sum_to_total(db):
    with pytest.raises(ValueError):
        save_expense(db, {
            "groupId": 1,
            "description": "Trip",
            "payer": "Sarah",
            "totalCents": 3000,
            "payments": [{"name": "Sarah", "cents": 2000}],
            "shares": [{"name": "Sarah", "cents": 3000}],
            "source": "manual",
            "createdBy": "Sarah",
        })


def b4_parsed():
    def item(name, price, names, mode="only", **extra):
        return {
            "name": name,
            "quantity": 1,
            "unitPrice": price,
            "participants": {"mode": mode, "names": names},
            **extra,
        }

    return {
        "description": "Trip",
        "payer": "ME",
        "items": [
            item("House", "840.00", [], mode="all", weights=[
                {"name": "ME", "weight": 3},
                {"name": "Rui", "weight": 3},
                {"name": "Kayla", "weight": 1},
            ]),
            item("Groceries", "120.00", [], mode="all", paidBy="Rui"),
            item("Transportation", "90.00", ["ME", "Kayla"],
                 paidBy="Kayla"),
        ],
        "charges": [],
        "statedTotal": None,
        "openQuestions": [],
    }


def test_chat_preview_includes_paid_and_settlement_then_confirm(db):
    from backend.llm import FakeLlmClient

    client = TestClient(create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=FakeLlmClient([b4_parsed()]),
    ))
    client.post("/api/session", json={"name": "Sarah"})

    body = client.post(
        "/api/chat", json={"groupId": 1, "message": "trip"}
    ).json()
    preview = body["preview"]

    assert {p["name"]: p["cents"] for p in preview["paid"]} == {
        "Sarah": 84000, "Kayla": 9000, "Rui": 12000,
    }
    assert {s["name"]: s["cents"] for s in preview["shares"]} == {
        "Sarah": 44500, "Kayla": 20500, "Rui": 40000,
    }
    assert preview["settlement"]["transfers"] == [
        {"from": "Rui", "to": "Sarah", "cents": 28000},
        {"from": "Kayla", "to": "Sarah", "cents": 11500},
    ]

    # Drafts never move balances.
    assert client.get("/api/groups/1").json()["summary"]["youAreOwed"] == 0

    client.post(f"/api/conversations/{body['conversationId']}/confirm")

    summary = client.get("/api/groups/1").json()["summary"]
    assert summary == {
        "totalBalance": 39500, "youOwe": 0, "youAreOwed": 39500,
    }
