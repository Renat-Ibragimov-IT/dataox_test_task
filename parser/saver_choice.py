from google_sheets.google_sheets_saver import GoogleSheetsSaver
from postgres.postgres_saver import PostgresSaver


def get_saver(saver_name):
    savers = {"postgres": PostgresSaver, "google_sheets": GoogleSheetsSaver}
    return savers[saver_name]()
