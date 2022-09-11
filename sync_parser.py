from bs4 import BeautifulSoup
from selenium import webdriver

from parser.apartment_parser import ApartmentParser
from parser.logger_conf import logger
from parser.saver_choice import get_saver
from parser.webdriver import WebDriver


class SyncParser:
    def __init__(self, page_from, page_to, save_to):
        self.page_from = page_from
        self.page_to = page_to
        self.save_to = save_to
        self.wd = WebDriver
        self.all_soups = []
        self.apartments = []
        self.parsed_data = []
        self.run_parser(self.page_from, self.page_to, self.save_to)

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

    def collect_soup(self, page_from: int, page_to: int):
        for page in range(page_from, page_to + 1):
            self.all_soups.append(self.get_soup(page))
            logger(f'Page # {page} parsed')
            try:
                self.all_soups[-1].find('a', {'title': 'Next'})['href']
            except TypeError:
                logger(f'Last page # {page} found')
                break

    def collect_apartments_cards(self, all_pages_soup_list) -> list:
        for page_soup in all_pages_soup_list:
            apartments_on_page = page_soup.find_all(
                'div', class_='search-item')
            for apartment_card in apartments_on_page:
                self.apartments.append(apartment_card)
        return self.apartments

    def get_parsed_data(self, cards_collection: list) -> list:
        for card in cards_collection:
            self.parsed_data.append(ApartmentParser(card)
                                    .collect_parsed_data())
        return self.parsed_data

    def run_parser(self, page_from: int, page_to: int, save_to):
        self.collect_soup(page_from, page_to)
        self.collect_apartments_cards(self.all_soups)
        self.get_parsed_data(self.apartments)

        with get_saver(save_to) as saver:
            saver.save(self.parsed_data)
