# StreakBoard

A habit tracking application built with Python, Streamlit, SQLite, and Plotly.

## Status

The first working habit tracker is available.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The SQLite database is created automatically when the app starts. Set
`DATABASE_PATH` in `.env` to use a custom database location.
