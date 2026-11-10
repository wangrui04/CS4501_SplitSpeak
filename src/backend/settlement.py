"""Net-position settlement ("simplified debts").

For each person, net = total paid - total cost share. People with a
negative net pay people with a positive net. Transfers are chosen
greedily: the largest debtor pays the largest creditor until one of
them reaches zero, with ties broken by roster order.
"""

from __future__ import annotations


def payments_of(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["totalCents"]}]


def compute_nets(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def _largest(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(candidates, key=lambda name: (-nets[name] * sign, order[name]))


def compute_settlement(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def member_balances(
    settlement: dict,
    current_user: str,
    roster: list[str],
) -> dict:
    """Each other member's balance relative to the session user.

    Positive cents mean the member owes the user; negative means the
    user owes the member. Someone who settles with a third person shows
    as "settled up" relative to the user.
    """
    relative = {name: 0 for name in roster if name != current_user}

    for transfer in settlement["transfers"]:
        if transfer["to"] == current_user and transfer["from"] in relative:
            relative[transfer["from"]] += transfer["cents"]
        elif transfer["from"] == current_user and transfer["to"] in relative:
            relative[transfer["to"]] -= transfer["cents"]

    balances = []
    for name, cents in relative.items():
        if cents > 0:
            status = "owes you"
        elif cents < 0:
            status = "you owe"
        else:
            status = "settled up"
        balances.append({"name": name, "cents": cents, "status": status})

    my_net = next(
        (n["netCents"] for n in settlement["nets"] if n["name"] == current_user),
        0,
    )

    return {
        "balances": balances,
        "summary": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }
