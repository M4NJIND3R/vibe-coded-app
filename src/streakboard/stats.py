from datetime import date, timedelta
from typing import Iterable, Optional, Union


CheckInDate = Union[date, str]


def _normalize_dates(check_in_dates: Iterable[CheckInDate]) -> set[date]:
    normalized = set()
    for check_in_date in check_in_dates:
        try:
            normalized.add(
                check_in_date
                if isinstance(check_in_date, date)
                else date.fromisoformat(check_in_date)
            )
        except (TypeError, ValueError):
            continue
    return normalized


def calculate_current_streak(
    check_in_dates: Iterable[CheckInDate],
    today: Optional[date] = None,
) -> int:
    completed_dates = _normalize_dates(check_in_dates)
    if not completed_dates:
        return 0

    reference_date = today or date.today()
    if reference_date in completed_dates:
        streak_date = reference_date
    elif reference_date - timedelta(days=1) in completed_dates:
        streak_date = reference_date - timedelta(days=1)
    else:
        return 0

    streak = 0
    while streak_date in completed_dates:
        streak += 1
        streak_date -= timedelta(days=1)
    return streak


def calculate_longest_streak(check_in_dates: Iterable[CheckInDate]) -> int:
    completed_dates = sorted(_normalize_dates(check_in_dates))
    if not completed_dates:
        return 0

    longest = 1
    current = 1
    for previous_date, current_date in zip(completed_dates, completed_dates[1:]):
        if current_date == previous_date + timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest
