import { formatCents } from '../money';

const BG_COLORS = ['#fce7ee', '#e8f3ff', '#f1eafc', '#e6f8f3', '#fff4e5'];

const STATUS_CLASS = {
  'owes you': 'positive',
  'you owe': 'negative',
  'settled up': 'settled',
};

// balances come from GET /api/groups/:id, relative to the signed-in user.
export default function RightSidebar({ balances = [] }) {
  return (
    <aside className="right" aria-label="Group balances">
      <h3>Group balances</h3>
      <div id="sideBalances">
        {balances.length === 0 ? (
          <p className="hint">No other members in this group.</p>
        ) : (
          balances.map((balance, index) => (
            <div key={balance.name} className="balanceentry">
              <span
                className="avatar"
                style={{ background: BG_COLORS[index % BG_COLORS.length] }}
                aria-hidden="true"
              >
                {balance.name.charAt(0)}
              </span>
              <span>
                {balance.name}
                <b className={STATUS_CLASS[balance.status] || 'settled'}>
                  {balance.status} {formatCents(balance.cents)}
                </b>
              </span>
            </div>
          ))
        )}
      </div>
      <div className="tip">
        All balances here are simulated. Expenses are saved only after you confirm them.
      </div>
    </aside>
  );
}
