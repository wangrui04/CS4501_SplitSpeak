import { useRef, useState } from 'react';
import { recordSettlement, sendReminder } from '../api';
import { formatCents, parseDollarsToCents } from '../money';

// Settle up (#46). Only the person being paid records a payment, so
// both tabs list just the people who currently owe the signed-in user.
// Amounts come from the group's displayed transfers; the server
// re-checks everything.

function dollarsInput(cents) {
  return formatCents(cents).slice(1).replace(/,/g, '');
}

function reminderMessage(debtor, currentUser, groupName) {
  return (
    `Hi ${debtor.from}, just a reminder that you still owe ${currentUser} ` +
    `${formatCents(debtor.cents)} for ${groupName}. Thanks!`
  );
}

function DebtorChoices({ legend, debtors, selected, onSelect }) {
  return (
    <fieldset className="settle-choices">
      <legend>{legend}</legend>
      {debtors.map((debtor) => (
        <label key={debtor.from} className="settle-choice">
          <input
            type="radio"
            name="settle-debtor"
            checked={selected === debtor.from}
            onChange={() => onSelect(debtor.from)}
          />
          {debtor.from} owes you {formatCents(debtor.cents)}
        </label>
      ))}
    </fieldset>
  );
}

export default function SettleUpModal({
  isOpen,
  onClose,
  onRecorded,
  group,
  currentUser,
}) {
  const debtors = (group?.transfers || []).filter(
    (transfer) => transfer.to === currentUser && transfer.cents > 0
  );
  const debtorsKey = debtors.map((d) => `${d.from}:${d.cents}`).join(',');

  const [tab, setTab] = useState('record');
  const [selected, setSelected] = useState(debtors[0]?.from ?? null);
  const [amount, setAmount] = useState(
    debtors[0] ? dollarsInput(debtors[0].cents) : ''
  );
  const [confirming, setConfirming] = useState(null);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState(null);
  const [pending, setPending] = useState(false);
  const pendingRef = useRef(false);

  const debtor =
    debtors.find((entry) => entry.from === selected) || debtors[0] || null;

  // When balances refresh (e.g. after a payment), reset the amount to
  // the new outstanding balance for the chosen person. Done during
  // render, as React recommends, rather than in an effect.
  const [seenDebtorsKey, setSeenDebtorsKey] = useState(debtorsKey);
  if (debtorsKey !== seenDebtorsKey) {
    const current =
      debtors.find((entry) => entry.from === selected) || debtors[0];
    setSeenDebtorsKey(debtorsKey);
    setSelected(current?.from ?? null);
    setAmount(current ? dollarsInput(current.cents) : '');
    setConfirming(null);
  }

  if (!isOpen) return null;

  const choose = (name) => {
    const entry = debtors.find((d) => d.from === name);
    setSelected(name);
    setAmount(dollarsInput(entry.cents));
    setConfirming(null);
    setError(null);
  };

  const switchTab = (next) => {
    setTab(next);
    setConfirming(null);
    setError(null);
    setStatus(null);
  };

  const startRecord = () => {
    setStatus(null);
    const cents = parseDollarsToCents(amount);

    if (cents === null || cents <= 0) {
      setError('Enter an amount greater than $0.00');
      return;
    }
    if (cents > debtor.cents) {
      setError(`Amount is more than the ${formatCents(debtor.cents)} owed`);
      return;
    }

    setError(null);
    setConfirming({ from: debtor.from, cents, shown: debtor.cents });
  };

  // Guard against double clicks with a ref, since state updates are async.
  const runOnce = async (action) => {
    if (pendingRef.current) return;
    pendingRef.current = true;
    setPending(true);
    try {
      await action();
    } finally {
      pendingRef.current = false;
      setPending(false);
    }
  };

  const confirmRecord = () =>
    runOnce(async () => {
      try {
        await recordSettlement(group.id, {
          from: confirming.from,
          to: currentUser,
          cents: confirming.cents,
          expectedOutstandingCents: confirming.shown,
        });
        setConfirming(null);
        setError(null);
        setStatus(
          `Recorded ${formatCents(confirming.cents)} from ${confirming.from}.`
        );
        onRecorded?.();
      } catch (err) {
        setConfirming(null);
        setStatus(null);
        setError(err.message || 'Could not record the payment');
      }
    });

  const message = debtor
    ? reminderMessage(debtor, currentUser, group.name)
    : '';

  const remind = () =>
    runOnce(async () => {
      try {
        await sendReminder(group.id, debtor.from);
        setError(null);
        setStatus(`Reminder sent to ${debtor.from} in SplitSpeak.`);
      } catch (err) {
        setStatus(null);
        setError(err.message || 'Could not send the reminder');
      }
    });

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(message);
      setError(null);
      setStatus('Message copied');
    } catch {
      setStatus(null);
      setError('Could not copy the message');
    }
  };

  const empty = (
    <p className="hint">No one owes you in this group.</p>
  );

  return (
    <div
      className="modalback open"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      role="presentation"
    >
      <div
        className="modal settle-modal"
        role="dialog"
        aria-label="Settle up"
        aria-modal="true"
      >
        <div className="modalhead">
          <span>Settle up</span>
          <button
            type="button"
            className="close"
            onClick={onClose}
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <div className="mode" role="tablist">
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'record'}
            className={tab === 'record' ? 'selected' : ''}
            onClick={() => switchTab('record')}
          >
            Record payment
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'remind'}
            className={tab === 'remind' ? 'selected' : ''}
            onClick={() => switchTab('remind')}
          >
            Send reminder
          </button>
        </div>

        <div className="modalbody" role="tabpanel">
          {!debtor ? (
            empty
          ) : tab === 'record' ? (
            confirming ? (
              <div className="settle-confirm">
                <p>
                  <b>
                    Record {confirming.from} paying you{' '}
                    {formatCents(confirming.cents)}?
                  </b>
                </p>
                <p className="hint">
                  This records a payment only; SplitSpeak does not transfer money.
                </p>
                <div className="settle-actions">
                  <button
                    type="button"
                    onClick={() => setConfirming(null)}
                    disabled={pending}
                  >
                    Back
                  </button>
                  <button
                    type="button"
                    className="teal"
                    onClick={confirmRecord}
                    disabled={pending}
                  >
                    Confirm payment
                  </button>
                </div>
              </div>
            ) : (
              <>
                <DebtorChoices
                  legend="Who paid you?"
                  debtors={debtors}
                  selected={debtor.from}
                  onSelect={choose}
                />
                <label className="settle-amount">
                  Amount ($)
                  <input
                    type="text"
                    inputMode="decimal"
                    value={amount}
                    onChange={(e) => {
                      setAmount(e.target.value);
                      setError(null);
                    }}
                  />
                </label>
                <p className="hint">
                  Leave the full amount for a full payment, or enter less for a
                  partial payment.
                </p>
                <div className="settle-actions">
                  <button
                    type="button"
                    onClick={() => {
                      setAmount(dollarsInput(debtor.cents));
                      setError(null);
                    }}
                  >
                    Full payment
                  </button>
                  <button type="button" className="teal" onClick={startRecord}>
                    Record payment
                  </button>
                </div>
              </>
            )
          ) : (
            <>
              <DebtorChoices
                legend="Who should be reminded?"
                debtors={debtors}
                selected={debtor.from}
                onSelect={choose}
              />
              <section className="settle-preview" aria-label="Reminder preview">
                <p>{message}</p>
              </section>
              <p className="hint">
                {debtor.from} will see this in SplitSpeak. No email or text is sent.
              </p>
              <div className="settle-actions">
                <button type="button" onClick={copy}>
                  Copy message
                </button>
                <button
                  type="button"
                  className="teal"
                  onClick={remind}
                  disabled={pending}
                >
                  Send reminder
                </button>
              </div>
            </>
          )}

          {error && (
            <p className="chat-error" role="alert">
              {error}
            </p>
          )}
          {status && (
            <p className="settle-status" role="status">
              {status}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
