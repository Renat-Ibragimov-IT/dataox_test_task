from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://"
                       "postgres:260592@localhost/test_db")
engine.connect()
