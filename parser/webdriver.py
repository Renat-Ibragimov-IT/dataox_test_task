import logging

from selenium.common import InvalidSessionIdException


class WebDriver:
    """
    Context manager for safe work with webdriver
    """

    def __init__(self, driver):
        """
        Method to initiate WebDriver class instance.
        Parameters
        __________
        driver : object
            WebDriver type object received from collector.
        """
        self.driver = driver

    def __enter__(self):
        """
        Method to use class object as context manager and validate its
        work.
        """
        try:
            return self.driver
        except InvalidSessionIdException:
            logging.warning("Something went wrong", exc_info=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Method to automatically close driver after finish of work.
        """
        self.driver.quit()
