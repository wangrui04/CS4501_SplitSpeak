
from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


Money = Annotated[
    str,
    Field(pattern=r"^(?:\d+(?:\.\d{1,2})?|\.\d{1,2})$"),
]


class Participants(StrictModel):
    mode: Literal["all", "only", "all_except"]
    names: list[str]


class Weight(StrictModel):
    name: str
    weight: int = Field(ge=1)


class Refund(StrictModel):
    amount: Money
    recipient: str


class Item(StrictModel):
    name: str
    quantity: int = Field(ge=1)
    unitPrice: Money | None
    participants: Participants
    # Optional extensions for trips: a different payer per item,
    # weighted splits (nights, "twice as much"), and refunds.
    paidBy: str | None = None
    weights: list[Weight] | None = None
    refund: Refund | None = None


class Charge(StrictModel):
    kind: Literal["tax", "tip", "fee"]
    amount: Money | None
    percent: Money | None
    method: Literal["proportional", "equal"] | None

    @model_validator(mode="after")
    def one_or_other(self):
        if self.amount is not None and self.percent is not None:
            raise ValueError(
                "Charge cannot specify both amount and percent"
            )
        return self


class OpenQuestion(StrictModel):
    field: str
    question: str


class ParsedExpense(StrictModel):
    description: str
    payer: str | None
    items: list[Item]
    charges: list[Charge]
    statedTotal: Money | None
    openQuestions: list[OpenQuestion]


class Share(StrictModel):
    name: str
    cents: int = Field(ge=0)
    summary: str


class Paid(StrictModel):
    name: str
    # Negative when a refund received exceeds what the person paid.
    cents: int


class Transfer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_: str = Field(alias="from")
    to: str
    cents: int = Field(gt=0)


class Settlement(StrictModel):
    nets: list[dict]
    transfers: list[Transfer]


class ExpensePreview(StrictModel):
    description: str | None = None
    payer: str
    currency: Literal["USD"]
    lineItems: list[dict]
    charges: list[dict]
    totalCents: int = Field(ge=0)
    shares: list[Share]
    paid: list[Paid] = []
    settlement: Settlement | None = None
    validated: bool


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    group_id: int | None = Field(default=None, alias="groupId")
    message: str
    conversation_id: int | None = Field(default=None, alias="conversationId")


class ConfirmRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    conversation_id: int | None = Field(default=None, alias="conversationId")


class ConfirmResponse(StrictModel):
    ok: bool
    expenseId: int
    conversationId: int
    status: str


class QuestionResponse(StrictModel):
    type: Literal["question"]
    question: str
    conversationId: int | None = None
    promptCount: int | None = None
    status: str | None = None


class PreviewResponse(StrictModel):
    type: Literal["preview"]
    preview: ExpensePreview
    conversationId: int | None = None
    promptCount: int | None = None
    status: str | None = None


class UnresolvedResponse(StrictModel):
    type: Literal["unresolved"]
    reason: str
    conversationId: int | None = None
    promptCount: int | None = None
    status: str | None = None
    fallback: str | None = "manual"


class ErrorResponse(StrictModel):
    type: Literal["error"]
    message: str
    conversationId: int | None = None
    promptCount: int | None = None
    status: str | None = None


ChatResponse = Union[
    QuestionResponse,
    PreviewResponse,
    UnresolvedResponse,
    ErrorResponse,
]
