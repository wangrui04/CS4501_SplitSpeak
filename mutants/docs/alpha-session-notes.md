# Alpha Session Notes

Running notes taken during the benchmark session. Record official pass/fail results in [alpha-results.md](alpha-results.md); this file holds the observations behind them.

---

## Session configuration

| Setting | Value |
| --- | --- |
| Commit SHA | `ce169ce` |
| Model | `openai/gpt-oss-120b` |
| Prompt version | `2026-11-02.3` |
| `LLM_PROVIDER` | `groq` |
| Tester | _name_ |

---

## Notes by run

### Run 1

| Scenario | Result | Prompts | Observation |
| --- | --- | ---: | --- |
| B1 Basic | Pass | 1 | No question asked, as expected. |
| B2 Moderate | Pass | 2 | Bot asked only "Who paid for this expense?", not about tax or tip. The full scripted follow-up was sent verbatim and also gave the tax and tip. |
| B3 Intermediate | Pass | 2 | Bot asked only for the nachos price. The scripted follow-up gave all prices, the split rule, and tax and tip. |
| B4 Advanced | Pass | 2 | Bot restated the full plan (house by nights 3 / 3 / 1, groceries equally, transportation between Sarah and Kayla) and asked for confirmation. |
| B5 Most complex (first attempt) | Invalid (tester error) | 3 | Bot showed a preview after turn 1 and again after the correction, without asking about the refund. Turn 3 (`if_asked`) was sent anyway, so the preview that should have been judged was not recorded. Redone below. |
| B5 Most complex (redo) | Pass | 2 | Preview after turn 1, then the correction (sent always) produced a preview matching the key; turn 3 correctly not sent. Behavior check not met: the bot never asked a question before the final preview (recorded only; does not affect pass/fail). |

**Run 1 total: 5 / 5 passed** (B5 counted from the redo).

### Run 2

| Scenario | Result | Prompts | Observation |
| --- | --- | ---: | --- |
| B1 Basic | Pass | 1 | No question asked. |
| B2 Moderate (first attempt) | Invalid (input not verbatim), redo | 2 | After turn 2 the bot replied: "Here's how I'd split it: the $18 meal for Rui (paid by Rui) shared only by Rui, the $24 meal for Sarah (paid by Sarah) shared only by Sarah, the $30 meal for Kayla (paid by Kayla) shared only by Kayla. The $6 tax and $14.40 tip are split proportionally based on the meal amounts (Rui 18, Sarah 24, Kayla 30). The overall bill payer is currently unspecified. Is this correct, and who should be set as the overall payer?" It read "everyone pays for their own food" as each person paying for their own meal and ignored "i paid" in turn 2. Tax and tip handling was correct. No scripted turns left, so the attempt ended. Category: multiple payers. Possible cause to review after the session: the prompt rule to set a payer only when the user says who paid may have treated "pays" in "everyone pays for their own food" as a payment statement. Run 1's B2 passed with the same configuration, so this also shows run-to-run variability. Input not verbatim: turn 2 was sent as "...based on what we ordered '" with a stray trailing apostrophe, so the attempt is invalid and is being redone. Under the same rule, any attempt with non-verbatim input is invalid whether it passed or failed. Without the stray character this attempt would have been a fail (ran out of script). |
| B2 Moderate (redo) | Pass | 2 | Bot asked "Who paid for this expense?" (the app's question, shown because the model left the payer empty). The verbatim turn 2 produced the correct split: $30.80 / $38.50 / $23.10, Kayla pays Sarah $38.50, Rui pays Sarah $23.10. |

**Run 2 total: 5 / 5 passed** (B2 counted from the redo).
| B3 Intermediate | Pass | 2 | Asked only "What was the price of the Nachos?". The scripted follow-up covered everything. |
| B4 Advanced | Pass | 2 | Asked an either/or question ("For the groceries $120 (paid by Rui) should the cost be split equally among Sarah, Rui, and Kayla, or weighted by the number of nights each stayed?") despite the confirm-the-plan rule. The scripted reply still produced the correct split. |
| B5 Most complex | Pass | 2 | Preview after turn 1 (correct for the original details: $295 / $220 / $265), then a correct preview after the correction; turn 3 correctly not sent. Never asked a question (behavior check not met). |

### Run 3

| Scenario | Result | Prompts | Observation |
| --- | --- | ---: | --- |
| B1 Basic | Pass | 1 | No question asked. |
| B2 Moderate | Fail | 1 | Preview after turn 1 with no question, so turn 2 (`if_asked`) was not sent. The model set each meal as paid by the person who ate it (Rui $18, Sarah $24, Kayla $30), reading "everyone pays for their own food" as payments. The app's multi-payer trip rule (commit `2e411f2`: if every item has a payer and there is no tax or tip, the main payer is whoever paid most) then chose Kayla as the payer instead of asking "Who paid?". Shares $24 / $30 / $18, no tax or tip. Category: multiple payers. Root cause is partly the app: before `2e411f2`, the same misreading would have triggered the "Who paid?" question. |
| B3 Intermediate | Pass | 2 | Asked only "What is the total price for the nachos?". The scripted follow-up covered everything. |
| B4 Advanced | Pass | 1 | Previewed right after turn 1 without confirming what "split it fairly" meant, so turn 2 (`if_asked`) was not sent. Its own choice (house by nights 3 / 3 / 1, groceries equal, transportation Sarah + Kayla) matched the key. Behavior check not met. |
| B5 Most complex | Pass | 2 | Preview after turn 1 (correct for the original details: $295 / $220 / $265), then a correct preview after the correction; turn 3 correctly not sent. Never asked a question (behavior check not met). |

**Run 3 total: 4 / 5 passed.**

**Session total: 14 / 15 passed (93.3%).** Threshold: ≥ 14 / 15.
