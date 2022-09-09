import datetime

from bs4 import BeautifulSoup
from selenium import webdriver

from database import engine
from models import apartments_db
from webdriver import WebDriver


def get_soup(page_num: int):
    """Function to get html.parser from WebDriver object.
    page_num: int -> argument to change website pages depending on how
    many pages is needed to parse"""
    with WebDriver(webdriver.Chrome()) as wd:
        wd.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/83.0.4103.97 Safari/537.36'})
        url = f'https://www.kijiji.ca/b-apartments-condos/page-{page_num}/' \
              f'city-of-toronto/c37l1700273'
        wd.get(url)
        return BeautifulSoup(wd.page_source, 'html.parser')


class ApartmentParser:
    """Class for creating parser object which should collect required info,
    validate it and save to DB"""
    def __init__(self, apartment):
        self.apartment = apartment
        self.img_link = self.parse_img_links()
        self.title_text = self.parse_title_text()
        self.date_posted = self.parse_date_posted()
        self.location = self.parse_location()
        self.bedrooms = self.parse_bedrooms()
        self.description = self.parse_description()
        self.price = self.parse_price()
        self.currency = self.parse_currency()

    def parse_img_links(self):
        """Method to check availability and parse the images links """
        try:
            img_link = self.apartment.find_next('picture').find_next('img'). \
                get('data-src')
        except AttributeError:
            img_link = 'Image not found'
        return img_link

    def parse_title_text(self):
        """Method to parse apartments titles"""
        return self.apartment.find_next('div', class_='title').text.strip()

    def parse_date_posted(self):
        """Method to parse the dates posted, change it to required format
         or change it to present date in case of entry like
         '< 6 hours ago'"""
        try:
            date_posted = datetime.datetime.strptime(
                self.apartment.find_next('span', class_='date-posted')
                .text.strip(), '%d/%m/%Y').strftime('%d-%m-%Y')
        except ValueError:
            date_posted = datetime.datetime.now().strftime('%d-%m-%Y')
        return date_posted

    def parse_location(self):
        """Method to parse locations"""
        return self.apartment.find_next('div', class_='location') \
            .find('span').text.strip()

    def parse_bedrooms(self):
        """Method to parse quantity of bedrooms"""
        return self.apartment.find_next('span', class_='bedrooms').text\
            .strip().replace(' ', '').replace('\n', '')

    def parse_description(self):
        """Method to parse descriptions and change it to required
        format"""
        desc_str = self.apartment.find_next('div', class_='description') \
            .text.strip()
        return desc_str[0: desc_str.find("  ")].replace('\n', ' ')

    def parse_price(self):
        """Method to parse prices and change it to 'Unknown' in case
        price entry is like 'Please Contact'"""
        price = self.apartment.find_next(
            'div', class_='price').text.strip()[1:]
        return 'Unknown' if price == 'lease Contact' else price

    def parse_currency(self):
        """Method to parse currencies and change it to 'Unknown' in case
        currency entry is like 'Please Contact'"""
        currency = self.apartment.find_next(
            'div', class_='price').text.strip()[0]
        return 'Unknown' if currency == 'P' else currency

    def save_to_db(self):
        """Method to save all collected info for each apartment to DB"""
        new_row = apartments_db.insert().values(
            img_link=self.img_link,
            title_text=self.title_text,
            date_posted=self.date_posted,
            location=self.location,
            bedrooms=self.bedrooms,
            description=self.description,
            price=self.price,
            currency=self.currency
        )
        connection = engine.connect()
        connection.execute(new_row)


def parser(browser):
    """Function to call parser object for each apartment on the page.
    browser: html.parser -> html page receiving by BeautifulSoup.
    As testing website have dynamic pagination we should check availability of
    "Next" button. If this button does not exist parsing should be finished."""
    apartments = browser.find_all('div', class_='search-item')
    for apartment in apartments:
        ApartmentParser(apartment).save_to_db()
    try:
        browser.find('a', {'title': 'Next'})['href']
    except TypeError:
        raise SystemExit('Parsing completed successfully')


def get_parser_for_pages(page_from: int, page_to: int):
    """Function to start parsing of certain page.
    page_from: int -> page number to start parsing from
    page_to: int -> last page for parsing number
    If it is needed to check all pages, 'page_from' should be 1 and
    'page_to' should be more than 150. If number of page on website will be
    less than 'page_to' argument, parser() function will terminate parsing
    after the last page on website using try-except block"""
    for page in range(page_from, page_to):
        parser(get_soup(page))


if __name__ == '__main__':
    get_parser_for_pages(1, 3)
