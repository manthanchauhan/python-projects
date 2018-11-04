import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('D:\Git\python-projects\sheets\sheets-08a73e26c6d1.json', scope)
gc = gspread.authorize(credentials)

wks = gc.open('sheet_API').sheet1
print(wks.get_all_records())
# wks.append_row(['first', 'second', 3])