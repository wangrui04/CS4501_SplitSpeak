
import sqlite3

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from backend.repository import get_group, list_groups


router = APIRouter()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class CreateGroupRequest(BaseModel):
    name: str
    members: list[str] = Field(default_factory=list)


class AddMemberRequest(BaseModel):
    name: str
mutants_x_normalize_member__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_normalize_member__mutmut)
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


def x_normalize_member__mutmut_orig(db, name):
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


def x_normalize_member__mutmut_1(db, name):
    if isinstance(name, str):
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


def x_normalize_member__mutmut_2(db, name):
    if not isinstance(name, str):
        raise ValueError(None)

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


def x_normalize_member__mutmut_3(db, name):
    if not isinstance(name, str):
        raise ValueError("XXMember name must be a stringXX")

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


def x_normalize_member__mutmut_4(db, name):
    if not isinstance(name, str):
        raise ValueError("member name must be a string")

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


def x_normalize_member__mutmut_5(db, name):
    if not isinstance(name, str):
        raise ValueError("MEMBER NAME MUST BE A STRING")

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


def x_normalize_member__mutmut_6(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = None

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


def x_normalize_member__mutmut_7(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name and len(name) > 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_8(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if name or len(name) > 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_9(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) >= 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_10(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 81:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_11(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError(None)

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_12(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("XXMember name must be 1-80 charactersXX")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_13(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_14(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("MEMBER NAME MUST BE 1-80 CHARACTERS")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT name FROM group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_15(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = None

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_16(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        None
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_17(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "XXSELECT DISTINCT name FROM group_membersXX"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_18(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "select distinct name from group_members"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_19(db, name):
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")

    name = name.strip()

    if not name or len(name) > 80:
        raise ValueError("Member name must be 1-80 characters")

    # Preserve spelling of existing demo profiles.
    rows = db.execute(
        "SELECT DISTINCT NAME FROM GROUP_MEMBERS"
    ).fetchall()

    for row in rows:
        if row["name"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_20(db, name):
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
        if row["XXnameXX"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_21(db, name):
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
        if row["NAME"].casefold() == name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_22(db, name):
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
        if row["name"].casefold() != name.casefold():
            return row["name"]

    return name


def x_normalize_member__mutmut_23(db, name):
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
            return row["XXnameXX"]

    return name


def x_normalize_member__mutmut_24(db, name):
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
            return row["NAME"]

    return name

mutants_x_normalize_member__mutmut['_mutmut_orig'] = x_normalize_member__mutmut_orig # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_1'] = x_normalize_member__mutmut_1 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_2'] = x_normalize_member__mutmut_2 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_3'] = x_normalize_member__mutmut_3 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_4'] = x_normalize_member__mutmut_4 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_5'] = x_normalize_member__mutmut_5 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_6'] = x_normalize_member__mutmut_6 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_7'] = x_normalize_member__mutmut_7 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_8'] = x_normalize_member__mutmut_8 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_9'] = x_normalize_member__mutmut_9 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_10'] = x_normalize_member__mutmut_10 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_11'] = x_normalize_member__mutmut_11 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_12'] = x_normalize_member__mutmut_12 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_13'] = x_normalize_member__mutmut_13 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_14'] = x_normalize_member__mutmut_14 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_15'] = x_normalize_member__mutmut_15 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_16'] = x_normalize_member__mutmut_16 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_17'] = x_normalize_member__mutmut_17 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_18'] = x_normalize_member__mutmut_18 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_19'] = x_normalize_member__mutmut_19 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_20'] = x_normalize_member__mutmut_20 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_21'] = x_normalize_member__mutmut_21 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_22'] = x_normalize_member__mutmut_22 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_23'] = x_normalize_member__mutmut_23 # type: ignore # mutmut generated
mutants_x_normalize_member__mutmut['x_normalize_member__mutmut_24'] = x_normalize_member__mutmut_24 # type: ignore # mutmut generated
mutants_x_create_group__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_create_group__mutmut)
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


def x_create_group__mutmut_orig(db, name, members):
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


def x_create_group__mutmut_1(db, name, members):
    name = None

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


def x_create_group__mutmut_2(db, name, members):
    name = name.strip()

    if not name and len(name) > 100:
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


def x_create_group__mutmut_3(db, name, members):
    name = name.strip()

    if name or len(name) > 100:
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


def x_create_group__mutmut_4(db, name, members):
    name = name.strip()

    if not name or len(name) >= 100:
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


def x_create_group__mutmut_5(db, name, members):
    name = name.strip()

    if not name or len(name) > 101:
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


def x_create_group__mutmut_6(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError(None)

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


def x_create_group__mutmut_7(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("XXGroup name must be 1-100 charactersXX")

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


def x_create_group__mutmut_8(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("group name must be 1-100 characters")

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


def x_create_group__mutmut_9(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("GROUP NAME MUST BE 1-100 CHARACTERS")

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


def x_create_group__mutmut_10(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) >= 50:
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


def x_create_group__mutmut_11(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 51:
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


def x_create_group__mutmut_12(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError(None)

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


def x_create_group__mutmut_13(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("XXToo many membersXX")

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


def x_create_group__mutmut_14(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("too many members")

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


def x_create_group__mutmut_15(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("TOO MANY MEMBERS")

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


def x_create_group__mutmut_16(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = None

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


def x_create_group__mutmut_17(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        None
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


def x_create_group__mutmut_18(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        "XXSELECT name FROM groupsXX"
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


def x_create_group__mutmut_19(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        "select name from groups"
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


def x_create_group__mutmut_20(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        "SELECT NAME FROM GROUPS"
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


def x_create_group__mutmut_21(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        "SELECT name FROM groups"
    ).fetchall()

    if any(
        None
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


def x_create_group__mutmut_22(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        "SELECT name FROM groups"
    ).fetchall()

    if any(
        row["XXnameXX"].casefold() == name.casefold()
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


def x_create_group__mutmut_23(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        "SELECT name FROM groups"
    ).fetchall()

    if any(
        row["NAME"].casefold() == name.casefold()
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


def x_create_group__mutmut_24(db, name, members):
    name = name.strip()

    if not name or len(name) > 100:
        raise ValueError("Group name must be 1-100 characters")

    if len(members) > 50:
        raise ValueError("Too many members")

    existing = db.execute(
        "SELECT name FROM groups"
    ).fetchall()

    if any(
        row["name"].casefold() != name.casefold()
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


def x_create_group__mutmut_25(db, name, members):
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
        raise ValueError(None)

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


def x_create_group__mutmut_26(db, name, members):
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
        raise ValueError("XXA group with this name already existsXX")

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


def x_create_group__mutmut_27(db, name, members):
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
        raise ValueError("a group with this name already exists")

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


def x_create_group__mutmut_28(db, name, members):
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
        raise ValueError("A GROUP WITH THIS NAME ALREADY EXISTS")

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


def x_create_group__mutmut_29(db, name, members):
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

    cleaned = None
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


def x_create_group__mutmut_30(db, name, members):
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
    seen = None

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


def x_create_group__mutmut_31(db, name, members):
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
        member = None
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


def x_create_group__mutmut_32(db, name, members):
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
        member = normalize_member(None, raw)
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


def x_create_group__mutmut_33(db, name, members):
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
        member = normalize_member(db, None)
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


def x_create_group__mutmut_34(db, name, members):
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
        member = normalize_member(raw)
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


def x_create_group__mutmut_35(db, name, members):
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
        member = normalize_member(db, )
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


def x_create_group__mutmut_36(db, name, members):
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
        key = None

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


def x_create_group__mutmut_37(db, name, members):
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

        if key not in seen:
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


def x_create_group__mutmut_38(db, name, members):
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
            raise ValueError(None)

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


def x_create_group__mutmut_39(db, name, members):
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
            raise ValueError("XXDuplicate group memberXX")

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


def x_create_group__mutmut_40(db, name, members):
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
            raise ValueError("duplicate group member")

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


def x_create_group__mutmut_41(db, name, members):
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
            raise ValueError("DUPLICATE GROUP MEMBER")

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


def x_create_group__mutmut_42(db, name, members):
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

        cleaned.append(None)
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


def x_create_group__mutmut_43(db, name, members):
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
        seen.add(None)

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


def x_create_group__mutmut_44(db, name, members):
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

    if cleaned:
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


def x_create_group__mutmut_45(db, name, members):
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
        raise ValueError(None)

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


def x_create_group__mutmut_46(db, name, members):
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
        raise ValueError("XXA group requires at least one memberXX")

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


def x_create_group__mutmut_47(db, name, members):
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
        raise ValueError("a group requires at least one member")

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


def x_create_group__mutmut_48(db, name, members):
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
        raise ValueError("A GROUP REQUIRES AT LEAST ONE MEMBER")

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


def x_create_group__mutmut_49(db, name, members):
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
            cursor = None

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


def x_create_group__mutmut_50(db, name, members):
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
                None,
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


def x_create_group__mutmut_51(db, name, members):
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
                None,
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


def x_create_group__mutmut_52(db, name, members):
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


def x_create_group__mutmut_53(db, name, members):
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


def x_create_group__mutmut_54(db, name, members):
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
                "XXINSERT INTO groups (name) VALUES (?)XX",
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


def x_create_group__mutmut_55(db, name, members):
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
                "insert into groups (name) values (?)",
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


def x_create_group__mutmut_56(db, name, members):
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
                "INSERT INTO GROUPS (NAME) VALUES (?)",
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


def x_create_group__mutmut_57(db, name, members):
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

            group_id = None

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


def x_create_group__mutmut_58(db, name, members):
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

            for position, member in enumerate(None):
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


def x_create_group__mutmut_59(db, name, members):
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
                    None,
                    (group_id, member, position),
                )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to create group") from None

    return get_group(db, group_id)


def x_create_group__mutmut_60(db, name, members):
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
                    None,
                )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to create group") from None

    return get_group(db, group_id)


def x_create_group__mutmut_61(db, name, members):
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
                    (group_id, member, position),
                )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to create group") from None

    return get_group(db, group_id)


def x_create_group__mutmut_62(db, name, members):
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
                    )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to create group") from None

    return get_group(db, group_id)


def x_create_group__mutmut_63(db, name, members):
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
        raise ValueError(None) from None

    return get_group(db, group_id)


def x_create_group__mutmut_64(db, name, members):
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
        raise ValueError("XXUnable to create groupXX") from None

    return get_group(db, group_id)


def x_create_group__mutmut_65(db, name, members):
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
        raise ValueError("unable to create group") from None

    return get_group(db, group_id)


def x_create_group__mutmut_66(db, name, members):
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
        raise ValueError("UNABLE TO CREATE GROUP") from None

    return get_group(db, group_id)


def x_create_group__mutmut_67(db, name, members):
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

    return get_group(None, group_id)


def x_create_group__mutmut_68(db, name, members):
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

    return get_group(db, None)


def x_create_group__mutmut_69(db, name, members):
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

    return get_group(group_id)


def x_create_group__mutmut_70(db, name, members):
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

    return get_group(db, )

mutants_x_create_group__mutmut['_mutmut_orig'] = x_create_group__mutmut_orig # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_1'] = x_create_group__mutmut_1 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_2'] = x_create_group__mutmut_2 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_3'] = x_create_group__mutmut_3 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_4'] = x_create_group__mutmut_4 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_5'] = x_create_group__mutmut_5 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_6'] = x_create_group__mutmut_6 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_7'] = x_create_group__mutmut_7 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_8'] = x_create_group__mutmut_8 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_9'] = x_create_group__mutmut_9 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_10'] = x_create_group__mutmut_10 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_11'] = x_create_group__mutmut_11 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_12'] = x_create_group__mutmut_12 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_13'] = x_create_group__mutmut_13 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_14'] = x_create_group__mutmut_14 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_15'] = x_create_group__mutmut_15 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_16'] = x_create_group__mutmut_16 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_17'] = x_create_group__mutmut_17 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_18'] = x_create_group__mutmut_18 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_19'] = x_create_group__mutmut_19 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_20'] = x_create_group__mutmut_20 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_21'] = x_create_group__mutmut_21 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_22'] = x_create_group__mutmut_22 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_23'] = x_create_group__mutmut_23 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_24'] = x_create_group__mutmut_24 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_25'] = x_create_group__mutmut_25 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_26'] = x_create_group__mutmut_26 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_27'] = x_create_group__mutmut_27 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_28'] = x_create_group__mutmut_28 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_29'] = x_create_group__mutmut_29 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_30'] = x_create_group__mutmut_30 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_31'] = x_create_group__mutmut_31 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_32'] = x_create_group__mutmut_32 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_33'] = x_create_group__mutmut_33 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_34'] = x_create_group__mutmut_34 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_35'] = x_create_group__mutmut_35 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_36'] = x_create_group__mutmut_36 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_37'] = x_create_group__mutmut_37 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_38'] = x_create_group__mutmut_38 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_39'] = x_create_group__mutmut_39 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_40'] = x_create_group__mutmut_40 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_41'] = x_create_group__mutmut_41 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_42'] = x_create_group__mutmut_42 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_43'] = x_create_group__mutmut_43 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_44'] = x_create_group__mutmut_44 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_45'] = x_create_group__mutmut_45 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_46'] = x_create_group__mutmut_46 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_47'] = x_create_group__mutmut_47 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_48'] = x_create_group__mutmut_48 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_49'] = x_create_group__mutmut_49 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_50'] = x_create_group__mutmut_50 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_51'] = x_create_group__mutmut_51 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_52'] = x_create_group__mutmut_52 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_53'] = x_create_group__mutmut_53 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_54'] = x_create_group__mutmut_54 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_55'] = x_create_group__mutmut_55 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_56'] = x_create_group__mutmut_56 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_57'] = x_create_group__mutmut_57 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_58'] = x_create_group__mutmut_58 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_59'] = x_create_group__mutmut_59 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_60'] = x_create_group__mutmut_60 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_61'] = x_create_group__mutmut_61 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_62'] = x_create_group__mutmut_62 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_63'] = x_create_group__mutmut_63 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_64'] = x_create_group__mutmut_64 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_65'] = x_create_group__mutmut_65 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_66'] = x_create_group__mutmut_66 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_67'] = x_create_group__mutmut_67 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_68'] = x_create_group__mutmut_68 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_69'] = x_create_group__mutmut_69 # type: ignore # mutmut generated
mutants_x_create_group__mutmut['x_create_group__mutmut_70'] = x_create_group__mutmut_70 # type: ignore # mutmut generated
mutants_x_add_member__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_add_member__mutmut)
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


def x_add_member__mutmut_orig(db, group_id, name):
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


def x_add_member__mutmut_1(db, group_id, name):
    group = None

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


def x_add_member__mutmut_2(db, group_id, name):
    group = get_group(None, group_id)

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


def x_add_member__mutmut_3(db, group_id, name):
    group = get_group(db, None)

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


def x_add_member__mutmut_4(db, group_id, name):
    group = get_group(group_id)

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


def x_add_member__mutmut_5(db, group_id, name):
    group = get_group(db, )

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


def x_add_member__mutmut_6(db, group_id, name):
    group = get_group(db, group_id)

    if group is not None:
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


def x_add_member__mutmut_7(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError(None)

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


def x_add_member__mutmut_8(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("XXGroup not foundXX")

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


def x_add_member__mutmut_9(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("group not found")

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


def x_add_member__mutmut_10(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("GROUP NOT FOUND")

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


def x_add_member__mutmut_11(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = None

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


def x_add_member__mutmut_12(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(None, name)

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


def x_add_member__mutmut_13(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, None)

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


def x_add_member__mutmut_14(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(name)

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


def x_add_member__mutmut_15(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, )

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


def x_add_member__mutmut_16(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        None
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


def x_add_member__mutmut_17(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() != member.casefold()
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


def x_add_member__mutmut_18(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["XXmembersXX"]
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


def x_add_member__mutmut_19(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["MEMBERS"]
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


def x_add_member__mutmut_20(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["members"]
    ):
        raise ValueError(None)

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


def x_add_member__mutmut_21(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["members"]
    ):
        raise ValueError("XXMember already belongs to this groupXX")

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


def x_add_member__mutmut_22(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["members"]
    ):
        raise ValueError("member already belongs to this group")

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


def x_add_member__mutmut_23(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["members"]
    ):
        raise ValueError("MEMBER ALREADY BELONGS TO THIS GROUP")

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


def x_add_member__mutmut_24(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["members"]
    ):
        raise ValueError("Member already belongs to this group")

    if len(group["members"]) > 50:
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


def x_add_member__mutmut_25(db, group_id, name):
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    member = normalize_member(db, name)

    if any(
        existing.casefold() == member.casefold()
        for existing in group["members"]
    ):
        raise ValueError("Member already belongs to this group")

    if len(group["members"]) >= 51:
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


def x_add_member__mutmut_26(db, group_id, name):
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
        raise ValueError(None)

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


def x_add_member__mutmut_27(db, group_id, name):
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
        raise ValueError("XXGroup member limit reachedXX")

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


def x_add_member__mutmut_28(db, group_id, name):
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
        raise ValueError("group member limit reached")

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


def x_add_member__mutmut_29(db, group_id, name):
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
        raise ValueError("GROUP MEMBER LIMIT REACHED")

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


def x_add_member__mutmut_30(db, group_id, name):
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
                None,
                (group_id, member, len(group["members"])),
            )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to add member") from None

    return get_group(db, group_id)


def x_add_member__mutmut_31(db, group_id, name):
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
                None,
            )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to add member") from None

    return get_group(db, group_id)


def x_add_member__mutmut_32(db, group_id, name):
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
                (group_id, member, len(group["members"])),
            )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to add member") from None

    return get_group(db, group_id)


def x_add_member__mutmut_33(db, group_id, name):
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
                )
    except sqlite3.IntegrityError:
        raise ValueError("Unable to add member") from None

    return get_group(db, group_id)


def x_add_member__mutmut_34(db, group_id, name):
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
        raise ValueError(None) from None

    return get_group(db, group_id)


def x_add_member__mutmut_35(db, group_id, name):
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
        raise ValueError("XXUnable to add memberXX") from None

    return get_group(db, group_id)


def x_add_member__mutmut_36(db, group_id, name):
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
        raise ValueError("unable to add member") from None

    return get_group(db, group_id)


def x_add_member__mutmut_37(db, group_id, name):
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
        raise ValueError("UNABLE TO ADD MEMBER") from None

    return get_group(db, group_id)


def x_add_member__mutmut_38(db, group_id, name):
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

    return get_group(None, group_id)


def x_add_member__mutmut_39(db, group_id, name):
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

    return get_group(db, None)


def x_add_member__mutmut_40(db, group_id, name):
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

    return get_group(group_id)


def x_add_member__mutmut_41(db, group_id, name):
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

    return get_group(db, )

mutants_x_add_member__mutmut['_mutmut_orig'] = x_add_member__mutmut_orig # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_1'] = x_add_member__mutmut_1 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_2'] = x_add_member__mutmut_2 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_3'] = x_add_member__mutmut_3 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_4'] = x_add_member__mutmut_4 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_5'] = x_add_member__mutmut_5 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_6'] = x_add_member__mutmut_6 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_7'] = x_add_member__mutmut_7 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_8'] = x_add_member__mutmut_8 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_9'] = x_add_member__mutmut_9 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_10'] = x_add_member__mutmut_10 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_11'] = x_add_member__mutmut_11 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_12'] = x_add_member__mutmut_12 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_13'] = x_add_member__mutmut_13 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_14'] = x_add_member__mutmut_14 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_15'] = x_add_member__mutmut_15 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_16'] = x_add_member__mutmut_16 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_17'] = x_add_member__mutmut_17 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_18'] = x_add_member__mutmut_18 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_19'] = x_add_member__mutmut_19 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_20'] = x_add_member__mutmut_20 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_21'] = x_add_member__mutmut_21 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_22'] = x_add_member__mutmut_22 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_23'] = x_add_member__mutmut_23 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_24'] = x_add_member__mutmut_24 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_25'] = x_add_member__mutmut_25 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_26'] = x_add_member__mutmut_26 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_27'] = x_add_member__mutmut_27 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_28'] = x_add_member__mutmut_28 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_29'] = x_add_member__mutmut_29 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_30'] = x_add_member__mutmut_30 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_31'] = x_add_member__mutmut_31 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_32'] = x_add_member__mutmut_32 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_33'] = x_add_member__mutmut_33 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_34'] = x_add_member__mutmut_34 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_35'] = x_add_member__mutmut_35 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_36'] = x_add_member__mutmut_36 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_37'] = x_add_member__mutmut_37 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_38'] = x_add_member__mutmut_38 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_39'] = x_add_member__mutmut_39 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_40'] = x_add_member__mutmut_40 # type: ignore # mutmut generated
mutants_x_add_member__mutmut['x_add_member__mutmut_41'] = x_add_member__mutmut_41 # type: ignore # mutmut generated


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
