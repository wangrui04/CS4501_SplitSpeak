import { formatWhen } from '../dates';

// In-app balance reminders sent to the signed-in user (#46).
export default function RemindersInbox({
  notifications = [],
  onMarkRead,
  onClose,
}) {
  return (
    <section className="reminders-inbox" aria-label="Reminders">
      <div className="reminders-head">
        <h3>Reminders</h3>
        {onClose && (
          <button
            type="button"
            className="close"
            onClick={onClose}
            aria-label="Close reminders"
          >
            ×
          </button>
        )}
      </div>
      {notifications.length === 0 ? (
        <p className="hint reminders-empty">No reminders</p>
      ) : (
        <ul>
          {notifications.map((note) => (
            <li key={note.id} className={note.readAt ? 'read' : 'unread'}>
              <p>{note.message}</p>
              <div className="reminder-meta">
                <small>
                  From {note.from} ·{' '}
                  <time dateTime={note.createdAt}>{formatWhen(note.createdAt)}</time>
                </small>
                {note.readAt ? (
                  <small className="reminder-read">Read</small>
                ) : (
                  <button
                    type="button"
                    className="link-btn"
                    onClick={() => onMarkRead(note.id)}
                  >
                    Mark as read
                  </button>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
