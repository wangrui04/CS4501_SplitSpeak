import { useEffect, useRef } from 'react';

export default function Header({
  currentUser,
  onSwitchUser,
  onSignOut,
  unreadReminders = 0,
  onOpenReminders,
  remindersPanel = null,
  onCloseReminders,
}) {
  const anchorRef = useRef(null);
  const buttonRef = useRef(null);
  const isRemindersOpen = Boolean(remindersPanel);

  // Close the reminders popover on Escape or a click outside it.
  useEffect(() => {
    if (!isRemindersOpen || !onCloseReminders) return undefined;

    const onMouseDown = (event) => {
      if (!anchorRef.current?.contains(event.target)) onCloseReminders();
    };
    const onKeyDown = (event) => {
      if (event.key === 'Escape') {
        onCloseReminders();
        buttonRef.current?.focus();
      }
    };

    document.addEventListener('mousedown', onMouseDown);
    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('mousedown', onMouseDown);
      document.removeEventListener('keydown', onKeyDown);
    };
  }, [isRemindersOpen, onCloseReminders]);

  const initial = currentUser ? currentUser.charAt(0).toUpperCase() : '?';

  return (
    <header className="top">
      <div className="brand">
        <span className="logo" aria-hidden="true">✓</span>
        <span>SplitSpeak</span>
      </div>

      <div className="header-user-section">
        <div className="user" aria-label="Current user">
          <span className="avatar" aria-hidden="true">{initial}</span>
          <span className="user-name">{currentUser || 'Not signed in'}</span>
        </div>

        {currentUser && (
          <div className="header-buttons">
            {onOpenReminders && (
              <div className="reminders-anchor" ref={anchorRef}>
                <button
                  ref={buttonRef}
                  type="button"
                  className="header-btn"
                  onClick={onOpenReminders}
                  aria-expanded={isRemindersOpen}
                  aria-label={
                    unreadReminders > 0
                      ? `Reminders (${unreadReminders} unread)`
                      : 'Reminders'
                  }
                >
                  Reminders
                  {unreadReminders > 0 && (
                    <span className="reminder-badge" aria-hidden="true">
                      {unreadReminders}
                    </span>
                  )}
                </button>
                {remindersPanel && (
                  <div className="reminders-popover">{remindersPanel}</div>
                )}
              </div>
            )}
            {onSwitchUser && (
              <button
                type="button"
                className="header-btn"
                onClick={onSwitchUser}
                aria-label="Switch user"
              >
                Switch user
              </button>
            )}
            {onSignOut && (
              <button
                type="button"
                className="header-btn signout-btn"
                onClick={onSignOut}
                aria-label="Sign out"
              >
                Sign out
              </button>
            )}
          </div>
        )}
      </div>
    </header>
  );
}
