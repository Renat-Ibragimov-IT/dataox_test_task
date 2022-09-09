import datetime
import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException

from database import engine
from models import apartments_db


class WebDriver:
    """Class for WebDriver with custom magic methods"""
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        try:
            return self.driver
        except InvalidSessionIdException:
            logging.warning("Something went wrong", exc_info=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def get_soup(page_num: int):
    """Function to get html.parser from WebDriver object.
    page_num: int - argument to change website pages depending on how
    many pages to parse"""
    with WebDriver(webdriver.Chrome()) as wd:
        wd.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/83.0.4103.97 Safari/537.36'})
        url = f'https://www.kijiji.ca/b-apartments-condos/page-{page_num}/' \
              f'city-of-toronto/c37l1700273'
        wd.get(url)
        return BeautifulSoup(wd.page_source, 'html.parser')


def parser(browser):
    """Global function to collect all necessary data and add it to DB"""
    apartments = browser.find_all('div', class_='clearfix')
    for apartment in apartments:

        def parse_img_links():
            """Function to check availability and parse the images links """
            try:
                img_link = apartment.findNext('picture').findNext('img'). \
                    get('data-src')
            except AttributeError:
                img_link = 'Image not found'
            return img_link

        def parse_title_text():
            """Function to parse apartments titles"""
            return apartment.findNext('div', class_='title').text.strip()

        def parse_date_posted():
            """Function to parse the dates posted, change it to required format
             or change it to present date in case of entry like
             '< 6 hours ago'"""
            try:
                date_posted = datetime.datetime.strptime(
                    apartment.findNext('span', class_='date-posted')
                    .text.strip(), '%d/%m/%Y').strftime('%d-%m-%Y')
            except ValueError:
                date_posted = datetime.datetime.now().strftime('%d-%m-%Y')
            return date_posted

        def parse_location():
            """Function to parse locations"""
            return apartment.findNext('div', class_='location') \
                .find('span').text.strip()

        def parse_bedrooms():
            """Function to parse quantity of bedrooms"""
            return apartment.findNext('span', class_='bedrooms').text.strip() \
                .replace(' ', '').replace('\n', '')

        def parse_description():
            """Function to parse descriptions and change it to required
            format"""
            desc_str = apartment.findNext('div', class_='description') \
                .text.strip()
            return desc_str[0: desc_str.find("  ")].replace('\n', ' ')

        def parse_price():
            """Function to parse prices and change it to 'Unknown' in case
            price entry is like 'Please Contact'"""
            price = apartment.findNext('div', class_='price').text.strip()[1:]
            return 'Unknown' if price == 'lease Contact' else price

        def parse_currency():
            """Function to parse currencies and change it to 'Unknown' in case
            currency entry is like 'Please Contact'"""
            currency = apartment.findNext(
                'div', class_='price').text.strip()[0]
            return 'Unknown' if currency == 'P' else currency

        def add_to_db():
            """Function to add all collected info for one apartment to DB"""
            new_row = apartments_db.insert().values(
                img_link=parse_img_links(),
                title_text=parse_title_text(),
                date_posted=parse_date_posted(),
                location=parse_location(),
                bedrooms=parse_bedrooms(),
                description=parse_description(),
                price=parse_price(),
                currency=parse_currency()
            )
            connection = engine.connect()
            connection.execute(new_row)

        add_to_db()

# As testing website have dynamic pagination we should check availability of
# "Next" button. If this button does not exist parsing should be finished.
    try:
        browser.find('a', {'title': 'Next'})['href']
    except TypeError:
        raise SystemExit('Parsing completed successfully')


if __name__ == '__main__':
    """If it is needed to check certain pages, 
    change the "range()" function arguments"""
    for page in range(1, 150):
        parser(get_soup(page))
