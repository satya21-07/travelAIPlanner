from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[1] / "travelai_app.sqlite3"


def init_db() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS itineraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL,
                start_location TEXT,
                days INTEGER NOT NULL,
                travelers INTEGER NOT NULL,
                budget REAL NOT NULL,
                currency TEXT NOT NULL,
                travel_style TEXT NOT NULL,
                interests TEXT NOT NULL,
                summary TEXT NOT NULL,
                total_estimated_cost REAL NOT NULL,
                daily_plan TEXT NOT NULL,
                cost_breakdown TEXT NOT NULL,
                tips TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_itinerary(plan: dict[str, Any]) -> dict[str, Any]:
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO itineraries (
                destination, start_location, days, travelers, budget, currency,
                travel_style, interests, summary, total_estimated_cost,
                daily_plan, cost_breakdown, tips
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                plan["destination"],
                plan["start_location"],
                plan["days"],
                plan["travelers"],
                plan["budget"],
                plan["currency"],
                plan["travel_style"],
                json.dumps(plan["interests"]),
                plan["summary"],
                plan["total_estimated_cost"],
                json.dumps(plan["daily_plan"]),
                json.dumps(plan["cost_breakdown"]),
                json.dumps(plan["tips"]),
            ),
        )
        connection.commit()
        return get_itinerary(cursor.lastrowid) or plan


def list_itineraries() -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute("SELECT * FROM itineraries ORDER BY created_at DESC LIMIT 25").fetchall()
        return [_decode(row) for row in rows]


def get_itinerary(itinerary_id: int) -> dict[str, Any] | None:
    with _connect() as connection:
        row = connection.execute("SELECT * FROM itineraries WHERE id = ?", (itinerary_id,)).fetchone()
        return _decode(row) if row else None


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=OFF")
    connection.execute("PRAGMA synchronous=OFF")
    return connection


def _decode(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    item["interests"] = json.loads(item["interests"])
    item["daily_plan"] = json.loads(item["daily_plan"])
    item["cost_breakdown"] = json.loads(item["cost_breakdown"])
    item["tips"] = json.loads(item["tips"])
    return item
