from pathlib import Path
from datetime import datetime, timedelta

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
        df_merge = df_merge.sort_values(by="Date", ascending=False)
        df_merge.to_csv(filepath, index=False)
    else:
        df = df.sort_values(by="Date", ascending=True)
        df.to_csv(filepath, index=False)


def string_to_dt(date_string) -> datetime | None:
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except Exception:
        return None
