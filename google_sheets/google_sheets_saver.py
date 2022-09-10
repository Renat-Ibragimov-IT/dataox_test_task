from google_sheets.google_sheets_connector import service, spreadsheet_id


class GoogleSheetsSaver:
    def save(self, data):
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="A1",
            valueInputOption="RAW",
            body={'values': [
                [data["img_link"], data["title_text"], data["date_posted"],
                 data["location"], data["bedrooms"], data["description"],
                 data["price"], data["currency"]]]}).execute()
