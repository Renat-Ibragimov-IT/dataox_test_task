import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(engine, expire_on_commit=False)
