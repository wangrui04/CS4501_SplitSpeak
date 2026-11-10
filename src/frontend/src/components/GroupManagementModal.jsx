
import { useState } from 'react';

import {
  createGroup,
  addGroupMember,
} from '../api';

export default function GroupManagementModal({
  mode,
  group,
  onClose,
  onSuccess,
}) {
  const isCreating = mode === 'create';

  const [groupName, setGroupName] = useState('');
  const [memberInput, setMemberInput] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    const name = groupName.trim();
    const member = memberInput.trim();

    if (isCreating && !name) {
      setError('Please enter a group name.');
      return;
    }

    if (!isCreating && !member) {
      setError('Please enter a member name.');
      return;
    }

    setSaving(true);

    try {
      let result;

      if (isCreating) {
        const members = memberInput
          .split(',')
          .map((value) => value.trim())
          .filter(Boolean);

        result = await createGroup(name, members);
      } else {
        result = await addGroupMember(
          group.id,
          member,
        );
      }

      await onSuccess(result);
    } catch (err) {
      setError(
        err.message || 'Unable to save changes.',
      );
    } finally {
      setSaving(false);
    }
  };

  const title = isCreating
    ? 'Create a group'
    : `Add member to ${group?.name}`;

  const fieldStyle = {
    width: '100%',
    boxSizing: 'border-box',
    padding: '11px 12px',
    border: '1px solid #d1d5db',
    borderRadius: '5px',
    fontSize: '14px',
  };

  const labelStyle = {
    display: 'block',
    marginBottom: '7px',
    color: '#444',
    fontSize: '13px',
    fontWeight: 600,
  };

  return (
    <div
      className="modalback open"
      onClick={(event) => {
        if (
          event.target === event.currentTarget &&
          !saving
        ) {
          onClose();
        }
      }}
    >
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-label={title}
        style={{
          maxWidth: '480px',
        }}
      >
        <div className="modalhead">
          <span>{title}</span>

          <button
            type="button"
            className="close"
            aria-label="Close modal"
            disabled={saving}
            onClick={onClose}
          >
            ×
          </button>
        </div>

        <form
          onSubmit={handleSubmit}
          className="modalbody"
          style={{
            gap: '18px',
          }}
        >
          {isCreating && (
            <div>
              <label
                htmlFor="group-management-name"
                style={labelStyle}
              >
                Group name
              </label>

              <input
                id="group-management-name"
                className="field"
                style={fieldStyle}
                value={groupName}
                maxLength={100}
                autoFocus
                onChange={(event) => {
                  setGroupName(event.target.value);
                }}
                placeholder="e.g. Boston Trip"
                disabled={saving}
              />
            </div>
          )}

          <div>
            <label
              htmlFor="group-management-members"
              style={labelStyle}
            >
              {isCreating
                ? 'Group members (optional)'
                : 'Member name'}
            </label>

            <input
              id="group-management-members"
              className="field"
              style={fieldStyle}
              value={memberInput}
              autoFocus={!isCreating}
              onChange={(event) => {
                setMemberInput(event.target.value);
              }}
              placeholder={
                isCreating
                  ? 'Anna, Ben, Cara'
                  : 'e.g. Anna'
              }
              disabled={saving}
            />

            <p
              style={{
                fontSize: '12px',
                color: '#888',
                lineHeight: 1.5,
                marginBottom: 0,
              }}
            >
              {isCreating
                ? "Separate names with commas. You'll automatically be included."
                : "The new member will appear in the group's expense-splitting options."}
            </p>
          </div>

          {error && (
            <div
              role="alert"
              className="name-picker-error"
              style={{
                marginBottom: 0,
              }}
            >
              {error}
            </div>
          )}

          <div
            style={{
              display: 'flex',
              justifyContent: 'flex-end',
              alignItems: 'center',
              gap: '10px',
              paddingTop: '6px',
            }}
          >
            <button
              type="button"
              className="btn-cancel"
              onClick={onClose}
              disabled={saving}
            >
              Cancel
            </button>

            <button
              type="submit"
              className="primary"
              disabled={saving}
            >
              {saving
                ? 'Saving...'
                : isCreating
                ? 'Create group'
                : 'Add member'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
