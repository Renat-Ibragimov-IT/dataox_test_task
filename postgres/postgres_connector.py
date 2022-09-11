from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://"
                       "postgres:260592@localhost/test_db")

Session = sessionmaker(engine, expire_on_commit=False)
