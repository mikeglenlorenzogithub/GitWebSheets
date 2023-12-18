import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheets(json_key, sheet_name):
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1

    return sheet