
import { useEffect, useState } from 'react';
import { fetchExpenseDetails, updateExpense } from '../api';
import { formatCents, parseDollarsToCents } from '../money';
import './ExpenseDetailsModal.css';

const dollars = (cents = 0) => (cents / 100).toFixed(2);

function totalOf(entries) {
  return entries.reduce((sum, entry) => sum + entry.cents, 0);
}

function itemTotal(item) {
  return item.totalCents ?? (
    (item.unitPriceCents || 0) * (item.quantity || 1)
    - (item.refundCents || 0)
  );
}

function splitAmount(total, names) {
  if (!names.length) return {};

  const base = Math.floor(total / names.length);
  const remainder = total - base * names.length;

  return Object.fromEntries(
    names.map((name, index) => [
      name,
      base + (index === 0 ? remainder : 0),
    ])
  );
}

function distribute(total, entries, members) {
  const active = entries.filter((entry) => entry.cents > 0);
  const names = active.length
    ? active.map((entry) => entry.name)
    : members;

  if (!names.length) return [];

  const weight = active.reduce((sum, entry) => sum + entry.cents, 0);
  let remaining = total;

  return names.map((name, index) => {
    const cents = index === names.length - 1
      ? remaining
      : weight > 0
        ? Math.floor(total * active[index].cents / weight)
        : Math.floor(total / names.length);

    remaining -= cents;
    return { name, cents };
  });
}

function calculateTransfers(shares, payments, members) {
  const nets = Object.fromEntries(
    members.map((name) => [name, 0])
  );

  payments.forEach(({ name, cents }) => {
    nets[name] = (nets[name] || 0) + cents;
  });

  shares.forEach(({ name, cents }) => {
    nets[name] = (nets[name] || 0) - cents;
  });

  const order = Object.fromEntries(
    members.map((name, index) => [name, index])
  );

  const sortNets = (a, b) =>
    b.cents - a.cents || order[a.name] - order[b.name];

  const debtors = members
    .filter((name) => nets[name] < 0)
    .map((name) => ({ name, cents: -nets[name] }))
    .sort(sortNets);

  const creditors = members
    .filter((name) => nets[name] > 0)
    .map((name) => ({ name, cents: nets[name] }))
    .sort(sortNets);

  const transfers = [];
  let i = 0;
  let j = 0;

  while (i < debtors.length && j < creditors.length) {
    const cents = Math.min(debtors[i].cents, creditors[j].cents);

    if (cents > 0) {
      transfers.push({
        from: debtors[i].name,
        to: creditors[j].name,
        cents,
      });
    }

    debtors[i].cents -= cents;
    creditors[j].cents -= cents;

    if (debtors[i].cents === 0) i++;
    if (creditors[j].cents === 0) j++;
  }

  return transfers;
}

function initialize(expense) {
  return {
    description: expense.description,
    payer: expense.payer,
    totalCents: expense.totalCents,
    shares: (expense.shares || []).map((s) => ({ ...s })),
    payments: (expense.payments || []).map((p) => ({ ...p })),
    lineItems: (expense.lineItems || []).map((item) => ({
      ...item,
      shares: item.shares ? { ...item.shares } : undefined,
    })),
    charges: (expense.charges || []).map((charge) => ({ ...charge })),
    version: expense.version || 1,
  };
}

function getParticipants(item, fallbackShares) {
  if (item.shares && Object.keys(item.shares).length) {
    return Object.keys(item.shares).filter(
      (name) => item.shares[name] > 0
    );
  }

  if (Array.isArray(item.participants)) {
    return item.participants;
  }

  return fallbackShares
    .filter((share) => share.cents > 0)
    .map((share) => share.name);
}

// Holds the unfinished text separately from the saved cents.
// This fixes the backspace/reset-to-0.00 issue.
function MoneyInput({
  cents,
  onCommit,
  label,
  allowNegative = false,
}) {
  const [text, setText] = useState(dollars(cents));

  useEffect(() => {
    setText(dollars(cents));
  }, [cents]);

  function commit() {
    const trimmed = text.trim();
    const negative = allowNegative && trimmed.startsWith('-');
    const amount = negative ? trimmed.slice(1) : trimmed;
    const parsed = parseDollarsToCents(amount);

    if (parsed === null || (!allowNegative && parsed < 0)) {
      setText(dollars(cents));
      return;
    }

    const next = negative ? -parsed : parsed;
    onCommit(next);
    setText(dollars(next));
  }

  return (
    <input
      className="field"
      type="text"
      inputMode="decimal"
      aria-label={label}
      value={text}
      onChange={(event) => setText(event.target.value)}
      onBlur={commit}
      onKeyDown={(event) => {
        if (event.key === 'Enter') event.currentTarget.blur();
      }}
    />
  );
}

function Avatar({ name }) {
  return (
    <span className="detail-avatar">
      {name?.charAt(0)?.toUpperCase() || '?'}
    </span>
  );
}

export default function ExpenseDetailsModal({
  group,
  expenseId,
  onClose,
  onSaved,
}) {
  const [expense, setExpense] = useState(null);
  const [draft, setDraft] = useState(null);
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');

  const members = group?.members || [];

  useEffect(() => {
    let active = true;

    fetchExpenseDetails(group.id, expenseId)
      .then((data) => {
        if (!active) return;
        setExpense(data);
        setDraft(initialize(data));
        setBusy(false);
      })
      .catch((err) => {
        if (active) {
          setError(err.message);
          setBusy(false);
        }
      });

    return () => { active = false; };
  }, [group.id, expenseId]);

  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape' && !busy) onClose();
    };

    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [busy, onClose]);

  function updateDraft(changes) {
    setDraft((previous) => ({ ...previous, ...changes }));
    setError('');
  }

  function adjustTotal(cents) {
    if (cents <= 0) return;

    setDraft((previous) => ({
      ...previous,
      totalCents: cents,
      // Changing an aggregate total removes itemization,
      // since the individual item prices no longer reconcile.
      lineItems: [],
      charges: [],
      shares: distribute(cents, previous.shares, members),
      payments: [{ name: previous.payer, cents }],
    }));
    setError('');
  }

  function updateMemberAmount(field, name, cents) {
    setDraft((previous) => {
      const entries = [...previous[field]];
      const index = entries.findIndex((entry) => entry.name === name);

      if (index >= 0) {
        entries[index] = { name, cents };
      } else {
        entries.push({ name, cents });
      }

      return { ...previous, [field]: entries };
    });
    setError('');
  }

  function changePayer(payer) {
    updateDraft({
      payer,
      payments: [{ name: payer, cents: draft.totalCents }],
    });
  }

  function changeItemName(index, name) {
    setDraft((previous) => ({
      ...previous,
      lineItems: previous.lineItems.map((item, i) =>
        i === index ? { ...item, name } : item
      ),
    }));
  }

  function updateItem(index, newCents, selectedNames = null) {
    if (newCents < 0) return;

    setDraft((previous) => {
      const oldItem = previous.lineItems[index];
      const oldCents = itemTotal(oldItem);
      const difference = newCents - oldCents;

      const oldParticipants = getParticipants(
        oldItem, previous.shares
      );

      const participants = selectedNames || oldParticipants;
      if (!participants.length) return previous;

      const oldAllocations = oldItem.shares
        ? { ...oldItem.shares }
        : splitAmount(oldCents, oldParticipants);

      const newAllocations = splitAmount(newCents, participants);

      const nextItem = {
        ...oldItem,
        totalCents: newCents,
        grossCents: newCents + (oldItem.refundCents || 0),
        shares: newAllocations,
      };

      // Remove the old unit price when using an aggregate item total.
      delete nextItem.unitPriceCents;

      const lineItems = previous.lineItems.map((item, i) =>
        i === index ? nextItem : item
      );

      const oldShares = Object.fromEntries(
        previous.shares.map((s) => [s.name, s.cents])
      );

      // Replace only this item's allocation.
      members.forEach((name) => {
        oldShares[name] = (oldShares[name] || 0)
          - (oldAllocations[name] || 0)
          + (newAllocations[name] || 0);
      });

      const shares = members.map((name) => ({
        name,
        cents: oldShares[name] || 0,
      }));

      const itemPayer = oldItem.paidBy || previous.payer;
      const payments = previous.payments.map((p) => ({ ...p }));
      const payerIndex = payments.findIndex(
        (p) => p.name === itemPayer
      );

      if (payerIndex >= 0) {
        payments[payerIndex].cents += difference;
      } else {
        payments.push({ name: itemPayer, cents: difference });
      }

      return {
        ...previous,
        lineItems,
        shares,
        payments,
        totalCents: previous.totalCents + difference,
      };
    });

    setError('');
  }

  function changeParticipants(index, name) {
    const item = draft.lineItems[index];
    const current = getParticipants(item, draft.shares);
    const next = current.includes(name)
      ? current.filter((n) => n !== name)
      : members.filter(
          (n) => current.includes(n) || n === name
        );

    if (next.length > 0) {
      updateItem(index, itemTotal(item), next);
    }
  }

  function cancelEdit() {
    setDraft(initialize(expense));
    setEditing(false);
    setError('');
  }

  async function handleSave() {
    if (!draft || busy) return;

    setError('');

    if (!draft.description.trim()) {
      setError('Description is required.');
      return;
    }

    if (draft.totalCents <= 0) {
      setError('Total must be greater than $0.');
      return;
    }

    if (
      totalOf(draft.shares) !== draft.totalCents ||
      totalOf(draft.payments) !== draft.totalCents
    ) {
      setError(
        'The amount paid and individual shares must both equal '
        + formatCents(draft.totalCents) + '.'
      );
      return;
    }

    if (draft.shares.some((s) => s.cents < 0)) {
      setError('Individual shares cannot be negative.');
      return;
    }

    const itemSum = draft.lineItems.reduce(
      (total, item) => total + itemTotal(item), 0
    );
    const chargeSum = draft.charges.reduce(
      (total, charge) => total + (charge.amountCents || 0), 0
    );

    if (
      (draft.lineItems.length || draft.charges.length)
      && itemSum + chargeSum !== draft.totalCents
    ) {
      setError('Item prices and charges must match the total.');
      return;
    }

    setBusy(true);

    try {
      await updateExpense(group.id, expenseId, draft);
      await onSaved?.();
      onClose();
    } catch (err) {
      setError(err.message || 'Unable to save changes.');
    } finally {
      setBusy(false);
    }
  }

  const current = editing ? draft : expense;

  const transfers = current
    ? calculateTransfers(
        current.shares,
        current.payments,
        members
      )
    : [];

  return (
    <div
      className="modalback open expense-detail-overlay"
      role="presentation"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget && !busy) {
          onClose();
        }
      }}
    >
      <div
        className="modal expense-detail-modal"
        role="dialog"
        aria-modal="true"
        aria-label="Expense details"
      >
        <div className="modalhead">
          <span>{editing ? 'Edit expense' : 'Expense details'}</span>
          <button
            className="close"
            type="button"
            aria-label="Close"
            disabled={busy}
            onClick={onClose}
          >
            ×
          </button>
        </div>

        {busy && !expense ? (
          <div className="modalbody">Loading details...</div>
        ) : !current ? (
          <div className="modalbody" role="alert">
            {error || 'Unable to load this expense.'}
          </div>
        ) : (
          <div className="modalbody expense-detail-body">
            {error && (
              <p className="expense-error" role="alert">{error}</p>
            )}

            {editing ? (
              <>
                <label className="minilabel" htmlFor="editDescription">
                  Description
                </label>
                <input
                  id="editDescription"
                  className="field"
                  value={draft.description}
                  onChange={(e) =>
                    updateDraft({ description: e.target.value })
                  }
                />

                <div className="expense-edit-grid">
                  <label>
                    <span className="minilabel">Total amount ($)</span>
                    <MoneyInput
                      key={`total-${editing}`}
                      label="Total amount ($)"
                      cents={draft.totalCents}
                      onCommit={adjustTotal}
                    />
                  </label>

                  <label>
                    <span className="minilabel">Paid by</span>
                    <select
                      className="field"
                      value={draft.payer}
                      onChange={(e) => changePayer(e.target.value)}
                    >
                      {members.map((name) => (
                        <option key={name} value={name}>{name}</option>
                      ))}
                    </select>
                  </label>
                </div>
              </>
            ) : (
              <>
                <h3 className="expense-detail-title">
                  {expense.description}
                </h3>
                <div className="expense-detail-total">
                  <span>Total expense</span>
                  <strong>{formatCents(expense.totalCents)}</strong>
                </div>
              </>
            )}

            {/* SECTION 1: ITEMIZED BREAKDOWN */}
            <section className="expense-detail-section">
              <h4>Expense breakdown</h4>
              <p className="expense-muted">
                What was purchased and who shared it
              </p>

              {current.lineItems.length ? (
                <div className="detail-items">
                  {current.lineItems.map((item, index) => {
                    const participants = getParticipants(
                      item, current.shares
                    );

                    return (
                      <div className="detail-item" key={index}>
                        <div className="detail-item-top">
                          {editing ? (
                            <input
                              className="field"
                              aria-label={`Item ${index + 1} name`}
                              value={item.name}
                              onChange={(e) =>
                                changeItemName(index, e.target.value)
                              }
                            />
                          ) : (
                            <strong>{item.name}</strong>
                          )}

                          {editing ? (
                            <div className="detail-edit-amount">
                              <MoneyInput
                                label={`${item.name} price ($)`}
                                cents={itemTotal(item)}
                                onCommit={(cents) =>
                                  updateItem(index, cents)
                                }
                              />
                            </div>
                          ) : (
                            <strong className="detail-item-price">
                              {formatCents(itemTotal(item))}
                            </strong>
                          )}
                        </div>

                        {item.quantity > 1 && (
                          <small className="expense-muted">
                            Quantity: {item.quantity}
                          </small>
                        )}

                        <div className="detail-item-participants">
                          <span>Split between:</span>
                          <div className="detail-name-tags">
                            {participants.map((name) => (
                              <span className="detail-name-tag" key={name}>
                                {name}
                              </span>
                            ))}
                          </div>
                        </div>

                        {editing && (
                          <div className="detail-participant-editor">
                            <small>Change who shares this item:</small>
                            <div className="detail-checkboxes">
                              {members.map((name) => (
                                <label key={name}>
                                  <input
                                    type="checkbox"
                                    checked={participants.includes(name)}
                                    onChange={() =>
                                      changeParticipants(index, name)
                                    }
                                  />
                                  {name}
                                </label>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })}

                  {current.charges.map((charge, index) => (
                    <div className="detail-charge" key={index}>
                      <span>{charge.kind || 'Additional charge'}</span>
                      <strong>
                        {formatCents(charge.amountCents || 0)}
                      </strong>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="detail-item">
                  <div className="detail-item-top">
                    <strong>{current.description}</strong>
                    <strong className="detail-item-price">
                      {formatCents(current.totalCents)}
                    </strong>
                  </div>

                  <div className="detail-item-participants">
                    <span>Split between:</span>
                    <div className="detail-name-tags">
                      {current.shares
                        .filter((s) => s.cents > 0)
                        .map((s) => (
                          <span className="detail-name-tag" key={s.name}>
                            {s.name}
                          </span>
                        ))}
                    </div>
                  </div>

                  <small className="expense-muted">
                    Individual items were not saved for this expense.
                  </small>
                </div>
              )}
            </section>

            {/* SECTION 2: WHO OWES WHOM */}
            <section className="expense-detail-section">
              <h4>Who owes whom</h4>
              <p className="expense-muted">
                Based on the amounts paid and each person's share
              </p>

              {transfers.length ? (
                <div className="detail-transfers">
                  {transfers.map((transfer, index) => (
                    <div className="detail-transfer" key={index}>
                      <Avatar name={transfer.from} />
                      <div className="detail-transfer-text">
                        <strong>{transfer.from}</strong>
                        <span>Owes {transfer.to}</span>
                      </div>
                      <strong className="detail-transfer-amount">
                        {formatCents(transfer.cents)}
                      </strong>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="detail-settled">
                  ✓ No outstanding payments for this expense.
                </div>
              )}
            </section>

            {/* EXTRA DETAILS IN EDIT MODE */}
            {editing && (
              <section className="expense-detail-section">
                <h4>Adjust payments and shares</h4>
                <p className="expense-muted">
                  Amounts must add up to {formatCents(draft.totalCents)}.
                </p>

                <div className="detail-financial-table">
                  <div className="detail-table-head">
                    <span>Person</span>
                    <span>Paid</span>
                    <span>Share</span>
                  </div>

                  {members.map((name) => {
                    const paid = draft.payments.find(
                      (p) => p.name === name
                    )?.cents || 0;
                    const share = draft.shares.find(
                      (s) => s.name === name
                    )?.cents || 0;

                    return (
                      <div className="detail-table-row" key={name}>
                        <strong>{name}</strong>
                        <MoneyInput
                          label={`Paid by ${name}`}
                          cents={paid}
                          allowNegative
                          onCommit={(cents) =>
                            updateMemberAmount('payments', name, cents)
                          }
                        />
                        <MoneyInput
                          label={`Share for ${name}`}
                          cents={share}
                          onCommit={(cents) =>
                            updateMemberAmount('shares', name, cents)
                          }
                        />
                      </div>
                    );
                  })}
                </div>

                <div className="detail-edit-status">
                  <span>
                    Paid: {formatCents(totalOf(draft.payments))}
                  </span>
                  <span>
                    Shares: {formatCents(totalOf(draft.shares))}
                  </span>
                </div>
              </section>
            )}

            <div className="manualbuttons expense-popup-actions">
              {editing ? (
                <>
                  <button
                    className="secondary"
                    type="button"
                    disabled={busy}
                    onClick={cancelEdit}
                  >
                    Cancel
                  </button>
                  <button
                    className="primary"
                    type="button"
                    disabled={busy}
                    onClick={handleSave}
                  >
                    {busy ? 'Saving...' : 'Save changes'}
                  </button>
                </>
              ) : (
                <>
                  <button
                    className="secondary"
                    type="button"
                    onClick={onClose}
                  >
                    Close
                  </button>
                  <button
                    className="primary"
                    type="button"
                    onClick={() => setEditing(true)}
                  >
                    Edit expense
                  </button>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
