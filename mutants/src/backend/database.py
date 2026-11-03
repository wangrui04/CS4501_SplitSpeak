
import sqlite3


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_create_database__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_create_database__mutmut)
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

    return db


def x_create_database__mutmut_orig(path=":memory:"):
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

    return db


def x_create_database__mutmut_1(path="XX:memory:XX"):
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

    return db


def x_create_database__mutmut_2(path=":MEMORY:"):
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

    return db


def x_create_database__mutmut_3(path=":memory:"):
    db = None
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

    return db


def x_create_database__mutmut_4(path=":memory:"):
    db = sqlite3.connect(
        None,
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

    return db


def x_create_database__mutmut_5(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=None,
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

    return db


def x_create_database__mutmut_6(path=":memory:"):
    db = sqlite3.connect(
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

    return db


def x_create_database__mutmut_7(path=":memory:"):
    db = sqlite3.connect(
        path,
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

    return db


def x_create_database__mutmut_8(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=True,
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

    return db


def x_create_database__mutmut_9(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=False,
    )
    db.row_factory = None
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

    return db


def x_create_database__mutmut_10(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=False,
    )
    db.row_factory = sqlite3.Row
    db.execute(None)

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

    return db


def x_create_database__mutmut_11(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=False,
    )
    db.row_factory = sqlite3.Row
    db.execute("XXPRAGMA foreign_keys=ONXX")

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

    return db


def x_create_database__mutmut_12(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=False,
    )
    db.row_factory = sqlite3.Row
    db.execute("pragma foreign_keys=on")

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

    return db


def x_create_database__mutmut_13(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=False,
    )
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA FOREIGN_KEYS=ON")

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

    return db


def x_create_database__mutmut_14(path=":memory:"):
    db = sqlite3.connect(
        path,
        check_same_thread=False,
    )
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")

    db.executescript(None)

    return db

mutants_x_create_database__mutmut['_mutmut_orig'] = x_create_database__mutmut_orig # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_1'] = x_create_database__mutmut_1 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_2'] = x_create_database__mutmut_2 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_3'] = x_create_database__mutmut_3 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_4'] = x_create_database__mutmut_4 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_5'] = x_create_database__mutmut_5 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_6'] = x_create_database__mutmut_6 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_7'] = x_create_database__mutmut_7 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_8'] = x_create_database__mutmut_8 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_9'] = x_create_database__mutmut_9 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_10'] = x_create_database__mutmut_10 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_11'] = x_create_database__mutmut_11 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_12'] = x_create_database__mutmut_12 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_13'] = x_create_database__mutmut_13 # type: ignore # mutmut generated
mutants_x_create_database__mutmut['x_create_database__mutmut_14'] = x_create_database__mutmut_14 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_seed_database__mutmut)
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


def x_seed_database__mutmut_orig(db):
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


def x_seed_database__mutmut_1(db):
    groups = None

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


def x_seed_database__mutmut_2(db):
    groups = [
        (
            "XXApartment 4BXX",
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


def x_seed_database__mutmut_3(db):
    groups = [
        (
            "apartment 4b",
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


def x_seed_database__mutmut_4(db):
    groups = [
        (
            "APARTMENT 4B",
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


def x_seed_database__mutmut_5(db):
    groups = [
        (
            "Apartment 4B",
            ["XXSarahXX", "Kayla", "Rui"],
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


def x_seed_database__mutmut_6(db):
    groups = [
        (
            "Apartment 4B",
            ["sarah", "Kayla", "Rui"],
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


def x_seed_database__mutmut_7(db):
    groups = [
        (
            "Apartment 4B",
            ["SARAH", "Kayla", "Rui"],
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


def x_seed_database__mutmut_8(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "XXKaylaXX", "Rui"],
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


def x_seed_database__mutmut_9(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "kayla", "Rui"],
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


def x_seed_database__mutmut_10(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "KAYLA", "Rui"],
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


def x_seed_database__mutmut_11(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "XXRuiXX"],
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


def x_seed_database__mutmut_12(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "rui"],
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


def x_seed_database__mutmut_13(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "RUI"],
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


def x_seed_database__mutmut_14(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "XXWeekend tripXX",
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


def x_seed_database__mutmut_15(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "weekend trip",
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


def x_seed_database__mutmut_16(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "WEEKEND TRIP",
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


def x_seed_database__mutmut_17(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["XXSarahXX", "Kayla", "Rui", "Aly", "Ben"],
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


def x_seed_database__mutmut_18(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["sarah", "Kayla", "Rui", "Aly", "Ben"],
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


def x_seed_database__mutmut_19(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["SARAH", "Kayla", "Rui", "Aly", "Ben"],
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


def x_seed_database__mutmut_20(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "XXKaylaXX", "Rui", "Aly", "Ben"],
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


def x_seed_database__mutmut_21(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "kayla", "Rui", "Aly", "Ben"],
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


def x_seed_database__mutmut_22(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "KAYLA", "Rui", "Aly", "Ben"],
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


def x_seed_database__mutmut_23(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "XXRuiXX", "Aly", "Ben"],
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


def x_seed_database__mutmut_24(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "rui", "Aly", "Ben"],
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


def x_seed_database__mutmut_25(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "RUI", "Aly", "Ben"],
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


def x_seed_database__mutmut_26(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "Rui", "XXAlyXX", "Ben"],
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


def x_seed_database__mutmut_27(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "Rui", "aly", "Ben"],
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


def x_seed_database__mutmut_28(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "Rui", "ALY", "Ben"],
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


def x_seed_database__mutmut_29(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "Rui", "Aly", "XXBenXX"],
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


def x_seed_database__mutmut_30(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "Rui", "Aly", "ben"],
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


def x_seed_database__mutmut_31(db):
    groups = [
        (
            "Apartment 4B",
            ["Sarah", "Kayla", "Rui"],
        ),
        (
            "Weekend trip",
            ["Sarah", "Kayla", "Rui", "Aly", "BEN"],
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


def x_seed_database__mutmut_32(db):
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
                None,
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


def x_seed_database__mutmut_33(db):
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
                None,
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


def x_seed_database__mutmut_34(db):
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


def x_seed_database__mutmut_35(db):
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


def x_seed_database__mutmut_36(db):
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
                "XXINSERT OR IGNORE INTO groups(name) VALUES(?)XX",
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


def x_seed_database__mutmut_37(db):
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
                "insert or ignore into groups(name) values(?)",
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


def x_seed_database__mutmut_38(db):
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
                "INSERT OR IGNORE INTO GROUPS(NAME) VALUES(?)",
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


def x_seed_database__mutmut_39(db):
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

            row = None

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


def x_seed_database__mutmut_40(db):
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
                None,
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


def x_seed_database__mutmut_41(db):
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
                None,
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


def x_seed_database__mutmut_42(db):
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


def x_seed_database__mutmut_43(db):
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


def x_seed_database__mutmut_44(db):
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
                "XXSELECT id FROM groups WHERE name=?XX",
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


def x_seed_database__mutmut_45(db):
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
                "select id from groups where name=?",
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


def x_seed_database__mutmut_46(db):
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
                "SELECT ID FROM GROUPS WHERE NAME=?",
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


def x_seed_database__mutmut_47(db):
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

            group_id = None

            for position, name in enumerate(members):
                db.execute(
                    """
                    INSERT OR IGNORE INTO group_members
                    (group_id, name, position)
                    VALUES (?, ?, ?)
                    """,
                    (group_id, name, position),
                )


def x_seed_database__mutmut_48(db):
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

            group_id = row["XXidXX"]

            for position, name in enumerate(members):
                db.execute(
                    """
                    INSERT OR IGNORE INTO group_members
                    (group_id, name, position)
                    VALUES (?, ?, ?)
                    """,
                    (group_id, name, position),
                )


def x_seed_database__mutmut_49(db):
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

            group_id = row["ID"]

            for position, name in enumerate(members):
                db.execute(
                    """
                    INSERT OR IGNORE INTO group_members
                    (group_id, name, position)
                    VALUES (?, ?, ?)
                    """,
                    (group_id, name, position),
                )


def x_seed_database__mutmut_50(db):
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

            for position, name in enumerate(None):
                db.execute(
                    """
                    INSERT OR IGNORE INTO group_members
                    (group_id, name, position)
                    VALUES (?, ?, ?)
                    """,
                    (group_id, name, position),
                )


def x_seed_database__mutmut_51(db):
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
                    None,
                    (group_id, name, position),
                )


def x_seed_database__mutmut_52(db):
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
                    None,
                )


def x_seed_database__mutmut_53(db):
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
                    (group_id, name, position),
                )


def x_seed_database__mutmut_54(db):
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
                    )

mutants_x_seed_database__mutmut['_mutmut_orig'] = x_seed_database__mutmut_orig # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_1'] = x_seed_database__mutmut_1 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_2'] = x_seed_database__mutmut_2 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_3'] = x_seed_database__mutmut_3 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_4'] = x_seed_database__mutmut_4 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_5'] = x_seed_database__mutmut_5 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_6'] = x_seed_database__mutmut_6 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_7'] = x_seed_database__mutmut_7 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_8'] = x_seed_database__mutmut_8 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_9'] = x_seed_database__mutmut_9 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_10'] = x_seed_database__mutmut_10 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_11'] = x_seed_database__mutmut_11 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_12'] = x_seed_database__mutmut_12 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_13'] = x_seed_database__mutmut_13 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_14'] = x_seed_database__mutmut_14 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_15'] = x_seed_database__mutmut_15 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_16'] = x_seed_database__mutmut_16 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_17'] = x_seed_database__mutmut_17 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_18'] = x_seed_database__mutmut_18 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_19'] = x_seed_database__mutmut_19 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_20'] = x_seed_database__mutmut_20 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_21'] = x_seed_database__mutmut_21 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_22'] = x_seed_database__mutmut_22 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_23'] = x_seed_database__mutmut_23 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_24'] = x_seed_database__mutmut_24 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_25'] = x_seed_database__mutmut_25 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_26'] = x_seed_database__mutmut_26 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_27'] = x_seed_database__mutmut_27 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_28'] = x_seed_database__mutmut_28 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_29'] = x_seed_database__mutmut_29 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_30'] = x_seed_database__mutmut_30 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_31'] = x_seed_database__mutmut_31 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_32'] = x_seed_database__mutmut_32 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_33'] = x_seed_database__mutmut_33 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_34'] = x_seed_database__mutmut_34 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_35'] = x_seed_database__mutmut_35 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_36'] = x_seed_database__mutmut_36 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_37'] = x_seed_database__mutmut_37 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_38'] = x_seed_database__mutmut_38 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_39'] = x_seed_database__mutmut_39 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_40'] = x_seed_database__mutmut_40 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_41'] = x_seed_database__mutmut_41 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_42'] = x_seed_database__mutmut_42 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_43'] = x_seed_database__mutmut_43 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_44'] = x_seed_database__mutmut_44 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_45'] = x_seed_database__mutmut_45 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_46'] = x_seed_database__mutmut_46 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_47'] = x_seed_database__mutmut_47 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_48'] = x_seed_database__mutmut_48 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_49'] = x_seed_database__mutmut_49 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_50'] = x_seed_database__mutmut_50 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_51'] = x_seed_database__mutmut_51 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_52'] = x_seed_database__mutmut_52 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_53'] = x_seed_database__mutmut_53 # type: ignore # mutmut generated
mutants_x_seed_database__mutmut['x_seed_database__mutmut_54'] = x_seed_database__mutmut_54 # type: ignore # mutmut generated
