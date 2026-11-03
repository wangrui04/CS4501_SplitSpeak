# Alpha Results: Benchmark Session (B1–B5)

This is the official alpha measurement (issue #33). Three team members each run the five benchmark scenarios in [benchmarks.md](benchmarks.md) through the UI, signed in as Sarah. That gives 15 attempts, and **at least 14 must pass**.

> If a teammate is already running the benchmark by hand, that run **is** this session. Agree on one person to record it here so it isn't done twice.

---

## 1. Frozen configuration

Fill this in **before** the session starts. Make no prompt or code changes until the session is over.

| Setting | Value |
| --- | --- |
| Date | 2026-11-02 |
| Commit SHA (`git rev-parse --short HEAD`) | `ce169ce` |
| Model | `openai/gpt-oss-120b` (via Groq) |
| Prompt version (`PROMPT_VERSION` in `src/backend/config.py`) | `2026-11-02.3` |
| `LLM_PROVIDER` | `groq` (never `fake` or `demo` for this session) |
| Recorder | Kayla Kim |

---

## 2. Procedure

1. Start the backend with a real `ANTHROPIC_API_KEY` and the frontend (see the README).
2. Sign in as **Sarah**, open **Apartment 4B**, and click **Add an expense** → **AI assistant**.
3. Use a **fresh conversation for each scenario**: close and reopen the modal, or click **Reset conversation**.
4. **Copy and paste** each prompt from [benchmarks.md](benchmarks.md). Never retype it.
5. Send follow-up turns by their mode:
   - `always`: send it after the bot's response, even if it already showed a preview. B5's correction is sent unprompted after the first preview.
   - `if_asked`: send it only if the bot asked a question it needs answered.
6. Compare the final preview with the key: **each person's share, amount paid, and every "who pays whom" transfer.**
7. Record the attempt in the table below. The prompt counter in the modal shows prompts used.

**Pass** = shares, amounts paid, and settlement all match exactly **and** the attempt used 5 prompts or fewer.

---

## 3. Attempts (15)

| # | Tester | Scenario | Conversation ID | Prompts | Shares match | Paid match | Settlement match | Pass | Notes |
| ---: | --- | --- | ---: | ---: | :---: | :---: | :---: | :---: | --- |
| 1 | Kayla Kim | B1 Basic | n/r | 1 | Y | Y | Y | ✅ | No question asked. |
| 2 | Kayla Kim | B2 Moderate | n/r | 2 | Y | Y | Y | ✅ | Asked only who paid; scripted reply also gave tax and tip. |
| 3 | Kayla Kim | B3 Intermediate | n/r | 2 | Y | Y | Y | ✅ | Asked only for the nachos price. |
| 4 | Kayla Kim | B4 Advanced | n/r | 2 | Y | Y | Y | ✅ | Restated full plan (house by nights, groceries equal, transportation Sarah + Kayla) and asked to confirm. |
| 5 | Kayla Kim | B5 Most complex | n/r | 2 | Y | Y | Y | ✅ | Redo: the first attempt was invalid (tester sent turn 3 without a question). Previews after turn 1 and after the correction; never asked a question (behavior check not met). |
| 6 | Kayla Kim | B1 Basic | | 1 | Y | Y | Y | ✅ | No question asked. |
| 7 | Kayla Kim | B2 Moderate | | 2 | Y | Y | Y | ✅ | Redo: the first attempt was invalid (turn 2 sent with a stray trailing "'"; it had run out of script). Redo asked "Who paid?", then the verbatim turn 2 produced the correct split. |
| 8 | Kayla Kim | B3 Intermediate | | 2 | Y | Y | Y | ✅ | Asked only for the nachos price. |
| 9 | Kayla Kim | B4 Advanced | | 2 | Y | Y | Y | ✅ | Asked an either/or question about groceries (equal or by nights) despite the confirm-the-plan rule; the scripted reply still produced the correct split. |
| 10 | Kayla Kim | B5 Most complex | | 2 | Y | Y | Y | ✅ | Preview after turn 1, then a correct preview after the correction; turn 3 correctly not sent. Never asked a question (behavior check not met). |
| 11 | Kayla Kim | B1 Basic | | 1 | Y | Y | Y | ✅ | No question asked. |
| 12 | Kayla Kim | B2 Moderate | | 1 | N | N | N | ❌ | Previewed after turn 1 without asking who paid; no tax or tip (shares $24 / $30 / $18). The model read "everyone pays for their own food" as each person paying for their own meal, and the app's trip rule (main payer = whoever paid most) then set Kayla as payer instead of asking. Category: multiple payers. |
| 13 | Kayla Kim | B3 Intermediate | | 2 | Y | Y | Y | ✅ | Asked only for the nachos price. |
| 14 | Kayla Kim | B4 Advanced | | 1 | Y | Y | Y | ✅ | Previewed after turn 1 without confirming what "fairly" meant (behavior check not met). Its own choice (house by nights, groceries equal, transportation Sarah + Kayla) matched the key. |
| 15 | Kayla Kim | B5 Most complex | | 2 | Y | Y | Y | ✅ | Preview after turn 1, then a correct preview after the correction; turn 3 correctly not sent. Never asked a question (behavior check not met). |

n/r = not recorded: the backend keeps conversations in memory and was restarted after Run 1, so those IDs were lost. For later attempts, the conversation ID is the `conversationId` field in each `/api/chat` response. To find it, open the browser dev tools, go to **Network**, and select the last `chat` request. With the ID, anyone can fetch the full transcript later from `GET /api/conversations/<id>`.

---

## 4. Results by scenario

Report per scenario, so one scenario failing for all three testers reads as one root cause, not three separate misses.

| Scenario | Passed (of 3) | Failure category | Root cause |
| --- | ---: | --- | --- |
| B1 Basic | 3 | — | — |
| B2 Moderate | 2 | multiple payers | Run 3: the model read "everyone pays for their own food" as each person paying for their own meal. The app's multi-payer trip rule (commit `2e411f2`) then picked the largest payer instead of asking "Who paid?", so no follow-up was possible and tax and tip were never added. In Run 2's (invalid) first attempt the same misreading appeared after turn 2. |
| B3 Intermediate | 3 | — | — |
| B4 Advanced | 3 | — | In Run 3 the model did not confirm "fairly" before previewing; it guessed the same rules as the key. |
| B5 Most complex | 3 | — | The model never asked a question in any run; corrections and the refund were applied correctly each time. |
| **Total** | **14 / 15** | | |

Invalid attempts (not counted, redone): Run 1 B5 (turn 3 sent without a question) and Run 2 B2 (turn 2 sent with a stray trailing apostrophe). Both are documented in [alpha-session-notes.md](alpha-session-notes.md).

Failure categories: participants, quantities, amounts, tax/tip, multiple payers, weights/nights, refund, correction, settlement, prompt limit.

---

## 5. Decision (Activity 1)

**Result:** 14 / 15 attempts passed (93.3%). The target is ≥ 14 / 15 (≥ 90%).

**Decision (draft for team review):** Validated, at the threshold, with caveats.

The assistant produced a split matching the answer key exactly (every cost share, amount paid, and settlement transfer) within 5 prompts in 14 of 15 attempts, meeting the 14 / 15 threshold with no margin. B1, B3, B4, and B5 passed in all three runs; the only failure was B2 in Run 3. That failure was a payer misreading ("everyone pays for their own food" taken as each person paying for their own meal), and an app rule for multi-payer trips then hid it instead of asking who paid. It is a specific, fixable root cause rather than a general weakness in extraction or calculation.

The result should be read with the limitations in §8. The margin is zero, all 15 attempts were run by one tester instead of three, and the model's clarifying-question behavior was inconsistent: B5 never asked a question, Run 3's B4 guessed what "fairly" meant, and B2 misread who paid in two of four attempts (including the invalid one). Next steps: fix the B2 root cause (below) and rerun the full session with three testers under the new version.

If the hypothesis was not validated:

Although the threshold was met, the B2 failure has a clear fix:

- **Root cause:** B2 Run 3, multiple payers: the model's misreading plus the app's trip-payer rule (see §4).
- **Fix plan:** when every item was paid only by the person who shares it (so nobody owes anyone), treat it as a likely misreading and ask "Who paid?" instead of picking a main payer. This is an app change in `src/backend/pipeline.py`, with tests written first.
- **Retest plan:** rerun all 5 scenarios with 3 testers under the new commit, recording the new commit SHA (and bumping `PROMPT_VERSION` only if the prompt changes).

---

## 6. Optional consistency runs

Run 1 above is official. Optionally repeat the session for Run 2 and Run 3 to check consistency:

| Scenario | Run 1 | Run 2 | Run 3 |
| --- | :---: | :---: | :---: |
| B1 Basic | | | |
| B2 Moderate | | | |
| B3 Intermediate | | | |
| B4 Advanced | | | |
| B5 Most complex | | | |

---

## 7. Supporting evidence: automated benchmark (ALPHA-32)

**Not available.** The automated benchmark could not complete on Groq's free tier. It was run once at the frozen commit with `--provider groq --runs 3`, but the runner sends prompts back to back, and from Run 1's B3 onward every request was rejected by Groq's rate limit (HTTP 429) before reaching the model. Only Run 1's B1 and B2 reached the model, and both passed. Because rate-limited attempts would be misreported as failures, that results file was discarded and is not used as evidence.

The runner and report themselves are built and tested (`src/tests/test_benchmark_runner.py`, `src/tests/test_benchmark_report.py`), and an offline run with scripted fixtures (`--provider fake`) reproduces every answer key. A live automated report needs a paid tier, or a pause between prompts (a possible future option for the runner).

Note: a single automated run of 5 scenarios passes 90% only at 5/5, because 4/5 is 80%. The human session above is the official result.

---

## 8. Limitations

- **One tester instead of three.** All 15 attempts were run by one team member (three runs of the five scenarios), not by three testers as planned. Results from a single person's runs are even more correlated.
- **Correlated testers.** Three testers paste identical scripts, so their attempts are not independent. A scenario the model gets wrong will usually fail for all three. That is why results are also reported per scenario.
- **Same team wrote the benchmark and the product.** The scenarios and answer keys were written by the people who built the assistant, which risks tuning to the test. External testers are planned for a later stage.
- **Scripted, not natural, input.** Follow-ups are scripted, so the session does not measure how real users phrase corrections.
- **LLM variability.** Model outputs vary between runs. One session is a sample, not a guarantee; the optional Run 2 and Run 3 give some sense of spread.
- **Small sample.** 15 attempts over 5 scenarios cannot establish accuracy across the broader target population.
