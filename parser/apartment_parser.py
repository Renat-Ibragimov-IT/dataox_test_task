import datetime

from postgres_connector import engine
from postgres_model import apartments_db
from google_sheets_connector import service, spreadsheet_id


class ApartmentParser:
    """Class for creating parser object which should collect required info,
    validate it and save to PostgresSQL or Google Sheets"""
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

    def save_to_postgres(self):
        """Method to save all collected info for each apartment to
        PostgresSQL"""
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

    def save_to_google_sheets(self):
        """Method to save all collected info for each apartment to
        Google Sheets"""
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="A1",
            valueInputOption="RAW",
            body={'values': [
                [self.img_link, self.title_text, self.date_posted,
                 self.location, self.bedrooms, self.description, self.price,
                 self.currency]]}).execute()
