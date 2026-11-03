"""Gemini provider: same contract as the Claude client (mocked SDK)."""

import json
import logging
from unittest.mock import MagicMock

import pytest
from google.genai import errors as genai_errors

from backend.config import DEFAULT_GEMINI_MODEL, SYSTEM_PROMPT
from backend.llm import (
    PARSED_EXPENSE_SCHEMA,
    ClaudeLlmClient,
    GeminiLlmClient,
    LlmError,
)
from backend.main import select_llm
from backend.pipeline import parse_turn
from benchmark.benchmark import BenchmarkRefused, run_benchmark


ROSTER = ["Sarah", "Kayla", "Rui"]
FAKE_KEY = "AIza-test-0123456789abcdef"


def expense(price="30.00"):
    return {
        "description": "Dinner",
        "payer": "ME",
        "items": [{
            "name": "Dinner",
            "quantity": 1,
            "unitPrice": price,
            "participants": {"mode": "all", "names": []},
        }],
        "charges": [],
        "statedTotal": price,
        "openQuestions": [],
    }


def gemini_response(data):
    response = MagicMock()
    response.text = data if isinstance(data, str) else json.dumps(data)
    return response


def make_client(responses):
    sdk = MagicMock()
    sdk.models.generate_content.side_effect = responses
    return GeminiLlmClient(api_key=FAKE_KEY, sdk=sdk), sdk


def parse(client, messages=None):
    return client.parse(
        messages=messages or [{"role": "user", "content": "Split dinner"}],
        roster=ROSTER,
        current_user="Sarah",
    )


def test_returns_valid_structured_output():
    client, sdk = make_client([gemini_response(expense())])

    assert parse(client) == expense()
    assert sdk.models.generate_content.call_count == 1


def test_request_uses_same_prompt_and_schema_as_claude():
    client, sdk = make_client([gemini_response(expense())])

    parse(client)

    kwargs = sdk.models.generate_content.call_args.kwargs
    config = kwargs["config"]
    assert kwargs["model"] == DEFAULT_GEMINI_MODEL
    assert config["response_mime_type"] == "application/json"
    assert config["response_json_schema"] == PARSED_EXPENSE_SCHEMA
    assert config["system_instruction"].startswith(SYSTEM_PROMPT)
    assert "Signed-in user (ME): Sarah" in config["system_instruction"]
    assert "temperature" not in config


def test_roles_mapped_and_user_text_delimited():
    client, sdk = make_client([gemini_response(expense())])

    parse(client, [
        {"role": "user", "content": "nachos with kayla"},
        {"role": "assistant", "content": "How much?"},
        {"role": "user", "content": "16"},
    ])

    contents = sdk.models.generate_content.call_args.kwargs["contents"]
    assert [c["role"] for c in contents] == ["user", "model", "user"]
    assert contents[0]["parts"][0]["text"] == "<user_message>\nnachos with kayla\n</user_message>"
    assert contents[1]["parts"][0]["text"] == "How much?"


def test_invalid_output_retries_once_then_succeeds():
    client, sdk = make_client([
        gemini_response({**expense(), "shares": [1000, 1000, 1000]}),
        gemini_response(expense()),
    ])

    assert parse(client) == expense()
    assert sdk.models.generate_content.call_count == 2
    retry_text = sdk.models.generate_content.call_args.kwargs["contents"][-1]["parts"][0]["text"]
    assert "Previous response invalid" in retry_text


def test_invalid_output_stops_after_retry():
    bad = gemini_response({**expense(), "totalCents": 3000})
    client, sdk = make_client([bad, bad])

    with pytest.raises(LlmError, match="LLM_INVALID_OUTPUT"):
        parse(client)
    assert sdk.models.generate_content.call_count == 2


def test_non_json_text_rejected():
    client, _ = make_client([gemini_response("Everyone owes $10")] * 2)

    with pytest.raises(LlmError, match="LLM_INVALID_OUTPUT"):
        parse(client)


def test_empty_response_rejected():
    empty = MagicMock()
    empty.text = None  # e.g. blocked by safety filters
    client, _ = make_client([empty, empty])

    with pytest.raises(LlmError, match="LLM_INVALID_OUTPUT"):
        parse(client)


def test_server_error_retried_once():
    client, sdk = make_client([
        genai_errors.ServerError(503, {"error": {"message": "overloaded"}}),
        gemini_response(expense()),
    ])

    assert parse(client) == expense()
    assert sdk.models.generate_content.call_count == 2


def test_quota_error_fails_without_leaking_key(caplog):
    client, sdk = make_client([
        genai_errors.ClientError(
            429, {"error": {"message": f"quota exceeded for {FAKE_KEY}"}}
        ),
    ])

    with caplog.at_level(logging.WARNING, logger="splitwise.llm"):
        with pytest.raises(LlmError) as raised:
            parse(client)

    assert str(raised.value) == "LLM_REQUEST_FAILED"
    assert sdk.models.generate_content.call_count == 1
    assert "HTTP 429" in caplog.text
    assert FAKE_KEY not in caplog.text


def test_key_required():
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        GeminiLlmClient(api_key=None, sdk=MagicMock())


def test_same_extraction_gives_same_preview_as_claude():
    """Switching providers must not change any calculated result."""
    claude_sdk = MagicMock()
    block = MagicMock()
    block.type = "text"
    block.text = json.dumps(expense("10.00"))
    claude_response = MagicMock()
    claude_response.stop_reason = "end_turn"
    claude_response.content = [block]
    claude_sdk.beta.messages.create.return_value = claude_response
    claude = ClaudeLlmClient(api_key="x", sdk=claude_sdk)

    gemini, _ = make_client([gemini_response(expense("10.00"))])

    previews = [
        parse_turn(
            llm=llm,
            conversation=[{"role": "user", "content": "dinner 10"}],
            roster=ROSTER,
            current_user="Sarah",
        )
        for llm in (claude, gemini)
    ]

    assert previews[0] == previews[1]
    assert previews[0]["type"] == "preview"


# Provider selection

def test_select_llm_gemini():
    llm = select_llm({"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": FAKE_KEY})

    assert isinstance(llm, GeminiLlmClient)
    assert llm.model == DEFAULT_GEMINI_MODEL


def test_select_llm_gemini_model_override():
    llm = select_llm({
        "LLM_PROVIDER": "gemini",
        "GEMINI_API_KEY": FAKE_KEY,
        "GEMINI_MODEL": "gemini-2.5-flash-lite",
    })

    assert llm.model == "gemini-2.5-flash-lite"


def test_select_llm_gemini_without_key_fails_at_startup():
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        select_llm({"LLM_PROVIDER": "gemini"})


def test_gemini_never_chosen_by_default():
    assert not isinstance(select_llm({"GEMINI_API_KEY": FAKE_KEY}), GeminiLlmClient)


def test_gemini_key_redacted_from_logs(caplog, monkeypatch):
    from backend.security import install_secret_redaction

    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    logger = logging.getLogger("splitwise.test.gemini")
    install_secret_redaction(logger)

    with caplog.at_level(logging.INFO, logger="splitwise.test.gemini"):
        logger.info("calling Gemini with %s", FAKE_KEY)

    assert FAKE_KEY not in caplog.text


# Benchmark

def test_benchmark_refuses_gemini_without_key():
    with pytest.raises(BenchmarkRefused, match="GEMINI_API_KEY"):
        run_benchmark(provider="gemini", env={})


def test_benchmark_refuses_gemini_in_ci():
    with pytest.raises(BenchmarkRefused, match="CI"):
        run_benchmark(provider="gemini", env={"CI": "true", "GEMINI_API_KEY": FAKE_KEY})
