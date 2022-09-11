from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://dataox:dataox"
                       "@localhost:5433/dataox_db")

Session = sessionmaker(engine, expire_on_commit=False)
