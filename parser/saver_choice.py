from google_sheets.google_sheets_saver import GoogleSheetsSaver
from postgres.postgres_saver import PostgresSaver


def get_saver(save_to: str) -> object:
    """
    Function to call certain saver object.
    Parameters
    __________
    save_to : str
        Type of saver to use according to argument given for CLI app.
    Returns
    _______
    Certain saver class instance.
    """
    savers = {"postgres": PostgresSaver, "google_sheets": GoogleSheetsSaver}
    return savers[save_to]()
