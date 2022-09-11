from bs4 import BeautifulSoup
from selenium import webdriver

from parser.apartment_parser import ApartmentParser
from parser.logger_conf import logger
from parser.webdriver import WebDriver


class SyncDataCollector:
    def __init__(self, page_from, page_to, save_to):
        self.page_from = page_from
        self.page_to = page_to
        self.save_to = save_to
        self.wd = WebDriver
        self.soup = []
        self.run_collector(page_from, page_to)
        self.run_parser = ApartmentParser(self.soup, self.save_to)

    def get_soup(self, page_num: int) -> BeautifulSoup:
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
        for page in range(page_from, page_to + 1):
            current_page_soup = self.get_soup(page)
            self.soup.append(current_page_soup)
            logger(f'Page # {page} parsed')
            if not current_page_soup.find('a', {'title': 'Next'}):
                logger(f'Last page # {page} found')
                break
