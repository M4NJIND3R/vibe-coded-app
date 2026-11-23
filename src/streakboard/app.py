from datetime import date, timedelta

import csv
from io import StringIO

import streamlit as st

from .charts import (
    calendar_heatmap,
    category_breakdown_chart,
    completion_rate_chart,
    weekly_completion_chart,
)
from .db import (
    add_habit,
    CATEGORIES,
    delete_habit,
    get_habits,
    get_all_check_ins,
    get_check_in_dates,
    init_db,
    is_habit_done_today,
    mark_habit_done,
    load_sample_data,
    undo_today_check_in,
    update_habit,
)
from .stats import calculate_current_streak, calculate_longest_streak


def run() -> None:
    st.set_page_config(
        page_title="StreakBoard",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E2E8F0;
        }
        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }
        .stButton > button[kind="primary"] {
            background-color: #2563EB;
            border-color: #2563EB;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    init_db()

    habits = get_habits()
    app_today = date.today()

    streaks = [
        calculate_longest_streak(get_check_in_dates(habit["id"]))
        for habit in habits
    ]
    today_completions = sum(
        is_habit_done_today(habit["id"], app_today)
        for habit in habits
    )
    best_streak = max(streaks, default=0)

    with st.sidebar:
        st.title("StreakBoard")
        st.caption("Build consistency, one day at a time.")
        st.divider()
        st.subheader("Add a habit")
        with st.form("add-habit", clear_on_submit=True):
            name = st.text_input(
                "Habit name",
                placeholder="e.g. Morning walk",
                max_chars=100,
            )
            description = st.text_area(
                "Description",
                placeholder="Optional",
                max_chars=1000,
            )
            category = st.selectbox("Category", CATEGORIES)
            submitted = st.form_submit_button("Add habit", type="primary")

            if submitted:
                try:
                    add_habit(name, description, category)
                    st.success(f"Added “{name.strip()}”")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))

        st.divider()
        st.caption("Small steps become strong streaks.")

    st.title("Your progress")
    metric_columns = st.columns(3)
    metric_columns[0].metric("Total habits", len(habits))
    metric_columns[1].metric("Today's completions", today_completions)
    metric_columns[2].metric("Best streak", f"{best_streak} day(s)")

    today_tab, dashboard_tab, manage_tab = st.tabs(
        ["Today", "Dashboard", "Manage"]
    )

    with today_tab:
        if not habits:
            st.info("You have a fresh start—add your first habit in the sidebar.")
        else:
            today_category = st.selectbox(
                "Filter by category",
                ["All categories", *CATEGORIES],
                key="today_category",
            )
            today_habits = [
                habit
                for habit in habits
                if today_category == "All categories"
                or habit["category"] == today_category
            ]
            if not today_habits:
                st.info("No habits match this category. Try another category.")

            for habit in today_habits:
                with st.container(border=True):
                    st.markdown(f"**{habit['name']}**")
                    st.caption(habit["category"])
                    if habit["description"]:
                        st.write(habit["description"])

                    check_in_dates = get_check_in_dates(habit["id"])
                    current_streak = calculate_current_streak(check_in_dates)
                    longest_streak = calculate_longest_streak(check_in_dates)
                    col_left, col_right = st.columns([3, 1])
                    col_left.markdown(
                        f"🔥 **{current_streak} day current streak**  "
                        f"· Personal best: {longest_streak} days"
                    )

                    done_today = is_habit_done_today(habit["id"], app_today)
                    if done_today:
                        col_right.success("Done today")
                        if col_right.button(
                            "Undo today",
                            key=f"undo_today_{habit['id']}",
                        ):
                            undo_today_check_in(habit["id"], app_today)
                            st.rerun()
                    else:
                        if col_right.button(
                            "Mark done",
                            key=f"mark_done_{habit['id']}",
                            type="primary",
                        ):
                            mark_habit_done(habit["id"], app_today)
                            st.rerun()

    with dashboard_tab:
        if not habits:
            st.info("No chart data yet. Complete a habit to begin your dashboard.")
        else:
            dashboard_category = st.selectbox(
                "Filter by category",
                ["All categories", *CATEGORIES],
                key="dashboard_category",
            )
            category_habits = [
                habit
                for habit in habits
                if dashboard_category == "All categories"
                or habit["category"] == dashboard_category
            ]
            habit_options = {"All habits": None}
            habit_options.update(
                {
                    f"{habit['name']} ({habit['id']})": habit["id"]
                    for habit in category_habits
                }
            )
            selected_label = st.selectbox("Habit", list(habit_options))
            selected_habit_id = habit_options[selected_label]

            if selected_habit_id is None:
                selected_habits = list(category_habits)
            else:
                selected_habits = [
                    habit for habit in category_habits
                    if habit["id"] == selected_habit_id
                ]

            selected_dates = []
            completion_rates = {}
            for habit in selected_habits:
                habit_dates = get_check_in_dates(habit["id"])
                selected_dates.extend(habit_dates)
                recent_dates = {
                    date.fromisoformat(check_in_date)
                    for check_in_date in habit_dates
                    if app_today - timedelta(days=89)
                    <= date.fromisoformat(check_in_date)
                    <= app_today
                }
                completion_rates[habit["name"]] = len(recent_dates) / 90 * 100

            st.plotly_chart(
                weekly_completion_chart(selected_dates, app_today),
                use_container_width=True,
            )
            st.plotly_chart(
                calendar_heatmap(selected_dates, app_today),
                use_container_width=True,
            )
            st.plotly_chart(
                completion_rate_chart(completion_rates),
                use_container_width=True,
            )
            category_counts = {
                category: sum(
                    habit["category"] == category
                    for habit in habits
                )
                for category in CATEGORIES
            }
            st.plotly_chart(
                category_breakdown_chart(category_counts),
                use_container_width=True,
            )

    with manage_tab:
        st.subheader("Manage habits")
        data_col, export_col = st.columns(2)

        with data_col:
            confirm_sample_key = "confirm_replace_sample_data"
            if st.session_state.get(confirm_sample_key):
                st.warning(
                    "Load sample habits and replace all existing habits and check-ins?"
                )
                yes_col, no_col = st.columns(2)
                if yes_col.button(
                    "Yes, replace data",
                    key="confirm_sample_yes",
                    type="primary",
                ):
                    load_sample_data(replace_existing=True)
                    st.session_state.pop(confirm_sample_key, None)
                    st.success("Sample data loaded.")
                    st.rerun()
                if no_col.button("Cancel", key="confirm_sample_cancel"):
                    st.session_state.pop(confirm_sample_key, None)
                    st.rerun()
            else:
                if st.button("Load sample data", type="secondary"):
                    if habits:
                        st.session_state[confirm_sample_key] = True
                        st.rerun()
                    else:
                        load_sample_data()
                        st.success("Loaded 5 sample habits with 60 days of check-ins.")
                        st.rerun()

        with export_col:
            check_ins = get_all_check_ins()
            csv_output = StringIO()
            csv_writer = csv.writer(csv_output)
            csv_writer.writerow(["habit_id", "habit_name", "category", "date"])
            for check_in in check_ins:
                csv_writer.writerow(
                    [
                        check_in["habit_id"],
                        check_in["habit_name"],
                        check_in["category"],
                        check_in["date"],
                    ]
                )
            st.download_button(
                "Download CSV",
                data=csv_output.getvalue(),
                file_name="streakboard_check_ins.csv",
                mime="text/csv",
                use_container_width=True,
                disabled=not check_ins,
                key="download_check_ins",
            )

        st.divider()
        if not habits:
            st.info("Nothing to manage yet. Add a habit from the sidebar.")
        else:
            for habit in habits:
                with st.container(border=True):
                    with st.form(
                        f"edit_habit_{habit['id']}",
                        clear_on_submit=False,
                    ):
                        edited_name = st.text_input(
                            "Habit name",
                            value=habit["name"],
                            key=f"edit_name_{habit['id']}",
                            max_chars=100,
                        )
                        edited_description = st.text_area(
                            "Description",
                            value=habit["description"] or "",
                            key=f"edit_description_{habit['id']}",
                            max_chars=1000,
                        )
                        current_category_index = CATEGORIES.index(
                            habit["category"]
                            if habit["category"] in CATEGORIES
                            else "Personal"
                        )
                        if len(habit["name"]) > 100:
                            st.caption("Stored habit name exceeds the display limit.")
                        edited_category = st.selectbox(
                            "Category",
                            CATEGORIES,
                            index=current_category_index,
                            key=f"edit_category_{habit['id']}",
                        )
                        if st.form_submit_button("Save changes", type="primary"):
                            try:
                                update_habit(
                                    habit["id"],
                                    edited_name,
                                    edited_description,
                                    edited_category,
                                )
                                st.success("Habit updated.")
                                st.rerun()
                            except ValueError as error:
                                st.error(str(error))

                    confirm_key = f"confirm_delete_{habit['id']}"
                    if st.session_state.get(confirm_key):
                        st.warning(
                            f"Delete “{habit['name']}” and all its check-ins?"
                        )
                        confirm_col, cancel_col = st.columns(2)
                        if confirm_col.button(
                            "Yes, delete",
                            key=f"confirm_yes_{habit['id']}",
                            type="primary",
                        ):
                            delete_habit(habit["id"])
                            st.session_state.pop(confirm_key, None)
                            exact_widget_keys = (
                                f"edit_name_{habit['id']}",
                                f"edit_description_{habit['id']}",
                                f"edit_category_{habit['id']}",
                                f"delete_habit_{habit['id']}",
                                f"confirm_yes_{habit['id']}",
                                f"confirm_cancel_{habit['id']}",
                                f"confirm_delete_{habit['id']}",
                                f"undo_today_{habit['id']}",
                                f"mark_done_{habit['id']}",
                                f"edit_habit_{habit['id']}",
                            )
                            for key in exact_widget_keys:
                                st.session_state.pop(key, None)
                            st.rerun()
                        if cancel_col.button(
                            "Cancel",
                            key=f"confirm_cancel_{habit['id']}",
                        ):
                            st.session_state.pop(confirm_key, None)
                            st.rerun()
                    else:
                        if st.button(
                            "Delete habit",
                            key=f"delete_habit_{habit['id']}",
                            type="secondary",
                        ):
                            st.session_state[confirm_key] = True
                            st.rerun()
