import os
import re
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_sheet_id(url_or_id):
    """Extracts the Sheet ID from a full Google Sheets URL or returns it if already an ID."""
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url_or_id)
    return match.group(1) if match else url_or_id

def load_and_clean_sheet_data(sheet_url_or_id, range_name="Sheet1"):
    """
    Fetches data from a Google Spreadsheet using the Sheets API.
    Provides basic data cleaning (removing empty rows/columns).
    """
    sheet_id = extract_sheet_id(sheet_url_or_id)
    
    # 1. Authenticate and build service
    api_key = os.environ.get("GOOGLE_API_KEY")
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    
    try:
        if creds_path and os.path.exists(creds_path):
            creds = service_account.Credentials.from_service_account_file(
                creds_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            service = build('sheets', 'v4', credentials=creds)
        elif api_key:
            service = build('sheets', 'v4', developerKey=api_key)
        else:
            raise ValueError("No authentication method found. Please set GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS in .env.")
            
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
        values = result.get('values', [])
        
        if not values:
            raise ValueError("No data found in the specified range.")
            
        # 2. Convert to Pandas DataFrame
        headers = values[0]
        data = values[1:]
        
        # Handle rows that might have fewer columns than the header
        processed_data = []
        for row in data:
            row_dict = {}
            for i, header in enumerate(headers):
                val = row[i] if i < len(row) else ""
                row_dict[header] = val
            processed_data.append(row_dict)
            
        df = pd.DataFrame(processed_data)
        
        # 3. Data Cleaning
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        # Drop completely empty rows and columns
        df.dropna(how='all', inplace=True)
        df.dropna(axis=1, how='all', inplace=True)
        # Fill NaN with empty string
        df.fillna("", inplace=True)
        
        return df

    except Exception as e:
        raise RuntimeError(f"Error fetching sheet data: {str(e)}")
