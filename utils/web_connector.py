import os
import platform
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



class WebDriverConnector:
    def __init__(self) -> None:
        self.driver = None
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--incognito")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )

    def _get_chrome_service(self) -> ChromeService:
        if platform.machine() == "aarch64":
            chromedriver_path = os.getenv("CHROMEDRIVER", str(Path("~/chromedriver/chromedriver").expanduser()))
            return ChromeService(executable_path=chromedriver_path)
        else:
            return ChromeService(ChromeDriverManager().install())

    def __enter__(self) -> webdriver.Chrome:
        # Set up the ChromeDriver
        self.driver = webdriver.Chrome(
            service=self._get_chrome_service(), options=self.options
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up and close the driver
        if self.driver:
            self.driver.quit()

