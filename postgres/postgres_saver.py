from postgres.postgres_connector import engine
from postgres.postgres_model import apartments_db


class PostgresSaver:
    def save(self, data):
        new_row = apartments_db.insert().values(
            img_link=data["img_link"],
            title_text=data["title_text"],
            date_posted=data["date_posted"],
            location=data["location"],
            bedrooms=data["bedrooms"],
            description=data["description"],
            price=data["price"],
            currency=data["currency"]
        )
        connection = engine.connect()
        connection.execute(new_row)
