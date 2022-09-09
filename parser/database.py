from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer

engine = create_engine("postgresql+psycopg2://postgres:260592@localhost/test_db")

metadata = MetaData()

apartments_db = Table('apartments_db', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('img_link', String),
                      Column('title_text', String),
                      Column('date_posted', String),
                      Column('location', String),
                      Column('bedrooms', String),
                      Column('description', String),
                      Column('price', String),
                      Column('currency', String))

metadata.create_all(engine)
