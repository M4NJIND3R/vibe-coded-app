# StreakBoard Build Log

## Prompt 0

**Prompt (verbatim):**

```text
I'm building a habit tracker called StreakBoard. Stack: Python, Streamlit, SQLite, Plotly.

First, set up the project:
1. Create .gitignore (Python, .env, __pycache__, *.db, venv), .env.example, requirements.txt, and a placeholder README.md.
2. Create PROMPT.md, a running log of how this app is built. For every prompt I give you, append an entry with: the prompt number, my prompt copied verbatim, a short summary of what you did, the files created or changed, and any problems or limitations. Start by logging this prompt as Prompt 0.
3. From now on, update PROMPT.md at the end of every response, without me having to ask.
```

**Summary:** Set up the initial StreakBoard workspace files, created this prompt log, and verified that each requested file exists with the expected content.

**Files created or changed:**
- `.gitignore`
- `.env.example`
- `requirements.txt`
- `README.md`
- `PROMPT.md`

**Problems or limitations:** None.

## Prompt 1

**Prompt (verbatim):**

```text
Build the first working version of StreakBoard. Users can add a habit (name, optional description), see a list of habits, and mark each as done for today. Store data in SQLite. Put database code in db.py and the UI in app.py. Tables: habits and check_ins (habit_id, date). make sure to create a virtual python environement using venv and use that, not global. Update PROMPT.md.
```

**Summary:** Added SQLite database helpers and the Streamlit habit UI, updated setup instructions, created the `venv` environment, installed dependencies, validated add/check-in behavior and Python syntax, and verified the running app's health endpoint.

**Files created or changed:**
- `db.py`
- `app.py`
- `README.md`
- `PROMPT.md`

**Problems or limitations:** The first server verification attempt failed because a cleanup command used invalid PowerShell `SilentlyStop` syntax; it was corrected, and the Streamlit health endpoint returned `200` with `ok`. The app is currently running locally on port 8501.

## Prompt 2

**Prompt (verbatim):**

```text
reorganize files in folders to make strcuture clean and modular
```

**Summary:** Reorganized the application into a thin root Streamlit entry point, a `src/streakboard` Python package for UI and database code, and a `data` folder for SQLite storage. Updated setup documentation and verified that the reorganized app compiles and is healthy.

**Files created or changed:**
- `app.py`
- `src/streakboard/__init__.py`
- `src/streakboard/app.py`
- `src/streakboard/db.py`
- `db.py` - removed from root
- `README.md`
- `PROMPT.md`
- `streakboard.db` - moved to `data/streakboard.db`

**Problems or limitations:** None. The reorganized app returned `200` with `ok` from the Streamlit health endpoint.

## Prompt 3

**Prompt (verbatim):**

```text
Add a stats.py module with functions to calculate the current streak and longest streak for a habit from its check-in dates. Show both streaks next to each habit in the UI. Keep the logic separate from Streamlit code. Update PROMPT.md.
```

**Summary:** Added a pure streak statistics module, a database function to retrieve check-in dates, and UI display of current and longest streaks beside each habit.

**Files created or changed:**
- `src/streakboard/stats.py`
- `src/streakboard/db.py`
- `src/streakboard/app.py`
- `README.md`
- `PROMPT.md`

**Problems or limitations:** None. Focused streak tests passed, source compilation passed, and the Streamlit health endpoint returned `200` with `ok`.

## Prompt 4

**Prompt (verbatim):**

```text
Write pytest unit tests in tests/test_stats.py for the streak functions. Cover: no check-ins, one check-in, consecutive days, a gap in the middle, check-ins crossing a month and year boundary, duplicate dates, and a streak where today isn't checked yet but yesterday was. Run the tests and report failures. Update PROMPT.md.
```

**Summary:** Added pytest unit coverage for all requested streak scenarios and updated dependencies with pytest.

**Files created or changed:**
- `tests/test_stats.py`
- `requirements.txt`
- `PROMPT.md`

**Problems or limitations:** None. Pytest was installed inside `venv` and all 11 tests passed.

## Prompt 5

**Prompt (verbatim):**

```text
Create charts.py with Plotly chart functions and add a "Dashboard" tab in app.py with: (1) a weekly completion bar chart for the last 8 weeks, (2) a calendar-style heatmap of check-ins for the last 90 days, and (3) a completion rate per habit chart. Add a habit selector to filter the charts. Update PROMPT.md.
```

**Summary:** Added Plotly chart functions for eight-week check-in totals, a 90-day calendar heatmap, and 90-day completion rates. Added My Habits and Dashboard tabs and a habit selector that filters the dashboard charts.

**Files created or changed:**
- `src/streakboard/charts.py`
- `src/streakboard/app.py`
- `README.md`
- `PROMPT.md`

**Problems or limitations:** None. Chart smoke checks passed, all 11 pytest tests passed, source compilation passed, and the Streamlit health endpoint returned `200` with `ok`.

## Prompt 6

**Prompt (verbatim):**

```text
Improve the interface: use a clean sidebar for adding habits, tabs for "Today", "Dashboard", and "Manage", st.metric cards for summary stats (total habits, today's completions, best streak), consistent colors, and friendly empty-state messages when there is no data. Update PROMPT.md.
```

**Summary:** Redesigned the interface with a sidebar add-habit form, Today/Dashboard/Manage tabs, summary metric cards, consistent blue-green styling, friendly empty states, and habit deletion in Manage.

**Files created or changed:**
- `src/streakboard/app.py`
- `src/streakboard/db.py`
- `PROMPT.md`

**Problems or limitations:** None. Source compilation passed, all 11 pytest tests passed, and the improved app returned `200` with `ok` from the Streamlit health endpoint.

## Prompt 7

**Prompt (verbatim):**

```text
Add habit categories (e.g., Health, Study, Work, Personal) stored in the database. Let users assign a category when creating a habit, filter the Today view and Dashboard by category, and add a category breakdown chart. Handle the database migration safely so existing data isn't lost. Update PROMPT.md.
```

**Summary:** Added Health, Study, Work, and Personal categories to habit creation and storage, category filters for Today and Dashboard, a category breakdown chart, and an SQLite migration that adds the category column without recreating or deleting existing data.

**Files created or changed:**
- `src/streakboard/db.py`
- `src/streakboard/app.py`
- `src/streakboard/charts.py`
- `tests/test_db_categories.py`
- `PROMPT.md`

**Problems or limitations:** None. An initial ad hoc migration shell check had quoting problems, so migration behavior was added as a focused pytest test. The category migration and streak test suite passed with 13 tests, and the app health endpoint returned `200` with `ok`.

## Prompt 8

**Prompt (verbatim):**

```text
Add a Manage tab where users can edit a habit's name, description, and category, delete a habit with a confirmation step (also deleting its check-ins), and undo today's check-in. Update PROMPT.md.
```

**Summary:** Added editable Manage forms for habit name, description, and category; confirmation-safe deletion that relies on the existing SQLite cascade; and an Undo today action for completed habits.

**Files created or changed:**
- `src/streakboard/db.py`
- `src/streakboard/app.py`
- `tests/test_db_mutations.py`
- `PROMPT.md`

**Problems or limitations:** None. Source compilation passed, all 17 tests passed, deletion-cascade behavior was covered, and the app health endpoint returned `200` with `ok`.

## Prompt 9

**Prompt (verbatim):**

```text
Add a "Load sample data" button that generates 5 sample habits with 60 days of realistic, randomized check-ins (don't overwrite existing data without confirmation), and a "Download CSV" button that exports all check-ins. Update PROMPT.md.
```

**Summary:** Added transactional sample-data loading for five realistic habits and randomized 60-day check-ins, with an explicit replacement confirmation when existing data exists. Added CSV export of all check-ins and disabled export when no check-ins exist.

**Files created or changed:**
- `src/streakboard/db.py`
- `src/streakboard/app.py`
- `tests/test_db_mutations.py`
- `PROMPT.md`

**Problems or limitations:** None. Source compilation passed, all 19 tests passed, and the app health endpoint returned `200` with `ok`.

## Prompt 10

**Prompt (verbatim):**

```text
Review the whole codebase for bugs and edge cases: duplicate check-ins on the same day, app state after deleting a habit, empty database, very long habit names, date handling around midnight, and Streamlit rerun issues. List the problems you find first, then fix them one by one. Update PROMPT.md with each bug and fix.
```

**Summary:** Reviewed database, UI, chart, stats, and tests; identified and fixed duplicate check-ins, stale deletion state, empty-data handling, overly long text, midnight date drift, malformed dates, duplicate-habit-name selectors, missing-habit marks, and unsafe sample replacement.

**Problems found and fixes:**
1. **Duplicate check-ins:** Composite primary key already prevented duplicates. Added a database existence check and duplicate-safe tests for `INSERT OR IGNORE`.
2. **Delete app state:** Deletion cascaded check-ins, but selector/widget keys could remain stale after rerun. Added cleanup for stale session keys after confirmed deletion.
3. **Empty database:** Tabs handled no habits, but dashboard selector and export assumptions could remain misleading. Preserved friendly empty states and disabled CSV export for no check-ins.
4. **Very long habit names/descriptions:** Added 100-character name and 1000-character description limits in database and Streamlit inputs.
5. **Midnight date handling:** Captured one `app_today = date.today()` value per run and reused it for metrics, mark, undo, charts, and dashboard windows.
6. **Malformed dates:** Stats and chart functions now ignore invalid date strings rather than crashing.
7. **Rerun issues:** Centralized mutation reruns and stale-key cleanup; dashboard habit selection now uses stable habit IDs and category-filtered labels.
8. **Missing habit mark:** `mark_habit_done` now verifies that a habit exists before inserting a check-in.
9. **Unsafe sample replacement:** `load_sample_data` refuses to replace existing records unless `replace_existing=True`; the UI confirms first.
10. **CSV/stale state:** Export uses current database rows and remains disabled until at least one check-in exists.

**Files created or changed:**
- `src/streakboard/db.py`
- `src/streakboard/app.py`
- `src/streakboard/stats.py`
- `src/streakboard/charts.py`
- `tests/test_stats.py`
- `tests/test_db_mutations.py`
- `PROMPT.md`

**Problems or limitations:** None. Source compilation passed, all 23 tests passed, and the reviewed app returned `200` with `ok` on port `8507`.

## Prompt 11

**Prompt (verbatim):**

```text
Review the whole codebase for bugs and edge cases again to re-verify
```

**Summary:** Performed a second full codebase review and narrowed two issues found in the deletion and malformed-date paths.

**Problems found and fixes:**
1. **Malformed legacy check-in dates:** Added database-level filtering in `get_check_in_dates` so invalid or impossible ISO dates are excluded instead of reaching stats or charts.
2. **Over-broad deletion cleanup:** Replaced substring-based session-state cleanup with an exact widget-key cleanup list for the deleted habit.

**Files created or changed:**
- `src/streakboard/db.py`
- `src/streakboard/app.py`
- `tests/test_db_mutations.py`
- `PROMPT.md`

**Problems or limitations:** The earlier preview process was no longer running; it was restarted and verified on port `8508`. Source compilation passed, all 24 tests passed, and the health endpoint returned `200` with `ok`.
