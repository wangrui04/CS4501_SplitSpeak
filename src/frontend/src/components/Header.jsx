export default function Header({
  currentUser,
  onSwitchUser,
  onSignOut,
}) {
  const initial = currentUser ? currentUser.charAt(0).toUpperCase() : '?';

  return (
    <header className="top">
      <div className="brand">
        <span className="logo" aria-hidden="true">✓</span>
        <span>splitwise</span>
      </div>

      <div className="header-user-section">
        <div className="user" aria-label="Current user">
          <span className="avatar" aria-hidden="true">{initial}</span>
          <span className="user-name">{currentUser || 'Not signed in'}</span>
        </div>

        {currentUser && (
          <div className="header-buttons">
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
