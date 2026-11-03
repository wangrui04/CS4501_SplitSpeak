# Alpha Submission: Checklist and Activities Draft

Due on Canvas **before class on Nov 5**: the Activities Document (PDF), the Presentation Slides (PDF), and the repo link (issue #37).

This file is a working draft. Copy each section into the Activities Document, fill in the blanks, and export to PDF.

---

## 1. Checklist

- [ ] The alpha session is done and recorded in [alpha-results.md](alpha-results.md) (#33).
- [ ] The automated benchmark report is attached as supporting evidence (#32).
- [ ] The Activities Document covers Activities 1–3 (sections 2–4 below), exported to PDF.
- [ ] The slides cover the product, methodology, results, and limitations (section 5), exported to PDF.
- [ ] The README has run instructions and links, and the repo is accessible to the instructors.
- [ ] Every issue is closed or explicitly deferred with a reason (section 6).
- [ ] Every PR links to an issue.
- [ ] A teammate walks this checklist and fresh-clones the repo to confirm the quick start works.
- [ ] Both PDFs and the repo link are submitted on Canvas.

---

## 2. Activity 1: Validation analysis

Copy the numbers and decision from [alpha-results.md](alpha-results.md) §4–5.

- **Hypothesis:** the AI expense assistant produces an accurate split, meaning every share, amount paid, and settlement transfer matches the key, within 5 user prompts in at least 90% of attempts.
- **Method:** 3 internal testers × 5 benchmark scenarios (B1–B5) = 15 attempts. Success requires at least 14 of 15. Prompts are pasted verbatim from [benchmarks.md](benchmarks.md).
- **Result:** _N_ / 15 (_N_%), broken down per scenario.
- **Decision:** _Validated_ / _Invalidated: pivot_, with root cause, fix plan, and retest plan if it failed.
- **Supporting evidence:** automated benchmark Run 1 (official) / Run 2 / Run 3 report.
- **Limitations:** see [alpha-results.md](alpha-results.md) §8.

---

## 3. Activity 2: Stories → issues coverage

| User story | Issues | Status |
| --- | --- | --- |
| US-01 Equal splitting | [#19](https://github.com/wangrui04/CS4501_Splitwise/issues/19), [#35](https://github.com/wangrui04/CS4501_Splitwise/issues/35) | _fill in_ |
| US-02 Selected members | [#20](https://github.com/wangrui04/CS4501_Splitwise/issues/20), [#35](https://github.com/wangrui04/CS4501_Splitwise/issues/35) | _fill in_ |
| US-03 Itemized splitting | [#22](https://github.com/wangrui04/CS4501_Splitwise/issues/22) | _fill in_ |
| US-04 Quantities and tax/tip | [#21](https://github.com/wangrui04/CS4501_Splitwise/issues/21), [#23](https://github.com/wangrui04/CS4501_Splitwise/issues/23) | _fill in_ |
| US-05 Missing / ambiguous info | [#24](https://github.com/wangrui04/CS4501_Splitwise/issues/24), [#30](https://github.com/wangrui04/CS4501_Splitwise/issues/30) | _fill in_ |
| US-06 Messy language and typos | [#25](https://github.com/wangrui04/CS4501_Splitwise/issues/25) | _fill in_ |
| US-07 Manual entry | [#26](https://github.com/wangrui04/CS4501_Splitwise/issues/26), [#27](https://github.com/wangrui04/CS4501_Splitwise/issues/27), [#30](https://github.com/wangrui04/CS4501_Splitwise/issues/30) | _fill in_ |
| US-08 Name-based sign-in | [#9](https://github.com/wangrui04/CS4501_Splitwise/issues/9), [#16](https://github.com/wangrui04/CS4501_Splitwise/issues/16), [#35](https://github.com/wangrui04/CS4501_Splitwise/issues/35) | _fill in_ |
| US-09 Balances and history | [#28](https://github.com/wangrui04/CS4501_Splitwise/issues/28), [#29](https://github.com/wangrui04/CS4501_Splitwise/issues/29) | _fill in_ |
| Benchmarks B1–B5 | [#28](https://github.com/wangrui04/CS4501_Splitwise/issues/28), [#31](https://github.com/wangrui04/CS4501_Splitwise/issues/31), [#32](https://github.com/wangrui04/CS4501_Splitwise/issues/32), [#33](https://github.com/wangrui04/CS4501_Splitwise/issues/33) | _fill in_ |
| Security (all stories) | [#34](https://github.com/wangrui04/CS4501_Splitwise/issues/34) | _fill in_ |
| End-to-end coverage | [#36](https://github.com/wangrui04/CS4501_Splitwise/issues/36) | _fill in_ |

---

## 4. Activity 3: TDD evidence

### What actually happened on `feature/alpha-25-37`

This sprint did **not** follow strict test-first order for most issues. State it plainly in the Activities Document:

- **The tests were AI-generated** (Claude Code), written alongside the implementation in the same sitting, usually test file first and code immediately after.
- **A failing run before implementation was confirmed for only some issues** (table below). For the rest, the tests were never run red before the code existed.
- **The tests were validated afterwards with modification (mutation) testing**, described below. That found 5 weak tests, which were then fixed.
- **The one truly test-first piece is #36.** The Playwright specs were committed on their own (`94b66e2`) before the features they cover (#27, #29, #30).

| Commit | Issue | Run red before implementation? |
| --- | --- | --- |
| `fa7fc81` | Upstream benchmark model | Partly: the test file failed to import because `WeightsMismatchError` didn't exist yet. No assertion was checked. |
| `e82120c` | #28 | Partly: only the chat-preview test was run red (`KeyError: 'paid'`). The rest of the file was written with the code. |
| `18c3494` | #26 | No |
| `b14b5a5` | #34 | No |
| `d0827a0` | #35 | Yes: the 2 contradictory "Kayla and I" tests failed. The other 10 already passed, so they did not drive any code. |
| `d88d6b2`, `e766b64` | #31, #32 | No. The code came first, and the report snapshot was generated from the code's own output. |
| `95f4762` | #25 | No |
| `94b66e2` | #36 | Committed first, but not run locally (no disk space for the browser). The first CI run on this commit is expected to fail. |
| `ed67f52` | #27, #30 | #30: yes, 5 of 6 escape-hatch tests failed first. #27: no. |
| `2ba43f9` | #29 | No |

**Failing CI runs:** _link the first GitHub Actions run for `94b66e2` once the branch is pushed._

### Validating the tests: modification testing

To check that the tests actually guard the critical code, 49 deliberate breaks ("mutants") were made one at a time: 39 in the backend and benchmark, 10 in the frontend. The full suite was run after each one, and the file was restored afterwards. A break is **caught** if at least one test fails. If every test still passes, the tests are weak there.

The script and the full list of breaks are in [`scripts/mutation_test.py`](../scripts/mutation_test.py). Run `.venv/bin/python scripts/mutation_test.py "$PWD"` from the repo root to repeat it.

Areas covered: dollars-to-cents conversion, leftover-cent rounding, "everyone except", resolving "I"/"me", weights, refunds, pooled tax/tip, the validator's sum and name checks, settlement order, tie-breaks, and direction, questions never becoming guessed previews, draft and double-confirm guards, manual-entry rules, rate limiting, input sanitizing, delimiting user text as data, the benchmark comparator, runner, and report, and the frontend money parser, form validation, balances, and escape hatch.

**First pass: 44 of 49 caught. These 5 got through:**

| Break | Why no test failed | Fix |
| --- | --- | --- |
| Confirm allowed for a draft not in "preview" status | The test only used drafts with no saved preview, so another check rejected them first. A real stale preview (preview, then a correction that triggers a question) was never tested. | New test `test_stale_preview_cannot_be_confirmed_after_followup_question` |
| No group refetch after saving | The App test checked a fetch that already happens on page load. | US-01 App test now requires a second fetch and the updated balance on screen |
| Validator accepts an unknown payer | Only unknown participants were tested. | New test `test_unknown_payer` |
| Refund larger than the item allowed | The test accepted any `ValueError`, and a later check raised one anyway. | Test now requires the "Refund is larger" error |
| Manual entry accepts $0 | Any 400 passed, including one from the validator's check. | New test `test_zero_amount_rejected_with_clear_message` |

**After the fixes: 49 of 49 caught.** The most valuable find was the first one: without that check, a stale preview could have been saved after the user had started correcting it.

### Other ways the AI-generated tests were reviewed and corrected

1. **Mocked tests hid a broken live path.** The Claude client tests mocked the SDK and checked for a forced `tool_choice`, so they passed while every real request to Sonnet 5.5 would fail (the model rejects forced tool use and `temperature`). The tests were rewritten to assert that those parameters are *not* sent, and the client moved to structured outputs (`24f6281`).
2. **A property test found a real bug.** The Hypothesis test for settlement produced an expense with an empty payments list, and `payments_of()` wrongly treated it as missing. The code was fixed, not the test.
3. **A wrong expectation in a generated test.** A comparator test expected both a share and a settlement mismatch, but its hand-built preview kept the original transfers, so only the share differed. The expectation was corrected.
4. **A test that encoded the wrong behavior.** The old manual-entry test asserted a payload built with `parseFloat` × 100, and that nothing was saved through the API. It was replaced with tests for the real endpoint and string-based cents conversion.
5. **An answer-key check against itself.** The benchmark keys are typed by hand from `Benchmarks.docx` rather than computed, so `test_answer_key_sanity` can catch typos: shares must equal amounts paid, and the settlement function must reproduce the key's transfers.

### Lessons for the next sprint

- Write the tests yourselves (or review AI-written tests) and run them red **before** implementing, then commit them separately so the order shows in git history.
- Run modification tests on new tests before relying on them.

---

## 5. Slides outline

1. **Problem:** splitting complicated shared bills is tedious and error-prone.
2. **Product:** Splitwise core plus a conversational assistant that asks before guessing and shows an itemized preview you must confirm.
3. **Architecture:** the LLM only extracts structured JSON; deterministic, unit-tested code does all arithmetic; validation and confirmation gate every save.
4. **Hypothesis and method:** ≥ 90% accurate within 5 prompts; 3 testers × 5 benchmark scenarios.
5. **Results:** per-scenario table, total _N_/15, and the decision.
6. **Supporting evidence:** automated Run 1/2/3 report and test counts.
7. **Limitations:** 3 internal testers, scripted scenarios, LLM variability, and the same team wrote the benchmark and the product.
8. **Next steps:** fixes from failures, external testers, settle up, corrections UI.

---

## 6. Issue status

| Issue | Status | Reason if deferred |
| --- | --- | --- |
| #2, #3 | _open_ | _documentation and professor confirmation; owned by the team_ |
| #4–#24 | _close if done, or defer with a reason_ | |
| #25–#30, #34, #35 | Done on `feature/alpha-25-37` | |
| #31 Benchmark runner | Done | Built and tested; verified offline with scripted fixtures. Live automated runs were blocked by the Groq free-tier rate limit (HTTP 429). |
| #32 Benchmark report | Done | Built and tested (snapshot test). Not generated from a live run, because live runs were blocked by the free-tier rate limit. |
| #36 Playwright E2E | Pending first CI run | Specs and CI job written; they run once the branch is pushed. |
| #33 | Session done (14 / 15), decision pending team review | |
| #37 | Pending: needs PDFs and Canvas submission | |
| #38 Corrections after a preview | _decide_ | Backend handles corrections (B5); no dedicated UI |
| #39 Itemized manual entry | Deferred | Optional; equal-split manual entry covers US-07 |
| #40 Settle up placeholder | Deferred | Optional; settlement is shown, but recording payments is out of alpha scope |
