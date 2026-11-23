from datetime import date

import pytest

from src.streakboard.stats import (
    calculate_current_streak,
    calculate_longest_streak,
)


TODAY = date(2026, 11, 23)


@pytest.mark.parametrize(
    ("check_in_dates", "expected_current", "expected_longest"),
    [
        ([], 0, 0),
        (["2026-11-23"], 1, 1),
        (
            ["2026-11-21", "2026-11-22", "2026-11-23"],
            3,
            3,
        ),
        (
            ["2026-11-18", "2026-11-19", "2026-11-21", "2026-11-22", "2026-11-23"],
            3,
            3,
        ),
        (
            ["2026-01-30", "2026-01-31", "2026-02-01", "2026-12-30", "2026-12-31"],
            0,
            3,
        ),
        (
            ["2026-11-20", "2026-11-20", "2026-11-21", "2026-11-22"],
            3,
            3,
        ),
        (
            ["2026-11-21", "2026-11-22"],
            2,
            2,
        ),
    ],
)
def test_streak_calculations(
    check_in_dates,
    expected_current,
    expected_longest,
):
    assert calculate_current_streak(check_in_dates, TODAY) == expected_current
    assert calculate_longest_streak(check_in_dates) == expected_longest


def test_streak_crosses_month_boundary():
    check_in_dates = ["2026-01-30", "2026-01-31", "2026-02-01"]

    assert calculate_current_streak(check_in_dates, date(2026, 2, 1)) == 3
    assert calculate_longest_streak(check_in_dates) == 3


def test_streak_crosses_year_boundary():
    check_in_dates = ["2025-12-30", "2025-12-31", "2026-01-01", "2026-01-02"]

    assert calculate_current_streak(check_in_dates, date(2026, 1, 2)) == 4
    assert calculate_longest_streak(check_in_dates) == 4


def test_duplicate_dates_do_not_inflate_streak():
    check_in_dates = [
        "2026-11-20",
        "2026-11-20",
        "2026-11-21",
        "2026-11-21",
        "2026-11-22",
    ]

    assert calculate_current_streak(check_in_dates, TODAY) == 3
    assert calculate_longest_streak(check_in_dates) == 3


def test_today_unchecked_but_yesterday_checked():
    check_in_dates = ["2026-11-21", "2026-11-22"]

    assert calculate_current_streak(check_in_dates, TODAY) == 2
