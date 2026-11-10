import { formatWhen } from '../dates';

// In-app balance reminders sent to the signed-in user (#46).
export default function RemindersInbox({ notifications = [], onMarkRead }) {
  return (
    <section className="reminders-inbox" aria-label="Reminders">
      <h3>Reminders</h3>
      {notifications.length === 0 ? (
        <p className="hint">No reminders</p>
      ) : (
        <ul>
          {notifications.map((note) => (
            <li key={note.id} className={note.readAt ? 'read' : 'unread'}>
              <p>{note.message}</p>
              <small>
                From {note.from} ·{' '}
                <time dateTime={note.createdAt}>{formatWhen(note.createdAt)}</time>
              </small>
              {note.readAt ? (
                <small className="hint"> · Read</small>
              ) : (
                <button type="button" onClick={() => onMarkRead(note.id)}>
                  Mark as read
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
