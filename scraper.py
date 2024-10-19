import datetime
import argparse
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from utils.web_connector import WebDriverConnector
from utils.utils import get_last_or_actual_work_datetime, save_to_csv, check_date_in_csv, string_to_dt


KEYS = {
    "Currency": "calendar__cell calendar__currency",
    "Impact": "calendar__cell calendar__impact",
    "Event": "calendar__cell calendar__event event",
    "Actual": "calendar__cell calendar__actual",
    "Forecast": "calendar__cell calendar__forecast",
    "Previous": "calendar__cell calendar__previous",
}
FILEPATH = Path(__file__).parent / "output" / "calendar.csv"


def forex_calendar(args) -> None:
    arg_dt = string_to_dt(args.date)
    workday_dt = arg_dt or get_last_or_actual_work_datetime()

    if check_date_in_csv(FILEPATH, workday_dt):
        return None

    with WebDriverConnector() as driver:

        # Format the date to "oct17.2024"
        formatted_date = workday_dt.strftime("%b%d.%Y").lower()

        # Load the Forex Factory page
        driver.get(f"https://www.forexfactory.com/calendar?day={formatted_date}")

        # Explicitly wait for the table element to load (adjust selector if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendar__table"))
        )

        forex_data = []
        table = driver.find_element(By.CLASS_NAME, "calendar__table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        try:
            for row in rows[4:]:
                cells_value = get_cells_value(row, workday_dt)

                if len(cells_value) >= 6:
                    forex_data.append(cells_value)
        except Exception:
            return None

    df = pd.DataFrame(forex_data)
    save_to_csv(df, FILEPATH)


def get_cells_value(row: WebElement, dt: datetime.datetime) -> list:
    cells_value = {"Date": dt.date()}
    for key, class_name in KEYS.items():
        text = row.find_element(By.XPATH, f'.//td[@class="{class_name}"]').text.strip()
        if key == "Impact":
            text = row.find_element(By.XPATH, ".//span[@title]").get_attribute("title")
        cells_value[key] = text
    return cells_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date format YYYY.MM.DD")
    args = parser.parse_args()
    forex_calendar(args)
