from postgres.postgres_connector import engine, Session
from postgres.postgres_model import Apartment


class PostgresSaver:
    """
    Class that is used for saving all data to PostgreSQL.
    Can be used as context manager.
    """
    def __enter__(self):
        """
        Magic method which is used to make the class as context manager.
        With calling class instance connection with DB will be established.
        Returns
        _______
        Class instance.
        """
        self.connection = engine.connect()
        self.session = Session
        return self

    def save(self, data_list: list):
        """
        Method to save all requested data to the DB.
        Calling this method DB session will be started, all data added to the
        session and committed at the end.
        Parameters
        __________
        data_list: list
            All collected and parsed data received from parser.
        """
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
        """
        Magic method which will close connection with DB.
        """
        self.connection.close()
