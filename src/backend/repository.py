
import json

from backend.settlement import compute_nets, settlement_entries


def list_groups(db):
    rows = db.execute(
        "SELECT id, name FROM groups ORDER BY id"
    )
    return [dict(row) for row in rows]


def get_group(db, group_id):
    row = db.execute(
        "SELECT id, name FROM groups WHERE id=?",
        (group_id,),
    ).fetchone()

    if row is None:
        return None

    result = dict(row)

    members = db.execute(
        """
        SELECT name FROM group_members
        WHERE group_id=?
        ORDER BY position
        """,
        (group_id,),
    )

    result["members"] = [
        member["name"] for member in members
    ]

    return result


def save_expense(db, data):
    group = get_group(db, data["groupId"])

    if group is None:
        raise ValueError("Unknown group")

    members = set(group["members"])
    shares = data["shares"]
    total = data["totalCents"]

    if (
        type(total) is not int
        or total <= 0
        or not shares
        or any(
            type(share["cents"]) is not int
            or share["cents"] < 0
            for share in shares
        )
    ):
        raise ValueError("Invalid cents")

    if sum(
        share["cents"] for share in shares
    ) != total:
        raise ValueError("Shares do not sum to total")

    if (
        data["payer"] not in members
        or data["createdBy"] not in members
        or any(
            share["name"] not in members
            for share in shares
        )
    ):
        raise ValueError("Unknown member")

    if len({
        share["name"] for share in shares
    }) != len(shares):
        raise ValueError("Duplicate shares")

    if data["source"] not in ("ai", "manual"):
        raise ValueError("Invalid source")

    payments = data.get("payments") or [
        {"name": data["payer"], "cents": total}
    ]

    if (
        any(type(payment["cents"]) is not int for payment in payments)
        or any(payment["name"] not in members for payment in payments)
        or len({payment["name"] for payment in payments}) != len(payments)
    ):
        raise ValueError("Invalid payments")

    if sum(payment["cents"] for payment in payments) != total:
        raise ValueError("Payments do not sum to total")

    with db:
        cursor = db.execute(
            """
            INSERT INTO expenses (
                group_id,
                description,
                payer_name,
                total_cents,
                source,
                created_by
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["groupId"],
                data["description"],
                data["payer"],
                total,
                data["source"],
                data["createdBy"],
            ),
        )

        expense_id = cursor.lastrowid

        for share in shares:
            db.execute(
                """
                INSERT INTO expense_shares
                (expense_id, name, cents)
                VALUES (?, ?, ?)
                """,
                (
                    expense_id,
                    share["name"],
                    share["cents"],
                ),
            )

        for payment in payments:
            db.execute(
                """
                INSERT INTO expense_payments
                (expense_id, name, cents)
                VALUES (?, ?, ?)
                """,
                (
                    expense_id,
                    payment["name"],
                    payment["cents"],
                ),
            )

    return {"id": expense_id}


def list_expenses(db, group_id):
    result = []

    rows = db.execute(
        """
        SELECT * FROM expenses
        WHERE group_id=?
        ORDER BY id
        """,
        (group_id,),
    ).fetchall()

    for row in rows:
        expense = dict(row)

        # Convert SQLite column names to API field names.
        expense["totalCents"] = expense.pop("total_cents")
        expense["groupId"] = expense.pop("group_id")
        expense["payer"] = expense.pop("payer_name")
        expense["createdBy"] = expense.pop("created_by")

        share_rows = db.execute(
            """
            SELECT name, cents
            FROM expense_shares
            WHERE expense_id=?
            ORDER BY rowid
            """,
            (expense["id"],),
        )

        expense["shares"] = [
            {
                "name": share["name"],
                "cents": share["cents"],
            }
            for share in share_rows
        ]

        payment_rows = db.execute(
            """
            SELECT p.name, p.cents
            FROM expense_payments p
            LEFT JOIN group_members m
                ON m.group_id=? AND m.name=p.name
            WHERE p.expense_id=?
            ORDER BY m.position, p.rowid
            """,
            (group_id, expense["id"]),
        )

        expense["payments"] = [
            {"name": row["name"], "cents": row["cents"]}
            for row in payment_rows
        ] or [{"name": expense["payer"], "cents": expense["totalCents"]}]

        result.append(expense)

    return result


def list_settlements(db, group_id):
    rows = db.execute(
        """
        SELECT * FROM settlements
        WHERE group_id=?
        ORDER BY id
        """,
        (group_id,),
    ).fetchall()

    return [
        {
            "id": row["id"],
            "groupId": row["group_id"],
            "from": row["from_name"],
            "to": row["to_name"],
            "cents": row["cents"],
            "recordedBy": row["recorded_by"],
            "recordedAt": row["recorded_at"],
        }
        for row in rows
    ]


def group_ledger(db, group_id):
    """Expenses plus recorded repayments, for net and transfer math."""
    return list_expenses(db, group_id) + settlement_entries(
        list_settlements(db, group_id)
    )


def get_group_balances(db, group_id):
    group = get_group(db, group_id)
    if group is None:
        return None

    nets = compute_nets(group_ledger(db, group_id), group["members"])

    return {
        member: nets.get(member, 0)
        for member in group["members"]
    }


def confirm_conversation_expense(db, conversation_id, confirmed_by):
    conv = get_conversation(db, conversation_id)
    if conv is None:
        raise ValueError("Conversation not found")

    if conv["status"] == "confirmed":
        raise ValueError("Expense has already been confirmed")

    if conv["status"] != "preview":
        raise ValueError("Draft is not in preview state")

    preview = conv["finalPreview"]
    if not preview or not isinstance(preview, dict):
        raise ValueError("Missing or invalid preview draft")

    if not preview.get("validated"):
        raise ValueError("Draft is not validated")

    group = get_group(db, conv["groupId"])
    if group is None:
        raise ValueError("Group not found")

    roster = set(group["members"])
    if confirmed_by not in roster:
        raise ValueError("Confirmed by user not in group roster")

    payer = preview.get("payer")
    if not payer or payer not in roster:
        raise ValueError("Unknown or missing payer")

    shares = preview.get("shares", [])
    if not shares:
        raise ValueError("Shares list is empty")

    total_cents = preview.get("totalCents")
    if type(total_cents) is not int or total_cents <= 0:
        raise ValueError("Total must be positive integer cents")

    computed_total = 0
    clean_shares = []
    seen_members = set()

    for share in shares:
        name = share.get("name")
        cents = share.get("cents")
        if name not in roster:
            raise ValueError(f"Unknown member in shares: {name}")
        if name in seen_members:
            raise ValueError(f"Duplicate member in shares: {name}")
        seen_members.add(name)

        if type(cents) is not int or cents < 0:
            raise ValueError("Shares must be nonnegative integer cents")

        computed_total += cents
        clean_shares.append({"name": name, "cents": cents})

    if computed_total != total_cents:
        raise ValueError(
            f"Shares sum ({computed_total}) does not match total ({total_cents})"
        )

    payments = _clean_payments(preview, payer, total_cents, roster)

    description = "Shared expense"
    if preview.get("description"):
        description = preview["description"]
    elif shares and shares[0].get("summary"):
        description = shares[0]["summary"]

    expense_data = {
        "groupId": conv["groupId"],
        "description": description,
        "payer": payer,
        "totalCents": total_cents,
        "shares": clean_shares,
        "payments": payments,
        "source": "ai",
        "createdBy": confirmed_by,
    }

    with db:
        saved = save_expense(db, expense_data)
        expense_id = saved["id"]

        update_conversation(
            db,
            conversation_id,
            {"status": "confirmed"},
        )
        add_conversation_message(
            db,
            conversation_id,
            "assistant",
            "Expense confirmed and saved.",
        )

    return {
        "expenseId": expense_id,
        "conversationId": conversation_id,
        "status": "confirmed",
    }


def _clean_payments(preview, payer, total_cents, roster):
    """Re-check the stored preview's amounts paid before saving."""
    paid = preview.get("paid")
    if not paid:
        return [{"name": payer, "cents": total_cents}]

    payments = []
    for entry in paid:
        name = entry.get("name")
        cents = entry.get("cents")
        if name not in roster or type(cents) is not int:
            raise ValueError("Invalid amounts paid in preview")
        if cents:
            payments.append({"name": name, "cents": cents})

    if sum(payment["cents"] for payment in payments) != total_cents:
        raise ValueError("Amounts paid do not match total")

    return payments


def create_conversation(db, data):
    with db:
        cursor = db.execute(
            """
            INSERT INTO conversations
            (group_id, user_name, prompt_count, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                data["groupId"],
                data["userName"],
                data["promptCount"],
                data["status"],
            ),
        )

        conversation_id = cursor.lastrowid

        for message in data.get("messages", []):
            db.execute(
                """
                INSERT INTO conversation_messages
                (conversation_id, role, content)
                VALUES (?, ?, ?)
                """,
                (
                    conversation_id,
                    message["role"],
                    message["content"],
                ),
            )

    return {"id": conversation_id}


def add_conversation_message(db, conversation_id, role, content):
    with db:
        cursor = db.execute(
            """
            INSERT INTO conversation_messages
            (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content),
        )
    return {"id": cursor.lastrowid}


def get_conversation_messages(db, conversation_id):
    rows = db.execute(
        """
        SELECT role, content
        FROM conversation_messages
        WHERE conversation_id=?
        ORDER BY id ASC
        """,
        (conversation_id,),
    ).fetchall()

    return [
        {"role": row["role"], "content": row["content"]}
        for row in rows
    ]


def get_conversation(db, conversation_id):
    row = db.execute(
        "SELECT * FROM conversations WHERE id=?",
        (conversation_id,),
    ).fetchone()

    if row is None:
        return None

    result = dict(row)
    messages = get_conversation_messages(db, conversation_id)

    return {
        "id": result["id"],
        "groupId": result["group_id"],
        "userName": result["user_name"],
        "promptCount": result["prompt_count"],
        "status": result["status"],
        "finalPreview": (
            json.loads(result["final_preview_json"])
            if result["final_preview_json"]
            else None
        ),
        "messages": messages,
    }


def list_conversations(db, group_id):
    rows = db.execute(
        """
        SELECT * FROM conversations
        WHERE group_id=?
        ORDER BY id ASC
        """,
        (group_id,),
    ).fetchall()

    return [
        {
            "id": row["id"],
            "groupId": row["group_id"],
            "userName": row["user_name"],
            "promptCount": row["prompt_count"],
            "status": row["status"],
            "finalPreview": (
                json.loads(row["final_preview_json"])
                if row["final_preview_json"]
                else None
            ),
            "messages": get_conversation_messages(db, row["id"]),
        }
        for row in rows
    ]


def update_conversation(db, conversation_id, data):
    mapping = {
        "promptCount": "prompt_count",
        "status": "status",
        "finalPreview": "final_preview_json",
    }

    fields = []
    values = []

    for key, value in data.items():
        if key == "messages":
            continue
        if key not in mapping:
            raise ValueError("Unknown field")

        fields.append(mapping[key] + "=?")

        if key == "finalPreview":
            value = json.dumps(value)

        values.append(value)

    with db:
        if fields:
            values.append(conversation_id)
            db.execute(
                f"""
                UPDATE conversations
                SET {", ".join(fields)},
                    updated_at=CURRENT_TIMESTAMP
                WHERE id=?
                """,
                values,
            )

        if "messages" in data:
            db.execute(
                "DELETE FROM conversation_messages WHERE conversation_id=?",
                (conversation_id,),
            )
            for message in data["messages"]:
                db.execute(
                    """
                    INSERT INTO conversation_messages
                    (conversation_id, role, content)
                    VALUES (?, ?, ?)
                    """,
                    (
                        conversation_id,
                        message["role"],
                        message["content"],
                    ),
                )


def delete_conversation(db, conversation_id):
    with db:
        db.execute(
            "DELETE FROM conversation_messages WHERE conversation_id=?",
            (conversation_id,),
        )
        db.execute(
            "DELETE FROM conversations WHERE id=?",
            (conversation_id,),
        )
