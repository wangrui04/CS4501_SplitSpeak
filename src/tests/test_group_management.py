
import pytest
from fastapi.testclient import TestClient

from backend.database import create_database, seed_database
from backend.main import create_app
from backend.repository import get_group


@pytest.fixture
def db():
    connection = create_database()
    seed_database(connection)

    yield connection

    connection.close()


@pytest.fixture
def client(db):
    app = create_app(
        db,
        session_secret=(
            "group-management-test-secret-at-least-32-chars"
        ),
    )

    with TestClient(app) as test_client:
        yield test_client


def sign_in(client, name="Sarah"):
    response = client.post(
        "/api/session",
        json={"name": name},
    )

    assert response.status_code == 200


def test_create_group_requires_login(client):
    response = client.post(
        "/api/groups",
        json={
            "name": "Boston Trip",
            "members": ["Anna"],
        },
    )

    assert response.status_code == 401


def test_create_group_includes_current_user(client):
    sign_in(client)

    response = client.post(
        "/api/groups",
        json={
            "name": "Boston Trip",
            "members": ["Anna", "Ben", "Cara"],
        },
    )

    assert response.status_code == 201

    group = response.json()

    assert group["name"] == "Boston Trip"
    assert group["members"] == [
        "Sarah",
        "Anna",
        "Ben",
        "Cara",
    ]


def test_created_group_is_persisted(client, db):
    sign_in(client)

    response = client.post(
        "/api/groups",
        json={"name": "Study Group"},
    )

    assert response.status_code == 201

    group_id = response.json()["id"]
    stored = get_group(db, group_id)

    assert stored["name"] == "Study Group"
    assert stored["members"] == ["Sarah"]


def test_duplicate_group_name_rejected(client):
    sign_in(client)

    first = client.post(
        "/api/groups",
        json={"name": "Boston Trip"},
    )

    second = client.post(
        "/api/groups",
        json={"name": "boston trip"},
    )

    assert first.status_code == 201
    assert second.status_code == 400


def test_add_member_to_existing_group(client):
    sign_in(client)

    response = client.post(
        "/api/groups/1/members",
        json={"name": "Anna"},
    )

    assert response.status_code == 201
    assert "Anna" in response.json()["members"]

    group = client.get("/api/groups/1").json()

    assert "Anna" in group["members"]


def test_duplicate_member_rejected(client):
    sign_in(client)

    response = client.post(
        "/api/groups/1/members",
        json={"name": "Kayla"},
    )

    assert response.status_code == 400


def test_non_member_cannot_modify_group(client):
    sign_in(client, "Aly")

    response = client.post(
        "/api/groups/1/members",
        json={"name": "Anna"},
    )

    assert response.status_code == 403


def test_new_member_can_sign_in(client):
    sign_in(client)

    response = client.post(
        "/api/groups/1/members",
        json={"name": "Anna"},
    )

    assert response.status_code == 201

    names = client.get(
        "/api/session/names"
    ).json()

    assert "Anna" in names

    client.delete("/api/session")
    sign_in(client, "Anna")

    groups = client.get("/api/groups").json()

    assert any(
        group["name"] == "Apartment 4B"
        for group in groups
    )


def test_groups_are_filtered_by_membership(client):
    sign_in(client, "Sarah")

    response = client.post(
        "/api/groups",
        json={"name": "Sarah's Group"},
    )

    assert response.status_code == 201

    client.delete("/api/session")
    sign_in(client, "Aly")

    groups = client.get("/api/groups").json()

    names = [group["name"] for group in groups]

    assert "Sarah's Group" not in names
    assert "Weekend trip" in names


def test_invalid_group_name_rejected(client):
    sign_in(client)

    response = client.post(
        "/api/groups",
        json={"name": "   "},
    )

    assert response.status_code == 400


def test_duplicate_initial_members_rejected(client):
    sign_in(client)

    response = client.post(
        "/api/groups",
        json={
            "name": "Duplicates",
            "members": ["Anna", "anna"],
        },
    )

    assert response.status_code == 400


def test_added_member_can_access_expense_options(client):
    sign_in(client)

    response = client.post(
        "/api/groups/1/members",
        json={"name": "Cara"},
    )

    assert response.status_code == 201

    group = client.get("/api/groups/1").json()

    assert "Cara" in group["members"]


def test_group_with_no_optional_members(client):
    sign_in(client)

    response = client.post(
        "/api/groups",
        json={"name": "Solo Expenses", "members": []},
    )

    assert response.status_code == 201
    assert response.json()["members"] == ["Sarah"]


def test_missing_group_returns_404(client):
    sign_in(client)

    response = client.post(
        "/api/groups/99999/members",
        json={"name": "Anna"},
    )

    assert response.status_code == 404
