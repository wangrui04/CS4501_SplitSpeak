"""Manual equal-split entry, using the same engine and validator as AI."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, ValidationError

from backend.allocation import (
    allocate_charges,
    allocate_items,
    parse_money_to_cents,
)
from backend.validator import validate


class ManualExpenseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str
    amount: str | int | float
    paidBy: str
    splitBetween: list[str]


class ManualEntryError(ValueError):
    pass


def _amount_text(amount) -> str:
    if isinstance(amount, bool):
        raise ManualEntryError("Amount must be a number")
    # str() keeps the user's decimals, so 12.345 is rejected below.
    return str(amount).strip()


def build_manual_expense(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "description, amount, paidBy, and splitBetween are required"
        ) from None

    description = request.description.strip()
    if not description:
        raise ManualEntryError("Description is required")

    amount = _amount_text(request.amount)
    try:
        cents = parse_money_to_cents(amount)
    except ValueError:
        raise ManualEntryError(
            "Amount must be a number with at most 2 decimals"
        ) from None
    if cents <= 0:
        raise ManualEntryError("Amount must be greater than 0")

    if request.paidBy not in roster:
        raise ManualEntryError(f"Unknown member {request.paidBy}")

    if not request.splitBetween:
        raise ManualEntryError("Choose at least one person to split with")

    for name in request.splitBetween:
        if name not in roster:
            raise ManualEntryError(f"Unknown member {name}")

    parsed = {
        "description": description,
        "payer": request.paidBy,
        "items": [{
            "name": description,
            "quantity": 1,
            "unitPrice": amount.removeprefix("$"),
            "participants": {
                "mode": "only",
                "names": list(request.splitBetween),
            },
        }],
        "charges": [],
        "statedTotal": None,
        "openQuestions": [],
    }

    allocation = allocate_items(
        parsed["items"], request.paidBy, roster, request.paidBy
    )
    allocation = allocate_charges([], allocation, request.paidBy, roster)

    result = validate(parsed, allocation, roster)
    if not result["ok"]:
        raise ManualEntryError(result["errors"][0]["message"])

    return {
        "description": description,
        "payer": request.paidBy,
        "totalCents": allocation["totalCents"],
        "shares": [
            {"name": name, "cents": allocation["shares"][name]}
            for name in roster
        ],
        "payments": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }
