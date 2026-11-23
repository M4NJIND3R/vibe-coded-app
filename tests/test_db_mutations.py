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


def test_load_sample_data_creates_five_habits_and_sixty_day_history(tmp_path, monkeypatch):
    database_path = tmp_path / "sample.db"
    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))
    db.init_db()

    created = db.load_sample_data(
        today=date(2026, 11, 23),
        replace_existing=False,
        seed=42,
    )

    habits = db.get_habits()
    assert created == 5
    assert len(habits) == 5
    all_check_ins = db.get_all_check_ins()
    assert all_check_ins
    for habit in habits:
        dates = db.get_check_in_dates(habit["id"])
        assert dates
        assert len(dates) <= 60
        assert min(dates) >= "2026-09-25"
        assert max(dates) <= "2026-11-23"


def test_load_sample_data_can_replace_existing_data(tmp_path, monkeypatch):
    database_path = tmp_path / "sample-replace.db"
    monkeypatch.setattr(db, "DATABASE_PATH", str(database_path))
    db.init_db()
    db.add_habit("Existing", "Should be removed")
    existing_id = db.get_habits()[0]["id"]
    db.mark_habit_done(existing_id, date(2026, 11, 23))

    db.load_sample_data(replace_existing=True, seed=7)

    habits = db.get_habits()
    assert len(habits) == 5
    assert all(habit["name"] != "Existing" for habit in habits)
    assert db.get_check_in_dates(existing_id) == []
