function formatCents(cents) {
  const abs = Math.abs(cents);
  return `$${(abs / 100).toFixed(2)}`;
}

export default function GroupView({
  group,
  balances = {},
  expenses = [],
  currentUser,
  onAddExpense,
  onSettleUp,
}) {
  if (!group) {
    return (
      <main className="middle">
        <div className="empty">
          <div className="empty-icon">⌂</div>
          <h3>Select a group</h3>
          <p>Choose a group from the sidebar to view expenses.</p>
        </div>
      </main>
    );
  }

  const userBalance = (currentUser && balances[currentUser]) || 0;
  const youOwe = userBalance < 0 ? Math.abs(userBalance) : 0;
  const youAreOwed = userBalance > 0 ? userBalance : 0;
  const balancePrefix = userBalance > 0 ? '+' : userBalance < 0 ? '-' : '';

  return (
    <main className="middle">
      <div className="panehead">
        <h1 id="pagetitle">{group.name}</h1>
        <div className="actions">
          <button
            type="button"
            className="orange"
            id="add"
            onClick={onAddExpense}
          >
            Add an expense
          </button>
          <button
            type="button"
            className="teal"
            id="settle"
            onClick={onSettleUp}
          >
            Settle up
          </button>
        </div>
      </div>

      <div className="sumstrip">
        <div>
          total balance
          <b
            id="totalbal"
            className={userBalance > 0 ? 'green' : userBalance < 0 ? 'orangeText' : ''}
          >
            {balancePrefix}{formatCents(userBalance)}
          </b>
        </div>
        <div>
          you owe
          <b id="youowe" className={youOwe > 0 ? 'orangeText' : ''}>
            {formatCents(youOwe)}
          </b>
        </div>
        <div>
          you are owed
          <b id="owed" className={youAreOwed > 0 ? 'green' : ''}>
            {formatCents(youAreOwed)}
          </b>
        </div>
      </div>

      <div className="month" id="month">
        EXPENSES
      </div>

      <div id="expenseList">
        {expenses.length === 0 ? (
          <div className="empty">
            <div className="empty-icon" aria-hidden="true">▧</div>
            <h3>No expenses yet</h3>
            <p>Add your first shared expense to see it here.</p>
          </div>
        ) : (
          expenses.map((expense) => {
            const userShare =
              expense.shares?.find((s) => s.name === currentUser)?.cents || 0;
            const isPayer = expense.payer === currentUser;
            const netForUser = isPayer
              ? expense.totalCents - userShare
              : -userShare;

            return (
              <div key={expense.id} className="expense-row" tabIndex={0}>
                <div className="exp-icon" aria-hidden="true">▧</div>
                <div className="exp-name">
                  <strong>{expense.description}</strong>
                  <small>
                    {expense.payer} paid {formatCents(expense.totalCents)}
                  </small>
                </div>
                <div className="paid">
                  total<b>{formatCents(expense.totalCents)}</b>
                </div>
                <div className="owes">
                  {netForUser > 0
                    ? 'you lent'
                    : netForUser < 0
                    ? 'you borrowed'
                    : 'your share'}
                  <b style={{ color: netForUser >= 0 ? '#1aad8c' : '#f06c42' }}>
                    {formatCents(Math.abs(netForUser || userShare))}
                  </b>
                </div>
              </div>
            );
          })
        )}
      </div>
    </main>
  );
}

