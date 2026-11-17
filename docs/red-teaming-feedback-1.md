# Alpha Test Feedback & Bug Analysis Report

This document compiles the critical issues identified during alpha testing of **SplitSpeak**, along with root-cause analysis, corresponding repository issues, and recommended improvements for test suites and validation logic.

---

## Executive Summary

Recent alpha test sessions highlighted three critical reliability bottlenecks in SplitSpeak's natural language processing and state management pipeline:

1. **Payer extraction failures** and silent `null` crashes on simple inputs.
2. **Inconsistent multi-clause parsing** leading to flaky behavior on complex prompts.
3. **Conversational amnesia / looping** where the model repeatedly asks for information already provided.

---

## Critical Issues & Analysis

### Critical Issue 1: Inadequate Natural Language Processing & Silent Crashes

* **Problem:** The app frequently fails to identify the buyer even in straightforward statements (e.g., *"Kayla bought $10 worth of pizza"*), resulting in a silent crash or returning `null` with uncaught errors.
* **Example Session:**
> **User:** I shared a pizza with Rui that she paid for. Sarah paid for another pizza and Rui had one slice.
> **App:** What was the price of the first pizza shared by you and Rui?
> **User:** $10
> **App:** What was the price of the second pizza that Sarah paid for?
> **User:** $15
> **App:** Who paid for this expense?
> **User:** Which expense?
> **App:** *[Ambiguity on multi-payer itemization breakdown and global vs. per-item payer mapping]*



---

### Critical Issue 2: Inconsistent Handling of Complex Requests

* **Problem:** Multi-clause prompts yield volatile results. For instance, given the prompt:
> *"Sarah bought a $10 pizza and I ate ⅔ of it. Rui bought a $20 pizza and shared it evenly."*


The model occasionally hallucinates that Rui bought everything and splits payments uniformly, yet passes successfully upon retesting minutes later. This points to underlying flakiness in complex constraint satisfaction.
* **Corresponding Repository Issue:** Closed [Issue #25 (Deliver US-06 messy language and typo handling)](https://github.com/wangrui04/CS4501_SplitSpeak/issues?q=is%3Aissue+state%3Aclosed).
* **Recommendation:** Tighten acceptance criteria for US-06 and expand test suites to include robust 2–3 sentence multi-item scenarios evaluated across repeated iterations.

---

### Critical Issue 3: Poor Conversational Memory & Redundant Prompts

* **Problem:** The model suffers from short-term context degradation, repeatedly looping back to ask questions it has already resolved (such as *"Who paid for this expense?"*).
* **Example Session:**
> **User:** Rui lent me $20 at 5% interest each day and it's been 2 days
> **App:** Who paid for this expense?
> **User:** Rui
> **App:** What is the interest amount (or total fee) for the loan?
> **User:** 5
> **App:** What method should be used to split the interest fee (equal or proportional)?
> **User:** She loaned it to me. I have to pay the interest fee.
> **App:** Who paid for this expense?
> **User:** Rui
> **App:** Who paid for this expense? *(Loop)*


* **Corresponding Repository Issue:** [`#49: Verify payer, tax, tip, and amounts against the user's text before previewing`](https://github.com/wangrui04/CS4501_SplitSpeak/issues/43) (Closed by `kayla-hekim`).

---

## Recommendations & Action Items

* [ ] **Implement Deterministic Grounding Checks:** Enforce backend validation rules that check parsed fields against the raw user text rather than relying solely on LLM conversational memory.
* [ ] **Expand Automated Test Coverage:** Broaden test scopes beyond single-turn inputs to simulate multi-turn, multi-item conversations.
* [ ] **State Locking:** Prevent downstream turns from overwriting successfully validated fields (like `payer`) with `null` values.