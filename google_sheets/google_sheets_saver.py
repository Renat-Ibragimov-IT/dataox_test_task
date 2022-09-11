from google_sheets.google_sheets_connector import service, spreadsheet_id


class GoogleSheetsSaver:
    def __enter__(self):
        self.service = service
        return self

    def save(self, all_data):
        data_to_save = []
        for data in all_data:
            data_to_save.append([data["img_link"], data["title_text"],
                                 data["date_posted"], data["location"],
                                 data["bedrooms"], data["description"],
                                 data["price"], data["currency"]])
        self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="A1",
            valueInputOption="RAW",
            body={'values': data_to_save}).execute()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
