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
