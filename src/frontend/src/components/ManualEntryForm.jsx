import { useState } from 'react';
import { createManualExpense } from '../api';
import { isAmountInput, parseDollarsToCents } from '../money';

function amountError(amount) {
  const text = amount.trim();
  if (!text) return null;
  if (!isAmountInput(text)) return 'Use digits and up to 2 decimals, e.g. 12.50.';
  if (parseDollarsToCents(text) <= 0) return 'Amount must be greater than $0.';
  return null;
}

export default function ManualEntryForm({
  group,
  currentUser,
  initialDescription = '',
  onSaved,
  onCancel,
}) {
  const members = group?.members || [];

  const [description, setDescription] = useState(initialDescription);
  const [amount, setAmount] = useState('');
  const [paidBy, setPaidBy] = useState(
    members.includes(currentUser) ? currentUser : members[0] || ''
  );
  const [splitBetween, setSplitBetween] = useState(members);
  const [saving, setSaving] = useState(false);
  const [serverError, setServerError] = useState(null);

  const amountProblem = amountError(amount);
  const splitProblem = splitBetween.length === 0 ? 'Choose at least one person to split with.' : null;
  const isValid =
    description.trim() !== '' && amount.trim() !== '' && !amountProblem && !splitProblem;

  const toggle = (member) => {
    setSplitBetween((prev) =>
      prev.includes(member)
        ? prev.filter((name) => name !== member)
        : members.filter((name) => prev.includes(name) || name === member)
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isValid || saving) return;

    setSaving(true);
    setServerError(null);
    try {
      await createManualExpense(group.id, {
        description: description.trim(),
        amount: amount.trim(),
        paidBy,
        splitBetween,
      });
      onSaved?.();
    } catch (err) {
      setServerError(err.message || 'Could not save the expense. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className="modalbody" id="manual" onSubmit={handleSubmit} noValidate>
      <p className="subtle" style={{ marginTop: 0 }}>
        Add an expense the usual way.
      </p>

      {serverError && (
        <div className="chat-error" role="alert">
          <span className="error-icon" aria-hidden="true">⚠</span>
          <span>{serverError}</span>
        </div>
      )}

      <label className="minilabel" htmlFor="desc">
        Description
      </label>
      <input
        className="field"
        id="desc"
        placeholder="e.g. Dinner"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <div className="minirow">
        <div style={{ flex: 1 }}>
          <label className="minilabel" htmlFor="amount">
            Amount ($)
          </label>
          <input
            className="field"
            id="amount"
            type="text"
            inputMode="decimal"
            placeholder="0.00"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            aria-invalid={Boolean(amountProblem)}
            aria-describedby={amountProblem ? 'amountError' : undefined}
          />
          {amountProblem && (
            <small id="amountError" className="field-error">
              {amountProblem}
            </small>
          )}
        </div>

        <div style={{ flex: 1 }}>
          <label className="minilabel" htmlFor="payer">
            Paid by
          </label>
          <select
            className="field"
            id="payer"
            value={paidBy}
            onChange={(e) => setPaidBy(e.target.value)}
          >
            {members.map((member) => (
              <option key={member} value={member}>
                {member}
              </option>
            ))}
          </select>
        </div>
      </div>

      <span className="minilabel" id="splitLabel">
        Split equally between
      </span>
      <div
        id="manualMembers"
        className="minirow checkbox-group"
        role="group"
        aria-labelledby="splitLabel"
      >
        {members.map((member) => (
          <label key={member} className="member-checkbox">
            <input
              type="checkbox"
              value={member}
              checked={splitBetween.includes(member)}
              onChange={() => toggle(member)}
            />{' '}
            {member}
          </label>
        ))}
      </div>
      {splitProblem && <small className="field-error">{splitProblem}</small>}

      <div className="manualbuttons">
        <button type="button" className="secondary" id="cancelManual" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" className="primary" id="saveManual" disabled={!isValid || saving}>
          {saving ? 'Saving...' : 'Save expense'}
        </button>
      </div>
    </form>
  );
}
