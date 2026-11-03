
from __future__ import annotations

from backend.allocation import parse_money_to_cents


def _error(code, field, message):
    return {
        "code": code,
        "field": field,
        "message": message,
    }


def validate(
    parsed: dict,
    allocation: dict,
    roster: list[str],
) -> dict:
    errors = []
    total = allocation.get("totalCents")
    shares = allocation.get("shares", {})

    if (
        type(total) is not int
        or any(type(value) is not int for value in shares.values())
    ):
        errors.append(_error(
            "NON_INTEGER_CENTS",
            "shares",
            "Amounts must be integer cents",
        ))

    if isinstance(total, (int, float)) and total <= 0:
        errors.append(_error(
            "NON_POSITIVE_TOTAL",
            "totalCents",
            "Total must be positive",
        ))

    if any(
        isinstance(value, (int, float)) and value < 0
        for value in shares.values()
    ):
        errors.append(_error(
            "NEGATIVE_AMOUNT",
            "shares",
            "Shares cannot be negative",
        ))

    if (
        type(total) is int
        and all(type(value) is int for value in shares.values())
        and sum(shares.values()) != total
    ):
        errors.append(_error(
            "SHARES_DONT_SUM",
            "shares",
            "Shares do not sum to total",
        ))

    paid = allocation.get("paid")

    if paid is not None and type(total) is int:
        if any(type(value) is not int for value in paid.values()):
            errors.append(_error(
                "NON_INTEGER_CENTS",
                "paid",
                "Amounts paid must be integer cents",
            ))
        elif sum(paid.values()) != total:
            errors.append(_error(
                "PAYMENTS_DONT_SUM",
                "paid",
                "Amounts paid do not sum to total",
            ))

    payer = parsed.get("payer")

    if payer is None:
        errors.append(_error(
            "MISSING_PAYER", "payer", "Who paid?"
        ))
    elif payer not in roster:
        errors.append(_error(
            "UNKNOWN_NAME",
            "payer",
            f"Unknown member {payer}",
        ))

    for name in shares:
        if name not in roster:
            errors.append(_error(
                "UNKNOWN_NAME",
                "shares",
                f"Unknown member {name}",
            ))

    item_total = 0
    item_net_total = 0
    missing_price = False

    for index, item in enumerate(parsed.get("items", [])):
        price = item.get("unitPrice")

        if price is None:
            errors.append(_error(
                "MISSING_PRICE",
                f"items[{index}].unitPrice",
                f"Missing price for {item.get('name', 'item')}",
            ))
            missing_price = True
        else:
            try:
                gross = parse_money_to_cents(price) * item.get("quantity", 1)
                item_total += gross
                item_net_total += gross
                refund = item.get("refund")
                if refund:
                    refund_cents = parse_money_to_cents(refund["amount"])
                    item_net_total -= refund_cents
                    if refund_cents > gross:
                        errors.append(_error(
                            "INVALID_REFUND",
                            f"items[{index}].refund",
                            f"Refund is larger than {item.get('name', 'item')}",
                        ))
            except (ValueError, TypeError):
                errors.append(_error(
                    "NEGATIVE_AMOUNT",
                    f"items[{index}].unitPrice",
                    "Invalid item amount",
                ))
                missing_price = True

        spec = item.get("participants", {})
        names = spec.get("names", [])

        for name in names:
            if name != "ME" and name not in roster:
                errors.append(_error(
                    "UNKNOWN_NAME",
                    f"items[{index}].participants",
                    f"Unknown member {name}",
                ))

        extra_names = []
        if item.get("paidBy"):
            extra_names.append(("paidBy", item["paidBy"]))
        for entry in item.get("weights") or []:
            extra_names.append(("weights", entry.get("name")))
        if item.get("refund"):
            extra_names.append(("refund", item["refund"].get("recipient")))

        for field, name in extra_names:
            if name != "ME" and name not in roster:
                errors.append(_error(
                    "UNKNOWN_NAME",
                    f"items[{index}].{field}",
                    f"Unknown member {name}",
                ))

        mode = spec.get("mode")
        if (
            (mode == "only" and not names)
            or (
                mode == "all_except"
                and set(names) >= set(roster)
            )
        ):
            errors.append(_error(
                "NO_PARTICIPANTS",
                f"items[{index}].participants",
                "Who should share this item?",
            ))

    for index, charge in enumerate(parsed.get("charges", [])):
        if charge.get("method") is None:
            errors.append(_error(
                "TAX_TIP_METHOD_MISSING",
                f"charges[{index}].method",
                "How should tax or tip be split?",
            ))

    stated = parsed.get("statedTotal")

    if stated is not None and not missing_price:
        try:
            stated_cents = parse_money_to_cents(stated)

            if (
                not parsed.get("charges")
                and stated_cents not in (item_total, item_net_total)
            ):
                errors.append(_error(
                    "STATED_TOTAL_MISMATCH",
                    "statedTotal",
                    (
                        f"Stated total ${stated_cents / 100:.2f} "
                        f"differs from items ${item_total / 100:.2f}"
                    ),
                ))
            elif (
                parsed.get("charges")
                and type(total) is int
                and stated_cents != total
            ):
                errors.append(_error(
                    "STATED_TOTAL_MISMATCH",
                    "statedTotal",
                    (
                        f"Stated total ${stated_cents / 100:.2f} "
                        f"differs from calculated ${total / 100:.2f}"
                    ),
                ))
        except ValueError:
            errors.append(_error(
                "NEGATIVE_AMOUNT",
                "statedTotal",
                "Invalid stated total",
            ))

    if errors:
        return {"ok": False, "errors": errors}

    return {"ok": True}


def question_for_error(error: dict) -> str:
    code = error["code"]
    message = error.get("message", "")

    if code == "MISSING_PRICE":
        name = message.removeprefix(
            "Missing price for "
        ).strip() or "the item"
        return f"How much was {name}?"

    if code == "UNKNOWN_NAME":
        return (
            f"{message}. Which group member did you mean?"
        )

    templates = {
        "MISSING_PAYER": "Who paid for this expense?",
        "NO_PARTICIPANTS": "Who should share this item?",
        "TAX_TIP_METHOD_MISSING":
            "Should tax/tip be shared equally or proportionally?",
        "STATED_TOTAL_MISMATCH":
            "The stated total differs from the calculated total. "
            "Which amount is correct?",
    }

    return templates.get(
        code,
        f"Please clarify: {message}",
    )
