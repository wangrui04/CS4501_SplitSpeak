
import { formatCents } from '../money';
import SettlementHistory from './SettlementHistory';

const EMPTY_SUMMARY = {
  totalBalance: 0,
  youOwe: 0,
  youAreOwed: 0,
};

// SQLite CURRENT_TIMESTAMP is UTC.
function monthLabel(createdAt) {
  if (!createdAt) return 'EXPENSES';

  const date = new Date(
    `${createdAt.replace(' ', 'T')}Z`,
  );

  if (Number.isNaN(date.getTime())) {
    return 'EXPENSES';
  }

  return date
    .toLocaleString('en-US', {
      month: 'long',
      year: 'numeric',
      timeZone: 'UTC',
    })
    .toUpperCase();
}

function groupByMonth(expenses) {
  const months = [];

  for (const expense of expenses) {
    const label = monthLabel(expense.created_at);
    const last = months[months.length - 1];

    if (last && last.label === label) {
      last.expenses.push(expense);
    } else {
      months.push({
        label,
        expenses: [expense],
      });
    }
  }

  return months;
}

function centsFor(entries, name) {
  return (
    (entries || []).find(
      (entry) => entry.name === name,
    )?.cents || 0
  );
}

function payerLabel(expense) {
  const payers = (expense.payments || []).filter(
    (payment) => payment.cents > 0,
  );

  if (payers.length > 1) {
    return `${payers.length} people paid`;
  }

  return `${payers[0]?.name || expense.payer} paid`;
}

function ExpenseRow({ expense, currentUser, onClick }) {
  const share = centsFor(expense.shares, currentUser);

  const paid = expense.payments
    ? centsFor(expense.payments, currentUser)
    : expense.payer === currentUser
    ? expense.totalCents
    : 0;

  const net = paid - share;

  let label = 'not involved';
  let className = 'settled';

  if (net > 0) {
    label = 'you lent';
    className = 'lent';
  } else if (net < 0) {
    label = 'you owe';
    className = 'borrowed';
  } else if (share > 0 || paid !== 0) {
    label = 'settled';
  }

  return (
    <li className="expense-row expense-clickable">
      {onClick && (
        <button
          type="button"
          className="expense-row-action"
          aria-label={`View ${expense.description} expense details`}
          onClick={() => onClick(expense)}
        />
      )}
      <div className="exp-icon" aria-hidden="true">
        ▧
      </div>

      <div className="exp-name">
        <strong>{expense.description}</strong>
        <small>
          {payerLabel(expense)}{' '}
          {formatCents(expense.totalCents)}
        </small>
      </div>

      <div className="paid">
        total
        <b>{formatCents(expense.totalCents)}</b>
      </div>

      <div className={`owes ${className}`}>
        {label}
        {net !== 0 && (
          <b>{formatCents(net)}</b>
        )}
      </div>
    </li>
  );
}

export default function GroupView({
  group,
  summary = EMPTY_SUMMARY,
  expenses = [],
  currentUser,
  onAddExpense,
  onSettleUp,
  onAddMember,
  settlements,
  onExpenseClick,
}) {
  if (!group) {
    return (
      <main className="middle">
        <div className="empty">
          <div className="empty-icon">⌂</div>
          <h3>Select a group</h3>
          <p>
            Choose a group from the sidebar to view expenses.
          </p>
        </div>
      </main>
    );
  }

  const {
    totalBalance,
    youOwe,
    youAreOwed,
  } = {
    ...EMPTY_SUMMARY,
    ...summary,
  };

  const balancePrefix =
    totalBalance > 0
      ? '+'
      : totalBalance < 0
      ? '-'
      : '';

  return (
    <main className="middle">
      <div className="panehead">
        <div>
          <h1 id="pagetitle">{group.name}</h1>
          <small
            style={{
              color: '#888',
              fontSize: '12px',
            }}
          >
            {group.members?.length || 0} members
          </small>
        </div>

        <div className="actions">
          <button
            type="button"
            className="teal"
            onClick={onAddMember}
            aria-label="Add member"
          >
            + Add member
          </button>

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
            className={
              totalBalance > 0
                ? 'green'
                : totalBalance < 0
                ? 'orangeText'
                : ''
            }
          >
            {balancePrefix}
            {formatCents(totalBalance)}
          </b>
        </div>

        <div>
          you owe
          <b
            id="youowe"
            className={
              youOwe > 0 ? 'orangeText' : ''
            }
          >
            {formatCents(youOwe)}
          </b>
        </div>

        <div>
          you are owed
          <b
            id="owed"
            className={
              youAreOwed > 0 ? 'green' : ''
            }
          >
            {formatCents(youAreOwed)}
          </b>
        </div>
      </div>

      <section id="expenseList" aria-label="Expenses">
        {expenses.length === 0 ? (
          <div className="empty">
            <div
              className="empty-icon"
              aria-hidden="true"
            >
              ▧
            </div>
            <h3>No expenses yet</h3>
            <p>
              Add your first shared expense to see it here.
            </p>
          </div>
        ) : (
          groupByMonth(expenses).map((month) => (
            <div
              key={month.label}
              className="month-section"
            >
              <h2 className="month">
                {month.label}
              </h2>

              <ul
                className="expense-list"
                aria-label={month.label}
              >
                {month.expenses.map((expense) => (
                  <ExpenseRow
                    key={expense.id}
                    expense={expense}
                    currentUser={currentUser}
                    onClick={onExpenseClick}
                  />
                ))}
              </ul>
            </div>
          ))
        )}
      </section>

      {settlements && <SettlementHistory settlements={settlements} />}
    </main>
  );
}
