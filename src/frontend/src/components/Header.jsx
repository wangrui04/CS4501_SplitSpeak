export default function Header({
  currentUser,
  onSwitchUser,
  onSignOut,
  unreadReminders = 0,
  onOpenReminders,
}) {
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
              <button
                type="button"
                className="header-btn"
                onClick={onOpenReminders}
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
