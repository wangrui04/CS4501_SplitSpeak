"""Issue #35: "I" / "me" resolves to whoever is signed in."""

import pytest
from fastapi.testclient import TestClient

from backend.database import create_database, seed_database
from backend.llm import FakeLlmClient
from backend.main import create_app
from backend.pipeline import parse_turn


ROSTER = ["Sarah", "Kayla", "Rui"]
SECRET = "test-secret-with-at-least-32-characters"


def item(name, price, mode, names):
    return {
        "name": name,
        "quantity": 1,
        "unitPrice": price,
        "participants": {"mode": mode, "names": names},
    }


def parsed(items, payer="ME", total=None):
    return {
        "description": "Dinner",
        "payer": payer,
        "items": items,
        "charges": [],
        "statedTotal": total,
        "openQuestions": [],
    }


def us01():
    # "I paid $30 for dinner, split evenly."
    return parsed([item("Dinner", "30.00", "all", [])], total="30.00")


def us02():
    # "I paid $24 for groceries for everyone except me."
    return parsed([item("Groceries", "24.00", "all_except", ["ME"])])


def run(raw, current_user):
    return parse_turn(
        llm=FakeLlmClient([raw]),
        conversation=[{"role": "user", "content": "..."}],
        roster=ROSTER,
        current_user=current_user,
    )


def shares(result):
    return {s["name"]: s["cents"] for s in result["preview"]["shares"]}


@pytest.mark.parametrize("user", ROSTER)
def test_me_payer_resolves_to_each_signed_in_user(user):
    result = run(us01(), user)

    assert result["type"] == "preview"
    assert result["preview"]["payer"] == user


def test_us01_as_kayla_shares_unchanged():
    result = run(us01(), "Kayla")

    assert result["preview"]["payer"] == "Kayla"
    assert shares(result) == {"Sarah": 1000, "Kayla": 1000, "Rui": 1000}


def test_us02_as_rui():
    result = run(us02(), "Rui")

    assert result["preview"]["payer"] == "Rui"
    assert shares(result) == {"Sarah": 1200, "Kayla": 1200, "Rui": 0}


@pytest.mark.parametrize("user", ROSTER)
def test_me_participant_resolves_to_each_user(user):
    result = run(
        parsed([item("Nachos", "12.00", "only", ["ME"])], payer="Sarah"),
        user,
    )

    assert shares(result)[user] == 1200


def test_kayla_and_i_as_kayla_asks_instead_of_guessing():
    result = run(
        parsed([item("Nachos", "16.00", "only", ["Kayla", "ME"])]),
        "Kayla",
    )

    assert result["type"] == "question"
    assert "Kayla" in result["question"]


def test_payer_named_and_me_is_fine_when_different_people():
    result = run(
        parsed([item("Nachos", "16.00", "only", ["Kayla", "ME"])]),
        "Sarah",
    )

    assert result["type"] == "preview"


def test_contradictory_case_through_api_never_previews():
    db = create_database(":memory:")
    seed_database(db)
    client = TestClient(create_app(
        db=db,
        session_secret=SECRET,
        llm=FakeLlmClient([
            parsed([item("Nachos", "16.00", "only", ["Kayla", "ME"])]),
        ]),
    ))
    client.post("/api/session", json={"name": "Kayla"})

    body = client.post("/api/chat", json={
        "groupId": 1, "message": "Kayla and I shared nachos for $16",
    }).json()

    assert body["type"] == "question"
    assert "preview" not in body


def test_llm_receives_signed_in_user():
    llm = FakeLlmClient([us01()])

    parse_turn(
        llm=llm,
        conversation=[{"role": "user", "content": "I paid"}],
        roster=ROSTER,
        current_user="Rui",
    )

    assert llm.calls[0]["current_user"] == "Rui"
