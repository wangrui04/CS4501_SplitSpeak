
import pytest
from fastapi.testclient import TestClient

from backend.database import create_database, seed_database
from backend.repository import (
    list_groups,
    get_group,
    save_expense,
    list_expenses,
    create_conversation,
    get_conversation,
    update_conversation,
    delete_conversation,
    add_conversation_message,
    get_conversation_messages,
    confirm_conversation_expense,
    get_group_balances,
)
from backend.main import create_app
from backend.llm import FakeLlmClient


@pytest.fixture
def db():
    connection = create_database(":memory:")
    seed_database(connection)
    yield connection
    connection.close()


@pytest.fixture
def client(db):
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
    )
    with TestClient(app) as test_client:
        yield test_client


def get_apartment(db):
    return next(
        group for group in list_groups(db)
        if group["name"] == "Apartment 4B"
    )


# Issue #8: SQLite database

def test_apartment_roster(db):
    group = get_apartment(db)
    details = get_group(db, group["id"])

    assert details["members"] == [
        "Sarah", "Kayla", "Rui"
    ]


def test_weekend_trip_roster(db):
    group = next(
        group for group in list_groups(db)
        if group["name"] == "Weekend trip"
    )

    details = get_group(db, group["id"])

    assert details["members"] == [
        "Sarah", "Kayla", "Rui", "Aly", "Ben"
    ]


def test_seed_is_idempotent(db):
    before = list_groups(db)

    seed_database(db)
    seed_database(db)

    after = list_groups(db)

    assert len(after) == len(before)
    assert len({g["name"] for g in after}) == len(after)


def valid_saved_expense(group_id):
    return {
        "groupId": group_id,
        "description": "Dinner",
        "payer": "Sarah",
        "totalCents": 3000,
        "source": "manual",
        "createdBy": "Sarah",
        "shares": [
            {"name": "Sarah", "cents": 1000},
            {"name": "Kayla", "cents": 1000},
            {"name": "Rui", "cents": 1000},
        ],
    }


def test_save_expense_persists_shares(db):
    group = get_apartment(db)
    data = valid_saved_expense(group["id"])

    saved = save_expense(db, data)
    expenses = list_expenses(db, group["id"])

    expense = next(
        e for e in expenses if e["id"] == saved["id"]
    )

    assert expense["totalCents"] == 3000
    assert expense["shares"] == data["shares"]


def test_invalid_expense_not_saved(db):
    group = get_apartment(db)
    data = valid_saved_expense(group["id"])
    data["shares"][0]["cents"] = 999

    before = len(list_expenses(db, group["id"]))

    with pytest.raises(ValueError):
        save_expense(db, data)

    after = len(list_expenses(db, group["id"]))
    assert after == before


def test_transaction_rolls_back(db):
    group = get_apartment(db)
    data = valid_saved_expense(group["id"])

    data["shares"][2]["name"] = "Unknown"

    before = len(list_expenses(db, group["id"]))

    with pytest.raises(ValueError):
        save_expense(db, data)

    assert len(list_expenses(db, group["id"])) == before


def test_conversation_crud(db):
    group = get_apartment(db)

    created = create_conversation(db, {
        "groupId": group["id"],
        "userName": "Sarah",
        "promptCount": 1,
        "status": "pending",
    })

    conversation_id = created["id"]
    assert get_conversation(db, conversation_id)

    update_conversation(db, conversation_id, {
        "promptCount": 2,
        "status": "preview",
    })

    updated = get_conversation(db, conversation_id)
    assert updated["promptCount"] == 2
    assert updated["status"] == "preview"

    delete_conversation(db, conversation_id)
    assert get_conversation(db, conversation_id) is None


# Issue #9: Name-based sessions and groups

def test_public_name_picker(client):
    response = client.get("/api/session/names")

    assert response.status_code == 200
    names = str(response.json())

    for name in ["Sarah", "Kayla", "Rui"]:
        assert name in names


def test_valid_name_login(client):
    response = client.post(
        "/api/session", json={"name": "Sarah"}
    )

    assert response.status_code == 200
    assert "set-cookie" in response.headers

    cookie = response.headers["set-cookie"].lower()

    assert "httponly" in cookie
    assert "samesite=lax" in cookie


def test_unknown_name_rejected(client):
    response = client.post(
        "/api/session", json={"name": "Unknown"}
    )
    assert response.status_code == 400


def test_protected_groups_require_login(client):
    response = client.get("/api/groups")
    assert response.status_code == 401



def test_tampered_session_rejected(client):
    # Log in to obtain a valid session cookie.
    response = client.post(
        "/api/session", json={"name": "Sarah"}
    )
    assert response.status_code == 200

    cookie_name = next(iter(client.cookies.keys()))
    original = client.cookies[cookie_name]

    # Remove all existing cookies so the original valid
    # cookie cannot accidentally be sent alongside
    # the tampered cookie.
    client.cookies.clear()

    # Send only the modified session cookie.
    client.cookies.set(
        cookie_name,
        original + "tampered",
    )

    response = client.get("/api/groups")

    assert response.status_code == 401



def test_session_identity_cannot_be_overridden(client):
    client.post("/api/session", json={"name": "Sarah"})

    response = client.get(
        "/api/session",
        params={"user": "Kayla"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Sarah"


def test_groups_available_after_login(client):
    client.post("/api/session", json={"name": "Sarah"})

    response = client.get("/api/groups")

    assert response.status_code == 200
    assert "Apartment 4B" in str(response.json())


def test_logout_invalidates_session(client):
    client.post("/api/session", json={"name": "Sarah"})

    response = client.delete("/api/session")
    assert response.status_code == 200

    response = client.get("/api/session")
    assert response.status_code == 401


@pytest.mark.parametrize("path", [
    "/api/groups",
    "/api/groups/1",
    "/api/conversations/1",
    "/api/chat/1",
])
def test_known_protected_routes(client, path):
    response = client.get(path)
    assert response.status_code == 401


# Issue #13: Chat orchestration endpoint

def make_scripted_expense(price="30.00", payer="Sarah", participants=None):
    if participants is None:
        participants = {"mode": "all", "names": []}
    return {
        "description": "Dinner",
        "payer": payer,
        "items": [{
            "name": "Pizza",
            "quantity": 1,
            "unitPrice": price,
            "participants": participants,
        }],
        "charges": [],
        "statedTotal": price,
        "openQuestions": [],
    }


def test_chat_requires_session(client):
    response = client.post(
        "/api/chat",
        json={"groupId": 1, "message": "I paid $30"},
    )
    assert response.status_code == 401


def test_chat_rejects_non_member(client, db):
    client.post("/api/session", json={"name": "Aly"})
    apartment = get_apartment(db)

    response = client.post(
        "/api/chat",
        json={"groupId": apartment["id"], "message": "I paid $30"},
    )
    assert response.status_code == 403


def test_chat_input_validation(client, db):
    client.post("/api/session", json={"name": "Sarah"})
    apartment = get_apartment(db)

    response = client.post(
        "/api/chat",
        json={"groupId": apartment["id"], "message": "   "},
    )
    assert response.status_code == 400

    response = client.post(
        "/api/chat",
        json={"message": "I paid $30"},
    )
    assert response.status_code == 400

    response = client.post(
        "/api/chat",
        json={"groupId": 9999, "message": "I paid $30"},
    )
    assert response.status_code == 404

    response = client.post(
        "/api/chat",
        json={"conversationId": 9999, "message": "I paid $30"},
    )
    assert response.status_code == 404


def test_chat_starts_conversation_and_returns_preview(db):
    fake = FakeLlmClient([make_scripted_expense("30.00")])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        response = test_client.post(
            "/api/chat",
            json={
                "groupId": apartment["id"],
                "message": "Sarah paid $30 for pizza",
            },
        )

        assert response.status_code == 200
        data = response.json()

        assert data["type"] == "preview"
        assert data["promptCount"] == 1
        assert data["status"] == "preview"
        assert data["preview"]["totalCents"] == 3000
        assert data["preview"]["payer"] == "Sarah"
        assert data["conversationId"] is not None

        conv = get_conversation(db, data["conversationId"])
        assert conv is not None
        assert conv["promptCount"] == 1
        assert conv["status"] == "preview"
        assert conv["finalPreview"]["totalCents"] == 3000
        assert len(conv["messages"]) == 2
        assert conv["messages"][0]["role"] == "user"
        assert conv["messages"][0]["content"] == "Sarah paid $30 for pizza"
        assert conv["messages"][1]["role"] == "assistant"


def test_chat_clarification_turn_and_context_maintenance(db):
    missing_price = make_scripted_expense(price=None)
    full_price = make_scripted_expense(price="30.00")

    fake = FakeLlmClient([missing_price, full_price])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        resp1 = test_client.post(
            "/api/chat",
            json={
                "groupId": apartment["id"],
                "message": "We shared pizza",
            },
        )
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert data1["type"] == "question"
        assert data1["promptCount"] == 1
        assert data1["status"] == "pending"
        conv_id = data1["conversationId"]

        resp2 = test_client.post(
            "/api/chat",
            json={
                "conversationId": conv_id,
                "message": "It was $30.00 and Sarah paid",
            },
        )
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["type"] == "preview"
        assert data2["promptCount"] == 2
        assert data2["status"] == "preview"
        assert data2["preview"]["totalCents"] == 3000

        assert len(fake.calls) == 2
        second_call_messages = fake.calls[1]["messages"]
        assert len(second_call_messages) == 3
        assert second_call_messages[0]["content"] == "We shared pizza"
        assert second_call_messages[1]["role"] == "assistant"
        assert second_call_messages[2]["content"] == "It was $30.00 and Sarah paid"

        conv = get_conversation(db, conv_id)
        assert len(conv["messages"]) == 4
        assert conv["promptCount"] == 2
        assert conv["status"] == "preview"


def test_chat_conversational_correction(db):
    initial_expense = make_scripted_expense("30.00")
    revised_expense = make_scripted_expense("45.00")

    fake = FakeLlmClient([initial_expense, revised_expense])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        resp1 = test_client.post(
            "/api/chat",
            json={
                "groupId": apartment["id"],
                "message": "I paid $30 for pizza",
            },
        )
        data1 = resp1.json()
        assert data1["type"] == "preview"
        assert data1["preview"]["totalCents"] == 3000

        resp2 = test_client.post(
            "/api/chat",
            json={
                "conversationId": data1["conversationId"],
                "message": "Actually the total was $45",
            },
        )
        data2 = resp2.json()
        assert data2["type"] == "preview"
        assert data2["promptCount"] == 2
        assert data2["preview"]["totalCents"] == 4500

        conv = get_conversation(db, data1["conversationId"])
        assert conv["finalPreview"]["totalCents"] == 4500


def test_chat_exceeding_five_prompts_marked_unsuccessful(db):
    questions = [
        make_scripted_expense(price=None)
        for _ in range(5)
    ]
    fake = FakeLlmClient(questions)
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        resp = test_client.post(
            "/api/chat",
            json={"groupId": apartment["id"], "message": "Prompt 1"},
        )
        assert resp.json()["promptCount"] == 1
        conv_id = resp.json()["conversationId"]

        for i in range(2, 6):
            resp = test_client.post(
                "/api/chat",
                json={"conversationId": conv_id, "message": f"Prompt {i}"},
            )
            assert resp.status_code == 200
            assert resp.json()["promptCount"] == i
            assert resp.json()["type"] == "question"
            assert resp.json()["status"] == "pending"

        resp6 = test_client.post(
            "/api/chat",
            json={"conversationId": conv_id, "message": "Prompt 6"},
        )
        assert resp6.status_code == 200
        data6 = resp6.json()

        assert data6["type"] == "unresolved"
        assert data6["status"] == "unsuccessful"
        assert data6["promptCount"] == 6
        assert data6["fallback"] == "manual"
        assert "exceeded" in data6["reason"].lower()

        conv = get_conversation(db, conv_id)
        assert conv["status"] == "unsuccessful"
        assert conv["promptCount"] == 6

        assert len(fake.calls) == 5


def test_chat_unresolved_response_fallback(db):
    fake = FakeLlmClient(["not-a-valid-dict"])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        resp = test_client.post(
            "/api/chat",
            json={"groupId": apartment["id"], "message": "Gibberish"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["type"] == "unresolved"
        assert data["status"] == "unresolved"
        assert data["fallback"] == "manual"


def test_chat_never_saves_unconfirmed_expenses(db):
    fake = FakeLlmClient([make_scripted_expense("30.00")])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        assert len(list_expenses(db, apartment["id"])) == 0

        resp = test_client.post(
            "/api/chat",
            json={
                "groupId": apartment["id"],
                "message": "Sarah paid $30 for pizza",
            },
        )
        assert resp.json()["type"] == "preview"

        assert len(list_expenses(db, apartment["id"])) == 0


def test_conversation_retrieval_endpoints(db):
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        created = create_conversation(
            db,
            {
                "groupId": apartment["id"],
                "userName": "Sarah",
                "promptCount": 1,
                "status": "pending",
            },
        )
        conv_id = created["id"]
        add_conversation_message(db, conv_id, "user", "Hello")
        add_conversation_message(db, conv_id, "assistant", "Hi")

        resp = test_client.get(f"/api/conversations/{conv_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == conv_id
        assert data["userName"] == "Sarah"
        assert len(data["messages"]) == 2

        resp_alias = test_client.get(f"/api/chat/{conv_id}")
        assert resp_alias.status_code == 200
        assert resp_alias.json()["id"] == conv_id

        test_client.post("/api/session", json={"name": "Aly"})
        resp_unauth = test_client.get(f"/api/conversations/{conv_id}")
        assert resp_unauth.status_code == 403


def test_group_chat_alias_endpoint(db):
    fake = FakeLlmClient([make_scripted_expense("25.00")])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        resp = test_client.post(
            f"/api/groups/{apartment['id']}/chat",
            json={"message": "Sarah paid $25 for groceries"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["type"] == "preview"
        assert data["preview"]["totalCents"] == 2500


# =========================================================
# Issue #14: Confirm endpoint and save guardrail
# =========================================================

def make_valid_preview_data(payer="Sarah", total_cents=3000):
    return {
        "payer": payer,
        "currency": "USD",
        "lineItems": [],
        "charges": [],
        "totalCents": total_cents,
        "shares": [
            {"name": "Sarah", "cents": 1000, "summary": "Dinner"},
            {"name": "Kayla", "cents": 1000, "summary": "Dinner"},
            {"name": "Rui", "cents": 1000, "summary": "Dinner"},
        ],
        "validated": True,
    }


def test_confirm_requires_session(client):
    response = client.post("/api/conversations/1/confirm")
    assert response.status_code == 401


def test_confirm_rejects_non_member(client, db):
    apartment = get_apartment(db)
    created = create_conversation(
        db,
        {
            "groupId": apartment["id"],
            "userName": "Sarah",
            "promptCount": 1,
            "status": "preview",
        },
    )
    update_conversation(
        db,
        created["id"],
        {"finalPreview": make_valid_preview_data()},
    )

    client.post("/api/session", json={"name": "Aly"})
    response = client.post(f"/api/conversations/{created['id']}/confirm")
    assert response.status_code == 403


def test_confirm_nonexistent_conversation(client):
    client.post("/api/session", json={"name": "Sarah"})
    response = client.post("/api/conversations/9999/confirm")
    assert response.status_code == 404


def test_valid_confirmation_saves_expense_and_updates_balances(db):
    fake = FakeLlmClient([make_scripted_expense("30.00")])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        initial_balances = get_group_balances(db, apartment["id"])
        assert initial_balances == {"Sarah": 0, "Kayla": 0, "Rui": 0}
        assert len(list_expenses(db, apartment["id"])) == 0

        chat_resp = test_client.post(
            "/api/chat",
            json={
                "groupId": apartment["id"],
                "message": "Sarah paid $30 for pizza for everyone",
            },
        )
        assert chat_resp.status_code == 200
        conv_id = chat_resp.json()["conversationId"]
        assert chat_resp.json()["type"] == "preview"

        assert len(list_expenses(db, apartment["id"])) == 0
        mid_balances = get_group_balances(db, apartment["id"])
        assert mid_balances == {"Sarah": 0, "Kayla": 0, "Rui": 0}

        confirm_resp = test_client.post(f"/api/conversations/{conv_id}/confirm")
        assert confirm_resp.status_code == 200
        confirm_data = confirm_resp.json()
        assert confirm_data["ok"] is True
        assert confirm_data["status"] == "confirmed"
        assert confirm_data["expenseId"] is not None

        expenses = list_expenses(db, apartment["id"])
        assert len(expenses) == 1
        saved_expense = expenses[0]
        assert saved_expense["id"] == confirm_data["expenseId"]
        assert saved_expense["payer"] == "Sarah"
        assert saved_expense["totalCents"] == 3000
        assert saved_expense["shares"] == [
            {"name": "Sarah", "cents": 1000},
            {"name": "Kayla", "cents": 1000},
            {"name": "Rui", "cents": 1000},
        ]

        post_balances = get_group_balances(db, apartment["id"])
        assert post_balances["Sarah"] == 2000
        assert post_balances["Kayla"] == -1000
        assert post_balances["Rui"] == -1000
        assert sum(post_balances.values()) == 0

        conv = get_conversation(db, conv_id)
        assert conv["status"] == "confirmed"


def test_duplicate_confirmation_prevented(db):
    fake = FakeLlmClient([make_scripted_expense("30.00")])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        chat_resp = test_client.post(
            "/api/chat",
            json={
                "groupId": apartment["id"],
                "message": "Sarah paid $30 for pizza",
            },
        )
        conv_id = chat_resp.json()["conversationId"]

        first = test_client.post(f"/api/conversations/{conv_id}/confirm")
        assert first.status_code == 200

        second = test_client.post(f"/api/conversations/{conv_id}/confirm")
        assert second.status_code == 400
        assert "already been confirmed" in second.json()["detail"].lower()

        assert len(list_expenses(db, apartment["id"])) == 1


def test_client_supplied_totals_or_shares_never_trusted(db):
    fake = FakeLlmClient([make_scripted_expense("30.00")])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        chat_resp = test_client.post(
            "/api/chat",
            json={
                "groupId": apartment["id"],
                "message": "Sarah paid $30 for pizza",
            },
        )
        conv_id = chat_resp.json()["conversationId"]

        tampered_body = {
            "totalCents": 1,
            "shares": [{"name": "Sarah", "cents": 1}],
        }
        confirm_resp = test_client.post(
            f"/api/conversations/{conv_id}/confirm",
            json=tampered_body,
        )
        assert confirm_resp.status_code == 200

        expenses = list_expenses(db, apartment["id"])
        assert len(expenses) == 1
        assert expenses[0]["totalCents"] == 3000
        assert expenses[0]["shares"][0]["cents"] == 1000


def test_reject_unresolved_or_pending_drafts(db):
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        pending_conv = create_conversation(
            db,
            {
                "groupId": apartment["id"],
                "userName": "Sarah",
                "promptCount": 1,
                "status": "pending",
            },
        )
        resp1 = test_client.post(f"/api/conversations/{pending_conv['id']}/confirm")
        assert resp1.status_code == 400

        unresolved_conv = create_conversation(
            db,
            {
                "groupId": apartment["id"],
                "userName": "Sarah",
                "promptCount": 1,
                "status": "unresolved",
            },
        )
        resp2 = test_client.post(f"/api/conversations/{unresolved_conv['id']}/confirm")
        assert resp2.status_code == 400

        unsuccessful_conv = create_conversation(
            db,
            {
                "groupId": apartment["id"],
                "userName": "Sarah",
                "promptCount": 6,
                "status": "unsuccessful",
            },
        )
        resp3 = test_client.post(f"/api/conversations/{unsuccessful_conv['id']}/confirm")
        assert resp3.status_code == 400


def test_server_draft_manipulated_total_rejected(db):
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        invalid_preview = {
            "payer": "Sarah",
            "currency": "USD",
            "lineItems": [],
            "charges": [],
            "totalCents": 3000,
            "shares": [
                {"name": "Sarah", "cents": 1500, "summary": "Dinner"},
                {"name": "Kayla", "cents": 1000, "summary": "Dinner"},
            ],
            "validated": True,
        }
        conv = create_conversation(
            db,
            {
                "groupId": apartment["id"],
                "userName": "Sarah",
                "promptCount": 1,
                "status": "preview",
            },
        )
        update_conversation(db, conv["id"], {"finalPreview": invalid_preview})

        resp = test_client.post(f"/api/conversations/{conv['id']}/confirm")
        assert resp.status_code == 400
        assert len(list_expenses(db, apartment["id"])) == 0


def test_confirm_via_body_endpoint(db):
    fake = FakeLlmClient([make_scripted_expense("24.00")])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )
    with TestClient(app) as test_client:
        test_client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)

        chat_resp = test_client.post(
            "/api/chat",
            json={
                "groupId": apartment["id"],
                "message": "Sarah paid $24 for groceries",
            },
        )
        conv_id = chat_resp.json()["conversationId"]

        resp = test_client.post(
            "/api/expenses/confirm",
            json={"conversationId": conv_id},
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] is True
        assert resp.json()["status"] == "confirmed"

        expenses = list_expenses(db, apartment["id"])
        assert len(expenses) == 1
        assert expenses[0]["totalCents"] == 2400


def test_us01_equal_splitting_end_to_end(db):
    """
    US-01: Equal Expense Splitting (Scenario: Dinner for $30.00).
    Input: "I paid $30 for dinner for Sarah, Kayla, and Rui. Split it equally."
    Expected Result:
      Payer: Sarah
      Total: $30.00
      Sarah: $10.00
      Kayla: $10.00
      Rui: $10.00
    Completed within 5 prompts, validated preview, confirmed, and balances updated.
    """
    us01_llm_output = {
        "description": "Dinner",
        "payer": "ME",  # "I paid" resolves to signed-in user Sarah
        "items": [
            {
                "name": "Dinner",
                "unitPrice": "30.00",
                "quantity": 1,
                "participants": {
                    "mode": "only",
                    "names": ["Sarah", "Kayla", "Rui"],
                },
            }
        ],
        "charges": [],
        "statedTotal": "30.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([us01_llm_output])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        # Step 1: Sign in as Sarah
        login_res = client.post("/api/session", json={"name": "Sarah"})
        assert login_res.status_code == 200
        assert login_res.json()["name"] == "Sarah"

        apartment = get_apartment(db)
        group_id = apartment["id"]

        # Initial balances must be zero
        initial_balances = get_group_balances(db, group_id)
        assert initial_balances == {"Sarah": 0, "Kayla": 0, "Rui": 0}
        assert len(list_expenses(db, group_id)) == 0

        # Step 2: Send US-01 prompt via /api/chat
        chat_res = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "message": "I paid $30 for dinner for Sarah, Kayla, and Rui. Split it equally.",
            },
        )
        assert chat_res.status_code == 200
        chat_data = chat_res.json()

        # Step 3: Validate preview response
        assert chat_data["type"] == "preview"
        assert chat_data["status"] == "preview"
        assert chat_data["promptCount"] == 1
        assert chat_data["promptCount"] <= 5

        preview = chat_data["preview"]
        assert preview["payer"] == "Sarah"  # Correct payer identified
        assert preview["totalCents"] == 3000
        assert preview["currency"] == "USD"
        assert preview["validated"] is True

        shares = {s["name"]: s["cents"] for s in preview["shares"]}
        # All participants identified with exact equal split ($10.00 each)
        assert shares == {
            "Sarah": 1000,
            "Kayla": 1000,
            "Rui": 1000,
        }
        assert sum(shares.values()) == 3000

        # Balances must NOT change before confirmation
        unconfirmed_balances = get_group_balances(db, group_id)
        assert unconfirmed_balances == {"Sarah": 0, "Kayla": 0, "Rui": 0}
        assert len(list_expenses(db, group_id)) == 0

        # Step 4: Confirm expense
        conv_id = chat_data["conversationId"]
        confirm_res = client.post(f"/api/conversations/{conv_id}/confirm")
        assert confirm_res.status_code == 200
        confirm_data = confirm_res.json()
        assert confirm_data["ok"] is True
        assert confirm_data["status"] == "confirmed"

        # Step 5: Verify saved database records and shares
        expenses = list_expenses(db, group_id)
        assert len(expenses) == 1
        saved = expenses[0]
        assert saved["id"] == confirm_data["expenseId"]
        assert saved["payer"] == "Sarah"
        assert saved["totalCents"] == 3000
        assert saved["description"] == "Dinner"
        assert saved["shares"] == [
            {"name": "Sarah", "cents": 1000},
            {"name": "Kayla", "cents": 1000},
            {"name": "Rui", "cents": 1000},
        ]

        # Step 6: Verify updated balances
        final_balances = get_group_balances(db, group_id)
        assert final_balances["Sarah"] == 2000   # Sarah paid $30, owes $10 -> net +$20.00
        assert final_balances["Kayla"] == -1000  # Kayla owes $10 -> net -$10.00
        assert final_balances["Rui"] == -1000    # Rui owes $10 -> net -$10.00
        assert sum(final_balances.values()) == 0


def test_us02_selected_member_splitting_end_to_end(db):
    """
    US-02: Splitting an Expense Between Selected Members.
    Scenario: "I paid $24 for groceries, but only Kayla and Rui are sharing them."
    Expected Result:
      Payer: Sarah
      Total: $24.00
      Sarah: $0.00 (nonparticipant receives zero)
      Kayla: $12.00
      Rui: $12.00
    Completed within 5 prompts, validated preview, confirmed, and balances updated.
    """
    us02_llm_output = {
        "description": "Groceries",
        "payer": "ME",  # "I paid" resolves to signed-in user Sarah
        "items": [
            {
                "name": "Groceries",
                "unitPrice": "24.00",
                "quantity": 1,
                "participants": {
                    "mode": "only",
                    "names": ["Kayla", "Rui"],
                },
            }
        ],
        "charges": [],
        "statedTotal": "24.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([us02_llm_output])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        # Step 1: Sign in as Sarah
        login_res = client.post("/api/session", json={"name": "Sarah"})
        assert login_res.status_code == 200
        assert login_res.json()["name"] == "Sarah"

        apartment = get_apartment(db)
        group_id = apartment["id"]

        # Initial balances must be zero
        initial_balances = get_group_balances(db, group_id)
        assert initial_balances == {"Sarah": 0, "Kayla": 0, "Rui": 0}

        # Step 2: Send US-02 prompt via /api/chat
        chat_res = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "message": "I paid $24 for groceries, but only Kayla and Rui are sharing them.",
            },
        )
        assert chat_res.status_code == 200
        chat_data = chat_res.json()

        # Step 3: Validate preview response
        assert chat_data["type"] == "preview"
        assert chat_data["status"] == "preview"
        assert chat_data["promptCount"] == 1
        assert chat_data["promptCount"] <= 5

        preview = chat_data["preview"]
        assert preview["payer"] == "Sarah"  # Correct payer identified
        assert preview["totalCents"] == 2400
        assert preview["currency"] == "USD"
        assert preview["validated"] is True

        shares = {s["name"]: s["cents"] for s in preview["shares"]}
        # Only specified participants charged; nonparticipant Sarah gets $0.00
        assert shares == {
            "Sarah": 0,
            "Kayla": 1200,
            "Rui": 1200,
        }
        assert sum(shares.values()) == 2400

        # Step 4: Confirm expense
        conv_id = chat_data["conversationId"]
        confirm_res = client.post(f"/api/conversations/{conv_id}/confirm")
        assert confirm_res.status_code == 200
        confirm_data = confirm_res.json()
        assert confirm_data["ok"] is True
        assert confirm_data["status"] == "confirmed"

        # Step 5: Verify saved database records and shares
        expenses = list_expenses(db, group_id)
        assert len(expenses) == 1
        saved = expenses[0]
        assert saved["id"] == confirm_data["expenseId"]
        assert saved["payer"] == "Sarah"
        assert saved["totalCents"] == 2400
        assert saved["description"] == "Groceries"
        assert saved["shares"] == [
            {"name": "Sarah", "cents": 0},
            {"name": "Kayla", "cents": 1200},
            {"name": "Rui", "cents": 1200},
        ]

        # Step 6: Verify updated balances
        final_balances = get_group_balances(db, group_id)
        assert final_balances["Sarah"] == 2400   # Sarah paid $24, owes $0 -> net +$24.00
        assert final_balances["Kayla"] == -1200  # Kayla owes $12 -> net -$12.00
        assert final_balances["Rui"] == -1200    # Rui owes $12 -> net -$12.00
        assert sum(final_balances.values()) == 0


def test_us02_exclusion_semantics_end_to_end(db):
    """
    US-02 variation: Participant exclusion mode 'all_except'.
    Scenario: "I paid $24 for groceries for everyone except me."
    """
    us02_exclusion_output = {
        "description": "Groceries",
        "payer": "ME",
        "items": [
            {
                "name": "Groceries",
                "unitPrice": "24.00",
                "quantity": 1,
                "participants": {
                    "mode": "all_except",
                    "names": ["ME"],
                },
            }
        ],
        "charges": [],
        "statedTotal": "24.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([us02_exclusion_output])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)
        group_id = apartment["id"]

        chat_res = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "message": "I paid $24 for groceries for everyone except me.",
            },
        )
        assert chat_res.status_code == 200
        preview = chat_res.json()["preview"]
        shares = {s["name"]: s["cents"] for s in preview["shares"]}
        assert shares == {"Sarah": 0, "Kayla": 1200, "Rui": 1200}


def test_us03_itemized_multi_way_splitting_end_to_end(db):
    """
    US-03: Itemized Splitting With Different Participants.
    Scenario: "I paid $42. Kayla and I shared $12 nachos. Rui had a $15 burger, and Kayla had a $15 pasta."
    Expected Result:
      Payer: Sarah
      Total: $42.00
      Sarah: $6.00 (half of nachos)
      Kayla: $21.00 (half of nachos $6.00 + pasta $15.00)
      Rui: $15.00 (burger)
    Completed within 5 prompts, validated preview, confirmed, and balances updated.
    """
    us03_llm_output = {
        "description": "Dinner",
        "payer": "ME",  # "I paid" resolves to signed-in user Sarah
        "items": [
            {
                "name": "Nachos",
                "unitPrice": "12.00",
                "quantity": 1,
                "participants": {
                    "mode": "only",
                    "names": ["ME", "Kayla"],
                },
            },
            {
                "name": "Burger",
                "unitPrice": "15.00",
                "quantity": 1,
                "participants": {
                    "mode": "only",
                    "names": ["Rui"],
                },
            },
            {
                "name": "Pasta",
                "unitPrice": "15.00",
                "quantity": 1,
                "participants": {
                    "mode": "only",
                    "names": ["Kayla"],
                },
            },
        ],
        "charges": [],
        "statedTotal": "42.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([us03_llm_output])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        # Step 1: Sign in as Sarah
        login_res = client.post("/api/session", json={"name": "Sarah"})
        assert login_res.status_code == 200
        assert login_res.json()["name"] == "Sarah"

        apartment = get_apartment(db)
        group_id = apartment["id"]

        # Initial balances must be zero
        initial_balances = get_group_balances(db, group_id)
        assert initial_balances == {"Sarah": 0, "Kayla": 0, "Rui": 0}

        # Step 2: Send US-03 prompt via /api/chat
        chat_res = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "message": (
                    "I paid $42. Kayla and I shared $12 nachos. "
                    "Rui had a $15 burger, and Kayla had a $15 pasta."
                ),
            },
        )
        assert chat_res.status_code == 200
        chat_data = chat_res.json()

        # Step 3: Validate preview response
        assert chat_data["type"] == "preview"
        assert chat_data["status"] == "preview"
        assert chat_data["promptCount"] == 1
        assert chat_data["promptCount"] <= 5

        preview = chat_data["preview"]
        assert preview["payer"] == "Sarah"  # Correct payer identified
        assert preview["totalCents"] == 4200
        assert preview["currency"] == "USD"
        assert preview["validated"] is True

        # Verify line items
        line_items = {it["name"]: it["totalCents"] for it in preview["lineItems"]}
        assert line_items == {
            "Nachos": 1200,
            "Burger": 1500,
            "Pasta": 1500,
        }

        # Verify itemized shares
        shares = {s["name"]: s["cents"] for s in preview["shares"]}
        assert shares == {
            "Sarah": 600,   # Half of nachos ($6.00)
            "Kayla": 2100,  # Half of nachos ($6.00) + pasta ($15.00)
            "Rui": 1500,    # Burger ($15.00)
        }
        assert sum(shares.values()) == 4200

        # Step 4: Confirm expense
        conv_id = chat_data["conversationId"]
        confirm_res = client.post(f"/api/conversations/{conv_id}/confirm")
        assert confirm_res.status_code == 200
        confirm_data = confirm_res.json()
        assert confirm_data["ok"] is True
        assert confirm_data["status"] == "confirmed"

        # Step 5: Verify saved database records and shares
        expenses = list_expenses(db, group_id)
        assert len(expenses) == 1
        saved = expenses[0]
        assert saved["id"] == confirm_data["expenseId"]
        assert saved["payer"] == "Sarah"
        assert saved["totalCents"] == 4200
        assert saved["description"] == "Dinner"
        assert saved["shares"] == [
            {"name": "Sarah", "cents": 600},
            {"name": "Kayla", "cents": 2100},
            {"name": "Rui", "cents": 1500},
        ]

        # Step 6: Verify updated balances
        final_balances = get_group_balances(db, group_id)
        assert final_balances["Sarah"] == 3600   # Sarah paid $42, owes $6 -> net +$36.00
        assert final_balances["Kayla"] == -2100  # Kayla owes $21 -> net -$21.00
        assert final_balances["Rui"] == -1500    # Rui owes $15 -> net -$15.00
        assert sum(final_balances.values()) == 0


def test_us04_quantities_and_tax_tip_end_to_end(db):
    """
    US-04: Unequal Quantities and Tax/Tip Allocation.
    Scenario: "I paid for dinner. Kayla got two $10 drinks, Rui got one $10 drink,
    and I didn't have anything. The tip was $6. Split the tip proportionally."
    Expected Result:
      Payer: Sarah
      Total: $36.00
      Sarah: $0.00 (nonparticipant receives zero for both items and tip)
      Kayla: $24.00 (two drinks $20.00 + proportional tip $4.00)
      Rui: $12.00 (one drink $10.00 + proportional tip $2.00)
    Completed within 5 prompts, validated preview, confirmed, and balances updated.
    """
    us04_llm_output = {
        "description": "Dinner",
        "payer": "ME",  # "I paid" resolves to signed-in user Sarah
        "items": [
            {
                "name": "Drinks",
                "unitPrice": "10.00",
                "quantity": 2,
                "participants": {
                    "mode": "only",
                    "names": ["Kayla"],
                },
            },
            {
                "name": "Drink",
                "unitPrice": "10.00",
                "quantity": 1,
                "participants": {
                    "mode": "only",
                    "names": ["Rui"],
                },
            },
        ],
        "charges": [
            {
                "kind": "tip",
                "amount": "6.00",
                "percent": None,
                "method": "proportional",
            }
        ],
        "statedTotal": "36.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([us04_llm_output])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        # Step 1: Sign in as Sarah
        login_res = client.post("/api/session", json={"name": "Sarah"})
        assert login_res.status_code == 200
        assert login_res.json()["name"] == "Sarah"

        apartment = get_apartment(db)
        group_id = apartment["id"]

        # Initial balances must be zero
        initial_balances = get_group_balances(db, group_id)
        assert initial_balances == {"Sarah": 0, "Kayla": 0, "Rui": 0}

        # Step 2: Send US-04 prompt via /api/chat
        chat_res = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "message": (
                    "I paid for dinner. Kayla got two $10 drinks, Rui got one $10 drink, "
                    "and I didn't have anything. The tip was $6. Split the tip proportionally."
                ),
            },
        )
        assert chat_res.status_code == 200
        chat_data = chat_res.json()

        # Step 3: Validate preview response
        assert chat_data["type"] == "preview"
        assert chat_data["status"] == "preview"
        assert chat_data["promptCount"] == 1
        assert chat_data["promptCount"] <= 5

        preview = chat_data["preview"]
        assert preview["payer"] == "Sarah"
        assert preview["totalCents"] == 3600
        assert preview["currency"] == "USD"
        assert preview["validated"] is True

        # Verify quantities and charges in preview
        assert len(preview["lineItems"]) == 2
        assert preview["lineItems"][0]["totalCents"] == 2000  # 2 x $10
        assert preview["lineItems"][1]["totalCents"] == 1000  # 1 x $10
        assert len(preview["charges"]) == 1
        assert preview["charges"][0]["kind"] == "tip"
        assert preview["charges"][0]["amountCents"] == 600

        # Verify individual shares
        shares = {s["name"]: s["cents"] for s in preview["shares"]}
        assert shares == {
            "Sarah": 0,    # Sarah didn't have anything -> $0.00
            "Kayla": 2400, # 2000 drinks + 400 proportional tip -> $24.00
            "Rui": 1200,   # 1000 drink + 200 proportional tip -> $12.00
        }
        assert sum(shares.values()) == 3600

        # Step 4: Confirm expense
        conv_id = chat_data["conversationId"]
        confirm_res = client.post(f"/api/conversations/{conv_id}/confirm")
        assert confirm_res.status_code == 200
        confirm_data = confirm_res.json()
        assert confirm_data["ok"] is True
        assert confirm_data["status"] == "confirmed"

        # Step 5: Verify saved database records and shares
        expenses = list_expenses(db, group_id)
        assert len(expenses) == 1
        saved = expenses[0]
        assert saved["id"] == confirm_data["expenseId"]
        assert saved["payer"] == "Sarah"
        assert saved["totalCents"] == 3600
        assert saved["description"] == "Dinner"
        assert saved["shares"] == [
            {"name": "Sarah", "cents": 0},
            {"name": "Kayla", "cents": 2400},
            {"name": "Rui", "cents": 1200},
        ]

        # Step 6: Verify updated balances
        final_balances = get_group_balances(db, group_id)
        assert final_balances["Sarah"] == 3600   # Sarah paid $36, owes $0 -> net +$36.00
        assert final_balances["Kayla"] == -2400  # Kayla owes $24 -> net -$24.00
        assert final_balances["Rui"] == -1200    # Rui owes $12 -> net -$12.00
        assert sum(final_balances.values()) == 0


def test_us05_missing_information_handling_end_to_end(db):
    """
    US-05: Handling Missing and Ambiguous Information.
    Scenario:
      Prompt 1: "Me and Kayla shared nachoes, Rui got two drinks, and I paid."
      AI Question: "How much were the nachos and each drink?"
      Prompt 2: "Nachos were $16 and drinks were $5 each. No tax or tip."
      Expected Result:
        Payer: Sarah
        Total: $26.00
        Sarah: $8.00 (half of nachos)
        Kayla: $8.00 (half of nachos)
        Rui: $10.00 (two drinks)
    Completed within 2 prompts (<= 5), validated preview, confirmed, and balances updated.
    """
    turn1_output = {
        "description": "Dinner",
        "payer": "ME",
        "items": [
            {
                "name": "Nachos",
                "unitPrice": None,
                "quantity": 1,
                "participants": {"mode": "only", "names": ["ME", "Kayla"]},
            },
            {
                "name": "Drinks",
                "unitPrice": None,
                "quantity": 2,
                "participants": {"mode": "only", "names": ["Rui"]},
            },
        ],
        "charges": [],
        "statedTotal": None,
        "openQuestions": [
            {
                "field": "items.unitPrice",
                "question": "How much were the nachos and each drink?",
            }
        ],
    }

    turn2_output = {
        "description": "Dinner",
        "payer": "ME",
        "items": [
            {
                "name": "Nachos",
                "unitPrice": "16.00",
                "quantity": 1,
                "participants": {"mode": "only", "names": ["ME", "Kayla"]},
            },
            {
                "name": "Drinks",
                "unitPrice": "5.00",
                "quantity": 2,
                "participants": {"mode": "only", "names": ["Rui"]},
            },
        ],
        "charges": [],
        "statedTotal": "26.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([turn1_output, turn2_output])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        # Step 1: Sign in as Sarah
        client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)
        group_id = apartment["id"]

        # Step 2: Send Prompt 1 with missing prices
        resp1 = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "message": "Me and Kayla shared nachoes, Rui got two drinks, and I paid.",
            },
        )
        assert resp1.status_code == 200
        data1 = resp1.json()

        # Follow-up question asked rather than inventing values
        assert data1["type"] == "question"
        assert data1["status"] == "pending"
        assert data1["promptCount"] == 1
        assert "nachos" in data1["question"].lower() or "how much" in data1["question"].lower()
        conv_id = data1["conversationId"]
        assert conv_id is not None

        # Verify no expense is created yet
        assert len(list_expenses(db, group_id)) == 0
        assert get_group_balances(db, group_id) == {"Sarah": 0, "Kayla": 0, "Rui": 0}

        # Step 3: Send Prompt 2 supplying the missing prices
        resp2 = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "conversationId": conv_id,
                "message": "Nachos were $16 and drinks were $5 each. No tax or tip.",
            },
        )
        assert resp2.status_code == 200
        data2 = resp2.json()

        assert data2["type"] == "preview"
        assert data2["status"] == "preview"
        assert data2["promptCount"] == 2
        assert data2["promptCount"] <= 5

        preview = data2["preview"]
        assert preview["payer"] == "Sarah"
        assert preview["totalCents"] == 2600
        assert preview["currency"] == "USD"
        assert preview["validated"] is True

        # Verify shares retain original participants and quantities
        shares = {s["name"]: s["cents"] for s in preview["shares"]}
        assert shares == {
            "Sarah": 800,   # Half of nachos ($8.00)
            "Kayla": 800,   # Half of nachos ($8.00)
            "Rui": 1000,    # Two drinks @ $5 = $10.00
        }
        assert sum(shares.values()) == 2600

        # Step 4: Confirm expense
        confirm_res = client.post(f"/api/conversations/{conv_id}/confirm")
        assert confirm_res.status_code == 200
        confirm_data = confirm_res.json()
        assert confirm_data["ok"] is True
        assert confirm_data["status"] == "confirmed"

        # Step 5: Verify saved database records and shares
        expenses = list_expenses(db, group_id)
        assert len(expenses) == 1
        saved = expenses[0]
        assert saved["totalCents"] == 2600
        assert saved["payer"] == "Sarah"
        assert saved["shares"] == [
            {"name": "Sarah", "cents": 800},
            {"name": "Kayla", "cents": 800},
            {"name": "Rui", "cents": 1000},
        ]

        # Step 6: Verify updated balances
        final_balances = get_group_balances(db, group_id)
        assert final_balances["Sarah"] == 1800   # Paid $26, owes $8 -> net +$18.00
        assert final_balances["Kayla"] == -800   # Kayla owes $8 -> net -$8.00
        assert final_balances["Rui"] == -1000    # Rui owes $10 -> net -$10.00
        assert sum(final_balances.values()) == 0


def test_us05_missing_payer_clarification_turn(db):
    """
    US-05 missing payer:
      Turn 1: "Kayla and I shared $20 pizza." (payer missing) -> Asks "Who paid?"
      Turn 2: "Kayla paid." -> Validated preview with payer Kayla.
    """
    turn1 = {
        "description": "Pizza",
        "payer": None,
        "items": [
            {
                "name": "Pizza",
                "unitPrice": "20.00",
                "quantity": 1,
                "participants": {"mode": "only", "names": ["Kayla", "ME"]},
            }
        ],
        "charges": [],
        "statedTotal": "20.00",
        "openQuestions": [],
    }

    turn2 = {
        "description": "Pizza",
        "payer": "Kayla",
        "items": [
            {
                "name": "Pizza",
                "unitPrice": "20.00",
                "quantity": 1,
                "participants": {"mode": "only", "names": ["Kayla", "ME"]},
            }
        ],
        "charges": [],
        "statedTotal": "20.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([turn1, turn2])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)
        group_id = apartment["id"]

        resp1 = client.post(
            "/api/chat",
            json={"groupId": group_id, "message": "Kayla and I shared $20 pizza."},
        )
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert data1["type"] == "question"
        assert "who paid" in data1["question"].lower()

        conv_id = data1["conversationId"]
        resp2 = client.post(
            "/api/chat",
            json={"groupId": group_id, "conversationId": conv_id, "message": "Kayla paid."},
        )
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["type"] == "preview"
        assert data2["preview"]["payer"] == "Kayla"
        assert data2["preview"]["totalCents"] == 2000
        shares = {s["name"]: s["cents"] for s in data2["preview"]["shares"]}
        assert shares == {"Sarah": 1000, "Kayla": 1000, "Rui": 0}


def test_us05_missing_participants_clarification_turn(db):
    """
    US-05 missing participants:
      Turn 1: "Sarah paid $15 for dessert." (participants missing) -> Asks "Who should share dessert?"
      Turn 2: "Sarah, Kayla, and Rui shared it." -> Validated preview with equal shares.
    """
    turn1 = {
        "description": "Dessert",
        "payer": "Sarah",
        "items": [
            {
                "name": "Dessert",
                "unitPrice": "15.00",
                "quantity": 1,
                "participants": {"mode": "only", "names": []},
            }
        ],
        "charges": [],
        "statedTotal": "15.00",
        "openQuestions": [],
    }

    turn2 = {
        "description": "Dessert",
        "payer": "Sarah",
        "items": [
            {
                "name": "Dessert",
                "unitPrice": "15.00",
                "quantity": 1,
                "participants": {"mode": "all", "names": []},
            }
        ],
        "charges": [],
        "statedTotal": "15.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([turn1, turn2])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)
        group_id = apartment["id"]

        resp1 = client.post(
            "/api/chat",
            json={"groupId": group_id, "message": "Sarah paid $15 for dessert."},
        )
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert data1["type"] == "question"
        assert "who should share" in data1["question"].lower()

        conv_id = data1["conversationId"]
        resp2 = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "conversationId": conv_id,
                "message": "Sarah, Kayla, and Rui shared it.",
            },
        )
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["type"] == "preview"
        assert data2["preview"]["totalCents"] == 1500
        shares = {s["name"]: s["cents"] for s in data2["preview"]["shares"]}
        assert shares == {"Sarah": 500, "Kayla": 500, "Rui": 500}


def test_us06_typos_and_unclear_instructions_end_to_end(db):
    """
    ALPHA-25 / US-06: Messy Language, Typos, and Unclear Instructions.
    Scenario:
      Prompt 1: "I paid for dinr. Me and Kayla shared nachoes for $16. Riu got 2 drnks for $5 each. Split the rest evenly."
      Expected AI Behavior:
        - Recognizes "dinr" as dinner.
        - Recognizes "nachoes" as nachos.
        - Recognizes "Riu" as Rui.
        - Recognizes "drnks" as drinks.
        - Identifies that "split the rest evenly" is unclear (no total amount specified).
        - Asks for clarification rather than assuming or inventing values.
      AI Question:
        "I understand that Sarah and Kayla shared $16 nachos, and Rui had two $5 drinks. When you say 'split the rest evenly,' is there another charge to split?"
      Prompt 2:
        "No, that's everything. No tax or tip."
      Expected Result:
        Payer: Sarah
        Total: $26.00
        Sarah: $8.00 (half of nachos)
        Kayla: $8.00 (half of nachos)
        Rui: $10.00 (two drinks @ $5.00)
    Completed within 2 prompts (<= 5), validated preview, confirmed, and balances updated.
    """
    turn1_llm_output = {
        "description": "Dinner",
        "payer": "ME",
        "items": [
            {
                "name": "Nachos",
                "unitPrice": "16.00",
                "quantity": 1,
                "participants": {"mode": "only", "names": ["ME", "Kayla"]},
            },
            {
                "name": "Drinks",
                "unitPrice": "5.00",
                "quantity": 2,
                "participants": {"mode": "only", "names": ["Rui"]},
            },
        ],
        "charges": [],
        "statedTotal": None,
        "openQuestions": [
            {
                "field": "charges",
                "question": (
                    "I understand that Sarah and Kayla shared $16 nachos, "
                    "and Rui had two $5 drinks. When you say 'split the rest evenly,' "
                    "is there another charge to split?"
                ),
            }
        ],
    }

    turn2_llm_output = {
        "description": "Dinner",
        "payer": "ME",
        "items": [
            {
                "name": "Nachos",
                "unitPrice": "16.00",
                "quantity": 1,
                "participants": {"mode": "only", "names": ["ME", "Kayla"]},
            },
            {
                "name": "Drinks",
                "unitPrice": "5.00",
                "quantity": 2,
                "participants": {"mode": "only", "names": ["Rui"]},
            },
        ],
        "charges": [],
        "statedTotal": "26.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([turn1_llm_output, turn2_llm_output])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        # Step 1: Sign in as Sarah
        client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)
        group_id = apartment["id"]

        # Step 2: Send Prompt 1 with typos and unclear "split the rest"
        resp1 = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "message": (
                    "I paid for dinr. Me and Kayla shared nachoes for $16. "
                    "Riu got 2 drnks for $5 each. Split the rest evenly."
                ),
            },
        )
        assert resp1.status_code == 200
        data1 = resp1.json()

        # Follow-up question is asked, not guessing residual amounts
        assert data1["type"] == "question"
        assert data1["status"] == "pending"
        assert data1["promptCount"] == 1
        assert "split the rest" in data1["question"].lower()
        conv_id = data1["conversationId"]
        assert conv_id is not None

        # Verify nothing is saved yet
        assert len(list_expenses(db, group_id)) == 0
        assert get_group_balances(db, group_id) == {"Sarah": 0, "Kayla": 0, "Rui": 0}

        # Step 3: Send Prompt 2 clarifying that there are no other charges
        resp2 = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "conversationId": conv_id,
                "message": "No, that's everything. No tax or tip.",
            },
        )
        assert resp2.status_code == 200
        data2 = resp2.json()

        assert data2["type"] == "preview"
        assert data2["status"] == "preview"
        assert data2["promptCount"] == 2
        assert data2["promptCount"] <= 5

        preview = data2["preview"]
        assert preview["payer"] == "Sarah"
        assert preview["totalCents"] == 2600
        assert preview["currency"] == "USD"
        assert preview["validated"] is True

        # Check line items and quantities
        nachos_item = next(item for item in preview["lineItems"] if "nacho" in item["name"].lower())
        assert nachos_item["totalCents"] == 1600
        assert set(nachos_item["shares"].keys()) == {"Sarah", "Kayla"}
        assert nachos_item["shares"]["Sarah"] == 800
        assert nachos_item["shares"]["Kayla"] == 800

        drinks_item = next(item for item in preview["lineItems"] if "drink" in item["name"].lower())
        assert drinks_item["totalCents"] == 1000
        assert list(drinks_item["shares"].keys()) == ["Rui"]
        assert drinks_item["shares"]["Rui"] == 1000

        # Shares: Sarah $8.00, Kayla $8.00, Rui $10.00
        shares = {s["name"]: s["cents"] for s in preview["shares"]}
        assert shares == {
            "Sarah": 800,
            "Kayla": 800,
            "Rui": 1000,
        }
        assert sum(shares.values()) == 2600

        # Step 4: Confirm expense
        confirm_res = client.post(f"/api/conversations/{conv_id}/confirm")
        assert confirm_res.status_code == 200
        confirm_data = confirm_res.json()
        assert confirm_data["ok"] is True
        assert confirm_data["status"] == "confirmed"

        # Step 5: Verify saved database record
        expenses = list_expenses(db, group_id)
        assert len(expenses) == 1
        saved = expenses[0]
        assert saved["totalCents"] == 2600
        assert saved["payer"] == "Sarah"
        assert saved["shares"] == [
            {"name": "Sarah", "cents": 800},
            {"name": "Kayla", "cents": 800},
            {"name": "Rui", "cents": 1000},
        ]

        # Step 6: Verify updated balances
        final_balances = get_group_balances(db, group_id)
        assert final_balances["Sarah"] == 1800   # Paid $26, owes $8 -> net +$18.00
        assert final_balances["Kayla"] == -800   # Kayla owes $8 -> net -$8.00
        assert final_balances["Rui"] == -1000    # Rui owes $10 -> net -$10.00
        assert sum(final_balances.values()) == 0


def test_us06_ambiguous_participant_name_asks_clarification(db):
    """
    US-06: Avoid guessing ambiguous participant names.
    If a participant name cannot be uniquely identified, trigger a clarification question.
    """
    turn1_llm_output = {
        "description": "Lunch",
        "payer": "ME",
        "items": [
            {
                "name": "Lunch",
                "unitPrice": "20.00",
                "quantity": 1,
                "participants": {"mode": "only", "names": ["ME", "Allie"]},
            }
        ],
        "charges": [],
        "statedTotal": "20.00",
        "openQuestions": [
            {
                "field": "items[0].participants",
                "question": "Unknown member Allie. Which group member did you mean?",
            }
        ],
    }

    turn2_llm_output = {
        "description": "Lunch",
        "payer": "ME",
        "items": [
            {
                "name": "Lunch",
                "unitPrice": "20.00",
                "quantity": 1,
                "participants": {"mode": "only", "names": ["ME", "Kayla"]},
            }
        ],
        "charges": [],
        "statedTotal": "20.00",
        "openQuestions": [],
    }

    fake = FakeLlmClient([turn1_llm_output, turn2_llm_output])
    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=fake,
    )

    with TestClient(app) as client:
        client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)
        group_id = apartment["id"]

        resp1 = client.post(
            "/api/chat",
            json={"groupId": group_id, "message": "I paid $20 for lunch with Allie."},
        )
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert data1["type"] == "question"
        assert "Allie" in data1["question"]

        conv_id = data1["conversationId"]
        resp2 = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "conversationId": conv_id,
                "message": "I meant Kayla.",
            },
        )
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["type"] == "preview"
        assert data2["preview"]["totalCents"] == 2000
        shares = {s["name"]: s["cents"] for s in data2["preview"]["shares"]}
        assert shares == {"Sarah": 1000, "Kayla": 1000, "Rui": 0}


def test_us06_demo_client_interactive(db):
    """
    US-06: Verify DemoLlmClient can execute the US-06 typo scenario end-to-end.
    """
    from backend.llm import DemoLlmClient

    app = create_app(
        db=db,
        session_secret="test-secret-with-at-least-32-characters",
        llm=DemoLlmClient(),
    )

    with TestClient(app) as client:
        client.post("/api/session", json={"name": "Sarah"})
        apartment = get_apartment(db)
        group_id = apartment["id"]

        # Prompt 1
        resp1 = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "message": (
                    "I paid for dinr. Me and Kayla shared nachoes for $16. "
                    "Riu got 2 drnks for $5 each. Split the rest evenly."
                ),
            },
        )
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert data1["type"] == "question"
        assert "split the rest" in data1["question"].lower()

        # Prompt 2
        resp2 = client.post(
            "/api/chat",
            json={
                "groupId": group_id,
                "conversationId": data1["conversationId"],
                "message": "No, that's everything. No tax or tip.",
            },
        )
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["type"] == "preview"
        assert data2["preview"]["totalCents"] == 2600
        shares = {s["name"]: s["cents"] for s in data2["preview"]["shares"]}
        assert shares == {"Sarah": 800, "Kayla": 800, "Rui": 1000}

