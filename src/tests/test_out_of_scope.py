"""Issue #54: loans, interest, and repayments are out of scope.

Red-team Critical Issue 3: "Rui lent me $20 at 5% interest each day..."
was treated as an expense, and the app asked question after question
that could never lead to a valid preview. The model now flags such
messages and the app answers with a fixed message on the first turn.
"""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend.config import OUT_OF_SCOPE_MESSAGES, SYSTEM_PROMPT
from backend.database import create_database, seed_database
from backend.llm import PARSED_EXPENSE_SCHEMA, FakeLlmClient
from backend.main import create_app
from backend.pipeline import parse_turn
from backend.repository import list_expenses
from backend.schemas import ParsedExpense


ROSTER = ["Sarah", "Kayla", "Rui"]
SECRET = "test-secret-with-at-least-32-characters"
LOAN = "Rui lent me $20 at 5% interest each day and it's been 2 days"


def expense(unsupported=None, **overrides):
    data = {
        "description": "Loan",
        "payer": "Rui",
        "items": [
            {
                "name": "Loan",
                "quantity": 1,
                "unitPrice": "20",
                "participants": {"mode": "only", "names": ["ME"]},
            }
        ],
        "charges": [],
        "statedTotal": None,
        "openQuestions": [],
        **overrides,
    }
    if unsupported is not None:
        data["unsupported"] = unsupported
    return data


def run(raw, text=LOAN):
    return parse_turn(
        llm=FakeLlmClient([raw]),
        conversation=[{"role": "user", "content": text}],
        roster=ROSTER,
        current_user="Kayla",
    )


# ------------------------------------------------------------------ schema


def test_schema_accepts_the_unsupported_flag():
    assert ParsedExpense.model_validate(expense("loan")).unsupported == "loan"
    assert ParsedExpense.model_validate(expense("other")).unsupported == "other"


def test_schema_flag_is_optional():
    assert ParsedExpense.model_validate(expense()).unsupported is None


def test_schema_rejects_unknown_flag_values():
    with pytest.raises(ValidationError):
        ParsedExpense.model_validate(expense("mortgage"))


def test_llm_schema_lists_the_flag_as_optional():
    assert "unsupported" in PARSED_EXPENSE_SCHEMA["properties"]
    assert "unsupported" not in PARSED_EXPENSE_SCHEMA["required"]


# ---------------------------------------------------------------- pipeline


def test_loan_gets_the_fixed_message_on_the_first_turn():
    result = run(expense("loan"))

    assert result == {"type": "unresolved", "reason": OUT_OF_SCOPE_MESSAGES["loan"]}


def test_flag_wins_over_the_models_own_questions():
    raw = expense("loan", openQuestions=[{"field": "payer", "question": "Who paid?"}])

    result = run(raw)

    assert result == {"type": "unresolved", "reason": OUT_OF_SCOPE_MESSAGES["loan"]}


def test_other_unsupported_requests_get_their_own_message():
    result = run(expense("other"), text="what's the weather")

    assert result == {"type": "unresolved", "reason": OUT_OF_SCOPE_MESSAGES["other"]}


def test_loan_message_points_to_settle_up_and_manual_entry():
    message = OUT_OF_SCOPE_MESSAGES["loan"]

    assert "Settle up" in message
    assert "manual entry" in message


def test_lending_mentioned_in_passing_is_still_an_expense():
    text = "I lent Rui my card and Rui paid for dinner, $30 split evenly"
    raw = expense(
        description="Dinner",
        items=[
            {
                "name": "Dinner",
                "quantity": 1,
                "unitPrice": "30",
                "participants": {"mode": "all", "names": []},
            }
        ],
    )

    result = run(raw, text=text)

    assert result["type"] == "preview", result


# --------------------------------------------------------------------- API


def test_api_returns_manual_fallback_and_saves_nothing():
    db = create_database(":memory:")
    seed_database(db)
    client = TestClient(create_app(
        db=db, session_secret=SECRET, llm=FakeLlmClient([expense("loan")])
    ))
    client.post("/api/session", json={"name": "Kayla"})

    body = client.post("/api/chat", json={"groupId": 1, "message": LOAN}).json()

    assert body["type"] == "unresolved"
    assert body["fallback"] == "manual"
    assert body["reason"] == OUT_OF_SCOPE_MESSAGES["loan"]
    assert list_expenses(db, 1) == []
    assert client.get("/api/groups/1").json()["summary"]["youOwe"] == 0


# ------------------------------------------------------------------ prompt


def test_system_prompt_explains_the_flag():
    assert "set unsupported to" in SYSTEM_PROMPT
    assert "lent" in SYSTEM_PROMPT  # the in-passing exception
