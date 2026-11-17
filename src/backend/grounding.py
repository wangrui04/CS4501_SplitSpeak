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
        diffs = [i for i, (a, b) in enumerate(zip(word, name)) if a != b]
        if len(diffs) <= 1:
            return True
        # Two swapped neighbouring letters ("riu" for "rui").
        first, second = diffs[0], diffs[-1]
        return (
            len(diffs) == 2
            and second == first + 1
            and word[first] == name[second]
            and word[second] == name[first]
        )
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


# ------------------------------------------------------ question templates
#
# Payer questions the app asks itself. The pipeline asks them and
# payer_answers() recognizes them, so both sides use the same strings.
# Only these count: an answer to a question the LLM worded is not evidence.

PAYER_QUESTION = "Who paid for this expense?"
ITEM_PAYER_QUESTION = "Who paid for {item}?"
PAYER_HINT = (
    "I still need to know who paid for this expense. "
    "Reply with just a name, e.g. {example}."
)
ITEM_PAYER_HINT = (
    "I still need to know who paid for {item}. "
    "Reply with just a name, e.g. {example}."
)
REPEAT_HINT = "I still need this before I can show a preview: {question}"
REPEAT_GIVE_UP = (
    "I still couldn't work this out from your answers. "
    "Please enter this expense manually."
)


def _template_pattern(template: str) -> re.Pattern:
    """Regex for a template: {item} is captured, {example} is any name."""
    parts = re.split(r"\{(\w+)\}", template)
    pattern = ""
    for index, part in enumerate(parts):
        if index % 2 == 0:
            pattern += re.escape(part)
        elif part == "item":
            pattern += "(?P<item>.+)"
        else:
            pattern += ".+"
    return re.compile(f"^{pattern}$")


_EXPENSE_QUESTIONS = [_template_pattern(PAYER_QUESTION), _template_pattern(PAYER_HINT)]
_ITEM_QUESTIONS = [_template_pattern(ITEM_PAYER_QUESTION), _template_pattern(ITEM_PAYER_HINT)]
_ONLY_PAYER_BLOCKERS = re.compile(
    r"\b(?:" + "|".join(map(re.escape, config.GROUNDING_NOT_ONLY_PAYER_WORDS)) + r")\b"
)


def _asks_only_who_paid(text: str) -> bool:
    """A question that asks who paid and nothing else, whoever wrote it.

    "Who paid for the lunch?" counts; "Who paid, and how should it be
    split?" does not, because a bare name can't answer both parts.
    """
    lowered = text.strip().lower()
    return (
        lowered.startswith("who paid")
        and lowered.endswith("?")
        and lowered.count("?") == 1
        and not _ONLY_PAYER_BLOCKERS.search(lowered)
    )


def _payer_question_target(text: str):
    """None if text isn't a payer question, else (kind, label).

    kind is "expense" or "item"; label is the item the question names,
    which ground_payers() matches against the current items.
    """
    text = text.strip()
    if any(pattern.match(text) for pattern in _EXPENSE_QUESTIONS):
        return ("expense", None)
    for pattern in _ITEM_QUESTIONS:
        match = pattern.match(text)
        if match and (pattern is not _ITEM_QUESTIONS[0] or _asks_only_who_paid(text)):
            return ("item", match.group("item"))
    if _asks_only_who_paid(text):
        return ("expense", None)
    return None


def _format_price(price: Decimal) -> str:
    if price == price.to_integral_value():
        return str(price.quantize(Decimal(1)))
    return str(price.quantize(Decimal("0.01")))


def item_labels(items: list[dict]) -> list[str]:
    """How questions name each item: "Pizza ($10)" when two share a name."""
    names = [item.get("name", "") for item in items]
    labels = []
    for index, item in enumerate(items):
        name = names[index]
        twins = [i for i, other in enumerate(names) if other.lower() == name.lower()]
        if len(twins) == 1:
            labels.append(name)
            continue
        price = _decimal(item.get("unitPrice"))
        twin_prices = [_decimal(items[i].get("unitPrice")) for i in twins]
        if price is not None and twin_prices.count(price) == 1:
            labels.append(f"{name} (${_format_price(price)})")
        else:
            labels.append(f"{name} #{twins.index(index) + 1}")
    return labels


def _match_label(label: str, labels: list[str]) -> int | None:
    def norm(text):
        text = " ".join(text.lower().split())
        return text[4:] if text.startswith("the ") else text

    wanted = norm(label)
    matches = [i for i, candidate in enumerate(labels) if norm(candidate) == wanted]
    return matches[0] if len(matches) == 1 else None


def _hint_example(roster: list[str], current_user: str) -> str:
    return next((name for name in roster if name != current_user), "me")


def repeat_hint(question: str, roster: list[str], current_user: str) -> str:
    """The clearer version of a question, used when it would repeat."""
    example = _hint_example(roster, current_user)
    target = _payer_question_target(question)
    if target is None:
        return REPEAT_HINT.format(question=question)
    kind, label = target
    if kind == "item":
        return ITEM_PAYER_HINT.format(item=label, example=example)
    return PAYER_HINT.format(example=example)


def _canonical(person: str | None, current_user: str) -> str | None:
    return ME if person == current_user else person


def _single_person(reply: str, roster: list[str], current_user: str) -> str | None:
    """The one person a short reply names ("Rui", "me"), else None."""
    found = set()
    for words in _clauses([reply]):
        for word in words:
            if word in _FIRST_PERSON:
                found.add(ME)
            for member in roster:
                if _names_person(word, member, current_user):
                    found.add(_canonical(member, current_user))
    return found.pop() if len(found) == 1 else None


def payer_answers(
    conversation: list[dict], roster: list[str], current_user: str
) -> list[tuple[str | None, str]]:
    """Who the user named in reply to a payer question, oldest first.

    Each entry is (item label or None, person), with ME for the signed-in
    user. Only one-name replies to questions that ask just "who paid"
    count (the app's own, or the LLM's); ground_payers() decides which
    item, if any, each one refers to.
    """
    answers = []
    for question, reply in zip(conversation, conversation[1:]):
        if question.get("role") != "assistant" or reply.get("role") != "user":
            continue
        target = _payer_question_target(question.get("content", ""))
        if target is None:
            continue
        person = _single_person(reply.get("content", ""), roster, current_user)
        if person is not None:
            answers.append((target[1], person))
    return answers


def _resolve_answers(answers, items):
    """(answer for the whole expense, {item index: person})."""
    labels = item_labels(items)
    expense_answer = None
    item_answers = {}
    for label, person in answers:
        index = _match_label(label, labels) if label is not None else None
        if index is None:
            expense_answer = person
            continue
        item_answers[index] = person
        if len(items) == 1:
            # "Who paid for the lunch?" when lunch is the whole expense.
            expense_answer = person
    return expense_answer, item_answers


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
    data: dict,
    texts: list[str],
    current_user: str,
    answers: list | None = None,
) -> tuple[dict, list[str]]:
    """Copy of data with any payer the user never stated cleared.

    A payer counts as stated when a message ties them to a payment word,
    or when the user named them alone in reply to a question asking only
    who paid (answers, from payer_answers()). Returns (data, fired) where
    fired names the checks that cleared a payer, so the pipeline asks.
    """
    grounded = copy.deepcopy(data)
    clauses = _clauses(texts)
    items = grounded.get("items", [])
    answered_expense, item_answers = _resolve_answers(answers or [], items)
    fired = []

    def answered(person, *named):
        person = _canonical(person, current_user)
        return any(name is not None and name == person for name in named)

    payer = grounded.get("payer")
    if (
        payer is not None
        and not _payer_grounded(payer, clauses, current_user)
        and not answered(payer, answered_expense)
    ):
        grounded["payer"] = None
        fired.append("payer")

    cleared_item = False
    for index, item in enumerate(items):
        paid_by = item.get("paidBy")
        item_answer = item_answers.get(index)
        if (
            paid_by
            and not _payer_grounded(paid_by, clauses, current_user)
            and not answered(paid_by, item_answer, answered_expense)
        ):
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
