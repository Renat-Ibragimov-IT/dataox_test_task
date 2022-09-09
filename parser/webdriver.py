import logging

from selenium.common import InvalidSessionIdException


class WebDriver:
    """Context manager for safe work with webdriver"""
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        try:
            return self.driver
        except InvalidSessionIdException:
            logging.warning("Something went wrong", exc_info=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
