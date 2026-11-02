"""Drive benchmark scenarios through the chat API.

Each scenario runs against a fresh in-memory database through FastAPI's
TestClient, signed in as the scenario's user. Turns marked "always" are
sent after every response (B5's correction comes after a preview);
"if_asked" turns are sent only when the last response was a question.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.config import MAX_PROMPTS_PER_CONVERSATION
from backend.database import create_database, seed_database
from backend.main import create_app
from benchmark.comparator import categorize, compare, describe
from benchmark.schema import Scenario, ScenarioResult

SESSION_SECRET = "benchmark-session-secret-at-least-32-chars"


def _client(llm) -> tuple[TestClient, object]:
    db = create_database(":memory:")
    seed_database(db)
    return TestClient(create_app(db=db, session_secret=SESSION_SECRET, llm=llm)), db


def _group_id(client: TestClient, name: str) -> int:
    for group in client.get("/api/groups").json():
        if group["name"] == name:
            return group["id"]
    raise ValueError(f"Unknown group {name}")


def _next_turn(scenario: Scenario, index: int, last_type: str):
    """Index of the next turn to send, skipping if_asked turns after a preview."""
    while index < len(scenario.turns):
        turn = scenario.turns[index]
        if turn.send == "always" or last_type == "question":
            return index
        index += 1
    return None


def _behavior(scenario: Scenario, asked_before_final: bool, asked_any: bool):
    behavior = scenario.behavior
    if behavior.mustNotAsk:
        return "no question", "asked" if asked_any else "no question", not asked_any
    if behavior.mustAskBeforeFinalPreview:
        observed = "asked" if asked_before_final else "no question"
        return "asked", observed, asked_before_final
    if behavior.mustEndWithQuestion:
        return "ends with question", "", True
    return "any", "asked" if asked_any else "no question", True


def run_scenario(scenario: Scenario, llm) -> ScenarioResult:
    client, db = _client(llm)
    transcript = []

    try:
        login = client.post("/api/session", json={"name": scenario.signedInAs})
        login.raise_for_status()
        group_id = _group_id(client, scenario.group)

        conversation_id = None
        prompt_count = 0
        asked_any = False
        last = {"type": None}
        index = 0
        reason = None

        while True:
            if prompt_count >= MAX_PROMPTS_PER_CONVERSATION:
                reason = f"prompt limit: no final preview within {MAX_PROMPTS_PER_CONVERSATION} prompts"
                break

            text = scenario.turns[index].text
            response = client.post("/api/chat", json={
                "groupId": group_id,
                "conversationId": conversation_id,
                "message": text,
            })
            prompt_count += 1

            if response.status_code != 200:
                last = {"type": "error"}
                transcript.append({"user": text, "status": response.status_code})
                reason = f"HTTP {response.status_code}: {response.json().get('detail')}"
                break

            last = response.json()
            conversation_id = last.get("conversationId", conversation_id)
            prompt_count = last.get("promptCount", prompt_count)
            transcript.append({
                "user": text,
                "type": last["type"],
                "assistant": last.get("question") or last.get("reason") or last.get("message"),
            })

            if last["type"] == "question":
                asked_any = True
            elif last["type"] not in ("preview",):
                reason = f"{last['type']}: {last.get('reason') or last.get('message')}"
                break

            following = _next_turn(scenario, index + 1, last["type"])
            if following is None:
                if last["type"] == "question" and not scenario.behavior.mustEndWithQuestion:
                    reason = "ran out of script"
                break
            index = following

        # The final preview is the last one shown; questions before it count.
        final_preview = last.get("preview") if last.get("type") == "preview" else None
        types = [entry.get("type") for entry in transcript]
        asked_before_final = "question" in types[:-1] if final_preview else asked_any

        mismatches = []
        if scenario.behavior.mustEndWithQuestion and scenario.expected is None:
            passed = last.get("type") == "question" and reason is None
            if not passed and reason is None:
                reason = "showed a preview instead of asking"
        elif reason is None and final_preview is not None:
            mismatches = compare(scenario.expected, final_preview, prompt_count)
            passed = not mismatches
            if mismatches:
                reason = describe(mismatches)
        else:
            passed = False
            reason = reason or "no final preview"

        expected_behavior, observed, behavior_ok = _behavior(
            scenario, asked_before_final, asked_any
        )
        if scenario.behavior.mustEndWithQuestion:
            observed = "ended with question" if last.get("type") == "question" else "did not ask"
            behavior_ok = last.get("type") == "question"

        return ScenarioResult(
            id=scenario.id,
            label=scenario.label,
            informational=scenario.informational,
            passed=passed,
            promptCount=prompt_count,
            failureReason=None if passed else reason,
            failureCategory=None if passed else categorize(scenario, reason, mismatches),
            mismatches=mismatches,
            behaviorExpected=expected_behavior,
            behaviorObserved=observed,
            behaviorOk=behavior_ok,
            transcript=transcript,
        )
    finally:
        client.close()
        db.close()
