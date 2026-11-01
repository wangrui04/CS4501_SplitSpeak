
from __future__ import annotations

from pydantic import ValidationError
from backend.schemas import ParsedExpense


class LlmError(Exception):
    pass


class FakeLlmClient:
    def __init__(self, scripted):
        self.scripted = list(scripted)
        self.calls = []

    def parse(self, *, messages, roster, current_user):
        self.calls.append({
            "messages": [dict(message) for message in messages],
            "roster": list(roster),
            "current_user": current_user,
        })

        if not self.scripted:
            raise LlmError("Scripted LLM exhausted")

        return self.scripted.pop(0)


class DemoLlmClient:
    """
    Demo LLM client for local interactive browser testing when ANTHROPIC_API_KEY is not set.
    Parses user expense stories and demo examples deterministically.
    """

    def parse(self, *, messages, roster, current_user):
        last_msg = messages[-1]["content"] if messages else ""
        text = last_msg.lower()
        all_text = " ".join(m.get("content", "") for m in messages).lower()

        # US-05 multi-turn clarification (missing prices)
        if "nacho" in all_text and "drink" in all_text:
            if "16" in text or "5" in text:
                return {
                    "description": "Dinner",
                    "payer": "ME",
                    "items": [
                        {
                            "name": "Nachos",
                            "unitPrice": "16.00",
                            "quantity": 1,
                            "participants": {"mode": "only", "names": ["ME", "Kayla"]},
                        },
                        {
                            "name": "Drinks",
                            "unitPrice": "5.00",
                            "quantity": 2,
                            "participants": {"mode": "only", "names": ["Rui"]},
                        },
                    ],
                    "charges": [],
                    "statedTotal": "26.00",
                    "openQuestions": [],
                }
            return {
                "description": "Dinner",
                "payer": "ME",
                "items": [
                    {
                        "name": "Nachos",
                        "unitPrice": None,
                        "quantity": 1,
                        "participants": {"mode": "only", "names": ["ME", "Kayla"]},
                    },
                    {
                        "name": "Drinks",
                        "unitPrice": None,
                        "quantity": 2,
                        "participants": {"mode": "only", "names": ["Rui"]},
                    },
                ],
                "charges": [],
                "statedTotal": None,
                "openQuestions": [
                    {
                        "field": "items.unitPrice",
                        "question": "How much were the nachos and each drink?",
                    }
                ],
            }

        # US-04: Unequal quantities + proportional tip
        if "drink" in text and "tip" in text and "proportional" in text:
            return {
                "description": "Dinner",
                "payer": "ME",
                "items": [
                    {
                        "name": "Drinks",
                        "unitPrice": "10.00",
                        "quantity": 2,
                        "participants": {"mode": "only", "names": ["Kayla"]},
                    },
                    {
                        "name": "Drink",
                        "unitPrice": "10.00",
                        "quantity": 1,
                        "participants": {"mode": "only", "names": ["Rui"]},
                    },
                ],
                "charges": [
                    {
                        "kind": "tip",
                        "amount": "6.00",
                        "percent": None,
                        "method": "proportional",
                    }
                ],
                "statedTotal": "36.00",
                "openQuestions": [],
            }

        # US-03: Multi-item splitting
        if "nacho" in text and ("burger" in text or "pasta" in text):
            return {
                "description": "Dinner",
                "payer": "ME",
                "items": [
                    {
                        "name": "Nachos",
                        "unitPrice": "12.00",
                        "quantity": 1,
                        "participants": {"mode": "only", "names": ["ME", "Kayla"]},
                    },
                    {
                        "name": "Burger",
                        "unitPrice": "15.00",
                        "quantity": 1,
                        "participants": {"mode": "only", "names": ["Rui"]},
                    },
                    {
                        "name": "Pasta",
                        "unitPrice": "15.00",
                        "quantity": 1,
                        "participants": {"mode": "only", "names": ["Kayla"]},
                    },
                ],
                "charges": [],
                "statedTotal": "42.00",
                "openQuestions": [],
            }

        # US-02: Selected member splitting / exclusion
        if "except" in text or "only" in text or "groceries" in text:
            import re

            m = re.search(r"\$?(\d+(?:\.\d{1,2})?)", text)
            amount = m.group(1) if m else "24.00"
            if "." not in amount:
                amount = f"{amount}.00"

            if "except" in text:
                excluded = [name for name in roster if name.lower() in text and name.lower() != "me"]
                if not excluded:
                    excluded = ["ME"]
                participants = {"mode": "all_except", "names": excluded}
            else:
                names = [name for name in roster if name.lower() in text and name.lower() != "me"]
                participants = {"mode": "only", "names": names if names else ["Kayla", "Rui"]}

            return {
                "description": "Groceries",
                "payer": "ME",
                "items": [
                    {
                        "name": "Groceries",
                        "unitPrice": amount,
                        "quantity": 1,
                        "participants": participants,
                    }
                ],
                "charges": [],
                "statedTotal": amount,
                "openQuestions": [],
            }

        # Default US-01: Equal split of specified or default amount
        import re

        m = re.search(r"\$?(\d+(?:\.\d{1,2})?)", text)
        amount = m.group(1) if m else "30.00"
        if "." not in amount:
            amount = f"{amount}.00"

        return {
            "description": "Dinner",
            "payer": "ME",
            "items": [
                {
                    "name": "Dinner",
                    "unitPrice": amount,
                    "quantity": 1,
                    "participants": {"mode": "all", "names": []},
                }
            ],
            "charges": [],
            "statedTotal": amount,
            "openQuestions": [],
        }


class ClaudeLlmClient:
    def __init__(
        self,
        api_key,
        model="claude-sonnet-5-5",
        sdk=None,
    ):
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY must be set"
            )

        self.model = model

        if sdk is None:
            from anthropic import Anthropic

            sdk = Anthropic(
                api_key=api_key,
                timeout=20.0,
                max_retries=0,
            )

        self.sdk = sdk

    def parse(self, *, messages, roster, current_user):
        system_prompt = (
            "Extract structured expense data. "
            "Never calculate shares or totals. "
            "Never invent amounts, payer, tax, or tip. "
            "Represent I/me as ME. "
            "Use all_except for everyone except a member. "
            "Ask about unknown details using openQuestions. "
            "Correct name typos only when unambiguous. "
            "Ask about ambiguous participant references. "
            f"Group roster: {roster}. "
            f"Signed-in user: {current_user}."
        )

        last_error = None

        for attempt in range(2):
            try:
                request_messages = [
                    dict(message)
                    for message in messages
                ]

                if attempt and last_error is not None:
                    request_messages.append({
                        "role": "user",
                        "content": (
                            "Previous tool response invalid: "
                            f"{last_error}. "
                            "Return a corrected structured tool call."
                        ),
                    })

                response = self.sdk.messages.create(
                    model=self.model,
                    max_tokens=2048,
                    temperature=0,
                    system=system_prompt,
                    messages=request_messages,
                    tools=[{
                        "name": "parse_expense",
                        "description": (
                            "Extract expense details only"
                        ),
                        "input_schema": (
                            ParsedExpense.model_json_schema()
                        ),
                    }],
                    tool_choice={
                        "type": "tool",
                        "name": "parse_expense",
                    },
                )

                blocks = [
                    block
                    for block in response.content
                    if (
                        getattr(block, "type", None)
                        == "tool_use"
                        and getattr(block, "name", None)
                        == "parse_expense"
                    )
                ]

                if not blocks:
                    raise LlmError(
                        "LLM_INVALID_OUTPUT: "
                        "missing structured tool call"
                    )

                parsed = ParsedExpense.model_validate(
                    blocks[0].input
                )

                return parsed.model_dump()

            except (ValidationError, LlmError) as exc:
                last_error = str(exc)

            except (ConnectionError, TimeoutError):
                last_error = "Temporary network failure"

            except Exception as exc:
                # Anthropic SDK uses dedicated error types.
                if exc.__class__.__name__ in (
                    "APIConnectionError",
                    "APITimeoutError",
                ):
                    last_error = "Temporary network failure"
                else:
                    raise LlmError(
                        "LLM_REQUEST_FAILED"
                    ) from None

        raise LlmError(
            "LLM_INVALID_OUTPUT: " + str(last_error)
        )
