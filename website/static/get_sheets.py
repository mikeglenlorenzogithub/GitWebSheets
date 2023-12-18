import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheets(json_key, spreadsheet_name, sheet_name):
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)
    client = gspread.authorize(creds)
    try:
        sheet = client.open(spreadsheet_name).worksheet(sheet_name)
    except:
        client.open(spreadsheet_name).add_worksheet(sheet_name, rows="1", cols="1")
        sheet = client.open(spreadsheet_name).worksheet(sheet_name)

    return sheet