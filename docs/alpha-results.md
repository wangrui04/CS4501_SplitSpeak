# Alpha Results: Benchmark Session (B1–B5)

This is the official alpha measurement (issue #33). Three team members each run the five benchmark scenarios in [benchmarks.md](benchmarks.md) through the UI, signed in as Sarah. That gives 15 attempts, and **at least 14 must pass**.

> If a teammate is already running the benchmark by hand, that run **is** this session. Agree on one person to record it here so it isn't done twice.

---

## 1. Frozen configuration

Fill this in **before** the session starts. Make no prompt or code changes until the session is over.

| Setting | Value |
| --- | --- |
| Date and time | _YYYY-MM-DD HH:MM_ |
| Commit SHA (`git rev-parse --short HEAD`) | _abc1234_ |
| Model (`LLM_MODEL`) | _claude-sonnet-5-5_ |
| Prompt version (`PROMPT_VERSION` in `src/backend/config.py`) | _2026-11-02.2_ |
| `LLM_PROVIDER` | `claude` (never `fake` or `demo` for this session) |
| Recorder | _name_ |

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
| 1 | | B1 Basic | | | | | | | |
| 2 | | B2 Moderate | | | | | | | |
| 3 | | B3 Intermediate | | | | | | | |
| 4 | | B4 Advanced | | | | | | | |
| 5 | | B5 Most complex | | | | | | | |
| 6 | | B1 Basic | | | | | | | |
| 7 | | B2 Moderate | | | | | | | |
| 8 | | B3 Intermediate | | | | | | | |
| 9 | | B4 Advanced | | | | | | | |
| 10 | | B5 Most complex | | | | | | | |
| 11 | | B1 Basic | | | | | | | |
| 12 | | B2 Moderate | | | | | | | |
| 13 | | B3 Intermediate | | | | | | | |
| 14 | | B4 Advanced | | | | | | | |
| 15 | | B5 Most complex | | | | | | | |

The conversation ID is the `conversationId` field in each `/api/chat` response. To find it, open the browser dev tools, go to **Network**, and select the last `chat` request. With the ID, anyone can fetch the full transcript later from `GET /api/conversations/<id>`.

---

## 4. Results by scenario

Report per scenario, so one scenario failing for all three testers reads as one root cause, not three separate misses.

| Scenario | Passed (of 3) | Failure category | Root cause |
| --- | ---: | --- | --- |
| B1 Basic | | | |
| B2 Moderate | | | |
| B3 Intermediate | | | |
| B4 Advanced | | | |
| B5 Most complex | | | |
| **Total** | **_/15** | | |

Failure categories: participants, quantities, amounts, tax/tip, multiple payers, weights/nights, refund, correction, settlement, prompt limit.

---

## 5. Decision (Activity 1)

**Result:** _N_ / 15 attempts passed (_N_%). The target is ≥ 14 / 15 (≥ 90%).

**Decision:** _Validated_ / _Invalidated: pivot_

_One or two paragraphs that support the decision with the numbers above._

If the hypothesis was not validated:

- **Root cause:** _which scenarios failed and why_
- **Fix plan:** _what changes (prompt, schema, engine) and which issue tracks it_
- **Retest plan:** _which scenarios are rerun, by whom, and when; bump `PROMPT_VERSION` if the prompt changes_

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

Run the automated benchmark at the same frozen commit and attach the report:

```bash
PYTHONPATH=src python3 -m benchmark run --runs 3 --model claude-sonnet-5-5
PYTHONPATH=src python3 -m benchmark report
```

_Paste the report here, or link the `src/benchmark/results/<timestamp>.md` file._

Note: a single automated run of 5 scenarios passes 90% only at 5/5, because 4/5 is 80%. The human session above is the official result.

---

## 8. Limitations

- **Correlated testers.** Three testers paste identical scripts, so their attempts are not independent. A scenario the model gets wrong will usually fail for all three. That is why results are also reported per scenario.
- **Same team wrote the benchmark and the product.** The scenarios and answer keys were written by the people who built the assistant, which risks tuning to the test. External testers are planned for a later stage.
- **Scripted, not natural, input.** Follow-ups are scripted, so the session does not measure how real users phrase corrections.
- **LLM variability.** Model outputs vary between runs. One session is a sample, not a guarantee; the optional Run 2 and Run 3 give some sense of spread.
- **Small sample.** 15 attempts over 5 scenarios cannot establish accuracy across the broader target population.
