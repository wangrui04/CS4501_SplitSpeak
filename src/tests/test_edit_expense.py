"""Test-first contracts for #44/#45: saved expense details and edits.

These tests are intentionally RED until the detail persistence and update route
are implemented. Run with PYTHONPATH=src pytest src/tests/test_edit_expense.py.
"""
import copy
import pytest
from fastapi.testclient import TestClient

from backend.database import create_database, seed_database
from backend.main import create_app
from backend.repository import save_expense, list_expenses


@pytest.fixture
def setup():
    db = create_database(":memory:")
    seed_database(db)
    app = create_app(db=db, session_secret="test-secret-with-at-least-32-characters")
    with TestClient(app) as client:
        yield db, client
    db.close()


def login(client, name="Sarah"):
    assert client.post("/api/session", json={"name": name}).status_code == 200


def original():
    return {
        "groupId": 1,
        "description": "Dinner",
        "payer": "Sarah",
        "totalCents": 3000,
        "source": "ai",
        "createdBy": "Sarah",
        "payments": [{"name": "Sarah", "cents": 3000}],
        "shares": [
            {"name": "Sarah", "cents": 1000},
            {"name": "Kayla", "cents": 1000},
            {"name": "Rui", "cents": 1000},
        ],
        "lineItems": [
            {"name": "Pizza", "quantity": 2, "unitPriceCents": 1000,
             "participants": ["Sarah", "Kayla", "Rui"]},
            {"name": "Soda", "quantity": 1, "unitPriceCents": 1000,
             "participants": ["Sarah", "Kayla", "Rui"]},
        ],
    }


def updated():
    item = original()
    item["description"] = "Corrected dinner"
    item["totalCents"] = 3600
    item["payments"] = [
        {"name": "Sarah", "cents": 2400},
        {"name": "Kayla", "cents": 1200},
    ]
    item["shares"] = [
        {"name": "Sarah", "cents": 1200},
        {"name": "Kayla", "cents": 1200},
        {"name": "Rui", "cents": 1200},
    ]
    item["lineItems"] = [
        {"name": "Pizza", "quantity": 2, "unitPriceCents": 1200,
         "participants": ["Sarah", "Kayla", "Rui"]},
        {"name": "Soda", "quantity": 1, "unitPriceCents": 1200,
         "participants": ["Sarah", "Kayla", "Rui"]},
    ]
    return item


def endpoint(expense_id, group_id=1):
    return f"/api/groups/{group_id}/expenses/{expense_id}"


def test_saved_expense_preserves_itemized_detail_for_popup(setup):
    db, client = setup
    login(client)
    saved = save_expense(db, original())
    response = client.get("/api/groups/1/expenses")
    assert response.status_code == 200
    expense = next(x for x in response.json() if x["id"] == saved["id"])
    assert expense["lineItems"] == original()["lineItems"]
    assert expense["payments"] == original()["payments"]
    assert expense["shares"] == original()["shares"]


def test_legacy_expense_without_items_is_still_readable(setup):
    db, client = setup
    login(client)
    legacy = original()
    del legacy["lineItems"]
    saved = save_expense(db, legacy)
    expense = next(e for e in client.get("/api/groups/1/expenses").json()
                   if e["id"] == saved["id"])
    assert expense["lineItems"] in ([], None)
    assert expense["totalCents"] == 3000
    assert expense["shares"] == legacy["shares"]


def test_edit_replaces_same_expense_and_updates_group_balances(setup):
    db, client = setup
    login(client)
    saved = save_expense(db, original())
    before_count = len(list_expenses(db, 1))
    response = client.put(endpoint(saved["id"]), json=updated())
    assert response.status_code == 200, response.text
    expenses = list_expenses(db, 1)
    assert len(expenses) == before_count
    expense = next(e for e in expenses if e["id"] == saved["id"])
    assert expense["description"] == "Corrected dinner"
    assert expense["totalCents"] == 3600
    assert expense["payments"] == updated()["payments"]
    assert expense["shares"] == updated()["shares"]
    assert expense["lineItems"] == updated()["lineItems"]
    group = client.get("/api/groups/1").json()
    nets = {n["name"]: n["netCents"] for n in group["nets"]}
    assert nets == {"Sarah": 1200, "Kayla": 0, "Rui": -1200}


@pytest.mark.parametrize("field,invalid", [
    ("totalCents", 3599),               # item totals no longer reconcile
    ("shares", [{"name": "Sarah", "cents": 1000}]),
    ("payments", [{"name": "Sarah", "cents": 3000}]),
    ("payer", "NotInGroup"),
    ("totalCents", -5),
])
def test_invalid_edit_is_atomic(setup, field, invalid):
    db, client = setup
    login(client)
    saved = save_expense(db, original())
    before = copy.deepcopy(list_expenses(db, 1))
    payload = updated()
    payload[field] = invalid
    response = client.put(endpoint(saved["id"]), json=payload)
    assert response.status_code in (400, 422), response.text
    assert list_expenses(db, 1) == before


def test_unauthenticated_edit_is_rejected(setup):
    db, client = setup
    saved = save_expense(db, original())
    response = client.put(endpoint(saved["id"]), json=updated())
    assert response.status_code == 401
    assert list_expenses(db, 1)[0]["totalCents"] == 3000


def test_nonmember_cannot_edit_expense(setup):
    db, client = setup
    saved = save_expense(db, original())
    login(client, "Aly")  # Aly belongs to Weekend trip, not Apartment 4B.
    response = client.put(endpoint(saved["id"]), json=updated())
    assert response.status_code == 403
    assert list_expenses(db, 1)[0]["totalCents"] == 3000


def test_cross_group_edit_is_rejected(setup):
    db, client = setup
    login(client)
    saved = save_expense(db, original())
    response = client.put(endpoint(saved["id"], group_id=2), json=updated())
    assert response.status_code == 404
    assert list_expenses(db, 1)[0]["totalCents"] == 3000


def test_unknown_expense_cannot_be_edited(setup):
    _, client = setup
    login(client)
    assert client.put(endpoint(999999), json=updated()).status_code == 404


def test_edit_legacy_expense_without_fabricated_items(setup):
    db, client = setup
    login(client)
    legacy = original()
    del legacy["lineItems"]
    saved = save_expense(db, legacy)
    correction = updated()
    del correction["lineItems"]
    response = client.put(endpoint(saved["id"]), json=correction)
    assert response.status_code == 200, response.text
    record = list_expenses(db, 1)[0]
    assert record["lineItems"] in (None, [])
    assert record["totalCents"] == 3600
