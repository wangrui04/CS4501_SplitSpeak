
import sqlite3
import threading


class _Result:
    """A query's rows, fetched while the lock was held.

    Supports what the app uses from a cursor: fetchone, fetchall,
    iteration, lastrowid, and rowcount.
    """

    def __init__(self, cursor):
        self._rows = cursor.fetchall() if cursor.description else []
        self._next = 0
        self.lastrowid = cursor.lastrowid
        self.rowcount = cursor.rowcount

    def fetchone(self):
        if self._next >= len(self._rows):
            return None
        row = self._rows[self._next]
        self._next += 1
        return row

    def fetchall(self):
        rows = self._rows[self._next:]
        self._next = len(self._rows)
        return rows

    def __iter__(self):
        return iter(self.fetchall())


class LockedConnection:
    """One SQLite connection shared safely across request threads.

    FastAPI runs sync endpoints in a thread pool, and a plain sqlite3
    connection must not be used by two threads at once. Every query
    runs under a re-entrant lock, and `with db:` holds it for the
    whole transaction, so a read-check-write sequence stays atomic and
    lastrowid always belongs to the caller's own insert.
    """

    def __init__(self, connection):
        self._connection = connection
        self._lock = threading.RLock()

    def execute(self, sql, parameters=()):
        with self._lock:
            return _Result(self._connection.execute(sql, parameters))

    def executescript(self, script):
        with self._lock:
            self._connection.executescript(script)

    def commit(self):
        with self._lock:
            self._connection.commit()

    def rollback(self):
        with self._lock:
            self._connection.rollback()

    def close(self):
        with self._lock:
            self._connection.close()

    def __enter__(self):
        self._lock.acquire()
        try:
            self._connection.__enter__()
        except BaseException:
            self._lock.release()
            raise
        return self

    def __exit__(self, *exc_info):
        try:
            return self._connection.__exit__(*exc_info)
        finally:
            self._lock.release()

    def __getattr__(self, name):
        return getattr(self._connection, name)


def create_database(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=False,
    )
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")

    db.executescript("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS group_members (
            group_id INTEGER NOT NULL REFERENCES groups(id),
            name TEXT NOT NULL,
            position INTEGER NOT NULL,
            PRIMARY KEY(group_id, name)
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL REFERENCES groups(id),
            description TEXT NOT NULL,
            payer_name TEXT NOT NULL,
            total_cents INTEGER NOT NULL,
            source TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS expense_shares (
            expense_id INTEGER NOT NULL REFERENCES expenses(id),
            name TEXT NOT NULL,
            cents INTEGER NOT NULL,
            PRIMARY KEY(expense_id, name)
        );

        -- Net amount each person paid toward an expense. A refund the
        -- person received is subtracted, so a value can be negative.
        CREATE TABLE IF NOT EXISTS expense_payments (
            expense_id INTEGER NOT NULL REFERENCES expenses(id),
            name TEXT NOT NULL,
            cents INTEGER NOT NULL,
            PRIMARY KEY(expense_id, name)
        );

        -- A recorded repayment between two members. Stored apart from
        -- expenses; no money moves.
        CREATE TABLE IF NOT EXISTS settlements (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL REFERENCES groups(id),
            from_name TEXT NOT NULL,
            to_name TEXT NOT NULL,
            cents INTEGER NOT NULL CHECK (cents > 0),
            recorded_by TEXT NOT NULL,
            recorded_at TEXT NOT NULL
        );

        -- In-app balance reminders. cents is the amount owed when sent.
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL REFERENCES groups(id),
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            cents INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            read_at TEXT
        );

        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL REFERENCES groups(id),
            user_name TEXT NOT NULL,
            prompt_count INTEGER NOT NULL,
            status TEXT NOT NULL,
            final_preview_json TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS conversation_messages (
            id INTEGER PRIMARY KEY,
            conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)


    # Add columns needed for editing saved expenses.
    columns = {
        row["name"]
        for row in db.execute("PRAGMA table_info(expenses)")
    }

    if "line_items_json" not in columns:
        db.execute(
            "ALTER TABLE expenses ADD COLUMN line_items_json TEXT"
        )

    if "charges_json" not in columns:
        db.execute(
            "ALTER TABLE expenses ADD COLUMN charges_json TEXT"
        )

    if "version" not in columns:
        db.execute(
            "ALTER TABLE expenses "
            "ADD COLUMN version INTEGER NOT NULL DEFAULT 1"
        )

    db.commit()

    return LockedConnection(db)


def seed_database(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "Rui", "Aly", "Ben"],
        ),
    ]

    with db:
        for group_name, members in groups:
            db.execute(
                "INSERT OR IGNORE INTO groups(name) VALUES(?)",
                (group_name,),
            )

            row = db.execute(
                "SELECT id FROM groups WHERE name=?",
                (group_name,),
            ).fetchone()

            group_id = row["id"]

            for position, name in enumerate(members):
                db.execute(
                    """
                    INSERT OR IGNORE INTO group_members
                    (group_id, name, position)
                    VALUES (?, ?, ?)
                    """,
                    (group_id, name, position),
                )
