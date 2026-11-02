
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Any
import re


class UnknownNameError(ValueError):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Unknown group member: {name}")


class MissingChargeMethodError(ValueError):
    def __init__(self, message="Tax/tip method missing"):
        super().__init__(message)


class MissingChargeAmountError(ValueError):
    def __init__(self, message="Missing charge amount or percentage"):
        super().__init__(message)


class WeightsMismatchError(ValueError):
    def __init__(self, item_name):
        self.item_name = item_name
        super().__init__(
            f"Weights for {item_name} must list exactly its participants"
        )


_MONEY = re.compile(
    r"^\$?(?:\d+(?:\.\d{1,2})?|\.\d{1,2})$"
)


def parse_money_to_cents(value: str) -> int:
    if not isinstance(value, str) or not _MONEY.fullmatch(value):
        raise ValueError(f"Invalid money amount: {value!r}")

    cents = Decimal(value.removeprefix("$")) * 100
    return int(cents)


def format_cents(cents: int) -> str:
    if not isinstance(cents, int):
        raise ValueError("Cents must be an integer")

    sign = "-" if cents < 0 else ""
    dollars = abs(cents) // 100
    remainder = abs(cents) % 100

    return f"{sign}${dollars:,}.{remainder:02d}"


def resolve_name(
    name: str,
    roster: list[str],
    current_user: str,
) -> str:
    resolved = current_user if name == "ME" else name

    if resolved not in roster:
        raise UnknownNameError(resolved)

    return resolved


def resolve_participants(
    spec: Any,
    roster: list[str],
    current_user: str,
) -> list[str]:
    if hasattr(spec, "model_dump"):
        spec = spec.model_dump()

    mode = spec["mode"]
    names = spec["names"]

    resolved = [
        current_user if name == "ME" else name
        for name in names
    ]

    for name in resolved:
        if name not in roster:
            raise UnknownNameError(name)

    if mode == "all":
        return list(roster)

    if mode == "only":
        return list(dict.fromkeys(resolved))

    if mode == "all_except":
        return [
            name for name in roster
            if name not in resolved
        ]

    raise ValueError("Unknown participant mode")


def split_cents(
    amount_cents: int,
    weights: list[int],
    sharers: list[str],
    payer: str,
    roster_order: list[str],
) -> dict[str, int]:
    if type(amount_cents) is not int or amount_cents < 0:
        raise ValueError(
            "Amount must be nonnegative integer cents"
        )

    if (
        not sharers
        or len(weights) != len(sharers)
        or len(set(sharers)) != len(sharers)
    ):
        raise ValueError("Invalid sharers")

    if (
        any(type(w) is not int or w < 0 for w in weights)
        or not sum(weights)
    ):
        raise ValueError(
            "Weights must be nonnegative integers with positive sum"
        )

    total_weight = sum(weights)

    base = {
        name: amount_cents * weight // total_weight
        for name, weight in zip(sharers, weights)
    }

    leftover = amount_cents - sum(base.values())

    if payer in sharers:
        base[payer] += leftover
    else:
        order = {
            name: index
            for index, name in enumerate(roster_order)
        }

        ranked = sorted(
            sharers,
            key=lambda name: (
                -(
                    amount_cents
                    * weights[sharers.index(name)]
                    % total_weight
                ),
                order.get(name, len(order)),
            ),
        )

        for name in ranked[:leftover]:
            base[name] += 1

    return base


def _item_weights(
    item: dict,
    sharers: list[str],
    roster: list[str],
    current_user: str,
) -> list[int]:
    if not item.get("weights"):
        return [1] * len(sharers)

    by_name = {}
    for entry in item["weights"]:
        name = resolve_name(entry["name"], roster, current_user)
        by_name[name] = entry["weight"]

    if set(by_name) != set(sharers):
        raise WeightsMismatchError(item["name"])

    return [by_name[name] for name in sharers]


def allocate_items(
    items: list,
    payer: str,
    roster: list[str],
    current_user: str,
) -> dict:
    shares = {name: 0 for name in roster}
    paid = {name: 0 for name in roster}
    total = 0
    line_items = []

    for raw in items:
        item = (
            raw.model_dump()
            if hasattr(raw, "model_dump")
            else raw
        )

        if item["unitPrice"] is None:
            raise ValueError("Missing item price")

        count = item["quantity"]

        if type(count) is not int or count < 1:
            raise ValueError("Invalid quantity")

        gross = parse_money_to_cents(
            item["unitPrice"]
        ) * count

        refund = item.get("refund")
        refund_cents = 0
        if refund:
            refund_cents = parse_money_to_cents(refund["amount"])
            if refund_cents > gross:
                raise ValueError(
                    f"Refund is larger than {item['name']}"
                )

        cents = gross - refund_cents

        item_payer = (
            resolve_name(item["paidBy"], roster, current_user)
            if item.get("paidBy")
            else payer
        )

        sharers = resolve_participants(
            item["participants"],
            roster,
            current_user,
        )

        if not sharers:
            raise ValueError("No participants")

        allocation = split_cents(
            cents,
            _item_weights(item, sharers, roster, current_user),
            sharers,
            item_payer,
            roster,
        )

        for name, amount in allocation.items():
            shares[name] += amount

        # Paying is recorded gross; a refund counts as negative paid.
        paid[item_payer] += gross
        if refund:
            recipient = resolve_name(
                refund["recipient"], roster, current_user
            )
            paid[recipient] -= refund_cents

        line_items.append({
            "name": item["name"],
            "totalCents": cents,
            "grossCents": gross,
            "refundCents": refund_cents,
            "paidBy": item_payer,
            "shares": allocation,
        })

        total += cents

    return {
        "totalCents": total,
        "shares": shares,
        "paid": paid,
        "lineItems": line_items,
    }


def _charge_cents(charge: dict, subtotal_cents: int) -> int:
    method = charge.get("method")
    if not method or method not in ("equal", "proportional"):
        raise MissingChargeMethodError("Should tax or tip be split equally or proportionally?")

    amount = charge.get("amount")
    percent = charge.get("percent")

    if amount is not None and percent is not None:
        raise ValueError("Charge cannot specify both amount and percent")

    if amount is None and percent is None:
        raise MissingChargeAmountError(f"How much was the {charge.get('kind', 'charge')}?")

    if amount is not None:
        return parse_money_to_cents(amount)

    percentage = Decimal(str(percent))
    return int(
        (Decimal(subtotal_cents) * percentage / 100).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )
    )


def allocate_charges(
    charges: list,
    allocation: dict,
    payer: str,
    roster: list[str],
) -> dict:
    """Add tax, tip, and fees on top of item shares.

    Charges with the same method are pooled and allocated once, so
    tax + tip split proportionally round like a single charge. Rounding
    them separately can move a cent between people.
    """
    subtotal_cents = allocation.get("totalCents", 0)
    current_shares = dict(allocation.get("shares", {name: 0 for name in roster}))
    base_item_shares = dict(allocation.get("shares", {name: 0 for name in roster}))
    paid = dict(allocation.get("paid", {name: 0 for name in roster}))
    line_items = list(allocation.get("lineItems", []))
    allocated_charges = []
    pools = {}

    for raw in charges:
        charge = raw.model_dump() if hasattr(raw, "model_dump") else dict(raw)
        charge_cents = _charge_cents(charge, subtotal_cents)

        charge_copy = dict(charge)
        charge_copy["amountCents"] = charge_cents
        allocated_charges.append(charge_copy)

        pool = pools.setdefault(
            charge["method"],
            {"method": charge["method"], "kinds": [], "amountCents": 0},
        )
        pool["kinds"].append(charge["kind"])
        pool["amountCents"] += charge_cents

    active = [
        name for name in roster
        if base_item_shares.get(name, 0) > 0
    ]
    if not active:
        active = list(roster)

    total_cents = subtotal_cents

    for pool in pools.values():
        if pool["method"] == "proportional":
            weights = [base_item_shares.get(name, 0) for name in active]
            if sum(weights) == 0:
                weights = [1] * len(active)
        else:
            weights = [1] * len(active)

        splits = split_cents(
            pool["amountCents"],
            weights,
            active,
            payer,
            roster,
        )

        for name, cents in splits.items():
            current_shares[name] = current_shares.get(name, 0) + cents

        pool["shares"] = splits
        total_cents += pool["amountCents"]
        # The main payer pays tax, tip, and fees.
        paid[payer] = paid.get(payer, 0) + pool["amountCents"]

    return {
        "totalCents": total_cents,
        "shares": current_shares,
        "paid": paid,
        "lineItems": line_items,
        "charges": allocated_charges,
        "chargeAllocations": list(pools.values()),
    }
