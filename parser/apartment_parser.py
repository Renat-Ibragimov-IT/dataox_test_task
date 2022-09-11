import datetime
from bs4 import BeautifulSoup
from parser.saver_choice import get_saver


class ApartmentParser:
    """Class for creating parser object which should collect required info,
    validate it and save all parsed data to list"""
    def __init__(self, soup, save_to):
        self.soup = soup
        self.save_to = save_to
        self.apartment = BeautifulSoup('')
        self.run_saver(self.save_to)

    def parse_img_links(self) -> str:
        """Method to check availability and parse the images links"""
        try:
            img_link = self.apartment.find_next('picture').find_next('img'). \
                get('data-src')
        except AttributeError:
            img_link = 'Image not found'
        return img_link

    def parse_title_text(self) -> str:
        """Method to parse apartments titles"""
        return self.apartment.find_next('div', class_='title').text.strip()

    def parse_date_posted(self) -> str:
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

    def parse_location(self) -> str:
        """Method to parse locations"""
        return self.apartment.find_next('div', class_='location') \
            .find('span').text.strip()

    def parse_bedrooms(self) -> str:
        """Method to parse quantity of bedrooms"""
        return self.apartment.find_next('span', class_='bedrooms').text\
            .strip().replace(' ', '').replace('\n', '')

    def parse_description(self) -> str:
        """Method to parse descriptions and change it to required
        format"""
        desc_str = self.apartment.find_next('div', class_='description') \
            .text.strip()
        return desc_str[0: desc_str.find("  ")].replace('\n', ' ')

    def parse_price(self) -> str:
        """Method to parse prices and change it to 'Unknown' in case
        price entry is like 'Please Contact'"""
        price = self.apartment.find_next(
            'div', class_='price').text.strip()[1:]
        return 'Unknown' if price == 'lease Contact' else price

    def parse_currency(self) -> str:
        """Method to parse currencies and change it to 'Unknown' in case
        currency entry is like 'Please Contact'"""
        currency = self.apartment.find_next(
            'div', class_='price').text.strip()[0]
        return 'Unknown' if currency == 'P' else currency

    def apartments_cards(self):
        apartments_cards = []
        for page_soup in self.soup:
            apartments_on_page = page_soup.find_all(
                'div', class_='search-item')
            for apartment_card in apartments_on_page:
                apartments_cards.append(apartment_card)
        return apartments_cards

    def get_parsed_data(self, cards_collection: list):
        parsed_data = []
        for card in cards_collection:
            parsed_data.append(self.collect_parsed_data(card))
        return parsed_data

    def collect_parsed_data(self, apartment_card):
        """Method to collect all parsed data and save it to list for
        future use"""
        self.apartment = apartment_card
        data = {"img_link": self.parse_img_links(),
                "title_text": self.parse_title_text(),
                "date_posted": self.parse_date_posted(),
                "location": self.parse_location(),
                "bedrooms": self.parse_bedrooms(),
                "description": self.parse_description(),
                "price": self.parse_price(),
                "currency": self.parse_currency()}
        return data

    def run_saver(self, save_to):
        parsed_data = self.get_parsed_data(self.apartments_cards())
        with get_saver(save_to) as saver:
            saver.save(parsed_data)
