import os
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH", "data/streakboard.db")
CATEGORIES = ("Health", "Study", "Work", "Personal")
MAX_HABIT_NAME_LENGTH = 100
MAX_HABIT_DESCRIPTION_LENGTH = 1000


def get_connection() -> sqlite3.Connection:
    """Open a configured SQLite connection with foreign keys enabled."""
    database_path = Path(DATABASE_PATH)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    """Create tables and safely add the category column to older databases."""
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
    """Validate and add a habit, returning its database ID."""
    cleaned_name = name.strip()
    if not cleaned_name:
        raise ValueError("Habit name cannot be empty.")
    if len(cleaned_name) > MAX_HABIT_NAME_LENGTH:
        raise ValueError(f"Habit name must be {MAX_HABIT_NAME_LENGTH} characters or fewer.")

    cleaned_description = description.strip() if description else None
    if cleaned_description and len(cleaned_description) > MAX_HABIT_DESCRIPTION_LENGTH:
        raise ValueError(
            f"Description must be {MAX_HABIT_DESCRIPTION_LENGTH} characters or fewer."
        )
    cleaned_category = category if category in CATEGORIES else "Personal"
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO habits (name, description, category) VALUES (?, ?, ?)",
            (cleaned_name, cleaned_description, cleaned_category),
        )
        return int(cursor.lastrowid)


def get_habits() -> list[sqlite3.Row]:
    """Return all habits ordered by newest first."""
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT id, name, description, category
            FROM habits
            ORDER BY id DESC
            """
        ).fetchall()


def mark_habit_done(habit_id: int, check_in_date: Optional[date] = None) -> bool:
    """Record one check-in for a habit on the selected date."""
    today = (check_in_date or date.today()).isoformat()
    with get_connection() as connection:
        habit = connection.execute(
            "SELECT 1 FROM habits WHERE id = ?",
            (habit_id,),
        ).fetchone()
        if habit is None:
            return False
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO check_ins (habit_id, date)
            VALUES (?, ?)
            """,
            (habit_id, today),
        )
        return cursor.rowcount > 0


def is_habit_done_today(habit_id: int, check_in_date: Optional[date] = None) -> bool:
    """Return whether a habit has a check-in on the selected date."""
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
    """Return valid ISO check-in dates belonging to a habit."""
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
        valid_dates = []
        for row in rows:
            try:
                date.fromisoformat(row["date"])
                valid_dates.append(row["date"])
            except (TypeError, ValueError):
                continue
        return valid_dates


def delete_habit(habit_id: int) -> None:
    """Delete a habit and its check-ins through the foreign-key cascade."""
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM habits WHERE id = ?",
            (habit_id,),
        )


def update_habit(
    habit_id: int,
    name: str,
    description: Optional[str],
    category: str,
) -> None:
    """Update a habit's name, description, and category."""
    cleaned_name = name.strip()
    if not cleaned_name:
        raise ValueError("Habit name cannot be empty.")
    if len(cleaned_name) > MAX_HABIT_NAME_LENGTH:
        raise ValueError(f"Habit name must be {MAX_HABIT_NAME_LENGTH} characters or fewer.")

    cleaned_category = category if category in CATEGORIES else "Personal"
    cleaned_description = description.strip() if description else None
    if cleaned_description and len(cleaned_description) > MAX_HABIT_DESCRIPTION_LENGTH:
        raise ValueError(
            f"Description must be {MAX_HABIT_DESCRIPTION_LENGTH} characters or fewer."
        )
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE habits
            SET name = ?, description = ?, category = ?
            WHERE id = ?
            """,
            (cleaned_name, cleaned_description, cleaned_category, habit_id),
        )


def undo_today_check_in(habit_id: int, check_in_date: Optional[date] = None) -> bool:
    """Remove a habit's check-in for the selected date."""
    today = (check_in_date or date.today()).isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM check_ins WHERE habit_id = ? AND date = ?",
            (habit_id, today),
        )
        return cursor.rowcount > 0


SAMPLE_HABITS = (
    ("Morning Walk", "Walk outside for at least 20 minutes", "Health"),
    ("Study Session", "Complete a focused study session", "Study"),
    ("Deep Work", "Protect one block for focused work", "Work"),
    ("Read Before Bed", "Read a book before sleeping", "Personal"),
    ("Drink Water", "Drink enough water throughout the day", "Health"),
)


def load_sample_data(
    today: Optional[date] = None,
    replace_existing: bool = False,
    seed: Optional[int] = None,
) -> int:
    """Load deterministic randomized sample habits and 60-day check-ins."""
    reference_date = today or date.today()
    rng = random.Random(seed)

    with get_connection() as connection:
        existing_count = connection.execute(
            "SELECT COUNT(*) AS count FROM habits"
        ).fetchone()["count"]
        if existing_count and not replace_existing:
            raise ValueError(
                "Existing habits found. Set replace_existing=True only after user confirmation."
            )
        if replace_existing:
            connection.execute("DELETE FROM check_ins")
            connection.execute("DELETE FROM habits")

        created = 0
        for name, description, category in SAMPLE_HABITS:
            cursor = connection.execute(
                "INSERT INTO habits (name, description, category) VALUES (?, ?, ?)",
                (name, description, category),
            )
            habit_id = int(cursor.lastrowid)
            created += 1

            completion_probability = rng.uniform(0.55, 0.82)
            missed_run = 0
            for offset in range(60):
                check_in_date = reference_date - timedelta(days=59 - offset)
                probability = completion_probability
                if missed_run >= 3:
                    probability += 0.25
                if rng.random() < probability:
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO check_ins (habit_id, date)
                        VALUES (?, ?)
                        """,
                        (habit_id, check_in_date.isoformat()),
                    )
                    missed_run = 0
                else:
                    missed_run += 1
        return created


def get_all_check_ins() -> list[sqlite3.Row]:
    """Return every check-in joined with its habit details for export."""
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                h.id AS habit_id,
                h.name AS habit_name,
                h.category AS category,
                ci.date AS date
            FROM check_ins AS ci
            JOIN habits AS h ON h.id = ci.habit_id
            ORDER BY ci.date DESC, h.name ASC
            """
        ).fetchall()
