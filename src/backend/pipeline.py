
from backend.schemas import ParsedExpense
from backend.allocation import (
    allocate_items,
    allocate_charges,
    resolve_participants,
    UnknownNameError,
    MissingChargeMethodError,
    MissingChargeAmountError,
    WeightsMismatchError,
)
from backend.settlement import compute_settlement
from backend.validator import validate, question_for_error


def parse_turn(*, llm, conversation, roster, current_user):
    try:
        raw = llm.parse(
            messages=conversation,
            roster=roster,
            current_user=current_user,
        )
        parsed = ParsedExpense.model_validate(raw)

    except Exception:
        return {
            "type": "unresolved",
            "reason": (
                "Unable to parse a valid structured expense"
            ),
        }

    data = parsed.model_dump()

    if data["openQuestions"]:
        return {
            "type": "question",
            "question": data["openQuestions"][0]["question"],
        }

    payer = (
        current_user
        if data["payer"] == "ME"
        else data["payer"]
    )

    data["payer"] = payer

    if payer is None:
        return {
            "type": "question",
            "question": "Who paid for this expense?",
        }

    if payer not in roster:
        return {
            "type": "question",
            "question": (
                f"Unknown member {payer}. Who paid?"
            ),
        }

    for item in data["items"]:
        if item["unitPrice"] is None:
            return {
                "type": "question",
                "question": (
                    f"How much was {item['name']}?"
                ),
            }

        names = item["participants"]["names"]
        if "ME" in names and current_user in names:
            # "Kayla and I" while signed in as Kayla: don't guess.
            return {
                "type": "question",
                "question": (
                    f"You're signed in as {current_user}, but "
                    f"{item['name']} lists both {current_user} and you. "
                    "Who else shared it?"
                ),
            }

        try:
            sharers = resolve_participants(
                item["participants"],
                roster,
                current_user,
            )

            if not sharers:
                return {
                    "type": "question",
                    "question": (
                        f"Who should share {item['name']}?"
                    ),
                }

        except UnknownNameError as error:
            return {
                "type": "question",
                "question": (
                    f"Unknown member {error.name}. "
                    "Who did you mean?"
                ),
            }

    try:
        allocation = allocate_items(
            data["items"],
            payer,
            roster,
            current_user,
        )

        allocation = allocate_charges(
            data["charges"],
            allocation,
            payer,
            roster,
        )

        result = validate(
            data,
            allocation,
            roster,
        )

    except UnknownNameError as error:
        return {
            "type": "question",
            "question": (
                f"Unknown member {error.name}. "
                "Who did you mean?"
            ),
        }
    except WeightsMismatchError as error:
        return {
            "type": "question",
            "question": (
                f"How should {error.item_name} be weighted "
                "between the people who shared it?"
            ),
        }
    except MissingChargeMethodError:
        return {
            "type": "question",
            "question": (
                "Should tax or tip be split "
                "equally or proportionally?"
            ),
        }
    except MissingChargeAmountError as exc:
        return {
            "type": "question",
            "question": str(exc),
        }
    except (ValueError, ZeroDivisionError) as exc:
        return {
            "type": "question",
            "question": (
                f"Please clarify this expense: {exc}"
            ),
        }

    if not result["ok"]:
        return {
            "type": "question",
            "question": question_for_error(
                result["errors"][0]
            ),
        }

    shares = [
        {
            "name": name,
            "cents": allocation["shares"][name],
            "summary": data["description"],
        }
        for name in roster
    ]
    paid = [
        {"name": name, "cents": allocation["paid"].get(name, 0)}
        for name in roster
    ]

    # Same function the group page uses, so testers, the benchmark,
    # and saved balances all read the same numbers.
    settlement = compute_settlement(
        [{"payments": paid, "shares": shares}],
        roster,
    )

    if settlement["error"]:
        return {
            "type": "question",
            "question": "Please clarify this expense: amounts paid "
            "do not match the shares.",
        }

    preview = {
        "description": data["description"],
        "payer": payer,
        "currency": "USD",
        "lineItems": allocation["lineItems"],
        "charges": allocation.get("charges", data["charges"]),
        "totalCents": allocation["totalCents"],
        "shares": shares,
        "paid": paid,
        "settlement": {
            "nets": settlement["nets"],
            "transfers": settlement["transfers"],
        },
        "validated": True,
    }

    return {
        "type": "preview",
        "preview": preview,
    }
