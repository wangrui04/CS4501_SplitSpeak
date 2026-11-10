
import json

from fastapi import APIRouter, HTTPException, Request

from backend.repository import get_group, list_expenses
from backend.settlement import compute_settlement

router = APIRouter()


def get_item_total(item):
    if type(item) is not dict:
        raise ValueError("Invalid line item")

    name = item.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Item name is required")

    if type(item.get("totalCents")) is int:
        amount = item["totalCents"]
    else:
        qty = item.get("quantity")
        price = item.get("unitPriceCents")
        if type(qty) is not int or qty < 1:
            raise ValueError("Invalid item quantity")
        if type(price) is not int or price < 0:
            raise ValueError("Invalid item price")
        amount = qty * price

    if amount < 0:
        raise ValueError("Item total cannot be negative")
    return amount


def validate_details(data, members):
    if not isinstance(data, dict):
        raise ValueError("Invalid expense")

    total = data.get("totalCents")
    if type(total) is not int or total <= 0:
        raise ValueError("Total must be positive integer cents")

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("Description is required")

    payer = data.get("payer")
    if payer not in members:
        raise ValueError("Unknown member")

    shares = data.get("shares")
    payments = data.get("payments")

    if not isinstance(shares, list) or not shares:
        raise ValueError("At least one share is required")

    if not isinstance(payments, list) or not payments:
        raise ValueError("At least one payment is required")

    for entries, label in (
        (shares, "shares"),
        (payments, "payments"),
    ):
        names = []

        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"Invalid {label}")

            name = entry.get("name")
            amount = entry.get("cents")

            if name not in members:
                raise ValueError("Unknown member")
            if type(amount) is not int:
                raise ValueError(f"Invalid {label}")
            if label == "shares" and amount < 0:
                raise ValueError("Shares cannot be negative")

            names.append(name)

        if len(names) != len(set(names)):
            raise ValueError(f"Duplicate member in {label}")

        if sum(e["cents"] for e in entries) != total:
            raise ValueError(f"{label.capitalize()} do not sum to total")

    items = data.get("lineItems")
    charges = data.get("charges")

    if items is not None:
        if not isinstance(items, list):
            raise ValueError("Invalid line items")

        if charges is not None and not isinstance(charges, list):
            raise ValueError("Invalid charges")

        item_total = sum(get_item_total(item) for item in items)

        charge_total = 0
        for charge in charges or []:
            if not isinstance(charge, dict):
                raise ValueError("Invalid charge")
            cents = charge.get("amountCents")
            if type(cents) is not int or cents < 0:
                raise ValueError("Invalid charge amount")
            charge_total += cents

        if items and item_total + charge_total != total:
            raise ValueError("Line items and charges do not sum to total")

        if items:
            for item in items:
                participants = item.get("participants")

                if participants is None and isinstance(
                    item.get("shares"), dict
                ):
                    participants = list(item["shares"])

                if participants is not None:
                    if not isinstance(participants, list):
                        raise ValueError("Invalid participants")
                    if any(name not in members for name in participants):
                        raise ValueError("Unknown item participant")

    return True


def update_saved_expense(db, group_id, expense_id, data):
    existing = db.execute(
        "SELECT * FROM expenses WHERE id=? AND group_id=?",
        (expense_id, group_id),
    ).fetchone()

    if existing is None:
        raise LookupError("Expense not found")

    group = get_group(db, group_id)
    if group is None:
        raise LookupError("Group not found")

    validate_details(data, group["members"])

    # Optional optimistic concurrency check.
    expected_version = data.get("version")
    if (
        expected_version is not None
        and expected_version != existing["version"]
    ):
        raise RuntimeError("Expense was updated by someone else")

    # Preserve old itemization when the caller explicitly sends it.
    # Missing itemization represents a legacy, aggregate-only expense.
    items = data.get("lineItems")
    charges = data.get("charges")

    with db:
        result = db.execute(
            """
            UPDATE expenses
            SET description=?, payer_name=?, total_cents=?,
                line_items_json=?, charges_json=?,
                version=version+1
            WHERE id=? AND group_id=? AND version=?
            """,
            (
                data["description"].strip(),
                data["payer"],
                data["totalCents"],
                json.dumps(items) if items is not None else None,
                json.dumps(charges) if charges is not None else None,
                expense_id,
                group_id,
                existing["version"],
            ),
        )

        if result.rowcount != 1:
            raise RuntimeError("Expense changed during editing")

        db.execute(
            "DELETE FROM expense_shares WHERE expense_id=?",
            (expense_id,),
        )
        db.execute(
            "DELETE FROM expense_payments WHERE expense_id=?",
            (expense_id,),
        )

        db.executemany(
            """
            INSERT INTO expense_shares (expense_id, name, cents)
            VALUES (?, ?, ?)
            """,
            [
                (expense_id, s["name"], s["cents"])
                for s in data["shares"]
            ],
        )

        db.executemany(
            """
            INSERT INTO expense_payments (expense_id, name, cents)
            VALUES (?, ?, ?)
            """,
            [
                (expense_id, p["name"], p["cents"])
                for p in data["payments"]
            ],
        )

    return next(
        expense for expense in list_expenses(db, group_id)
        if expense["id"] == expense_id
    )


@router.put("/api/groups/{group_id}/expenses/{expense_id}")
def edit_expense(
    group_id: int,
    expense_id: int,
    data: dict,
    request: Request,
):
    db = request.app.state.db

    group = get_group(db, group_id)
    if group is None:
        raise HTTPException(404, "Group not found")

    current_user = request.session.get("name")
    if current_user not in group["members"]:
        raise HTTPException(403, "Not a member of this group")

    try:
        return update_saved_expense(
            db, group_id, expense_id, data
        )
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(409, str(exc)) from exc


@router.get("/api/groups/{group_id}/expenses/{expense_id}")
def get_expense_detail(
    group_id: int,
    expense_id: int,
    request: Request,
):
    db = request.app.state.db
    group = get_group(db, group_id)

    if group is None:
        raise HTTPException(404, "Group not found")

    if request.session.get("name") not in group["members"]:
        raise HTTPException(403, "Not a member of this group")

    expense = next(
        (
            e for e in list_expenses(db, group_id)
            if e["id"] == expense_id
        ),
        None,
    )

    if expense is None:
        raise HTTPException(404, "Expense not found")

    settlement = compute_settlement(
        [expense], group["members"]
    )

    return {
        **expense,
        "settlement": settlement,
    }
