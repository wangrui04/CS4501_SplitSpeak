"""The shared SQLite connection must survive concurrent requests.

Found in the first #46 E2E run: the group page now loads four things
at once, the server's thread pool used the one connection from several
threads, and SQLite raised "bad parameter or other API misuse".
"""

from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from backend.database import create_database, seed_database
from backend.main import create_app
from backend.repository import save_expense


SECRET = "concurrency-test-secret-at-least-32-characters"


def test_concurrent_reads_and_writes_all_succeed():
    db = create_database()
    seed_database(db)
    app = create_app(db, session_secret=SECRET)

    with TestClient(app) as client:
        assert client.post("/api/session", json={"name": "Sarah"}).status_code == 200
        cookies = dict(client.cookies)

        def read(path):
            # One client per call: TestClient is not thread-safe itself.
            with TestClient(app, cookies=cookies) as worker:
                return worker.get(path).status_code

        def write(index):
            save_expense(db, {
                "groupId": 1,
                "description": f"Snack {index}",
                "payer": "Sarah",
                "totalCents": 300,
                "shares": [
                    {"name": "Sarah", "cents": 100},
                    {"name": "Kayla", "cents": 100},
                    {"name": "Rui", "cents": 100},
                ],
                "source": "manual",
                "createdBy": "Sarah",
            })
            return 200

        paths = [
            "/api/groups/1",
            "/api/groups/1/expenses",
            "/api/groups/1/settlements",
            "/api/notifications",
        ]

        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = [
                pool.submit(read, paths[i % len(paths)]) for i in range(200)
            ] + [pool.submit(write, i) for i in range(40)]
            statuses = [future.result() for future in futures]

    assert statuses == [200] * len(statuses)
    expenses = db.execute("SELECT COUNT(*) AS n FROM expenses").fetchone()["n"]
    assert expenses == 40
