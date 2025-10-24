import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from typing import Any
import hashlib

# GOOGLE_CREDS_JSON = '{"type": "service_account", ...}' 
# SHEETS_DOC_ID = 'your_sheet_id_here'

class GoogleSheetsExtractor:
    def __init__(self, creds_json: str, sheets_id: str):
        """
        Initializes the GoogleSheetFetcher with credentials and sheet ID.

        Args:
            creds_json (str): JSON string of Google service account credentials.
            sheets_id (str): The ID of the Google Sheets document.
        """
        self.creds_json = creds_json
        self.sheets_id = sheets_id
        
    def authorize_gspread(self) -> gspread.client.Client:
        """
        Handles the authorization process with Google Sheets.

        Returns:
            gspread.client.Client: The authorized gspread client.
        """
        creds_dict = json.loads(self.creds_json)
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
        client = gspread.authorize(credentials)
        return client
    
    def fetch_data(self) -> pd.DataFrame:
        """
        Fetches data from the Google Sheets document, converts it to a DataFrame,
        and adds/ensures the 'response_id' column.

        Returns:
            pd.DataFrame: DataFrame containing the data from the Google Sheets document.
        """
        try:
            client = self.authorize_gspread()
            sheet = client.open_by_key(self.sheets_id)
            worksheet = sheet.sheet1 # Target the first sheet

            # Fetch all data as a list of dictionaries
            # empty2zero=False ensures empty cells are represented as empty strings/None, not 0
            data = worksheet.get_all_records(empty2zero=False)
            df = pd.DataFrame(data)
            return df
        
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Error: Spreadsheet with ID '{self.sheets_id}' not found.")
            return pd.DataFrame()
        
        except Exception as e:
            print(f"An error occurred during data fetching: {e}")
            return pd.DataFrame()