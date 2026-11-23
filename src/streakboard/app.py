import streamlit as st

from .db import (
    add_habit,
    get_habits,
    init_db,
    is_habit_done_today,
    mark_habit_done,
)


def run() -> None:
    st.set_page_config(page_title="StreakBoard", page_icon=":chart_with_upwards_trend:")

    init_db()

    st.title("StreakBoard")
    st.caption("Add habits and check in once a day.")

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

    habits = get_habits()

    if not habits:
        st.info("No habits yet. Add one above to get started.")
    else:
        for habit in habits:
            with st.container(border=True):
                st.markdown(f"**{habit['name']}**")
                if habit["description"]:
                    st.write(habit["description"])

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
