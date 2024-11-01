import argparse
from pathlib import Path
from datetime import datetime
from argparse import Namespace

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from webdrivers.chrome import WebDriverConnector
from utils.utils import (
    get_last_or_actual_work_datetime,
    save_to_csv,
    string_to_dt,
    past_workdays_generator,
)


KEYS = {
    "Currency": "calendar__cell calendar__currency",
    "Impact": "calendar__cell calendar__impact",
    "Event": "calendar__cell calendar__event event",
    "Actual": "calendar__cell calendar__actual",
    "Forecast": "calendar__cell calendar__forecast",
    "Previous": "calendar__cell calendar__previous",
}
FILEPATH = Path(__file__).parent / "output" / "calendar.csv"


def forex_calendar(args: Namespace) -> None:
    if args.period:
        forex_data = backfill_data_extractor(args.period)
    else:
        arg_datetime = string_to_dt(args.date)
        forex_data = page_extractor(actual_dt=arg_datetime, filters={"impact": args.impact})

    if forex_data:
        df = pd.DataFrame(forex_data)
        save_to_csv(df, FILEPATH)


def page_extractor(actual_dt: datetime | None = None, filters: dict | None = None) -> list[dict]:
    forex_data = []
    workday_dt = actual_dt or get_last_or_actual_work_datetime()

    # Format the date to "oct17.2024"
    formatted_date = workday_dt.strftime("%b%d.%Y").lower()

    with WebDriverConnector() as driver:
        # Load the Forex Factory page
        driver.get(f"https://www.forexfactory.com/calendar?day={formatted_date}")

        try:
            # Explicitly wait for the table element to load (adjust selector if needed)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "calendar__table")))

            table = driver.find_element(By.CLASS_NAME, "calendar__table")
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows[4:]:
                cells_value = get_cells_value(row, workday_dt, filters)

                if cells_value and len(cells_value) >= 6 and cells_value["Actual"]:
                    forex_data.append(cells_value)
            return forex_data
        except Exception:
            return []


def backfill_data_extractor(period: str) -> list[dict]:
    history_data = []
    for dt in past_workdays_generator(period):
        history_data.extend(page_extractor(dt))

    return history_data


def get_cells_value(row: WebElement, actual_dt: datetime, filters: dict[str] | None = None) -> dict | None:
    cells_value = {"Date": actual_dt.date().strftime("%Y-%m-%d")}
    for key, class_name in KEYS.items():
        text = row.find_element(By.XPATH, f'.//td[@class="{class_name}"]').text.strip()
        if key == "Impact":
            text = row.find_element(By.XPATH, ".//span[@title]").get_attribute("title")
            if filters and filters["impact"].lower() not in text.lower():
                return None
        cells_value[key] = text.strip()
    return cells_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--date",
        type=str,
        default="",
        help="date format: YYYY-MM-DD",
    )
    parser.add_argument(
        "-i",
        "--impact",
        type=str,
        default="",
        help="select one of these choices: Low, Medium, High. Default: All impacts",
    )
    parser.add_argument(
        "-p",
        "--period",
        type=str,
        default="",
        help="period format: 1d, 1mo, 2mo, etc",
    )
    arguments = parser.parse_args()
    forex_calendar(arguments)
