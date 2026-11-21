
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "research_history.db"


def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS research (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                report TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_research(topic, report):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO research (topic, report, created_at)
            VALUES (?, ?, ?)
            """,
            (topic, report, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )


def get_history():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            """
            SELECT id, topic, created_at
            FROM research
            ORDER BY id DESC
            """
        ).fetchall()


def get_report(research_id):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(
            "SELECT report FROM research WHERE id = ?",
            (research_id,)
        ).fetchone()

    return result[0] if result else None


def delete_research(research_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM research WHERE id = ?",
            (research_id,)
        )

