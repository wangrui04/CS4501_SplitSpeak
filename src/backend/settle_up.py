"""Settle up: recorded repayments and in-app balance reminders (#46).

Only the creditor (the person being paid) records a repayment. A
repayment must match the transfer currently shown for that pair, and
the form sends the outstanding amount it displayed so a stale or
repeated submit is rejected. Reminders go only to members who owe the
sender right now, at most once per hour per sender, recipient, and
group. Nothing here moves real money.
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field, StrictInt

from backend.config import REMINDER_COOLDOWN_MINUTES
from backend.repository import get_group, group_ledger, list_settlements
from backend.settlement import compute_settlement


router = APIRouter()


class RecordSettlementRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_name: str = Field(alias="from")
    to_name: str = Field(alias="to")
    cents: StrictInt
    expected_outstanding_cents: StrictInt = Field(
        alias="expectedOutstandingCents"
    )


class ReminderRequest(BaseModel):
    to: str


def now(request):
    clock = getattr(request.app.state, "clock", None)
    return clock() if clock else datetime.now(timezone.utc)


def format_dollars(cents):
    return f"${cents // 100}.{cents % 100:02d}"


def member_group_or_error(request, group_id):
    group = get_group(request.app.state.db, group_id)

    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    if request.session.get("name") not in group["members"]:
        raise HTTPException(status_code=403, detail="Not a member of this group")

    return group


def outstanding_cents(db, group, debtor, creditor):
    """The cents debtor currently owes creditor in the shown transfers."""
    settlement = compute_settlement(
        group_ledger(db, group["id"]),
        group["members"],
    )

    return sum(
        transfer["cents"]
        for transfer in settlement["transfers"]
        if transfer["from"] == debtor and transfer["to"] == creditor
    )


@router.get("/api/groups/{group_id}/settlements")
def settlements_endpoint(group_id: int, request: Request):
    member_group_or_error(request, group_id)

    return list(reversed(list_settlements(request.app.state.db, group_id)))


@router.post("/api/groups/{group_id}/settlements", status_code=201)
def record_settlement_endpoint(
    group_id: int,
    payload: RecordSettlementRequest,
    request: Request,
):
    db = request.app.state.db
    group = member_group_or_error(request, group_id)
    current_user = request.session.get("name")
    debtor, creditor = payload.from_name, payload.to_name

    if creditor != current_user:
        raise HTTPException(
            status_code=403,
            detail="Only the person being paid can record this payment",
        )

    if debtor not in group["members"] or debtor == creditor:
        raise HTTPException(
            status_code=400,
            detail="Choose a different group member who owes you",
        )

    if payload.cents <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    # Read and write inside one transaction so two submits cannot both
    # pass the outstanding-amount check.
    with db:
        owed = outstanding_cents(db, group, debtor, creditor)

        if payload.expected_outstanding_cents != owed:
            raise HTTPException(
                status_code=409,
                detail="Balance changed, please refresh",
            )

        if owed == 0:
            raise HTTPException(
                status_code=400,
                detail=f"{debtor} does not owe you anything",
            )

        if payload.cents > owed:
            raise HTTPException(
                status_code=400,
                detail=f"Amount is more than the {format_dollars(owed)} owed",
            )

        cursor = db.execute(
            """
            INSERT INTO settlements
            (group_id, from_name, to_name, cents, recorded_by, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                group_id,
                debtor,
                creditor,
                payload.cents,
                current_user,
                now(request).isoformat(),
            ),
        )

    saved = next(
        entry
        for entry in list_settlements(db, group_id)
        if entry["id"] == cursor.lastrowid
    )

    return {**saved, "remainingCents": owed - payload.cents}


@router.post("/api/groups/{group_id}/reminders", status_code=201)
def send_reminder_endpoint(
    group_id: int,
    payload: ReminderRequest,
    request: Request,
):
    db = request.app.state.db
    group = member_group_or_error(request, group_id)
    sender = request.session.get("name")
    recipient = payload.to

    owed = (
        outstanding_cents(db, group, recipient, sender)
        if recipient in group["members"] and recipient != sender
        else 0
    )

    if owed == 0:
        raise HTTPException(
            status_code=400,
            detail="You can only remind someone who owes you",
        )

    sent_at = now(request)
    cutoff = sent_at - timedelta(minutes=REMINDER_COOLDOWN_MINUTES)

    with db:
        recent = db.execute(
            """
            SELECT 1 FROM notifications
            WHERE group_id=? AND sender=? AND recipient=? AND created_at>?
            """,
            (group_id, sender, recipient, cutoff.isoformat()),
        ).fetchone()

        if recent:
            raise HTTPException(
                status_code=429,
                detail=(
                    f"You already reminded {recipient} in the last "
                    f"{REMINDER_COOLDOWN_MINUTES} minutes"
                ),
            )

        message = (
            f"Hi {recipient}, just a reminder that you still owe {sender} "
            f"{format_dollars(owed)} for {group['name']}. Thanks!"
        )

        cursor = db.execute(
            """
            INSERT INTO notifications
            (group_id, sender, recipient, cents, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (group_id, sender, recipient, owed, message, sent_at.isoformat()),
        )

    return {"id": cursor.lastrowid, "to": recipient, "cents": owed, "message": message}


def notification_json(row):
    return {
        "id": row["id"],
        "groupId": row["group_id"],
        "from": row["sender"],
        "to": row["recipient"],
        "cents": row["cents"],
        "message": row["message"],
        "createdAt": row["created_at"],
        "readAt": row["read_at"],
    }


@router.get("/api/notifications")
def notifications_endpoint(request: Request):
    rows = request.app.state.db.execute(
        """
        SELECT * FROM notifications
        WHERE recipient=?
        ORDER BY id DESC
        """,
        (request.session.get("name"),),
    ).fetchall()

    return [notification_json(row) for row in rows]


@router.post("/api/notifications/{notification_id}/read")
def mark_read_endpoint(notification_id: int, request: Request):
    db = request.app.state.db

    with db:
        updated = db.execute(
            """
            UPDATE notifications
            SET read_at=COALESCE(read_at, ?)
            WHERE id=? AND recipient=?
            """,
            (
                now(request).isoformat(),
                notification_id,
                request.session.get("name"),
            ),
        ).rowcount

    # 404 for someone else's notification, so ids reveal nothing.
    if not updated:
        raise HTTPException(status_code=404, detail="Notification not found")

    return {"ok": True}
