export default function Sidebar({
  groups = [],
  selectedGroupId,
  onSelectGroup,
  friends = ['Kayla', 'Rui'],
  currentUser,
}) {
  const friendList = (friends || []).filter((f) => f !== currentUser);

  return (
    <aside className="left" aria-label="Sidebar navigation">
      <button type="button" className="navitem sel" id="dashboard">
        ▤ &nbsp; Dashboard
      </button>
      <button type="button" className="navitem" id="activity">
        ◷ &nbsp; Recent activity
      </button>

      <div className="side-title">
        <span>Groups</span>
        <span aria-hidden="true">＋</span>
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

      <div className="side-title">
        <span>Friends</span>
        <span aria-hidden="true">＋</span>
      </div>

      <div>
        {friendList.map((friend) => (
          <button key={friend} type="button" className="group-btn">
            ◉ &nbsp; {friend}
          </button>
        ))}
      </div>

      <p className="hint">
        Familiar Splitwise-style layout with an AI expense assistant.
      </p>
    </aside>
  );
}
