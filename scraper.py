import re
import time
import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


# FIXME: correct assign value and columns
def forex_calendar():
    # Regex pattern to match time strings in the format h:mmam or h:mmpm
    TIME_PATTERN = r"\b\d{1,2}:\d{2}(am|pm)\b"

    with WebDriverConnector() as driver:

        # Load the Forex Factory page
        driver.get("https://www.forexfactory.com")

        # Explicitly wait for the table element to load (adjust selector if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendar__table"))
        )

        forex = []
        table = driver.find_element(By.CLASS_NAME, "calendar__table")
        header = [
            "Date",
            "Currency",
            "Impact",
            "Detail",
            "Actual",
            "Forecast",
            "Previous",
        ]

        rows = table.find_elements(By.TAG_NAME, "tr")
        date_str = rows[4].find_element(By.TAG_NAME, "td").text
        date = str_to_dt(date_str).date()
        for row in rows[4:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            events = [date]
            for cell in cells[1:]:
                cell_text = cell.text.strip()
                if cell_text:
                    if re.match(TIME_PATTERN, cell_text):
                        continue
                    events.append(cell_text)
                else:
                    try:
                        events.append(
                            cell.find_element(
                                By.XPATH, ".//span[@title]"
                            ).get_attribute("title")
                        )
                    except:
                        pass

            if events and len(events) >= 6:
                forex.append(events)

    df = pd.DataFrame(forex, columns=header)
    save_to_csv(df)


def save_to_csv(df: pd.DataFrame) -> None:
    filepath = Path(__file__).parent / "output" / "calendar.csv"

    if filepath.exists():
        df_read = pd.read_csv(filepath)
        df_merge = pd.concat([df, df_read])
        df_merge.to_csv(filepath, index=False)
    else:
        df.to_csv(filepath, index=False)


def str_to_dt(date_str: str) -> datetime.datetime:
    date_str_split = date_str.split("\n")
    year = datetime.datetime.now().year

    # Convert the string to a datetime object
    date_obj = datetime.datetime.strptime(f"{year} {date_str_split[-1]}", "%Y %b %d")

    return date_obj


class WebDriverConnector:
    def __init__(self) -> None:
        self.driver = None
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )

    def __enter__(self) -> webdriver.Chrome:
        # Set up the ChromeDriver
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=self.options
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up and close the driver
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    forex_calendar()
