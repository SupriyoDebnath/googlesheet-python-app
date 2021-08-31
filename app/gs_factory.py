import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GSFactory:
    def __init__(self, spreadsheet_url):
        spreadsheet_url_prefix = 'https://docs.google.com/spreadsheets/d/'
        spreadsheet_url = spreadsheet_url.replace(spreadsheet_url_prefix, '')
        self.spreadsheet_id = spreadsheet_url.split('/')[0]
        self.worksheet_id = spreadsheet_url.split('/')[1].split('=')[-1]

        cred_file = os.path.join(os.getcwd(), 'app', 'static/project-gs-python-54a64508ea67.json')
        service_cred = service_account.Credentials.from_service_account_file(cred_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
        self.service_obj = build(serviceName='sheets', version='v4', credentials=service_cred, cache_discovery=False)

    
    def read_data(self):
        rows = []

        spreadsheet_obj = self.service_obj.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        for worksheet in spreadsheet_obj.get('sheets'):
            if worksheet.get('properties').get('sheetId') == int(self.worksheet_id):
                self.worksheet_name = worksheet.get('properties').get('title')
                worksheet_obj = self.service_obj.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=self.worksheet_name).execute()
                rows = worksheet_obj.get('values', [])
                break
        
        return rows
    

    def write_data(self, cdb_industry, cdb_sub_industry, row_index):
        if cdb_industry:
            cell_range = f'{self.worksheet_name}!B{row_index}'
            body = {
                'values': [[cdb_industry]]
            }
            self.service_obj.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id, range=cell_range, valueInputOption='RAW', body=body).execute()
        
        if cdb_sub_industry:
            cell_range = f'{self.worksheet_name}!C{row_index}'
            body = {
                'values': [[cdb_sub_industry]]
            }
            self.service_obj.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id, range=cell_range, valueInputOption='RAW', body=body).execute()


