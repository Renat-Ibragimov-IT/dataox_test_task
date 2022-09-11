from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from postgres.postgres_connector import engine

Base = declarative_base()


class Apartment(Base):
    __tablename__ = 'apartments_db'

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_link = Column(String)
    title_text = Column(String)
    date_posted = Column(String)
    location = Column(String)
    bedrooms = Column(String)
    description = Column(String)
    price = Column(String)
    currency = Column(String)


Base.metadata.create_all(engine)
