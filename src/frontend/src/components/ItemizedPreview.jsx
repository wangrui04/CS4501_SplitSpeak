import { useState } from 'react';
import { confirmExpense } from '../api';

function formatCents(cents) {
  if (cents === null || cents === undefined) return '$0.00';
  return `$${(Math.abs(cents) / 100).toFixed(2)}`;
}

export default function ItemizedPreview({
  preview,
  conversationId,
  currentUser,
  onConfirm,
  onEditInChat,
  onCancel,
}) {
  const [confirming, setConfirming] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  if (!preview) return null;

  const totalCents =
    preview.totalCents ??
    preview.total_cents ??
    (preview.items || preview.lineItems || []).reduce(
      (sum, it) => sum + (it.amountCents ?? it.amount_cents ?? it.cents ?? 0),
      0
    );

  const items = preview.lineItems || preview.items || [];
  const charges = preview.charges || [];

  // Standardize shares to array of { name, cents }
  let sharesList = [];
  if (Array.isArray(preview.shares)) {
    sharesList = preview.shares;
  } else if (preview.shares && typeof preview.shares === 'object') {
    sharesList = Object.entries(preview.shares).map(([name, cents]) => ({
      name,
      cents,
    }));
  }

  const description =
    preview.description ||
    preview.name ||
    (sharesList[0] && sharesList[0].summary) ||
    'Shared expense';

  const isValidated = preview.validated !== false;
  const paidList = Array.isArray(preview.paid) ? preview.paid : [];
  const transfers = preview.settlement?.transfers || [];

  const handleConfirm = async () => {
    if (!isValidated || confirming || success) return;

    if (!conversationId) {
      setError('Cannot confirm: missing conversation reference.');
      return;
    }

    setConfirming(true);
    setError(null);

    try {
      const result = await confirmExpense(conversationId);
      setSuccess(true);
      if (onConfirm) {
        onConfirm(result);
      }
    } catch (err) {
      setError(err.message || 'Failed to confirm expense. Please try again.');
    } finally {
      setConfirming(false);
    }
  };

  return (
    <div
      className="preview show"
      role="region"
      aria-label="Itemized expense preview"
      data-testid="itemized-preview"
    >
      <div className="preview-top-row">
        <span className={`valid ${isValidated ? 'is-valid' : 'is-invalid'}`}>
          {isValidated ? '✓ Validated' : '⚠ Unvalidated'}
        </span>
        <h4>{description}</h4>
      </div>

      <p className="subtle" style={{ fontSize: '12px', margin: '4px 0 10px' }}>
        Paid by <strong>{preview.payer}</strong> · {preview.currency || 'USD'}
      </p>

      {/* Itemized Line Items */}
      {items.length > 0 && (
        <div className="preview-section" aria-label="Line items">
          {items.map((it, idx) => {
            const itemName = it.description || it.name || `Item ${idx + 1}`;
            const itemCents =
              it.totalCents ??
              it.total_cents ??
              it.amountCents ??
              it.amount_cents ??
              it.cents ??
              0;
            const participants =
              it.participants ||
              it.people ||
              (it.shares ? Object.keys(it.shares).filter((k) => it.shares[k] > 0) : []);

            return (
              <div key={idx} className="itemline">
                <span>
                  <strong>{itemName}</strong>
                  {participants.length > 0 && (
                    <small>Split by: {participants.join(', ')}</small>
                  )}
                </span>
                <b>{formatCents(itemCents)}</b>
              </div>
            );
          })}
        </div>
      )}

      {/* Additional Charges (Tax & Tip) */}
      {charges.length > 0 ? (
        <div className="preview-charges" aria-label="Tax and tip">
          {charges.map((charge, idx) => {
            const chargeName =
              charge.kind === 'tax'
                ? 'Tax'
                : charge.kind === 'tip'
                ? 'Tip'
                : charge.name || 'Additional charge';
            const chargeCents =
              charge.amountCents ??
              charge.amount_cents ??
              charge.cents ??
              (charge.amount ? Math.round(parseFloat(charge.amount) * 100) : 0);

            return (
              <div key={idx} className="itemline charge-line">
                <span>
                  {chargeName}
                  {charge.percent && <small> ({charge.percent}%)</small>}
                </span>
                <b>{formatCents(chargeCents)}</b>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="tax-tip-note">
          <small>Tax & tip: Included or none specified</small>
        </div>
      )}

      {/* Expense Total */}
      <div className="itemline total-line">
        <strong>Total</strong>
        <strong>{formatCents(totalCents)}</strong>
      </div>

      {/* Participant Shares */}
      {sharesList.length > 0 && (
        <div className="sharetotal" aria-label="Individual shares">
          <b>Each person&apos;s share</b>
          {sharesList.map((share) => {
            const isMe = share.name === currentUser;
            return (
              <div key={share.name} className="itemline share-row">
                <span>
                  {share.name}
                  {isMe && <span className="you-pill"> (you)</span>}
                </span>
                <b>{formatCents(share.cents)}</b>
              </div>
            );
          })}
        </div>
      )}

      {/* Amounts paid, only when it is not a single payer */}
      {paidList.filter((entry) => entry.cents !== 0).length > 1 && (
        <div className="sharetotal">
          <b id="paidTitle">Amounts paid</b>
          <ul className="plain-list" aria-labelledby="paidTitle">
            {paidList.map((entry) => (
              <li key={entry.name} className="itemline">
                <span>{entry.name}</span>
                <b>
                  {entry.cents < 0 ? '-' : ''}
                  {formatCents(entry.cents)}
                </b>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Settlement: computed by the same backend function as balances */}
      {transfers.length > 0 && (
        <div className="sharetotal transfers">
          <b id="transfersTitle">Who pays whom</b>
          <ul className="plain-list" aria-labelledby="transfersTitle">
            {transfers.map((transfer) => (
              <li key={`${transfer.from}-${transfer.to}`} className="itemline">
                <span>
                  {transfer.from} pays {transfer.to}
                </span>{' '}
                <b>{formatCents(transfer.cents)}</b>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Status Feedback */}
      {error && (
        <div className="preview-feedback error" role="alert">
          <span className="error-icon" aria-hidden="true">⚠</span>
          <span>{error}</span>
        </div>
      )}
      {success && (
        <div className="preview-feedback success" role="status">
          ✓ Expense confirmed and saved! Group balances updated.
        </div>
      )}

      {/* Confirm / Cancel Actions */}
      <div className="manualbuttons preview-actions">
        {onEditInChat && !success && (
          <button
            type="button"
            className="secondary"
            id="editInChat"
            onClick={onEditInChat}
            disabled={confirming}
          >
            Edit in chat
          </button>
        )}
        {onCancel && !success && (
          <button
            type="button"
            className="secondary"
            id="cancelPreview"
            onClick={onCancel}
            disabled={confirming}
          >
            Cancel
          </button>
        )}
        <button
          type="button"
          className="primary btn-confirm"
          id="confirmExpense"
          onClick={handleConfirm}
          disabled={!isValidated || confirming || success}
        >
          {confirming
            ? 'Confirming...'
            : success
            ? 'Confirmed ✓'
            : 'Confirm expense'}
        </button>
      </div>
    </div>
  );
}

