from googleapiclient.discovery import build
from httplib2 import Response
from api.google.auth import auth

"""
    service class which contains different services offerred by Google
        and utilizes various tools such as drive & sheets api
"""
class google_service:
    drive_service = None
    sheets_service = None

    stock_headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    # constructor to initialize google services and account info
    def __init__(self):
        self.drive_service = build('drive', 'v3', credentials=auth.get_credentials())
        self.sheets_service = build('sheets', 'v4', credentials=auth.get_credentials())

    # get list of spreadsheet objects
    def get_spreadsheets(self):
        spreadsheet_type = "mimeType='application/vnd.google-apps.spreadsheet'"
        spreadsheets = []

        try:
            # get list of spreadsheet type using drive service
            response = self.drive_service.files().list(
                q=spreadsheet_type, spaces='drive').execute()
            for sheet in response['files']:
                spreadsheets.append(sheet)

        except Exception as error:
            print('Google api error:', error)

        return spreadsheets

    # clear spreadsheet from id and specificied range
    def clear_spreadsheet(self, id, range='Sheet1!A1:Z'):
        response = self.sheets_service.spreadsheets().values().clear(
            spreadsheetId=id, range=range, body={}).execute()

        return True if response else False

    # create new spreadsheet with title
    def create_spreadsheet(self, title):
        spreadsheet = None

        try:
            # create spreadsheet using google sheets service
            config = {
                'properties': {
                    'title': title
                }
            }
            spreadsheet = self.sheets_service.spreadsheets().create(config).execute()

        except Exception as error:
            print(error)

        return spreadsheet

    # update spreadsheet values using sheets api
    def update_spreadsheet(self, id, range, values):
        response = None

        try:
            response = self.sheets_service.spreadsheets().values().update(
                spreadsheetId=id, range=range, 
                valueInputOption='USER_ENTERED', body=values).execute()
        except Exception as error:
            raise Exception('Google sheets api insert exception occurred')

        return Response

    # get spreadsheet values using sheets api
    def get_spreadsheet(self, id, range):
        response = None
        try:
            response = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=id, range=range).execute()
        except Exception as error: 
            raise Exception('Google sheets api retrieve exception occurred')

        return response


service = google_service()