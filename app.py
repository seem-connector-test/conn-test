"""Intentionally vulnerable, synthetic scanner fixtures. Do not deploy."""

import sqlite3

from flask import Flask, request

app = Flask(__name__)


@app.get("/accounts")
def accounts():
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE accounts (name TEXT, team TEXT)")
        connection.executemany(
            "INSERT INTO accounts VALUES (?, ?)",
            [("demo-alice", "finance"), ("demo-bob", "engineering")],
        )
        team = request.args.get("team", "finance")
        # Deliberate SQL injection fixture: preserve until testing remediation.
        rows = connection.execute(
            f"SELECT name, team FROM accounts WHERE team = '{team}'"
        ).fetchall()
        return {"accounts": [{"name": name, "team": team} for name, team in rows]}
    finally:
        connection.close()


@app.get("/greeting")
def greeting():
    name = request.args.get("name", "demo-user")
    # Deliberate reflected XSS fixture: preserve until testing remediation.
    return f"<h1>Hello, {name}</h1>"
