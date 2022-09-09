from sqlalchemy import create_engine, MetaData

engine = create_engine("postgresql+psycopg2://"
                       "postgres:260592@localhost/test_db")
engine.connect()
