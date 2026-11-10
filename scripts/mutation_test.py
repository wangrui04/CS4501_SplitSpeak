"""Modification (mutation) testing: break one thing, run tests, restore.

Usage, from the repo root with a clean working tree:
    .venv/bin/python scripts/mutation_test.py "$PWD"        # all mutants
    .venv/bin/python scripts/mutation_test.py "$PWD" M24    # one mutant

A mutant is KILLED (good) if at least one test fails.
A mutant SURVIVES (bad test coverage) if every test still passes.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
ONLY = sys.argv[2] if len(sys.argv) > 2 else None
PY = [str(ROOT / ".venv/bin/python"), "-m", "pytest", "-q", "-p", "no:cacheprovider", "-x", "--no-header"]
FE = ["npx", "vitest", "run"]

B = "src/backend/"
F = "src/frontend/src/"

# (id, file, original snippet, mutated snippet, what it breaks)
MUTANTS = [
    # --- money and allocation engine ---
    ("M01", B + "allocation.py", 'Decimal(value.removeprefix("$")) * 100', 'Decimal(value.removeprefix("$")) * 10', "dollars->cents conversion off by 10x"),
    ("M02", B + "allocation.py", "        base[payer] += leftover", "        base[sharers[-1]] += leftover", "leftover cent goes to last sharer instead of payer"),
    ("M03", B + "allocation.py", "    leftover = amount_cents - sum(base.values())", "    leftover = 0", "leftover cents dropped (shares no longer sum)"),
    ("M04", B + "allocation.py", "            if name not in resolved\n", "            if name in resolved\n", "'everyone except X' becomes 'only X'"),
    ("M05", B + "allocation.py", '        current_user if name == "ME" else name\n        for name in names', '        name\n        for name in names', "'I/me' not resolved to signed-in user"),
    ("M06", B + "allocation.py", "            paid[recipient] -= refund_cents", "            paid[recipient] += refund_cents", "refund counted as extra paid instead of negative"),
    ("M07", B + "allocation.py", "    if not item.get(\"weights\"):\n        return [1] * len(sharers)", "    if True:\n        return [1] * len(sharers)", "weights (nights, 'twice as much') ignored"),
    ("M08", B + "allocation.py", "        cents = gross - refund_cents", "        cents = gross", "refund not subtracted from item cost"),
    ("M09", B + "allocation.py", '        if pool["method"] == "proportional":', '        if pool["method"] == "never":', "proportional tax/tip split equally"),
    ("M10", B + "allocation.py", '        paid[payer] = paid.get(payer, 0) + pool["amountCents"]', "        pass", "tax/tip not counted as paid by payer"),
    ("M11", B + "allocation.py", "        pool = pools.setdefault(\n            charge[\"method\"],", "        pool = pools.setdefault(\n            id(charge),", "tax and tip no longer pooled (B3 rounding)"),
    ("M12", B + "allocation.py", "            if refund_cents > gross:", "            if False:", "refund larger than item allowed"),
    # --- validator ---
    ("M13", B + "validator.py", "        and sum(shares.values()) != total\n", "        and False\n", "shares-sum-to-total check disabled"),
    ("M14", B + "validator.py", "        elif sum(paid.values()) != total:", "        elif False:", "paid-sum-to-total check disabled"),
    ("M15", B + "validator.py", "    elif payer not in roster:", "    elif False:", "unknown payer accepted"),
    ("M16", B + "validator.py", "    if isinstance(total, (int, float)) and total <= 0:", "    if isinstance(total, (int, float)) and total < 0:", "zero total accepted"),
    # --- settlement ---
    ("M17", B + "settlement.py", "key=lambda name: (-nets[name] * sign, order[name])", "key=lambda name: (nets[name] * sign, order[name])", "greedy picks smallest debtor/creditor"),
    ("M18", B + "settlement.py", "key=lambda name: (-nets[name] * sign, order[name])", "key=lambda name: (-nets[name] * sign, -order[name])", "tie-break by reverse roster order"),
    ("M19", B + "settlement.py", "    if sum(nets.values()) != 0:", "    if False:", "unbalanced input not rejected"),
    ("M20", B + "settlement.py", '            status = "owes you"\n        elif cents < 0:\n            status = "you owe"', '            status = "you owe"\n        elif cents < 0:\n            status = "owes you"', "balance direction swapped"),
    ("M21", B + "settlement.py", '            nets[share["name"]] = nets.get(share["name"], 0) - share["cents"]', '            nets[share["name"]] = nets.get(share["name"], 0) + share["cents"]', "shares added instead of subtracted"),
    # --- pipeline / save guardrails ---
    ("M22", B + "pipeline.py", '    if data["openQuestions"]:', "    if False:", "AI questions ignored (would preview guessed data)"),
    ("M23", B + "pipeline.py", '        if "ME" in names and current_user in names:', "        if False:", "'Kayla and I' as Kayla silently accepted"),
    ("M24", B + "repository.py", '    if conv["status"] != "preview":', "    if False:", "unconfirmed/pending draft can be confirmed"),
    ("M25", B + "repository.py", '    if sum(payment["cents"] for payment in payments) != total:', "    if False:", "save_expense accepts unbalanced payments"),
    ("M26", B + "repository.py", '    if conv["status"] == "confirmed":', "    if False:", "same expense can be confirmed twice"),
    ("M27", B + "manual.py", "    if cents <= 0:", "    if cents < 0:", "manual entry accepts $0"),
    ("M28", B + "manual.py", "    if not request.splitBetween:", "    if False:", "manual entry accepts empty split"),
    # --- security ---
    ("M29", B + "security.py", "        if len(hits) >= self.limit:", "        if len(hits) > self.limit:", "rate limit allows 21st message"),
    ("M30", B + "security.py", '    return _CONTROL_CHARS.sub("", text).strip()', "    return text.strip()", "control characters not stripped"),
    ("M31", B + "llm.py", '                "<user_message>\\n"\n                + content.replace("</user_message>", "")\n                + "\\n</user_message>"', "                content", "user text no longer delimited as data"),
    ("M32", B + "main.py", "        if len(message_text) > MAX_MESSAGE_LENGTH:", "        if False:", "overlong messages accepted"),
    ("M33", B + "main.py", "        if not chat_limiter.allow(current_user):", "        if False:", "rate limiter bypassed"),
    ("M34", B + "llm.py", "                    betas=[LLM_FALLBACK_BETA],", "                    betas=[LLM_FALLBACK_BETA],\n                    temperature=0,", "re-adds temperature (400 on Sonnet 5.5)"),
    # --- benchmark ---
    ("M35", "src/benchmark/comparator.py", "    if want != got:\n        mismatches.append(Mismatch(\n            field=\"settlement\",", "    if False:\n        mismatches.append(Mismatch(\n            field=\"settlement\",", "settlement mismatches not detected"),
    ("M36", "src/benchmark/comparator.py", "    if prompt_count > max_prompts:", "    if prompt_count > max_prompts + 1:", "6 prompts counted as passing"),
    ("M37", "src/benchmark/runner.py", '        if turn.send == "always" or last_type == "question":', "        if True:", "if_asked turns sent even after a preview"),
    ("M38", "src/benchmark/report.py", "        ok = total and passed / total >= THRESHOLD", "        ok = total and passed / total >= 0.75", "80% run reported as PASS"),
    ("M39", "src/benchmark/report.py", '        flaky = " ⚠" if len(outcomes) > 1 else ""', '        flaky = ""', "flaky scenarios not marked"),
    # --- Gemini provider ---
    ("G01", B + "llm.py", '"role": "model" if m["role"] == "assistant" else "user",', '"role": "user",', "assistant turns sent as user turns"),
    ("G02", B + "llm.py", '                        "response_json_schema": PARSED_EXPENSE_SCHEMA,\n', "", "Gemini schema not enforced"),
    ("G03", B + "llm.py", '                if name == "ServerError" or "Timeout" in name or "Connect" in name:', "                if False:", "Gemini 5xx not retried"),
    ("G04", B + "llm.py", '                request_messages = delimit_user_messages(messages)\n\n                if attempt and last_error is not None:\n                    request_messages.append({\n                        "role": "user",\n                        "content": (\n                            "Previous response invalid: "\n                            f"{last_error}. "\n                            "Return corrected JSON."\n                        ),\n                    })\n\n                response = self.sdk.models', '                request_messages = [dict(m) for m in messages]\n\n                response = self.sdk.models', "Gemini user text not delimited and no retry hint"),
    ("G05", B + "security.py", 'SECRET_ENV_VARS = ("ANTHROPIC_API_KEY", "GEMINI_API_KEY", "SESSION_SECRET")', 'SECRET_ENV_VARS = ("ANTHROPIC_API_KEY", "SESSION_SECRET")', "Gemini key not redacted from logs"),
    ("G06", B + "main.py", '            api_key=env.get("GEMINI_API_KEY"),', '            api_key=env.get("GEMINI_API_KEY") or "missing",', "Gemini starts without a key"),
    # --- Groq provider ---
    ("Q01", B + "llm.py", '                                "schema": PARSED_EXPENSE_SCHEMA,\n', "", "Groq schema not sent"),
    ("Q02", B + "llm.py", '                            {"role": "system", "content": system_prompt},\n', "", "Groq system prompt not sent"),
    ("Q03", B + "llm.py", "                if status >= 500:", "                if status >= 600:", "Groq 5xx not retried"),
    ("Q04", B + "llm.py", '                if str(exc) == "LLM_REQUEST_FAILED":\n                    raise\n', "", "Groq 429 retried instead of stopping"),
    ("Q05", B + "llm.py", '        self._headers = {"Authorization": f"Bearer {api_key}"}', '        self._headers = {}', "Groq key not sent"),
    ("Q06", B + "security.py", '    "GROQ_API_KEY",\n', "", "Groq key not redacted from logs"),
    # --- multi-payer trip: inferred main payer ---
    ("T01", B + "pipeline.py", '    if not items or data["charges"]:', "    if not items:", "tax/tip allowed without a known payer"),
    ("T02", B + "pipeline.py", '    if any(not item.get("paidBy") or item["unitPrice"] is None for item in items):', '    if any(item["unitPrice"] is None for item in items):', "payer inferred when an item has no payer"),
    ("T03", B + "pipeline.py", "key=lambda name: (-totals[name], order.get(name, len(order)))", "key=lambda name: (totals[name], order.get(name, len(order)))", "main payer is whoever paid the least"),
    ("T04", B + "pipeline.py", '            name = current_user if item["paidBy"] == "ME" else item["paidBy"]', '            name = item["paidBy"]', "ME not resolved when inferring payer"),
    # --- frontend ---
    ("F01", F + "money.js", "  return Number(whole) * 100 + Number(fraction);", "  return Number(whole) * 10 + Number(fraction);", "frontend dollars->cents off"),
    ("F02", F + "money.js", "const AMOUNT_PATTERN = /^(\\d+)(?:\\.(\\d{0,2}))?$|^\\.(\\d{1,2})$/;", "const AMOUNT_PATTERN = /^(\\d+)(?:\\.(\\d{0,3}))?$|^\\.(\\d{1,3})$/;", "3 decimals accepted"),
    ("F03", F + "components/ManualEntryForm.jsx", "  const splitProblem = splitBetween.length === 0 ? 'Choose at least one person to split with.' : null;", "  const splitProblem = null;", "Save allowed with nobody checked"),
    ("F04", F + "components/ManualEntryForm.jsx", "  if (parseDollarsToCents(text) <= 0) return 'Amount must be greater than $0.';", "", "Save allowed for $0"),
    ("F05", F + "components/GroupView.jsx", "  const net = paid - share;", "  const net = share - paid;", "'you lent' / 'you owe' swapped"),
    ("F06", F + "components/RightSidebar.jsx", "  'owes you': 'positive',\n  'you owe': 'negative',", "  'owes you': 'negative',\n  'you owe': 'positive',", "balance colors swapped"),
    ("F07", F + "components/AddExpenseModal.jsx", "  const firstUserMessage = messages.find((msg) => msg.role === 'user')?.content || '';", "  const firstUserMessage = [...messages].reverse().find((msg) => msg.role === 'user')?.content || '';", "prefill uses last message, not first"),
    ("F08", F + "components/AddExpenseModal.jsx", "  const isStuck = lastAssistant && ['unresolved', 'error'].includes(lastAssistant.type);", "  const isStuck = false;", "no switch-to-manual banner"),
    ("F09", F + "components/ItemizedPreview.jsx", "      {transfers.length > 0 && (", "      {false && (", "'who pays whom' hidden in preview"),
    ("F10", F + "App.jsx", "              onExpenseConfirmed={() => setRefreshKey((key) => key + 1)}", "              onExpenseConfirmed={() => {}}", "no refetch after saving"),
]


def run(cmd, cwd):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300)
    out = proc.stdout + proc.stderr
    failed = [line for line in out.splitlines() if line.startswith("FAILED") or " FAIL " in line or line.strip().startswith("×")]
    return proc.returncode, failed


results = []
for mid, rel, old, new, desc in MUTANTS:
    if ONLY and not mid.startswith(ONLY):
        continue
    path = ROOT / rel
    original = path.read_text()
    count = original.count(old)
    if count != 1:
        results.append({"id": mid, "file": rel, "desc": desc, "status": f"SKIPPED (pattern found {count}x)"})
        print(mid, "SKIPPED", count, flush=True)
        continue
    try:
        path.write_text(original.replace(old, new, 1))
        if rel.startswith("src/frontend"):
            code, failed = run(FE, ROOT / "src/frontend")
        else:
            code, failed = run(PY, ROOT)
    finally:
        path.write_text(original)
    status = "KILLED" if code != 0 else "SURVIVED"
    results.append({"id": mid, "file": rel, "desc": desc, "status": status, "caught_by": failed[:2]})
    print(mid, status, failed[:1], flush=True)

Path(sys.argv[0]).with_name("mutation_results.json").write_text(json.dumps(results, indent=2))
