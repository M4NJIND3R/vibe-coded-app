import os
import sqlite3
from datetime import date
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH", "data/streakboard.db")
CATEGORIES = ("Health", "Study", "Work", "Personal")


def get_connection() -> sqlite3.Connection:
    database_path = Path(DATABASE_PATH)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT NOT NULL DEFAULT 'Personal'
            );

            CREATE TABLE IF NOT EXISTS check_ins (
                habit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                PRIMARY KEY (habit_id, date),
                FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
            );
            """
        )

        habit_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(habits)").fetchall()
        }
        if "category" not in habit_columns:
            connection.execute(
                "ALTER TABLE habits ADD COLUMN category TEXT NOT NULL DEFAULT 'Personal'"
            )
            connection.execute(
                "UPDATE habits SET category = 'Personal' WHERE category IS NULL OR TRIM(category) = ''"
            )


def add_habit(
    name: str,
    description: Optional[str] = None,
    category: str = "Personal",
) -> int:
    cleaned_name = name.strip()
    if not cleaned_name:
        raise ValueError("Habit name cannot be empty.")

    cleaned_description = description.strip() if description else None
    cleaned_category = category if category in CATEGORIES else "Personal"
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO habits (name, description, category) VALUES (?, ?, ?)",
            (cleaned_name, cleaned_description, cleaned_category),
        )
        return int(cursor.lastrowid)


def get_habits() -> list[sqlite3.Row]:
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT id, name, description, category
            FROM habits
            ORDER BY id DESC
            """
        ).fetchall()


def mark_habit_done(habit_id: int, check_in_date: Optional[date] = None) -> bool:
    today = (check_in_date or date.today()).isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO check_ins (habit_id, date)
            VALUES (?, ?)
            """,
            (habit_id, today),
        )
        return cursor.rowcount > 0


def is_habit_done_today(habit_id: int, check_in_date: Optional[date] = None) -> bool:
    today = (check_in_date or date.today()).isoformat()
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT 1
            FROM check_ins
            WHERE habit_id = ? AND date = ?
            """,
            (habit_id, today),
        ).fetchone()
        return row is not None


def get_check_in_dates(habit_id: int) -> list[str]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT date
            FROM check_ins
            WHERE habit_id = ?
            ORDER BY date ASC
            """,
            (habit_id,),
        ).fetchall()
        return [row["date"] for row in rows]


def delete_habit(habit_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM habits WHERE id = ?",
            (habit_id,),
        )
