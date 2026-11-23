from datetime import date

from src.streakboard import db


def test_update_habit_changes_fields(tmp_path, monkeypatch):
    database_path = tmp_path / "update.db"
    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))
    db.init_db()

    habit_id = db.add_habit("Old name", "Old description", "Personal")
    db.update_habit(habit_id, "New name", "New description", "Work")

    habit = db.get_habits()[0]
    assert habit["name"] == "New name"
    assert habit["description"] == "New description"
    assert habit["category"] == "Work"


def test_update_habit_rejects_empty_name(tmp_path, monkeypatch):
    database_path = tmp_path / "update-empty.db"
    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))
    db.init_db()
    habit_id = db.add_habit("Valid name")

    try:
        db.update_habit(habit_id, "   ", "Description", "Health")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected an empty habit name to raise ValueError")

    assert db.get_habits()[0]["name"] == "Valid name"


def test_undo_today_check_in_removes_only_today(tmp_path, monkeypatch):
    database_path = tmp_path / "undo.db"
    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))
    db.init_db()
    habit_id = db.add_habit("Exercise")
    today = date(2026, 11, 23)
    yesterday = date(2026, 11, 22)
    db.mark_habit_done(habit_id, today)
    db.mark_habit_done(habit_id, yesterday)

    assert db.undo_today_check_in(habit_id, today)
    assert not db.is_habit_done_today(habit_id, today)
    assert db.is_habit_done_today(habit_id, yesterday)


def test_delete_habit_removes_check_ins(tmp_path, monkeypatch):
    database_path = tmp_path / "delete.db"
    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))
    db.init_db()
    habit_id = db.add_habit("Temporary")
    db.mark_habit_done(habit_id, date(2026, 11, 23))

    db.delete_habit(habit_id)

    assert db.get_habits() == []
    assert db.get_check_in_dates(habit_id) == []
