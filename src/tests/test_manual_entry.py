"""Issue #26: manual-entry expense endpoint."""

import pytest
from fastapi.testclient import TestClient

from backend.database import create_database, seed_database
from backend.llm import FakeLlmClient
from backend.main import create_app
from backend.repository import list_expenses


SECRET = "test-secret-with-at-least-32-characters"
URL = "/api/groups/1/expenses/manual"


@pytest.fixture
def db():
    connection = create_database(":memory:")
    seed_database(connection)
    yield connection
    connection.close()


def signed_in(db, name="Sarah", llm=None):
    client = TestClient(create_app(db=db, session_secret=SECRET, llm=llm))
    client.post("/api/session", json={"name": name})
    return client


def payload(**overrides):
    return {
        "description": "Dinner",
        "amount": "30.00",
        "paidBy": "Sarah",
        "splitBetween": ["Sarah", "Kayla", "Rui"],
        **overrides,
    }


def stored_shares(db):
    return {
        share["name"]: share["cents"]
        for share in list_expenses(db, 1)[-1]["shares"]
    }


def test_thirty_dollars_among_three(db):
    response = signed_in(db).post(URL, json=payload())

    assert response.status_code == 200
    assert stored_shares(db) == {"Sarah": 1000, "Kayla": 1000, "Rui": 1000}


def test_unchecked_member_gets_zero(db):
    signed_in(db).post(URL, json=payload(splitBetween=["Sarah", "Kayla"]))

    assert stored_shares(db) == {"Sarah": 1500, "Kayla": 1500, "Rui": 0}


def test_ten_dollars_remainder_goes_to_payer(db):
    signed_in(db).post(URL, json=payload(amount="10.00"))

    assert stored_shares(db) == {"Sarah": 334, "Kayla": 333, "Rui": 333}


def test_numeric_amount_accepted(db):
    response = signed_in(db).post(URL, json=payload(amount=12.5))

    assert response.status_code == 200
    assert sum(stored_shares(db).values()) == 1250


@pytest.mark.parametrize("amount", ["abc", 0, "0", -5, "-5", "12.345", ""])
def test_invalid_amounts_rejected(db, amount):
    response = signed_in(db).post(URL, json=payload(amount=amount))

    assert response.status_code == 400
    assert list_expenses(db, 1) == []


@pytest.mark.parametrize("amount", ["0", "0.00", 0])
def test_zero_amount_rejected_with_clear_message(db, amount):
    response = signed_in(db).post(URL, json=payload(amount=amount))

    assert response.status_code == 400
    assert response.json()["detail"] == "Amount must be greater than 0"


def test_unknown_payer_rejected(db):
    response = signed_in(db).post(URL, json=payload(paidBy="Aly"))

    assert response.status_code == 400


def test_unknown_split_member_rejected(db):
    response = signed_in(db).post(
        URL, json=payload(splitBetween=["Sarah", "Allie"])
    )

    assert response.status_code == 400


def test_empty_split_rejected(db):
    response = signed_in(db).post(URL, json=payload(splitBetween=[]))

    assert response.status_code == 400


def test_missing_fields_rejected_with_400(db):
    response = signed_in(db).post(URL, json={"description": "Dinner"})

    assert response.status_code == 400


def test_blank_description_rejected(db):
    response = signed_in(db).post(URL, json=payload(description="   "))

    assert response.status_code == 400


def test_no_session_is_401(db):
    client = TestClient(create_app(db=db, session_secret=SECRET))

    assert client.post(URL, json=payload()).status_code == 401


def test_non_member_is_403(db):
    # Aly is only in the Weekend trip group.
    response = signed_in(db, "Aly").post(URL, json=payload(paidBy="Sarah"))

    assert response.status_code == 403


def test_saved_as_manual_by_session_user(db):
    signed_in(db, "Kayla").post(URL, json=payload())

    expense = list_expenses(db, 1)[-1]
    assert expense["source"] == "manual"
    assert expense["createdBy"] == "Kayla"
    assert expense["payer"] == "Sarah"
    assert expense["payments"] == [{"name": "Sarah", "cents": 3000}]


def test_manual_and_ai_store_identical_shares(db):
    ai_expense = {
        "description": "Dinner",
        "payer": "ME",
        "items": [{
            "name": "Dinner",
            "quantity": 1,
            "unitPrice": "10.00",
            "participants": {"mode": "all", "names": []},
        }],
        "charges": [],
        "statedTotal": "10.00",
        "openQuestions": [],
    }
    client = signed_in(db, llm=FakeLlmClient([ai_expense]))

    chat = client.post(
        "/api/chat", json={"groupId": 1, "message": "dinner 10"}
    ).json()
    client.post(f"/api/conversations/{chat['conversationId']}/confirm")
    client.post(URL, json=payload(amount="10.00"))

    ai_saved, manual_saved = list_expenses(db, 1)
    assert ai_saved["shares"] == manual_saved["shares"]
    assert ai_saved["payments"] == manual_saved["payments"]
    assert ai_saved["totalCents"] == manual_saved["totalCents"]
