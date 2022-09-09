from sqlalchemy import Column, String, Integer, Date

from database import Base


class ApartmentDB(Base):
    __tablename__ = 'apartment_db'

    apartment_id = Column(Integer, primary_key=True, index=True)
    img_link = Column(String)
    title = Column(String)
    date_posted = Column(Date)
    location = Column(String)
    bedrooms = Column(String)
    description = Column(String)
    price = Column(String)
    currency = Column(String)
