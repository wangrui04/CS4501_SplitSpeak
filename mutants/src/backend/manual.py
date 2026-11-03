"""Manual equal-split entry, using the same engine and validator as AI."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, ValidationError

from backend.allocation import (
    allocate_charges,
    allocate_items,
    parse_money_to_cents,
)
from backend.validator import validate


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class ManualExpenseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str
    amount: str | int | float
    paidBy: str
    splitBetween: list[str]


class ManualEntryError(ValueError):
    pass
mutants_x__amount_text__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__amount_text__mutmut)
def _amount_text(amount) -> str:
    if isinstance(amount, bool):
        raise ManualEntryError("Amount must be a number")
    # str() keeps the user's decimals, so 12.345 is rejected below.
    return str(amount).strip()


def x__amount_text__mutmut_orig(amount) -> str:
    if isinstance(amount, bool):
        raise ManualEntryError("Amount must be a number")
    # str() keeps the user's decimals, so 12.345 is rejected below.
    return str(amount).strip()


def x__amount_text__mutmut_1(amount) -> str:
    if isinstance(amount, bool):
        raise ManualEntryError(None)
    # str() keeps the user's decimals, so 12.345 is rejected below.
    return str(amount).strip()


def x__amount_text__mutmut_2(amount) -> str:
    if isinstance(amount, bool):
        raise ManualEntryError("XXAmount must be a numberXX")
    # str() keeps the user's decimals, so 12.345 is rejected below.
    return str(amount).strip()


def x__amount_text__mutmut_3(amount) -> str:
    if isinstance(amount, bool):
        raise ManualEntryError("amount must be a number")
    # str() keeps the user's decimals, so 12.345 is rejected below.
    return str(amount).strip()


def x__amount_text__mutmut_4(amount) -> str:
    if isinstance(amount, bool):
        raise ManualEntryError("AMOUNT MUST BE A NUMBER")
    # str() keeps the user's decimals, so 12.345 is rejected below.
    return str(amount).strip()


def x__amount_text__mutmut_5(amount) -> str:
    if isinstance(amount, bool):
        raise ManualEntryError("Amount must be a number")
    # str() keeps the user's decimals, so 12.345 is rejected below.
    return str(None).strip()

mutants_x__amount_text__mutmut['_mutmut_orig'] = x__amount_text__mutmut_orig # type: ignore # mutmut generated
mutants_x__amount_text__mutmut['x__amount_text__mutmut_1'] = x__amount_text__mutmut_1 # type: ignore # mutmut generated
mutants_x__amount_text__mutmut['x__amount_text__mutmut_2'] = x__amount_text__mutmut_2 # type: ignore # mutmut generated
mutants_x__amount_text__mutmut['x__amount_text__mutmut_3'] = x__amount_text__mutmut_3 # type: ignore # mutmut generated
mutants_x__amount_text__mutmut['x__amount_text__mutmut_4'] = x__amount_text__mutmut_4 # type: ignore # mutmut generated
mutants_x__amount_text__mutmut['x__amount_text__mutmut_5'] = x__amount_text__mutmut_5 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build_manual_expense__mutmut)
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


def x_build_manual_expense__mutmut_orig(payload: dict, roster: list[str]) -> dict:
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


def x_build_manual_expense__mutmut_1(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = None
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


def x_build_manual_expense__mutmut_2(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(None)
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


def x_build_manual_expense__mutmut_3(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            None
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


def x_build_manual_expense__mutmut_4(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "XXdescription, amount, paidBy, and splitBetween are requiredXX"
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


def x_build_manual_expense__mutmut_5(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "description, amount, paidby, and splitbetween are required"
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


def x_build_manual_expense__mutmut_6(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "DESCRIPTION, AMOUNT, PAIDBY, AND SPLITBETWEEN ARE REQUIRED"
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


def x_build_manual_expense__mutmut_7(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "description, amount, paidBy, and splitBetween are required"
        ) from None

    description = None
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


def x_build_manual_expense__mutmut_8(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "description, amount, paidBy, and splitBetween are required"
        ) from None

    description = request.description.strip()
    if description:
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


def x_build_manual_expense__mutmut_9(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "description, amount, paidBy, and splitBetween are required"
        ) from None

    description = request.description.strip()
    if not description:
        raise ManualEntryError(None)

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


def x_build_manual_expense__mutmut_10(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "description, amount, paidBy, and splitBetween are required"
        ) from None

    description = request.description.strip()
    if not description:
        raise ManualEntryError("XXDescription is requiredXX")

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


def x_build_manual_expense__mutmut_11(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "description, amount, paidBy, and splitBetween are required"
        ) from None

    description = request.description.strip()
    if not description:
        raise ManualEntryError("description is required")

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


def x_build_manual_expense__mutmut_12(payload: dict, roster: list[str]) -> dict:
    """Validate a manual form and return a save_expense() payload."""
    try:
        request = ManualExpenseRequest.model_validate(payload)
    except ValidationError:
        raise ManualEntryError(
            "description, amount, paidBy, and splitBetween are required"
        ) from None

    description = request.description.strip()
    if not description:
        raise ManualEntryError("DESCRIPTION IS REQUIRED")

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


def x_build_manual_expense__mutmut_13(payload: dict, roster: list[str]) -> dict:
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

    amount = None
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


def x_build_manual_expense__mutmut_14(payload: dict, roster: list[str]) -> dict:
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

    amount = _amount_text(None)
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


def x_build_manual_expense__mutmut_15(payload: dict, roster: list[str]) -> dict:
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
        cents = None
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


def x_build_manual_expense__mutmut_16(payload: dict, roster: list[str]) -> dict:
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
        cents = parse_money_to_cents(None)
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


def x_build_manual_expense__mutmut_17(payload: dict, roster: list[str]) -> dict:
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
            None
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


def x_build_manual_expense__mutmut_18(payload: dict, roster: list[str]) -> dict:
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
            "XXAmount must be a number with at most 2 decimalsXX"
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


def x_build_manual_expense__mutmut_19(payload: dict, roster: list[str]) -> dict:
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
            "amount must be a number with at most 2 decimals"
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


def x_build_manual_expense__mutmut_20(payload: dict, roster: list[str]) -> dict:
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
            "AMOUNT MUST BE A NUMBER WITH AT MOST 2 DECIMALS"
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


def x_build_manual_expense__mutmut_21(payload: dict, roster: list[str]) -> dict:
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
    if cents < 0:
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


def x_build_manual_expense__mutmut_22(payload: dict, roster: list[str]) -> dict:
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
    if cents <= 1:
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


def x_build_manual_expense__mutmut_23(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(None)

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


def x_build_manual_expense__mutmut_24(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError("XXAmount must be greater than 0XX")

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


def x_build_manual_expense__mutmut_25(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError("amount must be greater than 0")

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


def x_build_manual_expense__mutmut_26(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError("AMOUNT MUST BE GREATER THAN 0")

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


def x_build_manual_expense__mutmut_27(payload: dict, roster: list[str]) -> dict:
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

    if request.paidBy in roster:
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


def x_build_manual_expense__mutmut_28(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(None)

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


def x_build_manual_expense__mutmut_29(payload: dict, roster: list[str]) -> dict:
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

    if request.splitBetween:
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


def x_build_manual_expense__mutmut_30(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(None)

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


def x_build_manual_expense__mutmut_31(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError("XXChoose at least one person to split withXX")

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


def x_build_manual_expense__mutmut_32(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError("choose at least one person to split with")

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


def x_build_manual_expense__mutmut_33(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError("CHOOSE AT LEAST ONE PERSON TO SPLIT WITH")

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


def x_build_manual_expense__mutmut_34(payload: dict, roster: list[str]) -> dict:
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
        if name in roster:
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


def x_build_manual_expense__mutmut_35(payload: dict, roster: list[str]) -> dict:
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
            raise ManualEntryError(None)

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


def x_build_manual_expense__mutmut_36(payload: dict, roster: list[str]) -> dict:
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

    parsed = None

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


def x_build_manual_expense__mutmut_37(payload: dict, roster: list[str]) -> dict:
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
        "XXdescriptionXX": description,
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


def x_build_manual_expense__mutmut_38(payload: dict, roster: list[str]) -> dict:
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
        "DESCRIPTION": description,
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


def x_build_manual_expense__mutmut_39(payload: dict, roster: list[str]) -> dict:
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
        "XXpayerXX": request.paidBy,
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


def x_build_manual_expense__mutmut_40(payload: dict, roster: list[str]) -> dict:
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
        "PAYER": request.paidBy,
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


def x_build_manual_expense__mutmut_41(payload: dict, roster: list[str]) -> dict:
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
        "XXitemsXX": [{
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


def x_build_manual_expense__mutmut_42(payload: dict, roster: list[str]) -> dict:
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
        "ITEMS": [{
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


def x_build_manual_expense__mutmut_43(payload: dict, roster: list[str]) -> dict:
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
            "XXnameXX": description,
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


def x_build_manual_expense__mutmut_44(payload: dict, roster: list[str]) -> dict:
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
            "NAME": description,
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


def x_build_manual_expense__mutmut_45(payload: dict, roster: list[str]) -> dict:
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
            "XXquantityXX": 1,
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


def x_build_manual_expense__mutmut_46(payload: dict, roster: list[str]) -> dict:
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
            "QUANTITY": 1,
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


def x_build_manual_expense__mutmut_47(payload: dict, roster: list[str]) -> dict:
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
            "quantity": 2,
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


def x_build_manual_expense__mutmut_48(payload: dict, roster: list[str]) -> dict:
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
            "XXunitPriceXX": amount.removeprefix("$"),
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


def x_build_manual_expense__mutmut_49(payload: dict, roster: list[str]) -> dict:
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
            "unitprice": amount.removeprefix("$"),
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


def x_build_manual_expense__mutmut_50(payload: dict, roster: list[str]) -> dict:
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
            "UNITPRICE": amount.removeprefix("$"),
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


def x_build_manual_expense__mutmut_51(payload: dict, roster: list[str]) -> dict:
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
            "unitPrice": amount.removeprefix(None),
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


def x_build_manual_expense__mutmut_52(payload: dict, roster: list[str]) -> dict:
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
            "unitPrice": amount.removesuffix("$"),
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


def x_build_manual_expense__mutmut_53(payload: dict, roster: list[str]) -> dict:
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
            "unitPrice": amount.removeprefix("XX$XX"),
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


def x_build_manual_expense__mutmut_54(payload: dict, roster: list[str]) -> dict:
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
            "XXparticipantsXX": {
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


def x_build_manual_expense__mutmut_55(payload: dict, roster: list[str]) -> dict:
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
            "PARTICIPANTS": {
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


def x_build_manual_expense__mutmut_56(payload: dict, roster: list[str]) -> dict:
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
                "XXmodeXX": "only",
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


def x_build_manual_expense__mutmut_57(payload: dict, roster: list[str]) -> dict:
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
                "MODE": "only",
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


def x_build_manual_expense__mutmut_58(payload: dict, roster: list[str]) -> dict:
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
                "mode": "XXonlyXX",
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


def x_build_manual_expense__mutmut_59(payload: dict, roster: list[str]) -> dict:
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
                "mode": "ONLY",
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


def x_build_manual_expense__mutmut_60(payload: dict, roster: list[str]) -> dict:
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
                "XXnamesXX": list(request.splitBetween),
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


def x_build_manual_expense__mutmut_61(payload: dict, roster: list[str]) -> dict:
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
                "NAMES": list(request.splitBetween),
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


def x_build_manual_expense__mutmut_62(payload: dict, roster: list[str]) -> dict:
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
                "names": list(None),
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


def x_build_manual_expense__mutmut_63(payload: dict, roster: list[str]) -> dict:
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
        "XXchargesXX": [],
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


def x_build_manual_expense__mutmut_64(payload: dict, roster: list[str]) -> dict:
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
        "CHARGES": [],
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


def x_build_manual_expense__mutmut_65(payload: dict, roster: list[str]) -> dict:
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
        "XXstatedTotalXX": None,
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


def x_build_manual_expense__mutmut_66(payload: dict, roster: list[str]) -> dict:
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
        "statedtotal": None,
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


def x_build_manual_expense__mutmut_67(payload: dict, roster: list[str]) -> dict:
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
        "STATEDTOTAL": None,
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


def x_build_manual_expense__mutmut_68(payload: dict, roster: list[str]) -> dict:
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
        "XXopenQuestionsXX": [],
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


def x_build_manual_expense__mutmut_69(payload: dict, roster: list[str]) -> dict:
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
        "openquestions": [],
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


def x_build_manual_expense__mutmut_70(payload: dict, roster: list[str]) -> dict:
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
        "OPENQUESTIONS": [],
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


def x_build_manual_expense__mutmut_71(payload: dict, roster: list[str]) -> dict:
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

    allocation = None
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


def x_build_manual_expense__mutmut_72(payload: dict, roster: list[str]) -> dict:
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
        None, request.paidBy, roster, request.paidBy
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


def x_build_manual_expense__mutmut_73(payload: dict, roster: list[str]) -> dict:
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
        parsed["items"], None, roster, request.paidBy
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


def x_build_manual_expense__mutmut_74(payload: dict, roster: list[str]) -> dict:
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
        parsed["items"], request.paidBy, None, request.paidBy
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


def x_build_manual_expense__mutmut_75(payload: dict, roster: list[str]) -> dict:
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
        parsed["items"], request.paidBy, roster, None
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


def x_build_manual_expense__mutmut_76(payload: dict, roster: list[str]) -> dict:
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
        request.paidBy, roster, request.paidBy
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


def x_build_manual_expense__mutmut_77(payload: dict, roster: list[str]) -> dict:
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
        parsed["items"], roster, request.paidBy
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


def x_build_manual_expense__mutmut_78(payload: dict, roster: list[str]) -> dict:
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
        parsed["items"], request.paidBy, request.paidBy
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


def x_build_manual_expense__mutmut_79(payload: dict, roster: list[str]) -> dict:
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
        parsed["items"], request.paidBy, roster, )
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


def x_build_manual_expense__mutmut_80(payload: dict, roster: list[str]) -> dict:
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
        parsed["XXitemsXX"], request.paidBy, roster, request.paidBy
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


def x_build_manual_expense__mutmut_81(payload: dict, roster: list[str]) -> dict:
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
        parsed["ITEMS"], request.paidBy, roster, request.paidBy
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


def x_build_manual_expense__mutmut_82(payload: dict, roster: list[str]) -> dict:
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
    allocation = None

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


def x_build_manual_expense__mutmut_83(payload: dict, roster: list[str]) -> dict:
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
    allocation = allocate_charges(None, allocation, request.paidBy, roster)

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


def x_build_manual_expense__mutmut_84(payload: dict, roster: list[str]) -> dict:
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
    allocation = allocate_charges([], None, request.paidBy, roster)

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


def x_build_manual_expense__mutmut_85(payload: dict, roster: list[str]) -> dict:
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
    allocation = allocate_charges([], allocation, None, roster)

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


def x_build_manual_expense__mutmut_86(payload: dict, roster: list[str]) -> dict:
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
    allocation = allocate_charges([], allocation, request.paidBy, None)

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


def x_build_manual_expense__mutmut_87(payload: dict, roster: list[str]) -> dict:
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
    allocation = allocate_charges(allocation, request.paidBy, roster)

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


def x_build_manual_expense__mutmut_88(payload: dict, roster: list[str]) -> dict:
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
    allocation = allocate_charges([], request.paidBy, roster)

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


def x_build_manual_expense__mutmut_89(payload: dict, roster: list[str]) -> dict:
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
    allocation = allocate_charges([], allocation, roster)

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


def x_build_manual_expense__mutmut_90(payload: dict, roster: list[str]) -> dict:
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
    allocation = allocate_charges([], allocation, request.paidBy, )

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


def x_build_manual_expense__mutmut_91(payload: dict, roster: list[str]) -> dict:
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

    result = None
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


def x_build_manual_expense__mutmut_92(payload: dict, roster: list[str]) -> dict:
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

    result = validate(None, allocation, roster)
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


def x_build_manual_expense__mutmut_93(payload: dict, roster: list[str]) -> dict:
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

    result = validate(parsed, None, roster)
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


def x_build_manual_expense__mutmut_94(payload: dict, roster: list[str]) -> dict:
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

    result = validate(parsed, allocation, None)
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


def x_build_manual_expense__mutmut_95(payload: dict, roster: list[str]) -> dict:
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

    result = validate(allocation, roster)
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


def x_build_manual_expense__mutmut_96(payload: dict, roster: list[str]) -> dict:
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

    result = validate(parsed, roster)
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


def x_build_manual_expense__mutmut_97(payload: dict, roster: list[str]) -> dict:
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

    result = validate(parsed, allocation, )
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


def x_build_manual_expense__mutmut_98(payload: dict, roster: list[str]) -> dict:
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
    if result["ok"]:
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


def x_build_manual_expense__mutmut_99(payload: dict, roster: list[str]) -> dict:
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
    if not result["XXokXX"]:
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


def x_build_manual_expense__mutmut_100(payload: dict, roster: list[str]) -> dict:
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
    if not result["OK"]:
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


def x_build_manual_expense__mutmut_101(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(None)

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


def x_build_manual_expense__mutmut_102(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(result["XXerrorsXX"][0]["message"])

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


def x_build_manual_expense__mutmut_103(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(result["ERRORS"][0]["message"])

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


def x_build_manual_expense__mutmut_104(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(result["errors"][1]["message"])

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


def x_build_manual_expense__mutmut_105(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(result["errors"][0]["XXmessageXX"])

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


def x_build_manual_expense__mutmut_106(payload: dict, roster: list[str]) -> dict:
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
        raise ManualEntryError(result["errors"][0]["MESSAGE"])

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


def x_build_manual_expense__mutmut_107(payload: dict, roster: list[str]) -> dict:
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
        "XXdescriptionXX": description,
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


def x_build_manual_expense__mutmut_108(payload: dict, roster: list[str]) -> dict:
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
        "DESCRIPTION": description,
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


def x_build_manual_expense__mutmut_109(payload: dict, roster: list[str]) -> dict:
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
        "XXpayerXX": request.paidBy,
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


def x_build_manual_expense__mutmut_110(payload: dict, roster: list[str]) -> dict:
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
        "PAYER": request.paidBy,
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


def x_build_manual_expense__mutmut_111(payload: dict, roster: list[str]) -> dict:
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
        "XXtotalCentsXX": allocation["totalCents"],
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


def x_build_manual_expense__mutmut_112(payload: dict, roster: list[str]) -> dict:
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
        "totalcents": allocation["totalCents"],
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


def x_build_manual_expense__mutmut_113(payload: dict, roster: list[str]) -> dict:
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
        "TOTALCENTS": allocation["totalCents"],
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


def x_build_manual_expense__mutmut_114(payload: dict, roster: list[str]) -> dict:
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
        "totalCents": allocation["XXtotalCentsXX"],
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


def x_build_manual_expense__mutmut_115(payload: dict, roster: list[str]) -> dict:
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
        "totalCents": allocation["totalcents"],
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


def x_build_manual_expense__mutmut_116(payload: dict, roster: list[str]) -> dict:
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
        "totalCents": allocation["TOTALCENTS"],
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


def x_build_manual_expense__mutmut_117(payload: dict, roster: list[str]) -> dict:
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
        "XXsharesXX": [
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


def x_build_manual_expense__mutmut_118(payload: dict, roster: list[str]) -> dict:
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
        "SHARES": [
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


def x_build_manual_expense__mutmut_119(payload: dict, roster: list[str]) -> dict:
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
            {"XXnameXX": name, "cents": allocation["shares"][name]}
            for name in roster
        ],
        "payments": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_120(payload: dict, roster: list[str]) -> dict:
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
            {"NAME": name, "cents": allocation["shares"][name]}
            for name in roster
        ],
        "payments": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_121(payload: dict, roster: list[str]) -> dict:
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
            {"name": name, "XXcentsXX": allocation["shares"][name]}
            for name in roster
        ],
        "payments": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_122(payload: dict, roster: list[str]) -> dict:
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
            {"name": name, "CENTS": allocation["shares"][name]}
            for name in roster
        ],
        "payments": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_123(payload: dict, roster: list[str]) -> dict:
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
            {"name": name, "cents": allocation["XXsharesXX"][name]}
            for name in roster
        ],
        "payments": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_124(payload: dict, roster: list[str]) -> dict:
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
            {"name": name, "cents": allocation["SHARES"][name]}
            for name in roster
        ],
        "payments": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_125(payload: dict, roster: list[str]) -> dict:
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
        "XXpaymentsXX": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_126(payload: dict, roster: list[str]) -> dict:
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
        "PAYMENTS": [
            {"name": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_127(payload: dict, roster: list[str]) -> dict:
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
            {"XXnameXX": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_128(payload: dict, roster: list[str]) -> dict:
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
            {"NAME": name, "cents": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_129(payload: dict, roster: list[str]) -> dict:
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
            {"name": name, "XXcentsXX": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_130(payload: dict, roster: list[str]) -> dict:
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
            {"name": name, "CENTS": cents}
            for name, cents in allocation["paid"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_131(payload: dict, roster: list[str]) -> dict:
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
            for name, cents in allocation["XXpaidXX"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_132(payload: dict, roster: list[str]) -> dict:
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
            for name, cents in allocation["PAID"].items()
            if cents
        ],
        "source": "manual",
    }


def x_build_manual_expense__mutmut_133(payload: dict, roster: list[str]) -> dict:
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
        "XXsourceXX": "manual",
    }


def x_build_manual_expense__mutmut_134(payload: dict, roster: list[str]) -> dict:
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
        "SOURCE": "manual",
    }


def x_build_manual_expense__mutmut_135(payload: dict, roster: list[str]) -> dict:
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
        "source": "XXmanualXX",
    }


def x_build_manual_expense__mutmut_136(payload: dict, roster: list[str]) -> dict:
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
        "source": "MANUAL",
    }

mutants_x_build_manual_expense__mutmut['_mutmut_orig'] = x_build_manual_expense__mutmut_orig # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_1'] = x_build_manual_expense__mutmut_1 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_2'] = x_build_manual_expense__mutmut_2 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_3'] = x_build_manual_expense__mutmut_3 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_4'] = x_build_manual_expense__mutmut_4 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_5'] = x_build_manual_expense__mutmut_5 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_6'] = x_build_manual_expense__mutmut_6 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_7'] = x_build_manual_expense__mutmut_7 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_8'] = x_build_manual_expense__mutmut_8 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_9'] = x_build_manual_expense__mutmut_9 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_10'] = x_build_manual_expense__mutmut_10 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_11'] = x_build_manual_expense__mutmut_11 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_12'] = x_build_manual_expense__mutmut_12 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_13'] = x_build_manual_expense__mutmut_13 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_14'] = x_build_manual_expense__mutmut_14 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_15'] = x_build_manual_expense__mutmut_15 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_16'] = x_build_manual_expense__mutmut_16 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_17'] = x_build_manual_expense__mutmut_17 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_18'] = x_build_manual_expense__mutmut_18 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_19'] = x_build_manual_expense__mutmut_19 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_20'] = x_build_manual_expense__mutmut_20 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_21'] = x_build_manual_expense__mutmut_21 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_22'] = x_build_manual_expense__mutmut_22 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_23'] = x_build_manual_expense__mutmut_23 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_24'] = x_build_manual_expense__mutmut_24 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_25'] = x_build_manual_expense__mutmut_25 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_26'] = x_build_manual_expense__mutmut_26 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_27'] = x_build_manual_expense__mutmut_27 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_28'] = x_build_manual_expense__mutmut_28 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_29'] = x_build_manual_expense__mutmut_29 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_30'] = x_build_manual_expense__mutmut_30 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_31'] = x_build_manual_expense__mutmut_31 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_32'] = x_build_manual_expense__mutmut_32 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_33'] = x_build_manual_expense__mutmut_33 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_34'] = x_build_manual_expense__mutmut_34 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_35'] = x_build_manual_expense__mutmut_35 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_36'] = x_build_manual_expense__mutmut_36 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_37'] = x_build_manual_expense__mutmut_37 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_38'] = x_build_manual_expense__mutmut_38 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_39'] = x_build_manual_expense__mutmut_39 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_40'] = x_build_manual_expense__mutmut_40 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_41'] = x_build_manual_expense__mutmut_41 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_42'] = x_build_manual_expense__mutmut_42 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_43'] = x_build_manual_expense__mutmut_43 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_44'] = x_build_manual_expense__mutmut_44 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_45'] = x_build_manual_expense__mutmut_45 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_46'] = x_build_manual_expense__mutmut_46 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_47'] = x_build_manual_expense__mutmut_47 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_48'] = x_build_manual_expense__mutmut_48 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_49'] = x_build_manual_expense__mutmut_49 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_50'] = x_build_manual_expense__mutmut_50 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_51'] = x_build_manual_expense__mutmut_51 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_52'] = x_build_manual_expense__mutmut_52 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_53'] = x_build_manual_expense__mutmut_53 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_54'] = x_build_manual_expense__mutmut_54 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_55'] = x_build_manual_expense__mutmut_55 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_56'] = x_build_manual_expense__mutmut_56 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_57'] = x_build_manual_expense__mutmut_57 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_58'] = x_build_manual_expense__mutmut_58 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_59'] = x_build_manual_expense__mutmut_59 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_60'] = x_build_manual_expense__mutmut_60 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_61'] = x_build_manual_expense__mutmut_61 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_62'] = x_build_manual_expense__mutmut_62 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_63'] = x_build_manual_expense__mutmut_63 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_64'] = x_build_manual_expense__mutmut_64 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_65'] = x_build_manual_expense__mutmut_65 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_66'] = x_build_manual_expense__mutmut_66 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_67'] = x_build_manual_expense__mutmut_67 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_68'] = x_build_manual_expense__mutmut_68 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_69'] = x_build_manual_expense__mutmut_69 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_70'] = x_build_manual_expense__mutmut_70 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_71'] = x_build_manual_expense__mutmut_71 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_72'] = x_build_manual_expense__mutmut_72 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_73'] = x_build_manual_expense__mutmut_73 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_74'] = x_build_manual_expense__mutmut_74 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_75'] = x_build_manual_expense__mutmut_75 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_76'] = x_build_manual_expense__mutmut_76 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_77'] = x_build_manual_expense__mutmut_77 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_78'] = x_build_manual_expense__mutmut_78 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_79'] = x_build_manual_expense__mutmut_79 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_80'] = x_build_manual_expense__mutmut_80 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_81'] = x_build_manual_expense__mutmut_81 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_82'] = x_build_manual_expense__mutmut_82 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_83'] = x_build_manual_expense__mutmut_83 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_84'] = x_build_manual_expense__mutmut_84 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_85'] = x_build_manual_expense__mutmut_85 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_86'] = x_build_manual_expense__mutmut_86 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_87'] = x_build_manual_expense__mutmut_87 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_88'] = x_build_manual_expense__mutmut_88 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_89'] = x_build_manual_expense__mutmut_89 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_90'] = x_build_manual_expense__mutmut_90 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_91'] = x_build_manual_expense__mutmut_91 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_92'] = x_build_manual_expense__mutmut_92 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_93'] = x_build_manual_expense__mutmut_93 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_94'] = x_build_manual_expense__mutmut_94 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_95'] = x_build_manual_expense__mutmut_95 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_96'] = x_build_manual_expense__mutmut_96 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_97'] = x_build_manual_expense__mutmut_97 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_98'] = x_build_manual_expense__mutmut_98 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_99'] = x_build_manual_expense__mutmut_99 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_100'] = x_build_manual_expense__mutmut_100 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_101'] = x_build_manual_expense__mutmut_101 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_102'] = x_build_manual_expense__mutmut_102 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_103'] = x_build_manual_expense__mutmut_103 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_104'] = x_build_manual_expense__mutmut_104 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_105'] = x_build_manual_expense__mutmut_105 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_106'] = x_build_manual_expense__mutmut_106 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_107'] = x_build_manual_expense__mutmut_107 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_108'] = x_build_manual_expense__mutmut_108 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_109'] = x_build_manual_expense__mutmut_109 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_110'] = x_build_manual_expense__mutmut_110 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_111'] = x_build_manual_expense__mutmut_111 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_112'] = x_build_manual_expense__mutmut_112 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_113'] = x_build_manual_expense__mutmut_113 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_114'] = x_build_manual_expense__mutmut_114 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_115'] = x_build_manual_expense__mutmut_115 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_116'] = x_build_manual_expense__mutmut_116 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_117'] = x_build_manual_expense__mutmut_117 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_118'] = x_build_manual_expense__mutmut_118 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_119'] = x_build_manual_expense__mutmut_119 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_120'] = x_build_manual_expense__mutmut_120 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_121'] = x_build_manual_expense__mutmut_121 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_122'] = x_build_manual_expense__mutmut_122 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_123'] = x_build_manual_expense__mutmut_123 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_124'] = x_build_manual_expense__mutmut_124 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_125'] = x_build_manual_expense__mutmut_125 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_126'] = x_build_manual_expense__mutmut_126 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_127'] = x_build_manual_expense__mutmut_127 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_128'] = x_build_manual_expense__mutmut_128 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_129'] = x_build_manual_expense__mutmut_129 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_130'] = x_build_manual_expense__mutmut_130 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_131'] = x_build_manual_expense__mutmut_131 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_132'] = x_build_manual_expense__mutmut_132 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_133'] = x_build_manual_expense__mutmut_133 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_134'] = x_build_manual_expense__mutmut_134 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_135'] = x_build_manual_expense__mutmut_135 # type: ignore # mutmut generated
mutants_x_build_manual_expense__mutmut['x_build_manual_expense__mutmut_136'] = x_build_manual_expense__mutmut_136 # type: ignore # mutmut generated
