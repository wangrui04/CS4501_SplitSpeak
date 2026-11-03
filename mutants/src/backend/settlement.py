"""Net-position settlement ("simplified debts").

For each person, net = total paid - total cost share. People with a
negative net pay people with a positive net. Transfers are chosen
greedily: the largest debtor pays the largest creditor until one of
them reaches zero, with ties broken by roster order.
"""

from __future__ import annotations


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_payments_of__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_payments_of__mutmut)
def payments_of(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_orig(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_1(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "XXpaymentsXX" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_2(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "PAYMENTS" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_3(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" not in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_4(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["XXpaymentsXX"]

    return [{"name": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_5(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["PAYMENTS"]

    return [{"name": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_6(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"XXnameXX": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_7(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"NAME": expense["payer"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_8(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["XXpayerXX"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_9(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["PAYER"], "cents": expense["totalCents"]}]


def x_payments_of__mutmut_10(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "XXcentsXX": expense["totalCents"]}]


def x_payments_of__mutmut_11(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "CENTS": expense["totalCents"]}]


def x_payments_of__mutmut_12(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["XXtotalCentsXX"]}]


def x_payments_of__mutmut_13(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["totalcents"]}]


def x_payments_of__mutmut_14(expense: dict) -> list[dict]:
    """An expense's payments; single-payer rows pay their own total."""
    if "payments" in expense:
        return expense["payments"]

    return [{"name": expense["payer"], "cents": expense["TOTALCENTS"]}]

mutants_x_payments_of__mutmut['_mutmut_orig'] = x_payments_of__mutmut_orig # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_1'] = x_payments_of__mutmut_1 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_2'] = x_payments_of__mutmut_2 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_3'] = x_payments_of__mutmut_3 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_4'] = x_payments_of__mutmut_4 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_5'] = x_payments_of__mutmut_5 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_6'] = x_payments_of__mutmut_6 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_7'] = x_payments_of__mutmut_7 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_8'] = x_payments_of__mutmut_8 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_9'] = x_payments_of__mutmut_9 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_10'] = x_payments_of__mutmut_10 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_11'] = x_payments_of__mutmut_11 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_12'] = x_payments_of__mutmut_12 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_13'] = x_payments_of__mutmut_13 # type: ignore # mutmut generated
mutants_x_payments_of__mutmut['x_payments_of__mutmut_14'] = x_payments_of__mutmut_14 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_compute_nets__mutmut)
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


def x_compute_nets__mutmut_orig(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_1(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = None

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_2(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 1 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_3(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(None):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_4(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = None
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_5(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["XXnameXX"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_6(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["NAME"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_7(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) - payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_8(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(None, 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_9(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], None) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_10(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_11(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], ) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_12(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["XXnameXX"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_13(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["NAME"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_14(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 1) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_15(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["XXcentsXX"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_16(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["CENTS"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_17(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["XXsharesXX"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_18(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["SHARES"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_19(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = None

    return nets


def x_compute_nets__mutmut_20(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["XXnameXX"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_21(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["NAME"]] = nets.get(share["name"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_22(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) + share["cents"]

    return nets


def x_compute_nets__mutmut_23(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(None, 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_24(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], None) - share["cents"]

    return nets


def x_compute_nets__mutmut_25(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(0) - share["cents"]

    return nets


def x_compute_nets__mutmut_26(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], ) - share["cents"]

    return nets


def x_compute_nets__mutmut_27(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["XXnameXX"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_28(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["NAME"], 0) - share["cents"]

    return nets


def x_compute_nets__mutmut_29(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 1) - share["cents"]

    return nets


def x_compute_nets__mutmut_30(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["XXcentsXX"]

    return nets


def x_compute_nets__mutmut_31(expenses: list[dict], roster: list[str]) -> dict[str, int]:
    nets = {name: 0 for name in roster}

    for expense in expenses:
        for payment in payments_of(expense):
            nets[payment["name"]] = (
                nets.get(payment["name"], 0) + payment["cents"]
            )
        for share in expense["shares"]:
            nets[share["name"]] = nets.get(share["name"], 0) - share["CENTS"]

    return nets

mutants_x_compute_nets__mutmut['_mutmut_orig'] = x_compute_nets__mutmut_orig # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_1'] = x_compute_nets__mutmut_1 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_2'] = x_compute_nets__mutmut_2 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_3'] = x_compute_nets__mutmut_3 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_4'] = x_compute_nets__mutmut_4 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_5'] = x_compute_nets__mutmut_5 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_6'] = x_compute_nets__mutmut_6 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_7'] = x_compute_nets__mutmut_7 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_8'] = x_compute_nets__mutmut_8 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_9'] = x_compute_nets__mutmut_9 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_10'] = x_compute_nets__mutmut_10 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_11'] = x_compute_nets__mutmut_11 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_12'] = x_compute_nets__mutmut_12 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_13'] = x_compute_nets__mutmut_13 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_14'] = x_compute_nets__mutmut_14 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_15'] = x_compute_nets__mutmut_15 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_16'] = x_compute_nets__mutmut_16 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_17'] = x_compute_nets__mutmut_17 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_18'] = x_compute_nets__mutmut_18 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_19'] = x_compute_nets__mutmut_19 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_20'] = x_compute_nets__mutmut_20 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_21'] = x_compute_nets__mutmut_21 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_22'] = x_compute_nets__mutmut_22 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_23'] = x_compute_nets__mutmut_23 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_24'] = x_compute_nets__mutmut_24 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_25'] = x_compute_nets__mutmut_25 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_26'] = x_compute_nets__mutmut_26 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_27'] = x_compute_nets__mutmut_27 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_28'] = x_compute_nets__mutmut_28 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_29'] = x_compute_nets__mutmut_29 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_30'] = x_compute_nets__mutmut_30 # type: ignore # mutmut generated
mutants_x_compute_nets__mutmut['x_compute_nets__mutmut_31'] = x_compute_nets__mutmut_31 # type: ignore # mutmut generated
mutants_x__largest__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__largest__mutmut)
def _largest(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(candidates, key=lambda name: (-nets[name] * sign, order[name]))


def x__largest__mutmut_orig(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(candidates, key=lambda name: (-nets[name] * sign, order[name]))


def x__largest__mutmut_1(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = None
    return min(candidates, key=lambda name: (-nets[name] * sign, order[name]))


def x__largest__mutmut_2(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net / sign > 0]
    return min(candidates, key=lambda name: (-nets[name] * sign, order[name]))


def x__largest__mutmut_3(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign >= 0]
    return min(candidates, key=lambda name: (-nets[name] * sign, order[name]))


def x__largest__mutmut_4(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 1]
    return min(candidates, key=lambda name: (-nets[name] * sign, order[name]))


def x__largest__mutmut_5(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(None, key=lambda name: (-nets[name] * sign, order[name]))


def x__largest__mutmut_6(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(candidates, key=None)


def x__largest__mutmut_7(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(key=lambda name: (-nets[name] * sign, order[name]))


def x__largest__mutmut_8(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(candidates, )


def x__largest__mutmut_9(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(candidates, key=lambda name: None)


def x__largest__mutmut_10(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(candidates, key=lambda name: (-nets[name] / sign, order[name]))


def x__largest__mutmut_11(nets: dict[str, int], order: dict[str, int], sign: int) -> str:
    candidates = [name for name, net in nets.items() if net * sign > 0]
    return min(candidates, key=lambda name: (+nets[name] * sign, order[name]))

mutants_x__largest__mutmut['_mutmut_orig'] = x__largest__mutmut_orig # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_1'] = x__largest__mutmut_1 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_2'] = x__largest__mutmut_2 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_3'] = x__largest__mutmut_3 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_4'] = x__largest__mutmut_4 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_5'] = x__largest__mutmut_5 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_6'] = x__largest__mutmut_6 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_7'] = x__largest__mutmut_7 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_8'] = x__largest__mutmut_8 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_9'] = x__largest__mutmut_9 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_10'] = x__largest__mutmut_10 # type: ignore # mutmut generated
mutants_x__largest__mutmut['x__largest__mutmut_11'] = x__largest__mutmut_11 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_compute_settlement__mutmut)
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


def x_compute_settlement__mutmut_orig(expenses: list[dict], roster: list[str]) -> dict:
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


def x_compute_settlement__mutmut_1(expenses: list[dict], roster: list[str]) -> dict:
    nets = None
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


def x_compute_settlement__mutmut_2(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(None, roster)
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


def x_compute_settlement__mutmut_3(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, None)
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


def x_compute_settlement__mutmut_4(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(roster)
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


def x_compute_settlement__mutmut_5(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, )
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


def x_compute_settlement__mutmut_6(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = None
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


def x_compute_settlement__mutmut_7(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(None)}
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


def x_compute_settlement__mutmut_8(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = None

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


def x_compute_settlement__mutmut_9(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"XXnameXX": name, "netCents": net} for name, net in nets.items()]

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


def x_compute_settlement__mutmut_10(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"NAME": name, "netCents": net} for name, net in nets.items()]

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


def x_compute_settlement__mutmut_11(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "XXnetCentsXX": net} for name, net in nets.items()]

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


def x_compute_settlement__mutmut_12(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netcents": net} for name, net in nets.items()]

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


def x_compute_settlement__mutmut_13(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "NETCENTS": net} for name, net in nets.items()]

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


def x_compute_settlement__mutmut_14(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(None) != 0:
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


def x_compute_settlement__mutmut_15(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) == 0:
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


def x_compute_settlement__mutmut_16(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 1:
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


def x_compute_settlement__mutmut_17(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"XXnetsXX": net_list, "transfers": [], "error": "UNBALANCED"}

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


def x_compute_settlement__mutmut_18(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"NETS": net_list, "transfers": [], "error": "UNBALANCED"}

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


def x_compute_settlement__mutmut_19(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "XXtransfersXX": [], "error": "UNBALANCED"}

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


def x_compute_settlement__mutmut_20(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "TRANSFERS": [], "error": "UNBALANCED"}

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


def x_compute_settlement__mutmut_21(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "XXerrorXX": "UNBALANCED"}

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


def x_compute_settlement__mutmut_22(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "ERROR": "UNBALANCED"}

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


def x_compute_settlement__mutmut_23(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "XXUNBALANCEDXX"}

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


def x_compute_settlement__mutmut_24(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "unbalanced"}

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


def x_compute_settlement__mutmut_25(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = None
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_26(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(None)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_27(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = None

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_28(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(None):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_29(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net <= 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_30(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 1 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_31(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = None
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_32(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(None, order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_33(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, None, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_34(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, None)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_35(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(order, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_36(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, -1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_37(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, )
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_38(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, +1)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_39(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -2)
        creditor = _largest(remaining, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_40(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = None
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_41(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(None, order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_42(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, None, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_43(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, None)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_44(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(order, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_45(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, 1)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_46(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, )
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_47(expenses: list[dict], roster: list[str]) -> dict:
    nets = compute_nets(expenses, roster)
    order = {name: index for index, name in enumerate(nets)}
    net_list = [{"name": name, "netCents": net} for name, net in nets.items()]

    if sum(nets.values()) != 0:
        return {"nets": net_list, "transfers": [], "error": "UNBALANCED"}

    remaining = dict(nets)
    transfers = []

    while any(net < 0 for net in remaining.values()):
        debtor = _largest(remaining, order, -1)
        creditor = _largest(remaining, order, 2)
        cents = min(-remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_48(expenses: list[dict], roster: list[str]) -> dict:
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
        cents = None

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_49(expenses: list[dict], roster: list[str]) -> dict:
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
        cents = min(None, remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_50(expenses: list[dict], roster: list[str]) -> dict:
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
        cents = min(-remaining[debtor], None)

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_51(expenses: list[dict], roster: list[str]) -> dict:
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
        cents = min(remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_52(expenses: list[dict], roster: list[str]) -> dict:
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
        cents = min(-remaining[debtor], )

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_53(expenses: list[dict], roster: list[str]) -> dict:
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
        cents = min(+remaining[debtor], remaining[creditor])

        transfers.append({"from": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_54(expenses: list[dict], roster: list[str]) -> dict:
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

        transfers.append(None)
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_55(expenses: list[dict], roster: list[str]) -> dict:
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

        transfers.append({"XXfromXX": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_56(expenses: list[dict], roster: list[str]) -> dict:
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

        transfers.append({"FROM": debtor, "to": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_57(expenses: list[dict], roster: list[str]) -> dict:
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

        transfers.append({"from": debtor, "XXtoXX": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_58(expenses: list[dict], roster: list[str]) -> dict:
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

        transfers.append({"from": debtor, "TO": creditor, "cents": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_59(expenses: list[dict], roster: list[str]) -> dict:
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

        transfers.append({"from": debtor, "to": creditor, "XXcentsXX": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_60(expenses: list[dict], roster: list[str]) -> dict:
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

        transfers.append({"from": debtor, "to": creditor, "CENTS": cents})
        remaining[debtor] += cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_61(expenses: list[dict], roster: list[str]) -> dict:
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
        remaining[debtor] = cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_62(expenses: list[dict], roster: list[str]) -> dict:
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
        remaining[debtor] -= cents
        remaining[creditor] -= cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_63(expenses: list[dict], roster: list[str]) -> dict:
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
        remaining[creditor] = cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_64(expenses: list[dict], roster: list[str]) -> dict:
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
        remaining[creditor] += cents

    return {"nets": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_65(expenses: list[dict], roster: list[str]) -> dict:
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

    return {"XXnetsXX": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_66(expenses: list[dict], roster: list[str]) -> dict:
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

    return {"NETS": net_list, "transfers": transfers, "error": None}


def x_compute_settlement__mutmut_67(expenses: list[dict], roster: list[str]) -> dict:
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

    return {"nets": net_list, "XXtransfersXX": transfers, "error": None}


def x_compute_settlement__mutmut_68(expenses: list[dict], roster: list[str]) -> dict:
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

    return {"nets": net_list, "TRANSFERS": transfers, "error": None}


def x_compute_settlement__mutmut_69(expenses: list[dict], roster: list[str]) -> dict:
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

    return {"nets": net_list, "transfers": transfers, "XXerrorXX": None}


def x_compute_settlement__mutmut_70(expenses: list[dict], roster: list[str]) -> dict:
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

    return {"nets": net_list, "transfers": transfers, "ERROR": None}

mutants_x_compute_settlement__mutmut['_mutmut_orig'] = x_compute_settlement__mutmut_orig # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_1'] = x_compute_settlement__mutmut_1 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_2'] = x_compute_settlement__mutmut_2 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_3'] = x_compute_settlement__mutmut_3 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_4'] = x_compute_settlement__mutmut_4 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_5'] = x_compute_settlement__mutmut_5 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_6'] = x_compute_settlement__mutmut_6 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_7'] = x_compute_settlement__mutmut_7 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_8'] = x_compute_settlement__mutmut_8 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_9'] = x_compute_settlement__mutmut_9 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_10'] = x_compute_settlement__mutmut_10 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_11'] = x_compute_settlement__mutmut_11 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_12'] = x_compute_settlement__mutmut_12 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_13'] = x_compute_settlement__mutmut_13 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_14'] = x_compute_settlement__mutmut_14 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_15'] = x_compute_settlement__mutmut_15 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_16'] = x_compute_settlement__mutmut_16 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_17'] = x_compute_settlement__mutmut_17 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_18'] = x_compute_settlement__mutmut_18 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_19'] = x_compute_settlement__mutmut_19 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_20'] = x_compute_settlement__mutmut_20 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_21'] = x_compute_settlement__mutmut_21 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_22'] = x_compute_settlement__mutmut_22 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_23'] = x_compute_settlement__mutmut_23 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_24'] = x_compute_settlement__mutmut_24 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_25'] = x_compute_settlement__mutmut_25 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_26'] = x_compute_settlement__mutmut_26 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_27'] = x_compute_settlement__mutmut_27 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_28'] = x_compute_settlement__mutmut_28 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_29'] = x_compute_settlement__mutmut_29 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_30'] = x_compute_settlement__mutmut_30 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_31'] = x_compute_settlement__mutmut_31 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_32'] = x_compute_settlement__mutmut_32 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_33'] = x_compute_settlement__mutmut_33 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_34'] = x_compute_settlement__mutmut_34 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_35'] = x_compute_settlement__mutmut_35 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_36'] = x_compute_settlement__mutmut_36 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_37'] = x_compute_settlement__mutmut_37 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_38'] = x_compute_settlement__mutmut_38 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_39'] = x_compute_settlement__mutmut_39 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_40'] = x_compute_settlement__mutmut_40 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_41'] = x_compute_settlement__mutmut_41 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_42'] = x_compute_settlement__mutmut_42 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_43'] = x_compute_settlement__mutmut_43 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_44'] = x_compute_settlement__mutmut_44 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_45'] = x_compute_settlement__mutmut_45 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_46'] = x_compute_settlement__mutmut_46 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_47'] = x_compute_settlement__mutmut_47 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_48'] = x_compute_settlement__mutmut_48 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_49'] = x_compute_settlement__mutmut_49 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_50'] = x_compute_settlement__mutmut_50 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_51'] = x_compute_settlement__mutmut_51 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_52'] = x_compute_settlement__mutmut_52 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_53'] = x_compute_settlement__mutmut_53 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_54'] = x_compute_settlement__mutmut_54 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_55'] = x_compute_settlement__mutmut_55 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_56'] = x_compute_settlement__mutmut_56 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_57'] = x_compute_settlement__mutmut_57 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_58'] = x_compute_settlement__mutmut_58 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_59'] = x_compute_settlement__mutmut_59 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_60'] = x_compute_settlement__mutmut_60 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_61'] = x_compute_settlement__mutmut_61 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_62'] = x_compute_settlement__mutmut_62 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_63'] = x_compute_settlement__mutmut_63 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_64'] = x_compute_settlement__mutmut_64 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_65'] = x_compute_settlement__mutmut_65 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_66'] = x_compute_settlement__mutmut_66 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_67'] = x_compute_settlement__mutmut_67 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_68'] = x_compute_settlement__mutmut_68 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_69'] = x_compute_settlement__mutmut_69 # type: ignore # mutmut generated
mutants_x_compute_settlement__mutmut['x_compute_settlement__mutmut_70'] = x_compute_settlement__mutmut_70 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_member_balances__mutmut)
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


def x_member_balances__mutmut_orig(
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


def x_member_balances__mutmut_1(
    settlement: dict,
    current_user: str,
    roster: list[str],
) -> dict:
    """Each other member's balance relative to the session user.

    Positive cents mean the member owes the user; negative means the
    user owes the member. Someone who settles with a third person shows
    as "settled up" relative to the user.
    """
    relative = None

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


def x_member_balances__mutmut_2(
    settlement: dict,
    current_user: str,
    roster: list[str],
) -> dict:
    """Each other member's balance relative to the session user.

    Positive cents mean the member owes the user; negative means the
    user owes the member. Someone who settles with a third person shows
    as "settled up" relative to the user.
    """
    relative = {name: 1 for name in roster if name != current_user}

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


def x_member_balances__mutmut_3(
    settlement: dict,
    current_user: str,
    roster: list[str],
) -> dict:
    """Each other member's balance relative to the session user.

    Positive cents mean the member owes the user; negative means the
    user owes the member. Someone who settles with a third person shows
    as "settled up" relative to the user.
    """
    relative = {name: 0 for name in roster if name == current_user}

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


def x_member_balances__mutmut_4(
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

    for transfer in settlement["XXtransfersXX"]:
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


def x_member_balances__mutmut_5(
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

    for transfer in settlement["TRANSFERS"]:
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


def x_member_balances__mutmut_6(
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
        if transfer["to"] == current_user or transfer["from"] in relative:
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


def x_member_balances__mutmut_7(
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
        if transfer["XXtoXX"] == current_user and transfer["from"] in relative:
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


def x_member_balances__mutmut_8(
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
        if transfer["TO"] == current_user and transfer["from"] in relative:
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


def x_member_balances__mutmut_9(
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
        if transfer["to"] != current_user and transfer["from"] in relative:
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


def x_member_balances__mutmut_10(
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
        if transfer["to"] == current_user and transfer["XXfromXX"] in relative:
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


def x_member_balances__mutmut_11(
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
        if transfer["to"] == current_user and transfer["FROM"] in relative:
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


def x_member_balances__mutmut_12(
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
        if transfer["to"] == current_user and transfer["from"] not in relative:
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


def x_member_balances__mutmut_13(
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
            relative[transfer["from"]] = transfer["cents"]
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


def x_member_balances__mutmut_14(
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
            relative[transfer["from"]] -= transfer["cents"]
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


def x_member_balances__mutmut_15(
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
            relative[transfer["XXfromXX"]] += transfer["cents"]
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


def x_member_balances__mutmut_16(
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
            relative[transfer["FROM"]] += transfer["cents"]
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


def x_member_balances__mutmut_17(
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
            relative[transfer["from"]] += transfer["XXcentsXX"]
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


def x_member_balances__mutmut_18(
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
            relative[transfer["from"]] += transfer["CENTS"]
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


def x_member_balances__mutmut_19(
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
        elif transfer["from"] == current_user or transfer["to"] in relative:
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


def x_member_balances__mutmut_20(
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
        elif transfer["XXfromXX"] == current_user and transfer["to"] in relative:
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


def x_member_balances__mutmut_21(
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
        elif transfer["FROM"] == current_user and transfer["to"] in relative:
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


def x_member_balances__mutmut_22(
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
        elif transfer["from"] != current_user and transfer["to"] in relative:
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


def x_member_balances__mutmut_23(
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
        elif transfer["from"] == current_user and transfer["XXtoXX"] in relative:
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


def x_member_balances__mutmut_24(
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
        elif transfer["from"] == current_user and transfer["TO"] in relative:
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


def x_member_balances__mutmut_25(
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
        elif transfer["from"] == current_user and transfer["to"] not in relative:
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


def x_member_balances__mutmut_26(
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
            relative[transfer["to"]] = transfer["cents"]

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


def x_member_balances__mutmut_27(
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
            relative[transfer["to"]] += transfer["cents"]

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


def x_member_balances__mutmut_28(
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
            relative[transfer["XXtoXX"]] -= transfer["cents"]

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


def x_member_balances__mutmut_29(
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
            relative[transfer["TO"]] -= transfer["cents"]

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


def x_member_balances__mutmut_30(
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
            relative[transfer["to"]] -= transfer["XXcentsXX"]

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


def x_member_balances__mutmut_31(
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
            relative[transfer["to"]] -= transfer["CENTS"]

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


def x_member_balances__mutmut_32(
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

    balances = None
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


def x_member_balances__mutmut_33(
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
        if cents >= 0:
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


def x_member_balances__mutmut_34(
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
        if cents > 1:
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


def x_member_balances__mutmut_35(
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
            status = None
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


def x_member_balances__mutmut_36(
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
            status = "XXowes youXX"
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


def x_member_balances__mutmut_37(
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
            status = "OWES YOU"
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


def x_member_balances__mutmut_38(
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
        elif cents <= 0:
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


def x_member_balances__mutmut_39(
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
        elif cents < 1:
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


def x_member_balances__mutmut_40(
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
            status = None
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


def x_member_balances__mutmut_41(
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
            status = "XXyou oweXX"
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


def x_member_balances__mutmut_42(
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
            status = "YOU OWE"
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


def x_member_balances__mutmut_43(
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
            status = None
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


def x_member_balances__mutmut_44(
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
            status = "XXsettled upXX"
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


def x_member_balances__mutmut_45(
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
            status = "SETTLED UP"
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


def x_member_balances__mutmut_46(
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
        balances.append(None)

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


def x_member_balances__mutmut_47(
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
        balances.append({"XXnameXX": name, "cents": cents, "status": status})

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


def x_member_balances__mutmut_48(
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
        balances.append({"NAME": name, "cents": cents, "status": status})

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


def x_member_balances__mutmut_49(
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
        balances.append({"name": name, "XXcentsXX": cents, "status": status})

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


def x_member_balances__mutmut_50(
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
        balances.append({"name": name, "CENTS": cents, "status": status})

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


def x_member_balances__mutmut_51(
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
        balances.append({"name": name, "cents": cents, "XXstatusXX": status})

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


def x_member_balances__mutmut_52(
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
        balances.append({"name": name, "cents": cents, "STATUS": status})

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


def x_member_balances__mutmut_53(
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

    my_net = None

    return {
        "balances": balances,
        "summary": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_54(
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
        None,
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


def x_member_balances__mutmut_55(
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
        None,
    )

    return {
        "balances": balances,
        "summary": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_56(
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


def x_member_balances__mutmut_57(
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
        )

    return {
        "balances": balances,
        "summary": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_58(
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
        (n["XXnetCentsXX"] for n in settlement["nets"] if n["name"] == current_user),
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


def x_member_balances__mutmut_59(
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
        (n["netcents"] for n in settlement["nets"] if n["name"] == current_user),
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


def x_member_balances__mutmut_60(
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
        (n["NETCENTS"] for n in settlement["nets"] if n["name"] == current_user),
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


def x_member_balances__mutmut_61(
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
        (n["netCents"] for n in settlement["XXnetsXX"] if n["name"] == current_user),
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


def x_member_balances__mutmut_62(
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
        (n["netCents"] for n in settlement["NETS"] if n["name"] == current_user),
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


def x_member_balances__mutmut_63(
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
        (n["netCents"] for n in settlement["nets"] if n["XXnameXX"] == current_user),
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


def x_member_balances__mutmut_64(
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
        (n["netCents"] for n in settlement["nets"] if n["NAME"] == current_user),
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


def x_member_balances__mutmut_65(
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
        (n["netCents"] for n in settlement["nets"] if n["name"] != current_user),
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


def x_member_balances__mutmut_66(
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
        1,
    )

    return {
        "balances": balances,
        "summary": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_67(
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
        "XXbalancesXX": balances,
        "summary": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_68(
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
        "BALANCES": balances,
        "summary": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_69(
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
        "XXsummaryXX": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_70(
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
        "SUMMARY": {
            "totalBalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_71(
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
            "XXtotalBalanceXX": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_72(
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
            "totalbalance": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_73(
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
            "TOTALBALANCE": my_net,
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_74(
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
            "XXyouOweXX": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_75(
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
            "youowe": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_76(
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
            "YOUOWE": sum(-b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_77(
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
            "youOwe": sum(None),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_78(
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
            "youOwe": sum(+b["cents"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_79(
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
            "youOwe": sum(-b["XXcentsXX"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_80(
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
            "youOwe": sum(-b["CENTS"] for b in balances if b["cents"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_81(
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
            "youOwe": sum(-b["cents"] for b in balances if b["XXcentsXX"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_82(
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
            "youOwe": sum(-b["cents"] for b in balances if b["CENTS"] < 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_83(
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
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] <= 0),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_84(
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
            "youOwe": sum(-b["cents"] for b in balances if b["cents"] < 1),
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_85(
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
            "XXyouAreOwedXX": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_86(
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
            "youareowed": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_87(
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
            "YOUAREOWED": sum(b["cents"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_88(
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
            "youAreOwed": sum(None),
        },
    }


def x_member_balances__mutmut_89(
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
            "youAreOwed": sum(b["XXcentsXX"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_90(
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
            "youAreOwed": sum(b["CENTS"] for b in balances if b["cents"] > 0),
        },
    }


def x_member_balances__mutmut_91(
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
            "youAreOwed": sum(b["cents"] for b in balances if b["XXcentsXX"] > 0),
        },
    }


def x_member_balances__mutmut_92(
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
            "youAreOwed": sum(b["cents"] for b in balances if b["CENTS"] > 0),
        },
    }


def x_member_balances__mutmut_93(
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
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] >= 0),
        },
    }


def x_member_balances__mutmut_94(
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
            "youAreOwed": sum(b["cents"] for b in balances if b["cents"] > 1),
        },
    }

mutants_x_member_balances__mutmut['_mutmut_orig'] = x_member_balances__mutmut_orig # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_1'] = x_member_balances__mutmut_1 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_2'] = x_member_balances__mutmut_2 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_3'] = x_member_balances__mutmut_3 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_4'] = x_member_balances__mutmut_4 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_5'] = x_member_balances__mutmut_5 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_6'] = x_member_balances__mutmut_6 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_7'] = x_member_balances__mutmut_7 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_8'] = x_member_balances__mutmut_8 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_9'] = x_member_balances__mutmut_9 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_10'] = x_member_balances__mutmut_10 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_11'] = x_member_balances__mutmut_11 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_12'] = x_member_balances__mutmut_12 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_13'] = x_member_balances__mutmut_13 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_14'] = x_member_balances__mutmut_14 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_15'] = x_member_balances__mutmut_15 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_16'] = x_member_balances__mutmut_16 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_17'] = x_member_balances__mutmut_17 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_18'] = x_member_balances__mutmut_18 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_19'] = x_member_balances__mutmut_19 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_20'] = x_member_balances__mutmut_20 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_21'] = x_member_balances__mutmut_21 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_22'] = x_member_balances__mutmut_22 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_23'] = x_member_balances__mutmut_23 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_24'] = x_member_balances__mutmut_24 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_25'] = x_member_balances__mutmut_25 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_26'] = x_member_balances__mutmut_26 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_27'] = x_member_balances__mutmut_27 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_28'] = x_member_balances__mutmut_28 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_29'] = x_member_balances__mutmut_29 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_30'] = x_member_balances__mutmut_30 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_31'] = x_member_balances__mutmut_31 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_32'] = x_member_balances__mutmut_32 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_33'] = x_member_balances__mutmut_33 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_34'] = x_member_balances__mutmut_34 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_35'] = x_member_balances__mutmut_35 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_36'] = x_member_balances__mutmut_36 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_37'] = x_member_balances__mutmut_37 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_38'] = x_member_balances__mutmut_38 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_39'] = x_member_balances__mutmut_39 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_40'] = x_member_balances__mutmut_40 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_41'] = x_member_balances__mutmut_41 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_42'] = x_member_balances__mutmut_42 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_43'] = x_member_balances__mutmut_43 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_44'] = x_member_balances__mutmut_44 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_45'] = x_member_balances__mutmut_45 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_46'] = x_member_balances__mutmut_46 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_47'] = x_member_balances__mutmut_47 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_48'] = x_member_balances__mutmut_48 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_49'] = x_member_balances__mutmut_49 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_50'] = x_member_balances__mutmut_50 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_51'] = x_member_balances__mutmut_51 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_52'] = x_member_balances__mutmut_52 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_53'] = x_member_balances__mutmut_53 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_54'] = x_member_balances__mutmut_54 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_55'] = x_member_balances__mutmut_55 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_56'] = x_member_balances__mutmut_56 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_57'] = x_member_balances__mutmut_57 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_58'] = x_member_balances__mutmut_58 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_59'] = x_member_balances__mutmut_59 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_60'] = x_member_balances__mutmut_60 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_61'] = x_member_balances__mutmut_61 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_62'] = x_member_balances__mutmut_62 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_63'] = x_member_balances__mutmut_63 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_64'] = x_member_balances__mutmut_64 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_65'] = x_member_balances__mutmut_65 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_66'] = x_member_balances__mutmut_66 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_67'] = x_member_balances__mutmut_67 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_68'] = x_member_balances__mutmut_68 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_69'] = x_member_balances__mutmut_69 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_70'] = x_member_balances__mutmut_70 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_71'] = x_member_balances__mutmut_71 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_72'] = x_member_balances__mutmut_72 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_73'] = x_member_balances__mutmut_73 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_74'] = x_member_balances__mutmut_74 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_75'] = x_member_balances__mutmut_75 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_76'] = x_member_balances__mutmut_76 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_77'] = x_member_balances__mutmut_77 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_78'] = x_member_balances__mutmut_78 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_79'] = x_member_balances__mutmut_79 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_80'] = x_member_balances__mutmut_80 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_81'] = x_member_balances__mutmut_81 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_82'] = x_member_balances__mutmut_82 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_83'] = x_member_balances__mutmut_83 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_84'] = x_member_balances__mutmut_84 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_85'] = x_member_balances__mutmut_85 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_86'] = x_member_balances__mutmut_86 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_87'] = x_member_balances__mutmut_87 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_88'] = x_member_balances__mutmut_88 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_89'] = x_member_balances__mutmut_89 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_90'] = x_member_balances__mutmut_90 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_91'] = x_member_balances__mutmut_91 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_92'] = x_member_balances__mutmut_92 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_93'] = x_member_balances__mutmut_93 # type: ignore # mutmut generated
mutants_x_member_balances__mutmut['x_member_balances__mutmut_94'] = x_member_balances__mutmut_94 # type: ignore # mutmut generated
