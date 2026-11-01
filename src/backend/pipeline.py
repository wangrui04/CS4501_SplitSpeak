
from backend.schemas import ParsedExpense
from backend.allocation import (
    allocate_items,
    allocate_charges,
    resolve_participants,
    UnknownNameError,
    MissingChargeMethodError,
    MissingChargeAmountError,
)
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

    preview = {
        "payer": payer,
        "currency": "USD",
        "lineItems": allocation["lineItems"],
        "charges": allocation.get("charges", data["charges"]),
        "totalCents": allocation["totalCents"],
        "shares": [
            {
                "name": name,
                "cents": allocation["shares"][name],
                "summary": data["description"],
            }
            for name in roster
        ],
        "validated": True,
    }

    return {
        "type": "preview",
        "preview": preview,
    }
