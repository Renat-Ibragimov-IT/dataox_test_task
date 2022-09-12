import datetime

from bs4 import BeautifulSoup

from parser.saver_choice import get_saver


class ApartmentParser:
    """
    Class for creating parser object which should collect required info,
    validate it and save all parsed data to list
    """
    def __init__(self, soup: list, save_to: str):
        """
        Magic method which will initiate ApartmentParser instance and run
        "run_saver()" function in order to save all parsed data.
        Parameters
        __________
        soup : list
            All data collected from webpages and received from collectors.
        save_to : str
            Type of saver to use. This parameter defined by argument at
            startup of CLI app
        """
        self.soup = soup
        self.save_to = save_to
        self.apartment = None
        self.run_saver(self.save_to)

    def parse_img_links(self) -> str:
        """
        Method to check availability and parse the images links
        Returns
        _______
        String with link to image source or "Image not found" text.
        """
        try:
            img_link = self.apartment.find_next('picture').find_next('img'). \
                get('data-src')
        except AttributeError:
            img_link = 'Image not found'
        return img_link

    def parse_title_text(self) -> str:
        """
        Method to parse apartments titles
        Returns
        _______
        String with title text
        """
        return self.apartment.find_next('div', class_='title').text.strip()

    def parse_date_posted(self) -> str:
        """
        Method to parse the dates posted, change it to required format
         or change it to present date in case of entry like
         '< 6 hours ago'
         Returns
         _______
         String with data posted in "dd-mm-yyyy" format or "Unknown" string.
         """
        try:
            date_posted = datetime.datetime.strptime(
                self.apartment.find_next('span', class_='date-posted')
                .text.strip(), '%d/%m/%Y').strftime('%d-%m-%Y')
        except ValueError:
            date_posted = datetime.datetime.now().strftime('%d-%m-%Y')
        return date_posted

    def parse_location(self) -> str:
        """
        Method to parse locations
        Returns
        _______
        String with location definition.
        """
        return self.apartment.find_next('div', class_='location') \
            .find('span').text.strip()

    def parse_bedrooms(self) -> str:
        """
        Method to parse quantity of bedrooms
        Returns
        _______
        String with text showing how many bedrooms does the apartment have.
        """
        return self.apartment.find_next('span', class_='bedrooms').text \
            .strip().replace(' ', '').replace('\n', '')

    def parse_description(self) -> str:
        """
        Method to parse descriptions and change it to required
        format.
        Returns
        _______
        String with description of apartment.
        """
        desc_str = self.apartment.find_next('div', class_='description') \
            .text.strip()
        return desc_str[0: desc_str.find("  ")].replace('\n', ' ')

    def parse_price(self) -> str:
        """
        Method to parse prices and change it to 'Unknown' in case
        price entry is like 'Please Contact'.
        Returns
        _______
        String with price of apartment or "Unknown" text.
        """
        price = self.apartment.find_next(
            'div', class_='price').text.strip()[1:]
        return 'Unknown' if price == 'lease Contact' else price

    def parse_currency(self) -> str:
        """
        Method to parse currencies and change it to 'Unknown' in case
        currency entry is like 'Please Contact'
        Returns
        _______
        String with currency type or "Unknown" text.
        """
        currency = self.apartment.find_next(
            'div', class_='price').text.strip()[0]
        return 'Unknown' if currency == 'P' else currency

    def apartments_cards(self) -> list:
        """
        Method to receive apartments info cards from html pages.
        Returns
        _______
        List of all apartments cards.
        """
        apartments_cards = []
        for page_soup in self.soup:
            apartments_on_page = page_soup.find_all(
                'div', class_='search-item')
            for apartment_card in apartments_on_page:
                apartments_cards.append(apartment_card)
        return apartments_cards

    def get_parsed_data(self, cards_collection: list) -> list:
        """
        Method to receive requested data from apartments cards using a certain
        function.
        Parameters
        __________
        cards_collection : list
            List with all apartments info cards
        Returns
        _______
        List with dicts containing all requested info from apartments info
        cards.
        """
        parsed_data = []
        for card in cards_collection:
            parsed_data.append(self.collect_parsed_data(card))
        return parsed_data

    def collect_parsed_data(self, apartment_card: list) -> dict:
        """
        Method to collect all parsed data from one apartment info card
        and save it as dict for future use.
        Parameters
        __________
        apartment_card : list
            List with one apartment info card to parse
        Returns
        _______
        Dict with all requested info parsed from apartment info card.
        """
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

    def run_saver(self, save_to: str):
        """
        Method to collect in list all requested data and to run certain saver.
        Parameters
        __________
        save_to : str
            Type of saver to use according to argument given for CLI app.
        """
        parsed_data = self.get_parsed_data(self.apartments_cards())
        with get_saver(save_to) as saver:
            saver.save(parsed_data)
