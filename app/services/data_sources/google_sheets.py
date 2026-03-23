from .base import DataSource
import gspread
from google.oauth2.service_account import Credentials

#  todo: replace key with an environment variable

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_client():
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )
    return gspread.authorize(creds)


class GoogleSheetsDataSource(DataSource):
    # uses the spreadsheet id
    def get_mentor_rows(self):
        client = get_client()
        sheet = client.open_by_key("1JJESL_vy9wIZxC4NyHOWNvzBK6-fNIvtBCkN3wX224M").worksheet("Mentor Responses")
        return sheet.get_all_records()


    def get_mentee_rows(self):
        client = get_client()
        sheet = client.open_by_key("1JJESL_vy9wIZxC4NyHOWNvzBK6-fNIvtBCkN3wX224M").worksheet("Mentee Responses")
        return sheet.get_all_records()