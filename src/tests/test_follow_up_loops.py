"""Issue #53: follow-up answers to the app's own questions, and no loops.

Red-team session (docs/red-teaming-feedback-1.md) found two problems
with the #49 grounding checks:
- "Who paid?" -> "Rui" was asked again forever, because a bare name has
  no payment word next to it.
- With per-item payers the app asked the generic "Who paid for this
  expense?", and the user answered "Which expense?".
"""

from backend.grounding import (
    ITEM_PAYER_QUESTION,
    PAYER_QUESTION,
    ground_payers,
    payer_answers,
    repeat_hint,
    user_texts,
)
from backend.llm import FakeLlmClient
from backend.pipeline import parse_turn


ROSTER = ["Sarah", "Kayla", "Rui"]


def item(name, price, names=(), mode="only", paid_by=None):
    return {
        "name": name,
        "quantity": 1,
        "unitPrice": price,
        "participants": {"mode": mode, "names": list(names)},
        "paidBy": paid_by,
    }


def parsed(items, payer=None, questions=()):
    return {
        "description": "Expense",
        "payer": payer,
        "items": items,
        "charges": [],
        "statedTotal": None,
        "openQuestions": [{"field": "x", "question": q} for q in questions],
    }


def user(text):
    return {"role": "user", "content": text}


def app(text):
    return {"role": "assistant", "content": text}


def run(raw, conversation, current_user="Kayla"):
    return parse_turn(
        llm=FakeLlmClient([raw]),
        conversation=conversation,
        roster=ROSTER,
        current_user=current_user,
    )


def ground(data, conversation, current_user="Kayla"):
    answers = payer_answers(conversation, ROSTER, current_user)
    return ground_payers(data, user_texts(conversation), current_user, answers)


# ------------------------------------------------------- answers as evidence


def test_bare_name_answer_grounds_the_payer():
    conversation = [user("lunch was 20"), app(PAYER_QUESTION), user("Rui")]

    data, fired = ground(parsed([item("Lunch", "20", mode="all")], payer="Rui"), conversation)

    assert data["payer"] == "Rui"
    assert fired == []


def test_me_answer_grounds_the_signed_in_user():
    conversation = [user("lunch was 20"), app(PAYER_QUESTION), user("me")]

    for payer in ("ME", "Kayla"):
        data, _ = ground(parsed([], payer=payer), conversation)
        assert data["payer"] == payer


def test_answer_with_a_name_typo_grounds_the_member():
    conversation = [user("lunch was 20"), app(PAYER_QUESTION), user("riu")]

    data, _ = ground(parsed([], payer="Rui"), conversation)

    assert data["payer"] == "Rui"


def test_answer_naming_two_members_grounds_neither():
    conversation = [user("lunch was 20"), app(PAYER_QUESTION), user("Rui and Sarah")]

    for payer in ("Rui", "Sarah"):
        data, fired = ground(parsed([], payer=payer), conversation)
        assert data["payer"] is None
        assert fired == ["payer"]


def test_name_answering_a_different_question_is_not_evidence():
    conversation = [user("lunch"), app("How much was Lunch?"), user("Rui")]

    data, _ = ground(parsed([], payer="Rui"), conversation)

    assert data["payer"] is None


def test_answer_to_an_llm_worded_question_is_not_evidence():
    conversation = [user("lunch was 20"), app("Who covered the bill?"), user("Rui")]

    data, _ = ground(parsed([], payer="Rui"), conversation)

    assert data["payer"] is None


def test_item_answer_grounds_only_that_item():
    question = ITEM_PAYER_QUESTION.format(item="Pizza 1")
    conversation = [user("pizzas were 10 and 15"), app(question), user("Rui")]
    items = [
        item("Pizza 1", "10", ["ME", "Rui"], paid_by="Rui"),
        item("Pizza 2", "15", ["Sarah", "Rui"], paid_by="Rui"),
    ]

    data, _ = ground(parsed(items), conversation)

    assert [it["paidBy"] for it in data["items"]] == ["Rui", None]


def test_answer_to_the_hint_also_counts():
    hint = repeat_hint(PAYER_QUESTION, ROSTER, "Kayla")
    conversation = [user("lunch was 20"), app(PAYER_QUESTION), user("idk"), app(hint), user("Rui")]

    data, _ = ground(parsed([], payer="Rui"), conversation)

    assert data["payer"] == "Rui"


# ------------------------------------------- red-team conversations (pipeline)

PIZZAS = (
    "I shared a pizza with Rui that she paid for. "
    "Sarah paid for another pizza and Rui had one slice."
)


def pizza_items():
    return [
        item("Pizza 1", "10", ["ME", "Rui"], paid_by="Rui"),
        item("Pizza 2", "15", ["Sarah", "Rui"], paid_by="Sarah"),
    ]


def pizza_conversation():
    return [
        user(PIZZAS),
        app("What was the price of the first pizza shared by you and Rui?"),
        user("$10"),
        app("What was the price of the second pizza that Sarah paid for?"),
        user("$15"),
    ]


def test_red_team_pizzas_ask_about_the_specific_pizza():
    result = run(parsed(pizza_items()), pizza_conversation())

    assert result == {"type": "question", "question": "Who paid for Pizza 1?"}


def test_red_team_pizzas_preview_after_naming_the_payer():
    conversation = pizza_conversation() + [app("Who paid for Pizza 1?"), user("Rui")]

    result = run(parsed(pizza_items()), conversation)

    assert result["type"] == "preview", result.get("question")
    paid = {entry["name"]: entry["cents"] for entry in result["preview"]["paid"]}
    assert paid == {"Sarah": 1500, "Kayla": 0, "Rui": 1000}


def test_red_team_bare_name_answer_does_not_loop():
    conversation = [
        user("Rui lent me $20 at 5% interest each day and it's been 2 days"),
        app(PAYER_QUESTION),
        user("Rui"),
    ]
    raw = parsed([item("Loan", "20", ["ME"])], payer="Rui")

    result = run(raw, conversation)

    assert result.get("question") != PAYER_QUESTION
    assert result["type"] == "preview", result.get("question")


def test_generic_question_kept_when_no_payer_is_known():
    raw = parsed([item("Lunch", "20", mode="all")])

    result = run(raw, [user("lunch was 20")])

    assert result == {"type": "question", "question": PAYER_QUESTION}


# --------------------------------------------------------------- loop guard


def test_same_payer_question_twice_becomes_the_hint():
    conversation = [user("lunch was 20"), app(PAYER_QUESTION), user("Rui and Sarah")]
    raw = parsed([item("Lunch", "20", mode="all")], payer="Rui")

    result = run(raw, conversation)

    assert result == {
        "type": "question",
        "question": (
            "I still need to know who paid for this expense. "
            "Reply with just a name, e.g. Sarah."
        ),
    }


def test_item_question_hint_names_the_item():
    question = ITEM_PAYER_QUESTION.format(item="Pizza 1")
    conversation = pizza_conversation() + [app(question), user("which expense?")]

    result = run(parsed(pizza_items()), conversation)

    assert result["question"] == (
        "I still need to know who paid for Pizza 1. Reply with just a name, e.g. Sarah."
    )


def test_hint_example_is_never_the_signed_in_user():
    assert repeat_hint(PAYER_QUESTION, ROSTER, "Sarah").endswith("e.g. Kayla.")


def test_repeated_llm_question_gets_a_generic_hint():
    question = "Should the nachos be split by slices or equally?"
    conversation = [user("nachos 12"), app(question), user("hmm")]
    raw = parsed([item("Nachos", "12", mode="all")], payer="ME", questions=[question])

    result = run(raw, conversation)

    assert result == {
        "type": "question",
        "question": f"I still need this before I can show a preview: {question}",
    }


def test_third_time_ends_in_manual_fallback():
    hint = repeat_hint(PAYER_QUESTION, ROSTER, "Kayla")
    conversation = [
        user("lunch was 20"),
        app(PAYER_QUESTION),
        user("not sure"),
        app(hint),
        user("which one"),
    ]
    raw = parsed([item("Lunch", "20", mode="all")])

    result = run(raw, conversation)

    assert result["type"] == "unresolved"
    assert "manually" in result["reason"]


def test_a_different_question_is_not_a_repeat():
    conversation = [user("lunch"), app("How much was Lunch?"), user("20")]
    raw = parsed([item("Lunch", "20", mode="all")])

    result = run(raw, conversation)

    assert result == {"type": "question", "question": PAYER_QUESTION}


# ------------------------------------------- "Kayla bought $10 worth of pizza"


def test_kayla_bought_pizza_previews():
    raw = parsed([item("Pizza", "10", mode="all")], payer="Kayla")

    result = run(raw, [user("Kayla bought $10 worth of pizza")], current_user="Sarah")

    assert result["type"] == "preview", result.get("question")
    assert result["preview"]["payer"] == "Kayla"


def test_kayla_bought_pizza_as_item_payer_previews():
    raw = parsed([item("Pizza", "10", mode="all", paid_by="Kayla")])

    result = run(raw, [user("Kayla bought $10 worth of pizza")], current_user="Sarah")

    assert result["type"] == "preview", result.get("question")
    assert result["preview"]["payer"] == "Kayla"


# ------------------------------------- AI-worded payer questions (Run 2 retest)


def test_ai_worded_pure_payer_question_counts():
    conversation = [user("lunch was 20"), app("Who paid for the lunch?"), user("Rui")]

    data, fired = ground(parsed([item("Lunch", "20", mode="all")], payer="Rui"), conversation)

    assert data["payer"] == "Rui"
    assert fired == []


def test_payer_question_that_also_asks_something_else_does_not_count():
    for question in (
        "Who paid, and how should it be split?",
        "Who paid for the lunch and who shared it?",
        "Who paid? How much was it?",
    ):
        conversation = [user("lunch was 20"), app(question), user("Rui")]
        data, _ = ground(parsed([], payer="Rui"), conversation)
        assert data["payer"] is None, question


def test_red_team_run_2_previews_after_plain_answer_to_ai_question():
    conversation = [
        user("lunch for me and Rui was $20, split evenly"),
        app(PAYER_QUESTION),
        user("Rui and Sarah"),
        app("You indicated that Rui and Sarah paid. Did they split the $20 between them?"),
        user("not sure"),
        app("Who paid for the lunch?"),
        user("Rui"),
    ]
    raw = parsed([item("Lunch", "20", ["ME", "Rui"])], payer="Rui")

    result = run(raw, conversation)

    assert result["type"] == "preview", result.get("question")
    assert result["preview"]["payer"] == "Rui"


# ------------------------------------------------------ duplicate item names


def same_name_pizzas(second_price="15"):
    return [
        item("Pizza", "10", ["ME", "Rui"]),
        item("Pizza", second_price, ["Sarah", "Rui"], paid_by="Sarah"),
    ]


DUPLICATE_TEXT = "a $10 pizza with Rui and Sarah paid for a $15 pizza"


def test_duplicate_item_names_are_told_apart_by_price():
    result = run(parsed(same_name_pizzas()), [user(DUPLICATE_TEXT)])

    assert result == {"type": "question", "question": "Who paid for Pizza ($10)?"}


def test_duplicate_names_and_prices_are_numbered():
    text = "a $10 pizza with Rui and Sarah paid for another $10 pizza"

    result = run(parsed(same_name_pizzas(second_price="10")), [user(text)])

    assert result == {"type": "question", "question": "Who paid for Pizza #1?"}


def test_answer_to_a_labelled_duplicate_grounds_that_item():
    items = same_name_pizzas()
    items[0]["paidBy"] = "Rui"
    conversation = [user(DUPLICATE_TEXT), app("Who paid for Pizza ($10)?"), user("Rui")]

    result = run(parsed(items), conversation)

    assert result["type"] == "preview", result.get("question")
    paid = {entry["name"]: entry["cents"] for entry in result["preview"]["paid"]}
    assert paid == {"Sarah": 1500, "Kayla": 0, "Rui": 1000}
