from postgres.postgres_connector import engine, Session
from postgres.postgres_model import Apartment


class PostgresSaver:
    def __enter__(self):
        self.connection = engine.connect()
        self.session = Session
        return self

    def save(self, data_list):
        with self.session.begin() as session:
            for data in data_list:
                new_row = Apartment(
                    img_link=data["img_link"],
                    title_text=data["title_text"],
                    date_posted=data["date_posted"],
                    location=data["location"],
                    bedrooms=data["bedrooms"],
                    description=data["description"],
                    price=data["price"],
                    currency=data["currency"])
                session.add(new_row)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
