"""Compare a final preview against a scenario's answer key."""

from __future__ import annotations

from backend.config import MAX_PROMPTS_PER_CONVERSATION
from benchmark.schema import Expected, Mismatch, Scenario


def _by_name(entries: list[dict]) -> dict[str, int]:
    return {entry["name"]: entry["cents"] for entry in entries}


def _transfer_key(transfer: dict) -> tuple[str, str, int]:
    return (transfer["from"], transfer["to"], transfer["cents"])


def _format_transfer(key) -> str:
    return f"{key[0]}->{key[1]} {key[2]}"


def compare(
    expected: Expected,
    preview: dict,
    prompt_count: int,
    max_prompts: int = MAX_PROMPTS_PER_CONVERSATION,
) -> list[Mismatch]:
    """Every share, amount paid, and transfer must match to the cent."""
    mismatches = []

    for field, actual_entries, expected_map in (
        ("shares", preview.get("shares", []), expected.shares),
        ("paid", preview.get("paid", []), expected.paid),
    ):
        actual = _by_name(actual_entries)
        for name in sorted(set(expected_map) | set(actual)):
            want = expected_map.get(name, 0)
            got = actual.get(name, 0)
            if want != got:
                mismatches.append(Mismatch(
                    field=f"{field}.{name}", expected=want, actual=got,
                ))

    want = sorted(t.key() for t in expected.settlement)
    got = sorted(
        _transfer_key(t)
        for t in preview.get("settlement", {}).get("transfers", [])
    )
    if want != got:
        mismatches.append(Mismatch(
            field="settlement",
            expected="; ".join(_format_transfer(k) for k in want),
            actual="; ".join(_format_transfer(k) for k in got),
        ))

    if prompt_count > max_prompts:
        mismatches.append(Mismatch(
            field="promptCount", expected=max_prompts, actual=prompt_count,
        ))

    return mismatches


def describe(mismatches: list[Mismatch]) -> str:
    """Short reason, e.g. "Kayla's share off by $0.01"."""
    parts = []
    for mismatch in mismatches:
        if mismatch.field == "promptCount":
            parts.append(f"used {mismatch.actual} prompts (max {mismatch.expected})")
        elif mismatch.field == "settlement":
            parts.append(f"settlement {mismatch.actual or 'none'} (expected {mismatch.expected})")
        else:
            kind, name = mismatch.field.split(".", 1)
            label = "share" if kind == "shares" else "amount paid"
            diff = abs(mismatch.actual - mismatch.expected)
            parts.append(f"{name}'s {label} off by ${diff // 100}.{diff % 100:02d}")
    return ", ".join(parts)


def categorize(scenario: Scenario, reason: str | None, mismatches: list[Mismatch]) -> str:
    """Map a failure to one category from schema.FAILURE_CATEGORIES."""
    primary = scenario.categories[0]
    fields = {m.field.split(".", 1)[0] for m in mismatches}

    if "promptCount" in fields or (reason or "").startswith("prompt limit"):
        return "prompt limit"
    if fields == {"settlement"}:
        return "settlement"
    if "paid" in fields:
        return "refund" if "refund" in scenario.categories else "multiple payers"
    if not mismatches and "correction" in scenario.categories:
        # No final preview after a scripted correction.
        return "correction"
    return primary
