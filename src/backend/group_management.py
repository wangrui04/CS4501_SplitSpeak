
import sqlite3

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from backend.repository import get_group, list_groups


router = APIRouter()


class CreateGroupRequest(BaseModel):
    name: str
    members: list[str] = Field(default_factory=list)


class AddMemberRequest(BaseModel):
    name: str


def normalize_member(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def create_group(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        "SELECT name FROM groups"
    ).fetchall()

    if any(
        row["name"].casefold() == name.casefold()
        for row in existing
    ):
        raise ValueError("A group with this name already exists")

    cleaned = []
    seen = set()

    for raw in members:
        member = normalize_member(db, raw)
        key = member.casefold()

        if key in seen:
            raise ValueError("Duplicate group member")

        cleaned.append(member)
        seen.add(key)

    if not cleaned:
        raise ValueError("A group requires at least one member")

    try:
        with db:
            cursor = db.execute(
                "INSERT INTO groups (name) VALUES (?)",
                (name,),
            )

            group_id = cursor.lastrowid

            for position, member in enumerate(cleaned):
                db.execute(
                    """
                    INSERT INTO group_members
                    (group_id, name, position)
                    VALUES (?, ?, ?)
                    """,
                    (group_id, member, position),
                )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to create group") from None

    return get_group(db, group_id)


def add_member(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["members"]
    ):
        raise ValueError("Member already belongs to this group")

    if len(group["members"]) >= 50:
        raise ValueError("Group member limit reached")

    try:
        with db:
            db.execute(
                """
                INSERT INTO group_members
                (group_id, name, position)
                VALUES (?, ?, ?)
                """,
                (group_id, member, len(group["members"])),
            )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to add member") from None

    return get_group(db, group_id)


@router.post("/api/groups", status_code=201)
def create_group_endpoint(
    payload: CreateGroupRequest,
    request: Request,
):
    db = request.app.state.db
    current_user = request.session["name"]

    # The creator is automatically a member.
    members = [current_user]

    for name in payload.members:
        if name.strip().casefold() == current_user.casefold():
            continue

        members.append(name)

    try:
        return create_group(db, payload.name, members)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/api/groups/{group_id}/members", status_code=201)
def add_member_endpoint(
    group_id: int,
    payload: AddMemberRequest,
    request: Request,
):
    db = request.app.state.db
    current_user = request.session["name"]

    group = get_group(db, group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found",
        )

    if current_user not in group["members"]:
        raise HTTPException(
            status_code=403,
            detail="Not a member of this group",
        )

    try:
        return add_member(db, group_id, payload.name)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
