"""#46 Settle up: recorded payments and in-app balance reminders.

Team decisions: only the creditor (the person being paid) records a
payment; a reminder can be repeated after 1 hour; the form sends the
outstanding amount it showed, and a stale amount is rejected.
"""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from backend.database import create_database, seed_database
from backend.main import create_app
from backend.repository import list_expenses, save_expense
from backend.settlement import compute_settlement, settlement_entries


SECRET = "settle-up-test-secret-at-least-32-characters"
APARTMENT = 1  # Sarah, Kayla, Rui
START = datetime(2026, 11, 10, 12, 0, tzinfo=timezone.utc)


class Clock:
    def __init__(self):
        self.now = START

    def __call__(self):
        return self.now

    def advance(self, **delta):
        self.now += timedelta(**delta)


@pytest.fixture
def db():
    connection = create_database()
    seed_database(connection)
    yield connection
    connection.close()


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def app(db, clock):
    application = create_app(db, session_secret=SECRET)
    application.state.clock = clock
    return application


def client_as(app, name):
    client = TestClient(app)
    assert client.post("/api/session", json={"name": name}).status_code == 200
    return client


def kayla_owes_sarah(db, cents=3000):
    save_expense(db, {
        "groupId": APARTMENT,
        "description": "Dinner",
        "payer": "Sarah",
        "totalCents": cents,
        "shares": [{"name": "Kayla", "cents": cents}],
        "source": "manual",
        "createdBy": "Sarah",
    })


def save_b4(db):
    # Rui owes Sarah $280.00 and Kayla owes Sarah $115.00.
    save_expense(db, {
        "groupId": APARTMENT,
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
        "source": "manual",
        "createdBy": "Sarah",
    })


def record(client, cents, frm="Kayla", to="Sarah", shown=None):
    return client.post(
        f"/api/groups/{APARTMENT}/settlements",
        json={
            "from": frm,
            "to": to,
            "cents": cents,
            "expectedOutstandingCents": cents if shown is None else shown,
        },
    )


def transfers(client):
    return client.get(f"/api/groups/{APARTMENT}").json()["transfers"]


# --- settlement math (unit) ---

def test_recorded_payment_reduces_the_debt():
    expenses = [{
        "payer": "Sarah",
        "totalCents": 3000,
        "shares": [{"name": "Kayla", "cents": 3000}],
    }]
    paid = [{"from": "Kayla", "to": "Sarah", "cents": 1000}]

    result = compute_settlement(
        expenses + settlement_entries(paid), ["Sarah", "Kayla", "Rui"]
    )

    assert result["transfers"] == [{"from": "Kayla", "to": "Sarah", "cents": 2000}]


def test_full_payment_clears_the_debt():
    expenses = [{
        "payer": "Sarah",
        "totalCents": 3000,
        "shares": [{"name": "Kayla", "cents": 3000}],
    }]
    paid = [
        {"from": "Kayla", "to": "Sarah", "cents": 1000},
        {"from": "Kayla", "to": "Sarah", "cents": 2000},
    ]

    result = compute_settlement(
        expenses + settlement_entries(paid), ["Sarah", "Kayla", "Rui"]
    )

    assert result["transfers"] == []
    assert all(net["netCents"] == 0 for net in result["nets"])


def test_settlement_entries_keep_nets_balanced():
    entries = settlement_entries([{"from": "Rui", "to": "Sarah", "cents": 2801}])

    assert sum(p["cents"] for p in entries[0]["payments"]) == 2801
    assert sum(s["cents"] for s in entries[0]["shares"]) == 2801


# --- recording payments (API) ---

def test_partial_then_remaining_payment(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    assert record(sarah, 1000, shown=3000).status_code == 201
    assert transfers(sarah) == [{"from": "Kayla", "to": "Sarah", "cents": 2000}]

    assert record(sarah, 2000).status_code == 201
    assert transfers(sarah) == []


def test_payment_updates_summary_and_balances(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    record(sarah, 1000, shown=3000)
    group = sarah.get(f"/api/groups/{APARTMENT}").json()

    assert group["summary"]["youAreOwed"] == 2000
    kayla = next(b for b in group["balances"] if b["name"] == "Kayla")
    assert kayla["cents"] == 2000


def test_payment_survives_and_expenses_untouched(app, db):
    kayla_owes_sarah(db)
    before = list_expenses(db, APARTMENT)
    sarah = client_as(app, "Sarah")

    record(sarah, 3000)

    assert list_expenses(db, APARTMENT) == before
    history = client_as(app, "Kayla").get(f"/api/groups/{APARTMENT}/settlements")
    assert history.status_code == 200
    [entry] = history.json()
    assert entry["from"] == "Kayla"
    assert entry["to"] == "Sarah"
    assert entry["cents"] == 3000
    assert entry["recordedBy"] == "Sarah"
    assert entry["recordedAt"]
    assert entry["id"]


def test_balances_endpoint_includes_payments(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    record(sarah, 1000, shown=3000)

    balances = sarah.get(f"/api/groups/{APARTMENT}/balances").json()
    assert balances == {"Sarah": 2000, "Kayla": -2000, "Rui": 0}


def test_only_the_creditor_can_record(app, db):
    kayla_owes_sarah(db)

    for name in ["Kayla", "Rui"]:
        response = record(client_as(app, name), 1000, shown=3000)
        assert response.status_code == 403

    assert transfers(client_as(app, "Sarah")) == [
        {"from": "Kayla", "to": "Sarah", "cents": 3000}
    ]


def test_requires_sign_in(app, db):
    kayla_owes_sarah(db)

    assert record(TestClient(app), 1000, shown=3000).status_code == 401


def test_non_member_rejected(app, db):
    kayla_owes_sarah(db)
    outsider = client_as(app, "Aly")  # only in Weekend trip

    assert record(outsider, 1000, frm="Kayla", to="Aly", shown=3000).status_code == 403
    assert outsider.get(f"/api/groups/{APARTMENT}/settlements").status_code == 403


@pytest.mark.parametrize("cents", [0, -500, 10.5, "1000", True, None])
def test_invalid_amounts_rejected(app, db, cents):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    response = record(sarah, cents, shown=3000)

    assert response.status_code in (400, 422)
    assert transfers(sarah) == [{"from": "Kayla", "to": "Sarah", "cents": 3000}]


def test_overpayment_rejected(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    response = record(sarah, 3001, shown=3000)

    assert response.status_code == 400
    assert transfers(sarah) == [{"from": "Kayla", "to": "Sarah", "cents": 3000}]


def test_no_outstanding_transfer_rejected(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    # Rui owes Sarah nothing, and the form shows that. (A form that
    # still showed an old amount gets 409; see the stale tests.)
    assert record(sarah, 500, frm="Rui", shown=0).status_code == 400


def test_payer_must_differ_from_recipient(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    assert record(sarah, 500, frm="Sarah", shown=500).status_code == 400


def test_unknown_member_rejected(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    assert record(sarah, 500, frm="Allie", shown=500).status_code == 400


def test_stale_amount_rejected(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    # The form showed $30, but $10 was recorded in another tab.
    record(sarah, 1000, shown=3000)
    response = record(sarah, 1000, shown=3000)

    assert response.status_code == 409
    assert transfers(sarah) == [{"from": "Kayla", "to": "Sarah", "cents": 2000}]


def test_double_submit_of_full_payment_records_once(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    first = record(sarah, 3000)
    second = record(sarah, 3000)

    assert first.status_code == 201
    assert second.status_code == 409
    assert len(sarah.get(f"/api/groups/{APARTMENT}/settlements").json()) == 1


def test_multi_party_records_against_displayed_transfer(app, db):
    save_b4(db)
    sarah = client_as(app, "Sarah")

    record(sarah, 28000, frm="Rui")

    assert transfers(sarah) == [{"from": "Kayla", "to": "Sarah", "cents": 11500}]


# --- reminders ---

def remind(client, to="Kayla"):
    return client.post(f"/api/groups/{APARTMENT}/reminders", json={"to": to})


def test_reminder_delivered_with_live_amount(app, db):
    kayla_owes_sarah(db, 1200)
    sarah = client_as(app, "Sarah")

    response = remind(sarah)

    assert response.status_code == 201
    inbox = client_as(app, "Kayla").get("/api/notifications").json()
    [note] = inbox
    assert note["from"] == "Sarah"
    assert note["to"] == "Kayla"
    assert note["groupId"] == APARTMENT
    assert note["cents"] == 1200
    assert note["message"] == (
        "Hi Kayla, just a reminder that you still owe Sarah $12.00 "
        "for Apartment 4B. Thanks!"
    )
    assert note["readAt"] is None
    assert note["createdAt"]


def test_reminder_only_visible_to_recipient(app, db):
    kayla_owes_sarah(db)
    remind(client_as(app, "Sarah"))

    assert client_as(app, "Rui").get("/api/notifications").json() == []
    assert client_as(app, "Sarah").get("/api/notifications").json() == []


def test_reminder_uses_balance_after_partial_payment(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    record(sarah, 1000, shown=3000)
    remind(sarah)

    [note] = client_as(app, "Kayla").get("/api/notifications").json()
    assert note["cents"] == 2000
    assert "$20.00" in note["message"]


@pytest.mark.parametrize("sender, recipient", [
    ("Sarah", "Rui"),    # Rui owes Sarah nothing
    ("Kayla", "Sarah"),  # Kayla owes Sarah, not the other way round
    ("Sarah", "Sarah"),
    ("Sarah", "Allie"),
])
def test_reminder_rejected_unless_recipient_owes_sender(app, db, sender, recipient):
    kayla_owes_sarah(db)

    response = remind(client_as(app, sender), to=recipient)

    assert response.status_code == 400
    assert client_as(app, "Kayla").get("/api/notifications").json() == []


def test_no_reminder_after_debt_is_paid(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    record(sarah, 3000)

    assert remind(sarah).status_code == 400


def test_reminder_cooldown_is_one_hour(app, db, clock):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")

    assert remind(sarah).status_code == 201

    clock.advance(minutes=59)
    assert remind(sarah).status_code == 429

    clock.advance(minutes=1)
    assert remind(sarah).status_code == 201

    assert len(client_as(app, "Kayla").get("/api/notifications").json()) == 2


def test_reminder_does_not_change_balances(app, db):
    kayla_owes_sarah(db)
    sarah = client_as(app, "Sarah")
    before = sarah.get(f"/api/groups/{APARTMENT}").json()

    remind(sarah)

    after = sarah.get(f"/api/groups/{APARTMENT}").json()
    assert after["transfers"] == before["transfers"]
    assert after["summary"] == before["summary"]


def test_reminders_require_sign_in_and_membership(app, db):
    kayla_owes_sarah(db)

    assert remind(TestClient(app)).status_code == 401
    assert remind(client_as(app, "Aly")).status_code == 403
    assert TestClient(app).get("/api/notifications").status_code == 401


def test_recipient_can_mark_reminder_read(app, db, clock):
    kayla_owes_sarah(db)
    remind(client_as(app, "Sarah"))
    kayla = client_as(app, "Kayla")
    [note] = kayla.get("/api/notifications").json()

    clock.advance(minutes=5)
    response = kayla.post(f"/api/notifications/{note['id']}/read")

    assert response.status_code == 200
    [note] = kayla.get("/api/notifications").json()
    assert note["readAt"] == (START + timedelta(minutes=5)).isoformat()


def test_only_recipient_can_mark_read(app, db):
    kayla_owes_sarah(db)
    remind(client_as(app, "Sarah"))
    [note] = client_as(app, "Kayla").get("/api/notifications").json()

    for name in ["Sarah", "Rui"]:
        response = client_as(app, name).post(f"/api/notifications/{note['id']}/read")
        assert response.status_code == 404

    [note] = client_as(app, "Kayla").get("/api/notifications").json()
    assert note["readAt"] is None
