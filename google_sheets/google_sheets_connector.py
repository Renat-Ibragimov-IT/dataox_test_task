import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

import config

CREDENTIALS_FILE = config.GS_CREDENTIALS_FILE
SPREADSHEET_ID = config.GS_SPREADSHEET_ID

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def init_column_names():
    """
    Function witch will initialize column names when start working with
    Google Sheets spreadsheet.
    """
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "A1:H1",
                 "majorDimension": "ROWS",
                 "values": [["Image link", "Title text", "Date posted",
                             "Location", "Bedrooms", "Description", "Price",
                             "Currency"]
                            ]},
            ]
        }
    ).execute()


if __name__ == "__main__":
    init_column_names()
