"""Groq provider: same contract as the Claude client (mocked HTTP)."""

import json
import logging

import httpx
import pytest

from backend.config import DEFAULT_GROQ_MODEL, GROQ_BASE_URL, SYSTEM_PROMPT
from backend.llm import PARSED_EXPENSE_SCHEMA, GroqLlmClient, LlmError
from backend.main import select_llm
from backend.pipeline import parse_turn
from benchmark.benchmark import BenchmarkRefused, run_benchmark


ROSTER = ["Sarah", "Kayla", "Rui"]
FAKE_KEY = "gsk_test_0123456789abcdef"


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


def completion(content, status=200):
    if not isinstance(content, str) and content is not None:
        content = json.dumps(content)
    return httpx.Response(status, json={
        "choices": [{"message": {"role": "assistant", "content": content}}],
    })


def make_client(responses):
    """responses: httpx.Response objects or exceptions, used in order."""
    requests = []
    queue = list(responses)

    def handler(request):
        requests.append(request)
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    http = httpx.Client(transport=httpx.MockTransport(handler))
    return GroqLlmClient(api_key=FAKE_KEY, http=http), requests


def parse(client, messages=None):
    return client.parse(
        messages=messages or [{"role": "user", "content": "Split dinner"}],
        roster=ROSTER,
        current_user="Sarah",
    )


def body(request):
    return json.loads(request.content)


def test_returns_valid_structured_output():
    client, requests = make_client([completion(expense())])

    assert parse(client) == expense()
    assert len(requests) == 1


def test_request_shape():
    client, requests = make_client([completion(expense())])

    parse(client)

    request = requests[0]
    sent = body(request)
    assert str(request.url) == GROQ_BASE_URL + "/chat/completions"
    assert request.headers["authorization"] == f"Bearer {FAKE_KEY}"
    assert sent["model"] == DEFAULT_GROQ_MODEL
    assert sent["response_format"]["type"] == "json_schema"
    assert sent["response_format"]["json_schema"]["schema"] == PARSED_EXPENSE_SCHEMA
    assert sent["messages"][0]["role"] == "system"
    assert sent["messages"][0]["content"].startswith(SYSTEM_PROMPT)
    assert "Signed-in user (ME): Sarah" in sent["messages"][0]["content"]
    assert "temperature" not in sent


def test_user_text_delimited_and_roles_kept():
    client, requests = make_client([completion(expense())])

    parse(client, [
        {"role": "user", "content": "nachos with kayla"},
        {"role": "assistant", "content": "How much?"},
        {"role": "user", "content": "16"},
    ])

    sent = body(requests[0])["messages"]
    assert [m["role"] for m in sent] == ["system", "user", "assistant", "user"]
    assert sent[1]["content"] == "<user_message>\nnachos with kayla\n</user_message>"
    assert sent[2]["content"] == "How much?"


def test_invalid_output_retries_once_then_succeeds():
    client, requests = make_client([
        completion({**expense(), "shares": [1000, 1000, 1000]}),
        completion(expense()),
    ])

    assert parse(client) == expense()
    assert len(requests) == 2
    assert "Previous response invalid" in body(requests[1])["messages"][-1]["content"]


def test_invalid_output_stops_after_retry():
    bad = {**expense(), "totalCents": 3000}
    client, requests = make_client([completion(bad), completion(bad)])

    with pytest.raises(LlmError, match="LLM_INVALID_OUTPUT"):
        parse(client)
    assert len(requests) == 2


def test_non_json_text_rejected():
    client, _ = make_client([completion("Everyone owes $10")] * 2)

    with pytest.raises(LlmError, match="LLM_INVALID_OUTPUT"):
        parse(client)


def test_empty_content_rejected():
    client, _ = make_client([completion(None), completion(None)])

    with pytest.raises(LlmError, match="LLM_INVALID_OUTPUT"):
        parse(client)


def test_server_error_retried_once():
    client, requests = make_client([
        httpx.Response(503, json={"error": "overloaded"}),
        completion(expense()),
    ])

    assert parse(client) == expense()
    assert len(requests) == 2


def test_network_error_retried_once():
    client, requests = make_client([
        httpx.ConnectError("connection refused"),
        completion(expense()),
    ])

    assert parse(client) == expense()
    assert len(requests) == 2


def test_rate_limit_fails_without_retry_or_leaking_key(caplog):
    client, requests = make_client([
        httpx.Response(429, json={"error": {"message": f"limit for {FAKE_KEY}"}}),
    ])

    with caplog.at_level(logging.WARNING, logger="splitwise.llm"):
        with pytest.raises(LlmError) as raised:
            parse(client)

    assert str(raised.value) == "LLM_REQUEST_FAILED"
    assert len(requests) == 1
    assert "HTTP 429" in caplog.text
    assert FAKE_KEY not in caplog.text


def test_unknown_model_logs_a_hint(caplog):
    client, _ = make_client([httpx.Response(404, json={"error": "not found"})])

    with caplog.at_level(logging.WARNING, logger="splitwise.llm"):
        with pytest.raises(LlmError):
            parse(client)

    assert "Set GROQ_MODEL" in caplog.text


def test_key_required():
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        GroqLlmClient(api_key=None, http=httpx.Client())


def test_same_extraction_gives_same_preview_as_fixture_path():
    """Switching providers must not change any calculated result."""
    from backend.llm import FakeLlmClient

    groq, _ = make_client([completion(expense("10.00"))])
    previews = [
        parse_turn(
            llm=llm,
            conversation=[{"role": "user", "content": "dinner 10"}],
            roster=ROSTER,
            current_user="Sarah",
        )
        for llm in (FakeLlmClient([expense("10.00")]), groq)
    ]

    assert previews[0] == previews[1]
    assert previews[0]["type"] == "preview"


# Provider selection

def test_select_llm_groq():
    llm = select_llm({"LLM_PROVIDER": "groq", "GROQ_API_KEY": FAKE_KEY})

    assert isinstance(llm, GroqLlmClient)
    assert llm.model == DEFAULT_GROQ_MODEL


def test_select_llm_groq_model_override():
    llm = select_llm({
        "LLM_PROVIDER": "groq",
        "GROQ_API_KEY": FAKE_KEY,
        "GROQ_MODEL": "openai/gpt-oss-20b",
    })

    assert llm.model == "openai/gpt-oss-20b"


def test_select_llm_groq_without_key_fails_at_startup():
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        select_llm({"LLM_PROVIDER": "groq"})


def test_groq_never_chosen_by_default():
    assert not isinstance(select_llm({"GROQ_API_KEY": FAKE_KEY}), GroqLlmClient)


def test_groq_key_redacted_from_logs(caplog, monkeypatch):
    from backend.security import install_secret_redaction

    monkeypatch.setenv("GROQ_API_KEY", FAKE_KEY)
    logger = logging.getLogger("splitwise.test.groq")
    install_secret_redaction(logger)

    with caplog.at_level(logging.INFO, logger="splitwise.test.groq"):
        logger.info("calling Groq with %s", FAKE_KEY)

    assert FAKE_KEY not in caplog.text


# Benchmark

def test_benchmark_refuses_groq_without_key():
    with pytest.raises(BenchmarkRefused, match="GROQ_API_KEY"):
        run_benchmark(provider="groq", env={})


def test_benchmark_refuses_groq_in_ci():
    with pytest.raises(BenchmarkRefused, match="CI"):
        run_benchmark(provider="groq", env={"CI": "true", "GROQ_API_KEY": FAKE_KEY})
