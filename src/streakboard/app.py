from datetime import date, timedelta

import streamlit as st

from .charts import (
    calendar_heatmap,
    completion_rate_chart,
    weekly_completion_chart,
)
from .db import (
    add_habit,
    get_habits,
    get_check_in_dates,
    init_db,
    is_habit_done_today,
    mark_habit_done,
)
from .stats import calculate_current_streak, calculate_longest_streak


def run() -> None:
    st.set_page_config(page_title="StreakBoard", page_icon=":chart_with_upwards_trend:")

    init_db()

    st.title("StreakBoard")
    st.caption("Add habits and check in once a day.")

    habits = get_habits()

    habits_tab, dashboard_tab = st.tabs(["My Habits", "Dashboard"])

    with habits_tab:
        with st.form("add-habit", clear_on_submit=True):
            name = st.text_input("Habit name")
            description = st.text_area("Description (optional)")
            submitted = st.form_submit_button("Add habit", type="primary")

            if submitted:
                try:
                    add_habit(name, description)
                    st.success(f"Added habit: {name.strip()}")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))

        st.divider()
        st.subheader("My habits")

        if not habits:
            st.info("No habits yet. Add one above to get started.")
        else:
            for habit in habits:
                with st.container(border=True):
                    st.markdown(f"**{habit['name']}**")
                    if habit["description"]:
                        st.write(habit["description"])

                    check_in_dates = get_check_in_dates(habit["id"])
                    current_streak = calculate_current_streak(check_in_dates)
                    longest_streak = calculate_longest_streak(check_in_dates)
                    st.markdown(
                        f"**Current streak:** {current_streak} day(s)  |  "
                        f"**Longest streak:** {longest_streak} day(s)"
                    )

                    done_today = is_habit_done_today(habit["id"])
                    if done_today:
                        st.success("Done today")
                    else:
                        if st.button(
                            "Mark done",
                            key=f"mark_done_{habit['id']}",
                            type="primary",
                        ):
                            mark_habit_done(habit["id"])
                            st.rerun()

    with dashboard_tab:
        if not habits:
            st.info("Add a habit to view dashboard charts.")
        else:
            habit_options = ["All habits"] + [habit["name"] for habit in habits]
            selected_name = st.selectbox("Habit", habit_options)

            if selected_name == "All habits":
                selected_habits = list(habits)
            else:
                selected_habits = [
                    habit for habit in habits if habit["name"] == selected_name
                ]

            selected_dates = []
            completion_rates = {}
            for habit in selected_habits:
                habit_dates = get_check_in_dates(habit["id"])
                selected_dates.extend(habit_dates)
                recent_dates = {
                    date.fromisoformat(check_in_date)
                    for check_in_date in habit_dates
                    if date.today() - timedelta(days=89)
                    <= date.fromisoformat(check_in_date)
                    <= date.today()
                }
                completion_rates[habit["name"]] = len(recent_dates) / 90 * 100

            st.plotly_chart(
                weekly_completion_chart(selected_dates),
                use_container_width=True,
            )
            st.plotly_chart(
                calendar_heatmap(selected_dates),
                use_container_width=True,
            )
            st.plotly_chart(
                completion_rate_chart(completion_rates),
                use_container_width=True,
            )
