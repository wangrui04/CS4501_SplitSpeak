
import logging

from pydantic import ValidationError

from backend.llm import LlmError
from backend.schemas import ParsedExpense
from backend.allocation import (
    parse_money_to_cents,
    allocate_items,
    allocate_charges,
    resolve_participants,
    UnknownNameError,
    MissingChargeMethodError,
    MissingChargeAmountError,
    WeightsMismatchError,
)
from backend.grounding import (
    amount_question,
    charge_question,
    ground_payers,
    user_texts,
)
from backend.settlement import compute_settlement
from backend.validator import validate, question_for_error

logger = logging.getLogger("splitwise.pipeline")


def _infer_trip_payer(data, roster, current_user):
    """Main payer for a multi-payer trip, or None if it must be asked.

    When every item names who paid and there is no tax, tip, or fee
    (those are charged to the main payer), the main payer is whoever
    paid the most, with ties broken by roster order.
    """
    items = data["items"]
    if not items or data["charges"]:
        return None
    if any(not item.get("paidBy") or item["unitPrice"] is None for item in items):
        return None

    totals = {}
    try:
        for item in items:
            name = current_user if item["paidBy"] == "ME" else item["paidBy"]
            cents = parse_money_to_cents(item["unitPrice"]) * item["quantity"]
            totals[name] = totals.get(name, 0) + cents
    except ValueError:
        return None

    order = {name: index for index, name in enumerate(roster)}
    return min(totals, key=lambda name: (-totals[name], order.get(name, len(order))))


def parse_turn(*, llm, conversation, roster, current_user):
    try:
        raw = llm.parse(
            messages=conversation,
            roster=roster,
            current_user=current_user,
        )
        parsed = ParsedExpense.model_validate(raw)

    except Exception as exc:
        # The user only sees "unresolved"; log why, for debugging.
        # Only our own error types are safe to print in full: their
        # messages are fixed strings plus schema validation details.
        # Anything else could echo request data or keys.
        detail = (
            str(exc)[:1000]
            if isinstance(exc, (LlmError, ValidationError))
            else "(details hidden)"
        )
        logger.warning(
            "LLM parse failed: %s: %s",
            exc.__class__.__name__,
            detail,
        )
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

    # Issue #49: don't trust the LLM's payer or amounts on their own.
    # Clear any payer the user never stated, so "Who paid?" is asked.
    texts = user_texts(conversation)
    data, _ = ground_payers(data, texts, current_user)

    payer = (
        current_user
        if data["payer"] == "ME"
        else data["payer"]
    )

    if payer is None:
        payer = _infer_trip_payer(data, roster, current_user)

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

    grounding_question = amount_question(data, texts) or charge_question(data, texts)
    if grounding_question:
        return {"type": "question", "question": grounding_question}

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
