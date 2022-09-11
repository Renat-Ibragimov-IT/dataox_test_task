import os

from dotenv import load_dotenv
load_dotenv()

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:" \
                          f"{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/" \
                          f"{POSTGRES_DB}"

GS_CREDENTIALS_FILE = os.getenv("GS_CREDENTIALS_FILE")
GS_SPREADSHEET_ID = os.getenv("GS_SPREADSHEET_ID")
