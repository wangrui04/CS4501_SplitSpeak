# SplitSpeak — Red Team Feedback Response & Remediation Plan

**Project:** SplitSpeak (Conversational Expense Assistant)  
**Source:** `feedback.md` — *Alpha Test Feedback & Bug Analysis Report*  
**Response date:** November 17, 2026  
**Repository:** https://github.com/wangrui04/CS4501_SplitSpeak

## 1. Summary and prioritization

We appreciate the Red Team's feedback. We agree that the most significant risk is **incorrect or missing payer information**, particularly when a request contains multiple expenses. This issue is compounded by the assistant's tendency to repeat clarification questions instead of correctly using information supplied in earlier turns. Both problems threaten the reliability of SplitSpeak's primary function: generating an accurate, understandable expense split.

The ratings below are **qualitative estimates based on the reported alpha-test behavior**, not measured production incident rates.

| Finding | Likelihood | Business / user impact | Priority |
| --- | --- | --- | --- |
| **1. Missing or incorrect payer extraction and `null` errors** | High — observed even in relatively simple scenarios | High — can block expense creation or attribute payment to the wrong person, producing incorrect balances and reducing trust | **Critical** |
| **2. Inconsistent parsing of multi-clause, multi-item prompts** | High — Red Team observed different outcomes on repeated attempts | High — may produce plausible but incorrect expense calculations | **Critical** |
| **3. Repeated questions and loss of conversational context** | High — reproduced in a Red Team session | Medium–High — prevents task completion and creates user frustration; unsupported loan scenarios also expose a scope-handling gap | **High** |

## 2. Response to each finding

### Finding 1 — Payer extraction failures, ambiguity, and silent errors

**Red Team finding:** SplitSpeak sometimes fails to identify who paid, even when the payer is provided, and may ask the ambiguous question “Who paid for this expense?” when several items are being discussed. The report also describes `null` values or crashes.

**Remediation:**

1. **Make clarification questions item-specific.** Ask which person paid for the particular item (and include its price when necessary), rather than asking a generic payer question. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56)
2. **Preserve answers to payer questions.** Recognize a one-name reply such as “Rui” as an answer to a single-payer clarification; avoid losing it in a later turn. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56), [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
3. **Ground extracted fields in user-provided evidence.** Request exact text evidence for an item's payer and price, and reject contradictory evidence before generating a preview. Continue to use existing grounding checks when evidence is absent. [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
4. **Check for silent failures.** Add or retain regression cases for missing/`null` payer values and ensure the application asks a specific question or gives a clear fallback instead of failing silently. This is a **verification / follow-up item**; the PR descriptions do not establish that every possible `null` crash has been eliminated.

**Success criteria:** A multi-item conversation with different payers leads to item-specific, nonrepeating clarification questions; a supplied payer is retained; no expense is finalized with an unsupported payer assignment or an unhandled `null` error.

### Finding 2 — Inconsistent interpretation of complex requests

**Red Team finding:** For a prompt involving a $10 pizza bought by Sarah and a $20 pizza bought by Rui, the assistant sometimes treats Rui as the payer of everything or applies a uniform split, despite giving the correct response on other runs.

**Remediation:**

1. **Validate each item independently.** Match each item's payer and price to the user's words instead of transferring one item's details to another. [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
2. **Verify tax, tip, and weighted splits.** Reject contradictory evidence (including swapped tax/tip amounts); clarify when a weight may have been applied to an unrelated item. [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
3. **Expand repeatability testing.** Re-run multi-sentence, multi-item prompts multiple times, including variations in wording, fractional shares, multiple payers, and item-specific weighted splits. Use the Red Team's two-pizza case as a required regression scenario.
4. **Tighten acceptance criteria.** A test passes only when the parsed payer, item amounts, allocation method, and resulting shares are all correct—not merely when the system produces a preview.

**Success criteria:** Repeated tests of the same complex scenario consistently preserve each item's payer and split instructions; ambiguous scenarios produce clarification rather than a confident incorrect preview.

### Finding 3 — Conversational loops and unsupported loan requests

**Red Team finding:** SplitSpeak asks for a payer repeatedly even after receiving an answer. One reported loop occurred with a loan-and-interest prompt.

**Remediation:**

1. **Add a repeated-question guard.** A repeated clarification should be reworded more clearly, then fall back to manual entry rather than looping indefinitely. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56)
2. **Reuse already supplied context.** Treat a simple response to a payer-only question as confirmation of that payer and avoid overwriting previously confirmed information with an empty field. [PR #56](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56), [PR #59](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59)
3. **Handle out-of-scope requests explicitly.** Loans, interest, and repayments are outside the current expense-entry MVP. Return an explanatory message at the first turn, without creating an expense or changing balances. [PR #57](https://github.com/wangrui04/CS4501_SplitSpeak/pull/57)
4. **Test full conversations.** Replay Red Team examples from the initial prompt through clarifications, not just isolated model responses.

**Success criteria:** No repeated payer-question loop; supported expense requests reach a correct preview or a clear manual-entry fallback; loan/interest requests are identified as unsupported without affecting balances.

## 3. Implementation and verification status

The following were **open pull requests when this response was prepared**. Their reported test results are from the PR descriptions; they should not be presented as merged or independently verified release results.

| PR | Proposed change | Reported evidence / remaining work |
| --- | --- | --- |
| [#56 — Follow-up loops](https://github.com/wangrui04/CS4501_SplitSpeak/pull/56) | Item-specific payer clarification, preservation of short answers, repeat-question guard, multi-turn tests | PR reports **512 backend tests passed** and successful Red Team live retests. **Merge pending.** |
| [#57 — Out-of-scope loans](https://github.com/wangrui04/CS4501_SplitSpeak/pull/57) | Explicit handling of loans, interest, repayments | PR reports **523 backend tests passed** and three relevant live checks. **Merge pending.** Recognition currently depends on the model setting an unsupported flag. |
| [#59 — Evidence grounding](https://github.com/wangrui04/CS4501_SplitSpeak/pull/59) | Exact-text evidence for payer, item price, and charges; guard against cross-item confusion | PR reports **552 backend tests passed**. **Benchmark B4 must be rerun:** its earlier version failed **2 of 3** live attempts on item-specific weighting; the updated prompt had not yet been retested. Other benchmarks also need final-prompt reruns. **Merge pending.** |

**Planned verification before closing the findings:**

- [ ] Merge dependent changes in the documented order: **#56 → #57 → #59**, after each PR's required checks pass.
- [ ] Rerun **B4** against PR #59's latest prompt, followed by **B1, B2, and B5** on the final version.
- [ ] Replay the Red Team's **two-pizza** and **loan-interest** conversations end to end, including repeated runs of the two-pizza prompt.
- [ ] Verify that expense balances are unchanged after rejected / out-of-scope inputs and that no unhandled `null` errors occur.
- [ ] Reopen or create follow-up issues if any failures remain; document expected versus actual behavior in regression tests.

## 4. Final response to the Red Team

The Red Team exposed weaknesses that our simpler, single-turn test cases did not reliably capture. In response, we are strengthening **payer and price grounding**, **multi-turn clarification handling**, and **out-of-scope detection**, while expanding regression tests to cover complex scenarios and repeated runs. Our immediate priority is to confirm these changes work consistently—particularly the weighted-split B4 scenario—before treating the findings as resolved. The ultimate goal is not simply to make the assistant answer more often, but to ensure it **asks for clarification rather than saving or previewing an incorrect split**.
