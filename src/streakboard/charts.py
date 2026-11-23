from datetime import date, timedelta
from typing import Iterable, Mapping

import plotly.graph_objects as go


def weekly_completion_chart(
    check_in_dates: Iterable[str],
    today: date | None = None,
) -> go.Figure:
    reference_date = today or date.today()
    completed = [
        date.fromisoformat(value)
        for value in check_in_dates
    ]

    current_week_start = reference_date - timedelta(days=reference_date.weekday())
    labels = []
    counts = []
    for week_offset in range(7, -1, -1):
        week_start = current_week_start - timedelta(weeks=week_offset)
        week_end = week_start + timedelta(days=6)
        count = sum(
            1
            for check_in_date in completed
            if week_start <= check_in_date <= week_end
        )
        labels.append(week_start.strftime("%b %d"))
        counts.append(count)

    figure = go.Figure(
        go.Bar(
            x=labels,
            y=counts,
            marker_color="#5B8DEF",
            text=counts,
            textposition="outside",
        )
    )
    figure.update_layout(
        title="Check-ins by week",
        xaxis_title="Week starting",
        yaxis_title="Completed check-ins",
        yaxis=dict(dtick=1),
        template="plotly_white",
        height=350,
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return figure


def calendar_heatmap(
    check_in_dates: Iterable[str],
    today: date | None = None,
) -> go.Figure:
    reference_date = today or date.today()
    completed = {
        date.fromisoformat(value)
        for value in check_in_dates
    }
    start_date = reference_date - timedelta(days=89)

    first_week_start = start_date - timedelta(days=start_date.weekday())
    week_starts = [
        first_week_start + timedelta(weeks=week)
        for week in range((reference_date - first_week_start).days // 7 + 1)
    ]

    z_values = []
    week_labels = []
    for weekday in range(7):
        weekday_values = []
        for week_start in week_starts:
            day = week_start + timedelta(days=weekday)
            weekday_values.append(1 if day in completed and start_date <= day <= reference_date else 0)
        z_values.append(weekday_values)
        week_labels.append(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][weekday])

    figure = go.Figure(
        go.Heatmap(
            z=z_values,
            x=[week.strftime("%b %d") for week in week_starts],
            y=week_labels,
            colorscale=[[0, "#EDF2F7"], [1, "#22C55E"]],
            showscale=False,
            zmin=0,
            zmax=1,
            hovertemplate="%{y}, week of %{x}: %{z}<extra></extra>",
        )
    )
    figure.update_layout(
        title="Check-in activity - last 90 days",
        template="plotly_white",
        height=330,
        xaxis=dict(side="top"),
        margin=dict(l=100, r=20, t=80, b=30),
    )
    return figure


def completion_rate_chart(
    completion_rates: Mapping[str, float],
) -> go.Figure:
    names = list(completion_rates)
    rates = [completion_rates[name] for name in names]

    figure = go.Figure(
        go.Bar(
            x=names,
            y=rates,
            marker_color="#22C55E",
            text=[f"{rate:.1f}%" for rate in rates],
            textposition="outside",
        )
    )
    figure.update_layout(
        title="90-day completion rate",
        xaxis_title="Habit",
        yaxis_title="Completion rate",
        yaxis=dict(range=[0, 100], ticksuffix="%"),
        template="plotly_white",
        height=350,
        margin=dict(l=50, r=20, t=60, b=80),
    )
    return figure


def category_breakdown_chart(
    category_counts: Mapping[str, int],
) -> go.Figure:
    names = list(category_counts)
    counts = [category_counts[name] for name in names]

    figure = go.Figure(
        go.Bar(
            x=names,
            y=counts,
            marker_color=["#2563EB", "#22C55E", "#F59E0B", "#8B5CF6"][: len(names)],
            text=counts,
            textposition="outside",
        )
    )
    figure.update_layout(
        title="Habits by category",
        xaxis_title="Category",
        yaxis_title="Number of habits",
        yaxis=dict(dtick=1),
        template="plotly_white",
        height=350,
        margin=dict(l=50, r=20, t=60, b=80),
    )
    return figure
