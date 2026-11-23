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
