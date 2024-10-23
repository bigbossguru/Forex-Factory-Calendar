import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Generator

import pandas as pd


def get_last_or_actual_work_datetime() -> datetime:
    # Get today's date and time
    now = datetime.now()

    # Check if today is a weekday (Monday to Friday)
    if now.weekday() < 5:  # 0-4 are Monday to Friday
        return now  # Return current datetime if it's a weekday
    else:
        # If it's Saturday (5) or Sunday (6), go back to Friday
        last_workday = now - timedelta(days=(now.weekday() - 4))
        return last_workday.replace(
            hour=now.hour,
            minute=now.minute,
            second=now.second,
            microsecond=now.microsecond,
        )


def save_to_csv(df: pd.DataFrame, filepath: Path) -> None:
    if filepath.exists():
        df_read = pd.read_csv(filepath)
        df_merge = pd.concat([df, df_read])
        df_merge = df_merge.drop_duplicates()
        df_merge = df_merge.sort_values(by="Date", ascending=False)
        df_merge.to_csv(filepath, index=False)
    else:
        df = df.drop_duplicates()
        df = df.sort_values(by="Date", ascending=False)
        df.to_csv(filepath, index=False)


def string_to_dt(date_string) -> datetime | None:
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except Exception:
        return None


def past_workdays_generator(period: str) -> Generator[datetime, None, None]:
    # Parse the time frame
    match = re.match(r"(\d+)(\w+)", period)
    if not match:
        raise ValueError("Invalid time frame format. Use format like '1mo'.")

    quantity, unit = int(match.group(1)), match.group(2)

    # Determine the timedelta based on the unit
    if unit == "d":
        delta = timedelta(days=quantity)
    elif unit == "mo":
        delta = timedelta(days=quantity * 30)  # Approximation for months
    elif unit == "y":
        delta = timedelta(days=quantity * 365)  # Approximation for years
    else:
        raise ValueError("Unsupported time unit. Use 'd', 'mo', or 'y'.")

    end_date = datetime.now()
    start_date = end_date - delta

    # Generate workdays
    current_date = start_date
    while current_date < end_date:
        if current_date.weekday() < 5:  # Monday to Friday are 0-4
            yield current_date
        current_date += timedelta(days=1)
