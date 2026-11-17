# SplitSpeak — Red Team Feedback Response & Remediation Plan

**Project:** SplitSpeak (Splitwise with a Conversational Expense Assistant)
**Red team report:** [`docs/red_teaming_feedback.md`](red_teaming_feedback.md), *Alpha Test Feedback & Bug Analysis Report*
**Presentation:** "When the AI loses track of who paid"
**Response date:** November 17, 2026
**Repository:** https://github.com/wangrui04/CS4501_SplitSpeak

Thank you to our Red Team for a focused, reproducible report. Every finding came with a real conversation we could replay, which made root-causing fast. Each of those conversations is now an automated regression test.

---

## 1. Summary and prioritization

We agree that the most significant risk is **incorrect or missing payer information**, particularly when a request contains multiple expenses. Two failures reinforce each other: the assistant sometimes **assigns a purchase to the wrong person**, and our follow-up logic **did not reuse answers from earlier turns**, so it repeated "Who paid?". Both threaten SplitSpeak's primary function: an accurate, understandable expense split.

Following our professor's guidance after alpha (don't rely on the LLM to decide whether required information was given), every fix is **deterministic application code**; the LLM still only interprets text.

The ratings below are **qualitative estimates based on the reported alpha-test behavior**, not measured production incident rates.

| Finding | Likelihood | Business / user impact | Priority |
| --- | --- | --- | --- |
| **1. Missing or incorrect payer extraction and `null` errors** | High: observed even in relatively simple scenarios | High: can block expense creation or attribute payment to the wrong person | **Critical** |
| **2. Inconsistent parsing of multi-clause, multi-item prompts** | High: the Red Team saw different outcomes on repeated attempts | High: may produce plausible but incorrect splits | **Critical** |
| **3. Repeated questions and loss of conversational context** | High: reproduced in a Red Team session | Medium–High: prevents task completion; the loan example also exposed a scope-handling gap | **High** |

Impact is shaped by our **confirmation gate**: no AI result changes balances until the user approves the itemized preview. Loops are therefore frustrating but don't save anything wrong. A misassigned payer is the most serious case, because the preview *looks* valid and a user may confirm it.

---

## 2. Response to each finding

### Finding 1 — Payer extraction failures, ambiguity, and silent errors

**Red Team finding:** SplitSpeak sometimes fails to identify who paid, even when the payer was given, and asks the ambiguous "Who paid for this expense?" when several items are involved (the user replied "Which expense?"). The report also describes `null` values or crashes.

**Root cause (verified by replaying the conversation):** the app had no item-specific payer question. A pronoun ("a pizza with Rui **that she paid for**") left one item without a grounded payer, and the generic question didn't say which item it meant. With tax and tip, it also asked the generic question when every item already had a payer and only the charges were unclaimed.

**Remediation:**

1. **Make clarification questions item-specific.** Ask "Who paid for Pizza ($10)?" (adding the price when two items share a name), or "Who paid the tax and tip?" when only the charges are unclaimed. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56), [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
2. **Preserve answers to payer questions.** Treat a one-name reply ("Rui", "me") to a question that asks only who paid as the answer. If the app asked and the LLM still leaves that payer empty, the answer fills it in; it never overrides a payer the LLM set, so later corrections still win. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56), [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
3. **Ground extracted fields in user-provided evidence.** Request the exact text behind each item's payer and price, and reject contradictory evidence before showing a preview. The existing grounding checks still apply when evidence is missing or paraphrased. [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
4. **Check for silent failures.** We could not reproduce a crash for "Kayla bought $10 worth of pizza" with scripted or live model output; it previews correctly, and two regression tests now cover it. This remains a **verification / follow-up item**: the PRs do not prove that every possible `null` crash is gone, and we'd welcome the server log if it recurs.

**Success criteria:** A multi-item conversation with different payers leads to item-specific, non-repeating clarification questions; a supplied payer is retained; no expense is finalized with an unsupported payer assignment or an unhandled `null` error.

### Finding 2 — Inconsistent interpretation of complex requests

**Red Team finding:** For "Sarah bought a $10 pizza and I ate ⅔ of it. Rui bought a $20 pizza and shared it evenly.", the assistant sometimes treats Rui as the payer of everything or applies a uniform split, but answers correctly on other runs.

**Root cause (verified):** our earlier grounding check (#49) confirmed that a payer's name appeared *anywhere* next to a payment word, not *for that item*. "Rui bought" really is typed, so Rui passed for every item. Amounts had the same gap: a swapped tax and tip are both numbers the user typed.

**Remediation:**

1. **Notice a dropped payer.** If the user said "Sarah paid…" but the LLM's reading has Sarah paying for nothing, the app asks "What did Sarah pay for?" instead of previewing. It's asked once per person, and names must match exactly. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56)
2. **Validate each item independently.** Match each item's payer and price to the user's own words. A word-for-word quote that contradicts its value is rejected; for example, "Rui bought a $20 pizza" offered as the payer of the $10 pizza becomes "Who paid for Pizza ($10)?". [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
3. **Verify tax, tip, and weighted splits.** A charge's amount must be the number nearest its own word in the quote, so "tax 9 tip 18" with tax = 18 is rejected (swapped tax and tip). A prompt rule keeps weights (e.g. nights stayed) on the items the user tied them to, and asks otherwise. [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
4. **Expand repeatability testing.** Re-run multi-sentence, multi-item prompts several times, with variations in wording, fractional shares, multiple payers, and item-specific weights. The Red Team's two-pizza case is a required regression scenario.
5. **Tighten acceptance criteria.** A test passes only when the parsed payer, item amounts, allocation method, and resulting shares are all correct, not merely when a preview appears.

**Success criteria:** Repeated runs of the same complex scenario consistently keep each item's payer and split instructions; ambiguous scenarios produce a clarification instead of a confident incorrect preview.

### Finding 3 — Conversational loops and unsupported loan requests

**Red Team finding:** SplitSpeak asked for a payer repeatedly even after receiving an answer. One reported loop occurred with "Rui lent me $20 at 5% interest each day and it's been 2 days".

**Root cause (verified, reproduced):** the payer check required a payment word ("Rui paid"). A bare answer, "Rui", never counted, so the payer was cleared and the question repeated. Separately, a loan isn't a shared expense, so no answer could ever produce a valid split.

**Remediation:**

1. **Add a repeated-question guard.** The app never asks the exact same question twice in a row: the second time it asks a clearer version ("I still need to know who paid for this expense. Reply with just a name, e.g. Sarah."), and if that is unanswered too, it offers manual entry. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56)
2. **Reuse already supplied context.** Treat a simple reply to a payer-only question as the payer (Finding 1, item 2), and never overwrite a confirmed payer with an empty field. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56), [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
3. **Ask for missing details together.** All of the LLM's open questions are shown in one message (previously only the first was shown), and the prompt asks for every missing fact at once, so the 5-prompt limit isn't spent one fact at a time. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56)
4. **Handle out-of-scope requests explicitly.** Loans, interest, and repayments are outside the MVP. The LLM flags them (`unsupported: "loan" | "other"`), and the app replies on the first turn ("I can only split shared expenses, not loans, interest, or repayments…"), pointing to Settle up or manual entry, without creating an expense or changing balances. We deliberately did **not** add interest calculation, since it would change what the product is. [PR #57](https://github.com/wangrui04/CS4501_SplitSpeak/pull/57)
5. **Test full conversations.** Replay the Red Team examples from the first prompt through every clarification, not just isolated model responses.

**Success criteria:** No repeated payer-question loop; supported expense requests reach a correct preview or a clear manual-entry fallback; loan and interest requests are identified as unsupported without affecting balances.

---

## 3. Response to the Red Team's recommendations

| Recommendation | Status |
| --- | --- |
| Deterministic grounding checks against raw user text | ✅ Payer, amount, and charge checks, the dropped-payer check, and evidence-quote verification, all in code (`src/backend/grounding.py`) |
| Multi-turn, multi-item test coverage | ✅ Both Red Team conversations are replayed turn by turn (`src/tests/test_follow_up_loops.py`), plus multi-item evidence tests (`src/tests/test_evidence_quotes.py`) and out-of-scope tests (`src/tests/test_out_of_scope.py`) |
| State locking: don't let later turns null a validated payer | ✅ Answers to payer questions persist across turns and fill an empty payer; the repeated-question guard ends loops |
| Tighten US-06 and test complex prompts over repeated runs | 🔄 Three multi-item prompts run live, all correct so far; the B4 weighted-split rerun is pending (Section 4) |

---

## 4. Implementation and verification status

The following were **open pull requests when this response was prepared**. Results come from local test runs and live retests recorded in each PR description; they should not be presented as merged or independently verified release results.

| PR | Change | Evidence / remaining work |
| --- | --- | --- |
| [#56 — Follow-up loops](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56) (issue #53) | Item-specific payer questions, short-answer handling, repeated-question guard, dropped-payer check, batched questions, multi-turn tests | **512 backend tests passed**; offline benchmark **20/20**; Red Team conversations retested live. **Merge pending.** |
| [#57 — Out-of-scope loans](https://github.com/wangrui04/CS4501_SplitSpeak/pull/57) (issue #54) | Explicit handling of loans, interest, repayments | **523 backend tests passed**; three live checks passed (loan, repayment, "I lent Rui my card" purchase still works). Depends on the model setting the flag. **Merge pending.** |
| [#59 — Evidence grounding](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59) (issue #55) | Exact-text evidence for payer, item price, and charges; "Who paid the tax and tip?"; fill an empty payer from the app's own question; weights stay on their items | **552 backend tests passed**; offline benchmark **20/20**. **B4 must be rerun:** on the previous prompt it failed **2 of 3** live attempts (nights applied to every item), and the rerun on the new prompt was blocked by the LLM provider's rate limit. **Merge pending.** |

**Live retests so far (Groq):**

| Scenario | Result |
| --- | --- |
| Red Team pizzas → item-specific question → plain "Rui" | ✅ Correct preview: Rui paid $10, Sarah paid $15 |
| Plain-name answer to "Who paid?" (incl. AI-worded "Who paid for the lunch?") | ✅ Preview, no repeat |
| Loan with interest; repayment ("Rui paid me back $15") | ✅ Out-of-scope message on the first reply |
| Two pizzas with ⅔ share | ✅ Sarah paid $10, Rui paid $20 |
| Tacos + drinks + tax/tip | ✅ Rui $33, Sarah $9; Tax $3 and Tip $6 not swapped |
| Groceries / snacks / movies, three payers | ✅ Kayla $40, Sarah $12, Rui $18 |
| Benchmarks B1, B2, B3 | ✅ |
| Benchmark B4 (weighted split) | ⚠️ Pending rerun on the final prompt |

**Planned verification before closing the findings:**

- [ ] Merge dependent changes in order, **#56 → #57 → #59**, after each PR's required checks pass.
- [ ] Rerun **B4** three times against PR #59's latest prompt, then **B1, B2, and B5** once on the final version.
- [ ] Replay the Red Team's **two-pizza** and **loan-interest** conversations end to end, including repeated runs of the two-pizza prompt.
- [ ] Confirm balances are unchanged after rejected or out-of-scope inputs, and that no unhandled `null` errors occur.
- [ ] Reopen or create follow-up issues for any remaining failures, recording expected versus actual behavior in regression tests.

**Known limits and next steps:**

- **B4 not yet confirmed.** If the new prompt rule doesn't fix it, we'll add a code-generated confirmation of weighted splits ("House by nights 3/3/1, Groceries equal… Is that right?") as its own issue.
- **The repeated-question guard catches exact repeats only.** The LLM can still rephrase a question it already asked; the 5-prompt limit remains the final backstop.
- **Evidence and the out-of-scope flag depend on the model returning them.** When it omits them, the older deterministic checks still apply.

---

## 5. Final response to the Red Team

The Red Team exposed weaknesses that our simpler, single-turn test cases did not reliably capture. In response, we strengthened **payer and price grounding**, **multi-turn clarification handling**, and **out-of-scope detection**, and expanded regression tests to cover complex scenarios and full conversations. Our immediate priority is to confirm these changes work consistently, particularly the weighted-split B4 scenario, before treating the findings as resolved. The goal is not to make the assistant answer more often, but to make sure it **asks for clarification rather than previewing or saving an incorrect split**.
