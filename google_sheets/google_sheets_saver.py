from google_sheets.google_sheets_connector import service, SPREADSHEET_ID


class GoogleSheetsSaver:
    """
    Class that is used for saving all data to Google Sheets spreadsheet.
    Can be used as context manager.
    """
    def __enter__(self):
        """
        Magic method which is used to make the class as context manager.
        With calling class instance connection options will be taken from
        Google Sheet connector.
        Returns
        _______
        Class instance.
        """
        self.service = service
        return self

    def save(self, data_list: list):
        """
        Method to save all requested data to the Google Sheets spreadsheet.
        Parameters
        __________
        data_list: list
            All collected and parsed data received from parser.
        """
        data_to_save = []
        for data in data_list:
            data_to_save.append([data["img_link"], data["title_text"],
                                 data["date_posted"], data["location"],
                                 data["bedrooms"], data["description"],
                                 data["price"], data["currency"]])
        self.service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="A1",
            valueInputOption="RAW",
            body={'values': data_to_save}).execute()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
