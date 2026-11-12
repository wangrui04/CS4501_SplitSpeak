import { useState, useEffect } from 'react';
import { fetchAvailableNames } from '../api';
import LoadingSpinner from './LoadingSpinner';

export default function NamePicker({
  onSelectUser,
  onCancel,
  currentUserName,
  isModal = false,
  initialNames = null,
}) {
  const [names, setNames] = useState(initialNames || []);
  const [selectedName, setSelectedName] = useState(
    currentUserName || (initialNames && initialNames[0]) || ''
  );
  const [loading, setLoading] = useState(!initialNames);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (initialNames) return;

    let isMounted = true;
    async function loadNames() {
      try {
        const available = await fetchAvailableNames();
        if (isMounted) {
          setNames(available || []);
          if (available && available.length > 0) {
            setSelectedName((prev) => prev || available[0]);
          }
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || 'Failed to load available users. Please try again.');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    loadNames();
    return () => {
      isMounted = false;
    };
  }, [initialNames]);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!selectedName) {
      setError('Please select a profile to continue');
      return;
    }

    setError(null);
    setSubmitting(true);
    try {
      await onSelectUser(selectedName);
    } catch (err) {
      setError(err.message || 'Sign in failed. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const content = (
    <div
      className={`name-picker-card ${isModal ? 'modal' : 'standalone'}`}
      role={isModal ? 'dialog' : 'region'}
      aria-label={isModal ? 'Switch user' : 'Sign in to SplitSpeak'}
    >
      <div className="name-picker-header">
        <div className="name-picker-brand">
          <span className="logo" aria-hidden="true">✓</span>
          <h2>{isModal ? 'Switch User' : 'Sign in to SplitSpeak'}</h2>
        </div>
        {isModal && onCancel && (
          <button
            type="button"
            className="name-picker-close"
            onClick={onCancel}
            aria-label="Close"
          >
            ✕
          </button>
        )}
      </div>

      <div className="name-picker-body">
        <p className="name-picker-subtitle">
          {isModal
            ? 'Select another member to switch your active session:'
            : 'Select your profile to access your shared expenses:'}
        </p>

        {loading ? (
          <LoadingSpinner message="Loading available profiles..." />
        ) : (
          <>
            {error && (
              <div className="name-picker-error" role="alert">
                <span className="error-icon" aria-hidden="true">⚠</span>
                <span>{error}</span>
              </div>
            )}

            <div className="name-picker-list" role="radiogroup" aria-label="Profiles">
              {names.map((name) => {
                const isSelected = selectedName === name;
                const isCurrent = currentUserName === name;
                const initial = name.charAt(0).toUpperCase();

                return (
                  <button
                    key={name}
                    type="button"
                    role="radio"
                    aria-checked={isSelected}
                    className={`name-picker-item ${isSelected ? 'selected' : ''}`}
                    onClick={() => {
                      setSelectedName(name);
                      setError(null);
                    }}
                  >
                    <span className="avatar" aria-hidden="true">
                      {initial}
                    </span>
                    <span className="name-picker-name">
                      {name}
                      {isCurrent ? ' (current)' : ''}
                    </span>
                    {isSelected && (
                      <span className="checkmark" aria-hidden="true">
                        ✓
                      </span>
                    )}
                  </button>
                );
              })}
            </div>

            <div className="name-picker-actions">
              {isModal && onCancel && (
                <button
                  type="button"
                  className="btn-cancel"
                  onClick={onCancel}
                  disabled={submitting}
                >
                  Cancel
                </button>
              )}
              <button
                type="button"
                className="primary btn-signin"
                onClick={handleSubmit}
                disabled={submitting || !selectedName || names.length === 0}
              >
                {submitting
                  ? 'Signing in...'
                  : isModal
                  ? `Switch to ${selectedName || 'user'}`
                  : `Continue as ${selectedName || 'user'}`}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );

  if (isModal) {
    return (
      <div className="modalback open" onClick={(e) => e.target === e.currentTarget && onCancel && onCancel()}>
        {content}
      </div>
    );
  }

  return <div className="name-picker-container">{content}</div>;
}
