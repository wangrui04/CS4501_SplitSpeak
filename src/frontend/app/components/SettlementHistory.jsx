import { formatCents } from '../money';
import { formatWhen } from '../dates';

// Recorded repayments for a group, newest first (#46).
export default function SettlementHistory({ settlements = [] }) {
  return (
    <section className="settlement-history" aria-label="Payments">
      <h3>Payments</h3>
      {settlements.length === 0 ? (
        <p className="hint">No payments recorded yet.</p>
      ) : (
        <ul>
          {settlements.map((entry) => (
            <li key={entry.id}>
              <span>
                <b>
                  {entry.from} paid {entry.to} {formatCents(entry.cents)}
                </b>
              </span>
              <small>
                Recorded by {entry.recordedBy} ·{' '}
                <time dateTime={entry.recordedAt}>
                  {formatWhen(entry.recordedAt)}
                </time>
              </small>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
