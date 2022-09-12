from bs4 import BeautifulSoup
from selenium import webdriver

from parser.apartment_parser import ApartmentParser
from parser.logger_conf import logger
from parser.webdriver import WebDriver


class SyncDataCollector:
    """
    Class of data collector using synchronous operation scheme.
    """

    def __init__(self, page_from, page_to, save_to):
        """
        Method to initiate class instance, start data collection and run
        parser by calling parser object. All parameters receiving from
        CLI app arguments.
        Parameters
        __________
        page_from : int
            Specified the site page to start parsing.
        page_to : int
            Specified the site page to end parsing.
        save_to : str
            Specified how the data will be saved.
        """
        self.page_from = page_from
        self.page_to = page_to
        self.save_to = save_to
        self.wd = WebDriver
        self.soup = []
        self.run_collector(page_from, page_to)
        ApartmentParser(self.soup, self.save_to)

    def get_soup(self, page_num: int) -> BeautifulSoup:
        """
        Method to receive html code from certain page.
        Parameters
        __________
        page_num : int
            Number of website page to collect html code.
        Returns
        _______
        BeautifulSoup object with data collected.
        """
        with self.wd(webdriver.Chrome()) as wd:
            wd.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.97 Safari/537.36'})
            url = f'https://www.kijiji.ca/b-apartments-condos/' \
                  f'page-{page_num}/city-of-toronto/c37l1700273'
            wd.get(url)
            return BeautifulSoup(wd.page_source, 'html.parser')

    def run_collector(self, page_from: int, page_to: int):
        """Function to collect html data from all user-defined website pages
        and savi it to the list for future use.
        As testing website have dynamic pagination we should check
        availability of "Next" button. If this button does not exist
        collecting should be finished.
        Parameters
        __________
        page_from : int
            Specified the site page to start parsing.
        page_to : int
            Specified the site page to end parsing.
        """
        for page in range(page_from, page_to + 1):
            current_page_soup = self.get_soup(page)
            self.soup.append(current_page_soup)
            logger(f'Page # {page} parsed')
            if not current_page_soup.find('a', {'title': 'Next'}):
                logger(f'Last page # {page} found')
                break
