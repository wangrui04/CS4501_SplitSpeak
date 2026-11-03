
export default function Sidebar({
  groups = [],
  selectedGroupId,
  onSelectGroup,
  onCreateGroup,
  onAddFriend,
  friends = [],
  currentUser,
}) {
  const friendList = (friends || []).filter(
    (friend) => friend !== currentUser
  );

  return (
    <aside className="left" aria-label="Sidebar navigation">
      <button
        type="button"
        className="navitem sel"
        id="dashboard"
      >
        ▤ &nbsp; Dashboard
      </button>

      <button
        type="button"
        className="navitem"
        id="activity"
      >
        ◷ &nbsp; Recent activity
      </button>

      {/* Groups */}
      <div className="side-title">
        <span>Groups</span>

        <button
          type="button"
          aria-label="Create a group"
          title="Create a group"
          onClick={onCreateGroup}
          style={{
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            color: '#777',
            fontSize: '19px',
            lineHeight: 1,
          }}
        >
          +
        </button>
      </div>

      <nav aria-label="Groups">
        {groups.map((group) => {
          const isActive = group.id === selectedGroupId;

          return (
            <button
              key={group.id}
              type="button"
              className={`group-btn ${isActive ? 'active' : ''}`}
              onClick={() => onSelectGroup(group.id)}
              aria-current={isActive ? 'page' : undefined}
            >
              ⌂ &nbsp; {group.name}
            </button>
          );
        })}
      </nav>

      <button
        type="button"
        className="group-btn"
        onClick={onCreateGroup}
        style={{
          color: '#16a88c',
          fontWeight: 600,
          cursor: 'pointer',
        }}
      >
        + &nbsp; Create a group
      </button>

      {/* Friends */}
      <div className="side-title">
        <span>Friends</span>

        <button
          type="button"
          aria-label="Add friend"
          title={
            selectedGroupId
              ? 'Add friend to current group'
              : 'Select a group first'
          }
          onClick={onAddFriend}
          disabled={!selectedGroupId}
          style={{
            background: 'transparent',
            border: 'none',
            cursor: selectedGroupId ? 'pointer' : 'not-allowed',
            color: '#777',
            fontSize: '19px',
            lineHeight: 1,
            opacity: selectedGroupId ? 1 : 0.4,
          }}
        >
          +
        </button>
      </div>

      <div>
        {friendList.map((friend) => (
          <button
            key={friend}
            type="button"
            className="group-btn"
          >
            ◉ &nbsp; {friend}
          </button>
        ))}
      </div>

      <p className="hint">
        Add friends to the selected group to split expenses together.
      </p>
    </aside>
  );
}
