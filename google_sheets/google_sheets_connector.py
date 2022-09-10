import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = '../credentials.json'
spreadsheet_id = '1_MXpz6URmT-Cz5Tas9SlirPQO9tc75fT6u5vXqg26LA'


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def init_column_names():
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
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
