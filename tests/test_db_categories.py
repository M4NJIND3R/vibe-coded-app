import sqlite3

from src.streakboard import db


def test_category_migration_preserves_existing_habit(tmp_path, monkeypatch):
    database_path = tmp_path / "legacy.db"
    with sqlite3.connect(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            );
            CREATE TABLE check_ins (
                habit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                PRIMARY KEY (habit_id, date)
            );
            INSERT INTO habits (name, description)
            VALUES ('Legacy habit', 'Keep this data');
            """
        )

    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))
    db.init_db()

    habits = db.get_habits()
    assert len(habits) == 1
    assert habits[0]["name"] == "Legacy habit"
    assert habits[0]["description"] == "Keep this data"
    assert habits[0]["category"] == "Personal"


def test_category_is_stored_with_new_habit(tmp_path, monkeypatch):
    database_path = tmp_path / "categories.db"
    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))
    db.init_db()

    habit_id = db.add_habit("Read", "Read a chapter", "Study")
    habit = db.get_habits()[0]

    assert habit["id"] == habit_id
    assert habit["category"] == "Study"
