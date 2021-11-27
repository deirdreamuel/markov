from json import load
from os.path import dirname

from google.oauth2.service_account import Credentials

"""
    auth class to authenticate google api
"""
class google_auth:
    __credentials = None
    __service_account_info = None

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.readonly'
    ]

    # constructor to initialize google services and account info
    def __init__(self):
        self.__service_account_info = load(open(dirname(__file__) + '/credentials.json'))
        self.__credentials = Credentials.from_service_account_info(
            self.__service_account_info, scopes=self.scopes)
    
    # get credentials for authentication
    def get_credentials(self):
        if not self.__credentials:
            raise 'Exception occurred while obtaining google api credentials'
        return self.__credentials
    
auth = google_auth()
