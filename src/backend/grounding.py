"""Deterministic checks of the LLM's reading against the user's own words.

The LLM interprets; it does not get the last word on whether the user
gave the required facts. After schema validation and before allocation,
these checks confirm from the user's messages alone (never another LLM
call) that:

- a payer or per-item payer is tied to a payment word ("I paid",
  "Alex covered it", "paid by Sam");
- every item price, refund, and tax/tip/fee amount or percent was typed;
- a tax, tip, or fee the user mentioned was not silently dropped.

A failed check only clears an ungrounded payer (so the normal "Who
paid?" question is asked) or produces a question. It never changes an
amount and never saves anything.
"""

from __future__ import annotations

import copy
import logging
import re
from decimal import Decimal, InvalidOperation

from backend import config

logger = logging.getLogger("splitwise.grounding")

ME = "ME"

_CLAUSE_SPLIT = re.compile(r"[.!?;,\n]+")
_WORD = re.compile(r"[a-z0-9']+")
_NUMBER = re.compile(
    # Letters may touch a number ("ipaid30for"); digits and dots may not.
    r"(?<![\d.,])\$?\s?((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)(?!\d|,\d)"
    r"(\s*(?:%|percent\b|pct\b))?"
)
# "Alex paid me back" is a repayment, not paying for the expense.
_REPAYMENT_WORDS = ("back",)


def _phrases(words) -> list[tuple[str, ...]]:
    return [tuple(phrase.lower().split()) for phrase in words]


_PAYMENT = _phrases(config.GROUNDING_PAYMENT_WORDS)
_PAYMENT_BY = _phrases(config.GROUNDING_PAYMENT_BY_WORDS)
_FILLER = frozenset(config.GROUNDING_PAYER_FILLER_WORDS)
_FIRST_PERSON = frozenset(config.GROUNDING_FIRST_PERSON_WORDS)
_CHARGE_WORDS = {
    kind: _phrases(words) for kind, words in config.GROUNDING_CHARGE_WORDS.items()
}
_COVER_BEFORE = _phrases(config.GROUNDING_INCLUDED_WORDS) + _phrases(
    config.GROUNDING_NONE_WORDS
)
_COVER_AFTER = _phrases(config.GROUNDING_COVERED_AFTER_WORDS)


# ------------------------------------------------------------------ helpers


def user_texts(conversation: list[dict]) -> list[str]:
    """The user's own messages; assistant questions are never evidence."""
    return [
        message.get("content", "")
        for message in conversation
        if message.get("role") == "user"
    ]


def _clauses(texts: list[str]) -> list[list[str]]:
    clauses = []
    for text in texts:
        normalized = text.lower().replace("’", "'")
        for clause in _CLAUSE_SPLIT.split(normalized):
            words = _WORD.findall(clause)
            if words:
                clauses.append(words)
    return clauses


def _phrase_at(words: list[str], start: int, phrase: tuple[str, ...]) -> bool:
    return tuple(words[start : start + len(phrase)]) == phrase


def _within_one_edit(word: str, name: str) -> bool:
    if abs(len(word) - len(name)) > 1:
        return False
    if len(word) == len(name):
        return sum(a != b for a, b in zip(word, name)) <= 1
    shorter, longer = sorted((word, name), key=len)
    return any(longer[:i] + longer[i + 1 :] == shorter for i in range(len(longer)))


def _names_person(word: str, person: str, current_user: str) -> bool:
    """Does one word refer to this person (ME, or a roster name)?"""
    if person == ME or person == current_user:
        if word in _FIRST_PERSON:
            return True
        if person == ME:
            return False
    name = person.lower().split()[0]
    if word in (name, f"{name}s", f"{name}'s"):
        return True
    # Small typos ("Riu" for "Rui") that the LLM is allowed to correct.
    return len(name) >= 3 and _within_one_edit(word, name)


# -------------------------------------------------------------------- payer


def _person_forms(person: str, current_user: str) -> set[str]:
    forms = set()
    if person == ME or person == current_user:
        forms |= _FIRST_PERSON
    if person != ME:
        forms.add(person.lower().split()[0])
    return forms


def _squashed_says_paid(word: str, person: str, current_user: str) -> bool:
    """Text typed without spaces: "ipaid30fordinner" starts with "i" + "paid"."""
    return any(
        word.startswith(form + "".join(phrase))
        for form in _person_forms(person, current_user)
        for phrase in _PAYMENT
    )


def _says_paid(words: list[str], person: str, current_user: str) -> bool:
    for index, word in enumerate(words):
        if _squashed_says_paid(word, person, current_user):
            return True
        if not _names_person(word, person, current_user):
            continue

        # "<person> [filler...] <payment word>"
        cursor = index + 1
        while cursor < len(words) and words[cursor] in _FILLER:
            cursor += 1
        for phrase in _PAYMENT:
            if _phrase_at(words, cursor, phrase):
                after = words[cursor + len(phrase) : cursor + len(phrase) + 2]
                if not any(back in after for back in _REPAYMENT_WORDS):
                    return True

        # "<paid by> <person>"
        for phrase in _PAYMENT_BY:
            if index >= len(phrase) and _phrase_at(words, index - len(phrase), phrase):
                return True
    return False


def _payer_grounded(person: str, clauses: list[list[str]], current_user: str) -> bool:
    return any(_says_paid(words, person, current_user) for words in clauses)


def ground_payers(
    data: dict, texts: list[str], current_user: str
) -> tuple[dict, list[str]]:
    """Copy of data with any payer the user never stated cleared.

    Returns (data, fired) where fired names the checks that cleared a
    payer. Clearing a payer makes the pipeline ask "Who paid?".
    """
    grounded = copy.deepcopy(data)
    clauses = _clauses(texts)
    fired = []

    payer = grounded.get("payer")
    if payer is not None and not _payer_grounded(payer, clauses, current_user):
        grounded["payer"] = None
        fired.append("payer")

    cleared_item = False
    for item in grounded.get("items", []):
        paid_by = item.get("paidBy")
        if paid_by and not _payer_grounded(paid_by, clauses, current_user):
            item["paidBy"] = None
            cleared_item = True
    if cleared_item:
        fired.append("item_payer")

    for check in fired:
        logger.info("grounding check fired: %s", check)
    return grounded, fired


# ------------------------------------------------------------------ amounts


def _typed_numbers(texts: list[str]) -> tuple[set[Decimal], set[Decimal]]:
    """(plain amounts, percents) the user typed, as exact decimals."""
    amounts: set[Decimal] = set()
    percents: set[Decimal] = set()
    for text in texts:
        for match in _NUMBER.finditer(text.lower()):
            value = Decimal(match.group(1).replace(",", ""))
            (percents if match.group(2) else amounts).add(value)
    return amounts, percents


def _decimal(value) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def amount_question(data: dict, texts: list[str]) -> str | None:
    """A question for the first price or charge the user never typed."""
    amounts, percents = _typed_numbers(texts)

    for item in data.get("items", []):
        price = _decimal(item.get("unitPrice"))
        if price is not None:
            quantity = item.get("quantity") or 1
            if price not in amounts and price * quantity not in amounts:
                logger.info("grounding check fired: %s", "item_amount")
                return f"How much was {item['name']}?"

        refund = item.get("refund") or {}
        refund_amount = _decimal(refund.get("amount"))
        if refund_amount is not None and refund_amount not in amounts:
            logger.info("grounding check fired: %s", "refund_amount")
            return f"How much was the refund on {item['name']}?"

    for charge in data.get("charges", []):
        amount = _decimal(charge.get("amount"))
        percent = _decimal(charge.get("percent"))
        ungrounded = (amount is not None and amount not in amounts) or (
            percent is not None and percent not in percents
        )
        if ungrounded:
            logger.info("grounding check fired: %s", "charge_amount")
            return f"How much was the {charge['kind']}?"

    return None


# ------------------------------------------------------------------ charges


def _mentions(words: list[str], kind: str) -> list[tuple[int, int]]:
    """(start, end) word spans where this charge kind is mentioned."""
    spans = []
    for index in range(len(words)):
        for phrase in _CHARGE_WORDS[kind]:
            if _phrase_at(words, index, phrase):
                spans.append((index, index + len(phrase)))
    return spans


def _covered(words: list[str], start: int, end: int) -> bool:
    """Is the mention at words[start:end] said to be included or none?"""
    window = config.GROUNDING_COVER_WINDOW_WORDS
    for phrase in _COVER_BEFORE:
        for begin in range(max(0, start - window - len(phrase)), start):
            phrase_end = begin + len(phrase)
            if phrase_end <= start and _phrase_at(words, begin, phrase):
                return True
    for phrase in _COVER_AFTER:
        for begin in range(end, min(len(words), end + window + 1)):
            if _phrase_at(words, begin, phrase):
                return True
    return False


def _join_kinds(kinds: list[str]) -> str:
    if len(kinds) == 1:
        return f"the {kinds[0]}"
    if len(kinds) == 2:
        return f"the {kinds[0]} and {kinds[1]}"
    return "the " + ", ".join(kinds[:-1]) + f", and {kinds[-1]}"


def charge_question(data: dict, texts: list[str]) -> str | None:
    """Ask about a tax, tip, or fee the user mentioned but the LLM dropped."""
    parsed_kinds = {charge["kind"] for charge in data.get("charges", [])}
    mentioned: set[str] = set()
    covered: set[str] = set()

    for words in _clauses(texts):
        for kind in _CHARGE_WORDS:
            for start, end in _mentions(words, kind):
                mentioned.add(kind)
                if _covered(words, start, end):
                    covered.add(kind)

    missing = [
        kind
        for kind in _CHARGE_WORDS
        if kind in mentioned and kind not in covered and kind not in parsed_kinds
    ]
    if not missing:
        return None

    logger.info("grounding check fired: %s", "charge_missing")
    subject = _join_kinds(missing)
    if len(missing) == 1:
        return (
            f"How much was {subject}, and should it be split equally or "
            "proportionally? If it was already included, say so."
        )
    return (
        f"How much were {subject}, and should they be split equally or "
        "proportionally? If they were already included, say so."
    )
