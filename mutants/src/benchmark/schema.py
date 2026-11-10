"""Scenario and results file schemas. All amounts are integer cents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCENARIO_DIR = Path(__file__).parent / "scenarios"
RESULTS_DIR = Path(__file__).parent / "results"

FAILURE_CATEGORIES = (
    "participants",
    "quantities",
    "amounts",
    "tax/tip",
    "multiple payers",
    "weights/nights",
    "refund",
    "correction",
    "settlement",
    "prompt limit",
)


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Turn(Strict):
    text: str
    send: Literal["always", "if_asked"]


class Transfer(Strict):
    from_: str = Field(alias="from")
    to: str
    cents: int = Field(gt=0)

    def key(self) -> tuple[str, str, int]:
        return (self.from_, self.to, self.cents)


class Expected(Strict):
    shares: dict[str, int]
    paid: dict[str, int]
    settlement: list[Transfer]
    expectedPrompts: int = Field(ge=1)


class Behavior(Strict):
    mustNotAsk: bool = False
    mustAskBeforeFinalPreview: bool = False
    # Informational cases that should end with a clarification question.
    mustEndWithQuestion: bool = False


class Scenario(Strict):
    id: str
    label: str
    signedInAs: str = "Sarah"
    group: str = "Apartment 4B"
    turns: list[Turn] = Field(min_length=1)
    expected: Expected | None = None
    informational: bool = False
    behavior: Behavior = Behavior()
    # Failure categories this scenario exercises; the first is primary.
    categories: list[str] = Field(default_factory=lambda: ["amounts"])
    notes: str = ""

    @model_validator(mode="after")
    def expected_or_question(self):
        if self.expected is None and not self.behavior.mustEndWithQuestion:
            raise ValueError("expected is required unless the case must end with a question")
        if self.turns[0].send != "always":
            raise ValueError("the first turn must be sent always")
        unknown = set(self.categories) - set(FAILURE_CATEGORIES)
        if unknown:
            raise ValueError(f"unknown categories: {sorted(unknown)}")
        return self


class Mismatch(Strict):
    field: str
    expected: int | str | None
    actual: int | str | None


class ScenarioResult(Strict):
    id: str
    label: str
    informational: bool
    passed: bool
    promptCount: int
    failureReason: str | None = None
    failureCategory: str | None = None
    mismatches: list[Mismatch] = []
    behaviorExpected: str
    behaviorObserved: str
    behaviorOk: bool
    transcript: list[dict] = []


class Run(Strict):
    run: int = Field(ge=1)
    official: bool
    results: list[ScenarioResult]


class ResultsFile(Strict):
    schemaVersion: Literal[1] = 1
    model: str
    promptVersion: str
    commitSha: str
    timestamp: str
    provider: str
    runs: list[Run]


def load_scenarios(*folders: str) -> list[Scenario]:
    scenarios = []
    for folder in folders:
        for path in sorted((SCENARIO_DIR / folder).glob("*.json")):
            scenarios.append(Scenario.model_validate(json.loads(path.read_text())))
    return scenarios
