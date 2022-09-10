from bs4 import BeautifulSoup
from selenium import webdriver

from apartment_parser import ApartmentParser
from webdriver import WebDriver


def get_soup(page_num: int) -> BeautifulSoup:
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


def parser(browser):
    """Function to call parser object for each apartment on the page and send
    it to parser object. In case there is needed to safe all data to
    PostgresSQL parser object function "save_to_postgres()" should be called,
    if needed to save to Google Sheets, call parser object function
    "save_to_google_sheets()".
    browser: html.parser -> html page receiving by BeautifulSoup.
    As testing website have dynamic pagination we should check availability of
    "Next" button. If this button does not exist parsing should be finished."""
    apartments = browser.find_all('div', class_='search-item')
    for apartment in apartments:
        ApartmentParser(apartment).save_to_google_sheets()
    try:
        browser.find('a', {'title': 'Next'})['href']
    except TypeError:
        raise SystemExit('Parsing completed successfully')


def get_parser_for_pages(page_from: int, page_to: int):
    """Function to start parsing of certain pages.
    page_from: int -> page number to start parsing from
    page_to: int -> last page for parsing number
    If it is needed to check all pages, 'page_from' should be 1 and
    'page_to' should be more than 150. If number of page on website will be
    less than 'page_to' argument, parser() function will terminate parsing
    after the last page on website using try-except block"""
    for page in range(page_from, page_to):
        parser(get_soup(page))


if __name__ == '__main__':
    get_parser_for_pages(1, 2)
