# API Reference

All amounts are **integer cents**. Every `/api/*` route except the session routes needs a signed session cookie, which you get from `POST /api/session`. Group routes also require the signed-in user to be a member (otherwise `403`).

---

## Sessions

| Method | Path | Body | Notes |
| --- | --- | --- | --- |
| `GET` | `/api/session/names` | | Names available on the picker |
| `POST` | `/api/session` | `{ "name": "Sarah" }` | Sign in; `400` for unknown names |
| `GET` | `/api/session` | | Current user, or `401` |
| `DELETE` | `/api/session` | | Sign out |

---

## Groups and balances

### `GET /api/groups/:id`

Returns the group plus settlement relative to the signed-in user.

```json
{
  "id": 1,
  "name": "Apartment 4B",
  "members": ["Sarah", "Kayla", "Rui"],
  "nets": [{ "name": "Sarah", "netCents": 39500 }],
  "transfers": [{ "from": "Rui", "to": "Sarah", "cents": 28000 }],
  "balances": [{ "name": "Rui", "cents": 28000, "status": "owes you" }],
  "summary": { "totalBalance": 39500, "youOwe": 0, "youAreOwed": 39500 }
}
```

- `net = total paid − total cost share`. A refund received counts as negative paid.
- Transfers are greedy: the largest debtor pays the largest creditor, with ties broken by roster order. This produces at most n − 1 transfers.
- `balances[].cents` is positive when that member owes you and negative when you owe them. `status` is `owes you`, `you owe`, or `settled up`. Someone who settles with a third person shows as `settled up` relative to you.
- `summary.totalBalance` is your net; `youOwe` and `youAreOwed` sum your transfers.
- Recorded repayments (see [Settle up](#settle-up)) count toward nets and transfers. Expenses are never changed.

### `GET /api/groups/:id/expenses`

Confirmed expenses, newest first. Each expense has `description`, `payer`, `totalCents`, `source` (`ai` or `manual`), `createdBy`, `created_at` (UTC), `shares[]`, and `payments[]` (`{ name, cents }`).

### `GET /api/groups/:id/balances`

Legacy map of each member's net, including recorded repayments, e.g. `{ "Sarah": 2000, "Kayla": -1000 }`.

---

## Settle up

Records repayments and sends in-app reminders. No money moves: SplitSpeak only records that a payment happened.

### `POST /api/groups/:id/settlements`

Records that `from` repaid `to`. Only the person being paid (`to`) can record it.

```json
{ "from": "Kayla", "to": "Sarah", "cents": 1000, "expectedOutstandingCents": 3000 }
```

`expectedOutstandingCents` is the amount the form showed. Returns `201` with the saved entry (`id`, `from`, `to`, `cents`, `recordedBy`, `recordedAt`) and `remainingCents`.

| Problem | Response |
| --- | --- |
| Not signed in | `401` |
| Not a member, or not the person being paid | `403` |
| Unknown member, same person, nothing owed, `cents` not positive, or more than is owed | `400` |
| `cents` or `expectedOutstandingCents` not an integer | `422` |
| `expectedOutstandingCents` differs from the live amount (stale form or repeated submit) | `409` |

The amount owed is the current transfer from `from` to `to` in `GET /api/groups/:id`. With simplified debts, that can differ from who paid the original expense.

### `GET /api/groups/:id/settlements`

Recorded repayments, newest first.

### `POST /api/groups/:id/reminders`

`{ "to": "Kayla" }` sends Kayla an in-app reminder of what she currently owes the signed-in user, for example: "Hi Kayla, just a reminder that you still owe Sarah $12.00 for Apartment 4B. Thanks!" Returns `201`. Returns `400` unless `to` currently owes you, and `429` if you reminded that person in this group within the last 60 minutes (`REMINDER_COOLDOWN_MINUTES`). Reminders never change balances, and nothing is sent by email or SMS.

### `GET /api/notifications`

The signed-in user's reminders, newest first: `id`, `groupId`, `from`, `to`, `cents` (amount when sent), `message`, `createdAt`, and `readAt` (`null` until read).

### `POST /api/notifications/:id/read`

Marks one of your reminders as read. Returns `404` for anyone else's.

---

## Manual entry

### `POST /api/groups/:id/expenses/manual`

```json
{ "description": "Dinner", "amount": "30.00", "paidBy": "Sarah", "splitBetween": ["Sarah", "Kayla", "Rui"] }
```

The server builds an equal split with the same engine, rounding rule, and validator as the AI path, and saves it with `source = "manual"`. The amount can be a string or a number. It must be greater than 0 with at most 2 decimals. Errors return `400` with a `detail` message.

---

## AI chat

### `POST /api/chat`

```json
{ "groupId": 1, "conversationId": null, "message": "I paid $30 for dinner, split evenly" }
```

Response `type` is one of:

- `question`: `{ question }`. The assistant needs more information.
- `preview`: `{ preview }` with `lineItems`, `charges`, `totalCents`, `shares[]`, `paid[]`, and `settlement { nets, transfers }`. Settlement is computed by the same function as group balances.
- `unresolved`: `{ reason, fallback: "manual" }`. The UI offers manual entry.
- `error`: `{ message }`.

All responses include `conversationId`, `promptCount`, and `status`. Limits:

| Limit | Response |
| --- | --- |
| More than 5 prompts in a conversation | `unresolved` |
| More than 20 messages per minute per user | `429` |
| Message longer than 1000 characters (after control characters are stripped) | `400` |
| Message to a confirmed or unsuccessful conversation | `409` |

`POST /api/groups/:id/chat` is an alias.

### `POST /api/conversations/:id/confirm`

Saves the stored, validated preview. Balances change only here. Any shares or totals the client sends are ignored. Aliases: `/api/chat/:id/confirm`, `/api/drafts/:id/confirm`, and `POST /api/expenses/confirm` with `{ conversationId }`.

### `GET /api/conversations/:id`

Returns the conversation's transcript, status, and final preview.
