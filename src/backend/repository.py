
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

    source = data.get("source")

    if source not in ("ai", "manual"):
        raise ValueError("Invalid source")

    if data.get("createdBy") not in group["members"]:
        raise ValueError("Unknown member")

    payments = validate_expense_data(data, group)

    ensure_expense_details_table(db)

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
                data["totalCents"],
                source,
                data["createdBy"],
            ),
        )

        expense_id = cursor.lastrowid

        for share in data["shares"]:
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

        store_expense_details(
            db,
            expense_id,
            data,
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
            {
                "name": payment["name"],
                "cents": payment["cents"],
            }
            for payment in payment_rows
        ] or [
            {
                "name": expense["payer"],
                "cents": expense["totalCents"],
            }
        ]

        expense.update(
            get_expense_details(db, expense["id"])
        )

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
            raise ValueError(
                "Shares must be nonnegative integer cents"
            )

        computed_total += cents

        clean_shares.append({
            "name": name,
            "cents": cents,
        })

    if computed_total != total_cents:
        raise ValueError(
            "Shares do not match total"
        )

    payments = _clean_payments(
        preview,
        payer,
        total_cents,
        roster,
    )

    description = (
        preview.get("description")
        or (
            shares[0].get("summary")
            if shares else None
        )
        or "Shared expense"
    )

    expense_data = {
        "groupId": conv["groupId"],
        "description": description,
        "payer": payer,
        "totalCents": total_cents,
        "shares": clean_shares,
        "payments": payments,
        "source": "ai",
        "createdBy": confirmed_by,
        "lineItems": preview.get("lineItems") or [],
        "charges": preview.get("charges") or [],
    }

    # The existing preview has already passed the allocation
    # validator. Revalidate saved values before persistence.
    validate_expense_data(expense_data, group)

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


def ensure_expense_details_table(db):
    """
    Add itemized expense storage without changing existing
    saved expenses or requiring a separate migration.
    """
    db.execute("""
        CREATE TABLE IF NOT EXISTS expense_details (
            expense_id INTEGER PRIMARY KEY
                REFERENCES expenses(id) ON DELETE CASCADE,
            line_items_json TEXT NOT NULL DEFAULT '[]',
            charges_json TEXT NOT NULL DEFAULT '[]',
            version INTEGER NOT NULL DEFAULT 1
        )
    """)


def get_expense_details(db, expense_id):
    ensure_expense_details_table(db)

    row = db.execute(
        """
        SELECT line_items_json, charges_json, version
        FROM expense_details
        WHERE expense_id=?
        """,
        (expense_id,),
    ).fetchone()

    if row is None:
        return {
            "lineItems": [],
            "charges": [],
            "version": 1,
        }

    return {
        "lineItems": json.loads(row["line_items_json"]),
        "charges": json.loads(row["charges_json"]),
        "version": row["version"],
    }


def store_expense_details(db, expense_id, data, version=1):
    ensure_expense_details_table(db)

    db.execute(
        """
        INSERT INTO expense_details (
            expense_id,
            line_items_json,
            charges_json,
            version
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(expense_id) DO UPDATE SET
            line_items_json=excluded.line_items_json,
            charges_json=excluded.charges_json,
            version=excluded.version
        """,
        (
            expense_id,
            json.dumps(data.get("lineItems") or []),
            json.dumps(data.get("charges") or []),
            version,
        ),
    )


def validate_expense_details(data, members):
    """
    Validate itemization when it exists.
    Older manual expenses without items are supported.
    """
    items = data.get("lineItems") or []
    charges = data.get("charges") or []

    if not isinstance(items, list):
        raise ValueError("Invalid line items")

    if not isinstance(charges, list):
        raise ValueError("Invalid charges")

    if not items and not charges:
        return

    total = 0

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Invalid item")

        if not str(item.get("name", "")).strip():
            raise ValueError("Item name is required")

        quantity = item.get("quantity", 1)

        if type(quantity) is not int or quantity < 1:
            raise ValueError("Invalid item quantity")

        unit_price = item.get("unitPriceCents")
        refund = item.get("refundCents", 0)

        if type(refund) is not int or refund < 0:
            raise ValueError("Invalid refund")

        if unit_price is not None:
            if type(unit_price) is not int or unit_price < 0:
                raise ValueError("Invalid unit price")

            item_total = unit_price * quantity - refund

            if (
                "totalCents" in item
                and item["totalCents"] != item_total
            ):
                raise ValueError("Item total does not match price")
        else:
            item_total = item.get("totalCents")

            if type(item_total) is not int:
                raise ValueError("Invalid item total")

        if item_total < 0:
            raise ValueError("Item total cannot be negative")

        participants = item.get("participants")

        if isinstance(participants, list):
            if not participants or any(
                name not in members for name in participants
            ):
                raise ValueError("Invalid item participants")

        paid_by = item.get("paidBy")

        if paid_by and paid_by not in members:
            raise ValueError("Unknown item payer")

        item_shares = item.get("shares")

        if isinstance(item_shares, dict):
            if any(name not in members for name in item_shares):
                raise ValueError("Unknown item participant")

            if any(
                type(cents) is not int or cents < 0
                for cents in item_shares.values()
            ):
                raise ValueError("Invalid item shares")

            if sum(item_shares.values()) != item_total:
                raise ValueError("Item shares do not match cost")

        total += item_total

    for charge in charges:
        if not isinstance(charge, dict):
            raise ValueError("Invalid charge")

        cents = charge.get("amountCents")

        if type(cents) is not int or cents < 0:
            raise ValueError("Invalid charge amount")

        total += cents

    if total != data["totalCents"]:
        raise ValueError(
            "Item and charge totals do not match expense total"
        )


def validate_expense_data(data, group):
    """
    Shared validation for creating and editing expenses.
    All financial calculations use integer cents.
    """
    members = set(group["members"])

    total = data.get("totalCents")
    payer = data.get("payer")
    description = data.get("description")
    created_by = data.get("createdBy")

    if (
        type(total) is not int
        or total <= 0
    ):
        raise ValueError("Invalid cents")

    if not isinstance(description, str) or not description.strip():
        raise ValueError("Description is required")

    if payer not in members:
        raise ValueError("Unknown payer")

    if created_by is not None and created_by not in members:
        raise ValueError("Unknown member")

    if data.get("groupId", group["id"]) != group["id"]:
        raise ValueError("Group mismatch")

    shares = data.get("shares")

    if not isinstance(shares, list) or not shares:
        raise ValueError("Missing shares")

    share_names = []
    share_total = 0

    for share in shares:
        if not isinstance(share, dict):
            raise ValueError("Invalid shares")

        name = share.get("name")
        cents = share.get("cents")

        if name not in members:
            raise ValueError("Unknown member")

        if type(cents) is not int or cents < 0:
            raise ValueError("Invalid share amount")

        share_names.append(name)
        share_total += cents

    if len(share_names) != len(set(share_names)):
        raise ValueError("Duplicate shares")

    if share_total != total:
        raise ValueError("Shares do not sum to total")

    payments = data.get("payments")

    if payments is None:
        payments = [{"name": payer, "cents": total}]

    if not isinstance(payments, list) or not payments:
        raise ValueError("Missing payments")

    payment_names = []
    payment_total = 0

    for payment in payments:
        if not isinstance(payment, dict):
            raise ValueError("Invalid payments")

        name = payment.get("name")
        cents = payment.get("cents")

        if name not in members:
            raise ValueError("Unknown payment member")

        # Negative payments are allowed for received refunds.
        if type(cents) is not int:
            raise ValueError("Invalid payment amount")

        payment_names.append(name)
        payment_total += cents

    if len(payment_names) != len(set(payment_names)):
        raise ValueError("Duplicate payments")

    if payment_total != total:
        raise ValueError("Payments do not sum to total")

    validate_expense_details(data, members)

    return payments


def edit_expense(db, group_id, expense_id, data):
    """
    Update an existing expense rather than creating another.
    The API route must check session authorization first.
    """
    group = get_group(db, group_id)

    if group is None:
        raise ValueError("Group not found")

    existing = db.execute(
        """
        SELECT * FROM expenses
        WHERE id=? AND group_id=?
        """,
        (expense_id, group_id),
    ).fetchone()

    if existing is None:
        raise LookupError("Expense not found")

    payments = validate_expense_data(data, group)

    existing_details = get_expense_details(db, expense_id)
    current_version = existing_details["version"]

    if (
        "version" in data
        and data["version"] != current_version
    ):
        raise RuntimeError(
            "Expense was modified. Refresh and try again."
        )

    # Preserve saved details when the client omits them.
    updated_data = dict(data)

    if "lineItems" not in updated_data:
        updated_data["lineItems"] = existing_details["lineItems"]

    if "charges" not in updated_data:
        updated_data["charges"] = existing_details["charges"]

    validate_expense_details(
        updated_data,
        set(group["members"]),
    )

    with db:
        db.execute(
            """
            UPDATE expenses
            SET description=?,
                payer_name=?,
                total_cents=?
            WHERE id=? AND group_id=?
            """,
            (
                data["description"].strip(),
                data["payer"],
                data["totalCents"],
                expense_id,
                group_id,
            ),
        )

        db.execute(
            """
            DELETE FROM expense_shares
            WHERE expense_id=?
            """,
            (expense_id,),
        )

        db.execute(
            """
            DELETE FROM expense_payments
            WHERE expense_id=?
            """,
            (expense_id,),
        )

        for share in data["shares"]:
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

        store_expense_details(
            db,
            expense_id,
            updated_data,
            version=current_version + 1,
        )

    return {
        "ok": True,
        "expenseId": expense_id,
        "version": current_version + 1,
    }
