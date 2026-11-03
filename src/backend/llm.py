
from __future__ import annotations

import copy
import json
import logging
from pathlib import Path

from anthropic import transform_schema
from pydantic import ValidationError

from backend.config import (
    DEFAULT_GEMINI_MODEL,
    DEFAULT_LLM_MODEL,
    LLM_FALLBACK_BETA,
    LLM_MAX_ATTEMPTS,
    LLM_MAX_TOKENS,
    LLM_TIMEOUT_SECONDS,
    SYSTEM_PROMPT,
)
from backend.schemas import ParsedExpense

PARSED_EXPENSE_SCHEMA = transform_schema(ParsedExpense)

logger = logging.getLogger("splitwise.llm")


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


FIXTURES_PATH = Path(__file__).parent / "fixtures" / "llm_fixtures.json"


class FixtureLlmClient:
    """TEST-ONLY: returns scripted outputs keyed by the last user message.

    Enabled only with LLM_PROVIDER=fake, for E2E tests and offline
    benchmark smoke runs. It never calls a paid API.
    """

    def __init__(self, path=FIXTURES_PATH):
        self.responses = json.loads(Path(path).read_text())["responses"]
        self.calls = []

    def parse(self, *, messages, roster, current_user):
        last = next(
            message["content"]
            for message in reversed(messages)
            if message["role"] == "user"
        )
        self.calls.append({"message": last, "current_user": current_user})

        if last not in self.responses:
            raise LlmError("No fixture for this message")

        return copy.deepcopy(self.responses[last])


class DemoLlmClient:
    """
    Demo LLM client for local interactive browser testing when ANTHROPIC_API_KEY is not set.
    Parses user expense stories and demo examples deterministically.
    """

    def parse(self, *, messages, roster, current_user):
        last_msg = messages[-1]["content"] if messages else ""
        text = last_msg.lower()
        all_text = " ".join(m.get("content", "") for m in messages).lower()

        # US-06: Typos and unclear instructions ("the rest", "dinr", "nachoes", "riu", "drnks")
        if (
            "the rest" in all_text
            or "dinr" in all_text
            or "nachoes" in all_text
            or "riu" in all_text
            or "drnks" in all_text
        ):
            if any(term in text for term in ["everything", "no", "that's it", "none"]):
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
                "statedTotal": None,
                "openQuestions": [
                    {
                        "field": "charges",
                        "question": (
                            f"I understand that {current_user} and Kayla shared $16 nachos, "
                            "and Rui had two $5 drinks. When you say 'split the rest evenly,' "
                            "is there another charge to split?"
                        ),
                    }
                ],
            }

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
        model=DEFAULT_LLM_MODEL,
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
                timeout=LLM_TIMEOUT_SECONDS,
                max_retries=0,
            )

        self.sdk = sdk

    def parse(self, *, messages, roster, current_user):
        system_prompt = (
            SYSTEM_PROMPT
            + f"\nGroup roster: {roster}."
            + f"\nSigned-in user (ME): {current_user}."
        )

        last_error = None

        for attempt in range(LLM_MAX_ATTEMPTS):
            try:
                request_messages = delimit_user_messages(messages)

                if attempt and last_error is not None:
                    request_messages.append({
                        "role": "user",
                        "content": (
                            "Previous response invalid: "
                            f"{last_error}. "
                            "Return corrected JSON."
                        ),
                    })

                # Sonnet 5.5 rejects forced tool_choice and sampling
                # params, so JSON comes from output_config.format.
                response = self.sdk.beta.messages.create(
                    model=self.model,
                    max_tokens=LLM_MAX_TOKENS,
                    system=system_prompt,
                    messages=request_messages,
                    output_config={
                        "format": {
                            "type": "json_schema",
                            "schema": PARSED_EXPENSE_SCHEMA,
                        },
                    },
                    betas=[LLM_FALLBACK_BETA],
                    fallbacks="default",
                )

                if getattr(response, "stop_reason", None) == "refusal":
                    raise LlmError("LLM_REFUSED")

                texts = [
                    block.text
                    for block in response.content
                    if getattr(block, "type", None) == "text"
                ]

                if not texts:
                    raise LlmError(
                        "LLM_INVALID_OUTPUT: "
                        "missing structured JSON"
                    )

                try:
                    data = json.loads(texts[0])
                except (TypeError, ValueError):
                    raise LlmError(
                        "LLM_INVALID_OUTPUT: response was not JSON"
                    ) from None

                parsed = ParsedExpense.model_validate(data)

                return parsed.model_dump(exclude_defaults=True)

            except (ValidationError, LlmError) as exc:
                if str(exc) == "LLM_REFUSED":
                    raise
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
                    # Never echo SDK errors: they can include headers.
                    raise LlmError(
                        "LLM_REQUEST_FAILED"
                    ) from None

        raise LlmError(
            "LLM_INVALID_OUTPUT: " + str(last_error)
        )


class GeminiLlmClient:
    """Same contract as ClaudeLlmClient, backed by the Gemini API.

    Uses the same system prompt, the same ParsedExpense JSON schema, and
    the same retry-once-on-invalid-output rule. Only the provider differs.
    """

    def __init__(
        self,
        api_key,
        model=DEFAULT_GEMINI_MODEL,
        sdk=None,
    ):
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY must be set"
            )

        self.model = model

        if sdk is None:
            from google import genai
            from google.genai import types

            sdk = genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(
                    timeout=int(LLM_TIMEOUT_SECONDS * 1000),
                ),
            )

        self.sdk = sdk

    def parse(self, *, messages, roster, current_user):
        system_prompt = (
            SYSTEM_PROMPT
            + f"\nGroup roster: {roster}."
            + f"\nSigned-in user (ME): {current_user}."
        )

        last_error = None

        for attempt in range(LLM_MAX_ATTEMPTS):
            try:
                request_messages = delimit_user_messages(messages)

                if attempt and last_error is not None:
                    request_messages.append({
                        "role": "user",
                        "content": (
                            "Previous response invalid: "
                            f"{last_error}. "
                            "Return corrected JSON."
                        ),
                    })

                response = self.sdk.models.generate_content(
                    model=self.model,
                    contents=[
                        {
                            # Gemini calls the assistant role "model".
                            "role": "model" if m["role"] == "assistant" else "user",
                            "parts": [{"text": m["content"]}],
                        }
                        for m in request_messages
                    ],
                    config={
                        "system_instruction": system_prompt,
                        "response_mime_type": "application/json",
                        "response_json_schema": PARSED_EXPENSE_SCHEMA,
                    },
                )

                text = getattr(response, "text", None)
                if not text:
                    raise LlmError(
                        "LLM_INVALID_OUTPUT: "
                        "missing structured JSON"
                    )

                try:
                    data = json.loads(text)
                except (TypeError, ValueError):
                    raise LlmError(
                        "LLM_INVALID_OUTPUT: response was not JSON"
                    ) from None

                parsed = ParsedExpense.model_validate(data)

                return parsed.model_dump(exclude_defaults=True)

            except (ValidationError, LlmError) as exc:
                last_error = str(exc)

            except (ConnectionError, TimeoutError):
                last_error = "Temporary network failure"

            except Exception as exc:
                name = exc.__class__.__name__
                code = getattr(exc, "code", None)
                # 5xx and network errors are worth one retry.
                if name == "ServerError" or "Timeout" in name or "Connect" in name:
                    last_error = "Temporary network failure"
                    continue
                # Log the status code (e.g. 429 = free-tier quota used up)
                # but never the message, which could echo request details.
                logger.warning(
                    "Gemini request failed: %s (HTTP %s)", name, code
                )
                if code == 404:
                    logger.warning(
                        "Gemini model %r was not found for this key. "
                        "Set GEMINI_MODEL to a model your key can use.",
                        self.model,
                    )
                raise LlmError(
                    "LLM_REQUEST_FAILED"
                ) from None

        raise LlmError(
            "LLM_INVALID_OUTPUT: " + str(last_error)
        )


def delimit_user_messages(messages):
    """Wrap user text in tags so the model treats it as data."""
    delimited = []

    for message in messages:
        content = message["content"]

        if message["role"] == "user":
            content = (
                "<user_message>\n"
                + content.replace("</user_message>", "")
                + "\n</user_message>"
            )

        delimited.append({"role": message["role"], "content": content})

    return delimited
