function formatMoney(cents) {
  const abs = Math.abs(cents);
  return `$${(abs / 100).toFixed(2)}`;
}

export default function RightSidebar({
  members = [],
  balances = {},
  currentUser,
}) {
  const otherMembers = currentUser
    ? members.filter((m) => m !== currentUser)
    : members;

  const bgColors = ['#fce7ee', '#e8f3ff', '#f1eafc', '#e6f8f3', '#fff4e5'];

  return (
    <aside className="right" aria-label="Group balances">
      <h3>Group balances</h3>
      <div id="sideBalances">
        {otherMembers.length === 0 ? (
          <p className="hint">No other members in this group.</p>
        ) : (
          otherMembers.map((member, index) => {
            const amountCents = balances[member] || 0;
            const isNegative = amountCents < 0;
            const isPositive = amountCents > 0;
            const statusText = isNegative
              ? 'owes the group '
              : isPositive
              ? 'is owed '
              : 'settled up ';

            return (
              <div key={member} className="balanceentry">
                <span
                  className="avatar"
                  style={{ background: bgColors[index % bgColors.length] }}
                  aria-hidden="true"
                >
                  {member.charAt(0)}
                </span>
                <span>
                  {member}
                  <b className={isPositive ? 'negative' : ''}>
                    {statusText}
                    {formatMoney(amountCents)}
                  </b>
                </span>
              </div>
            );
          })
        )}
      </div>
      <div className="tip">
        All balances here reflect confirmed expenses. AI drafts are saved only after you confirm them.
      </div>
    </aside>
  );
}

