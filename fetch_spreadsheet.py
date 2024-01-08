from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd
import json
import os

# Constants

SPREADSHEET_ID = '1l7rJg5KgztDPjFVIuQn5PAmpPujJLqgMlIXSjWqjtd4' 
RANGE_NAME = 'hdxgruesa2021!A:FW'  

def fetch_spreadsheet_data(spreadsheet_id, range_name):
    """Fetch data from a Google Spreadsheet."""
    # Set up the credentials
    creds = Credentials.from_service_account_info(json.loads(os.environ['GOOGLE_SHEETS_CREDS']), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    
    # Build the service
    service = build('sheets', 'v4', credentials=creds)
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    
    # Get the values
    values = result.get('values', '-')

    if not values:
        print('No data found.')

    return values

data = fetch_spreadsheet_data(SPREADSHEET_ID, RANGE_NAME)


# convert data to dataframe
# assuming `data` is a list of lists, where each inner list is a row of data
num_columns_in_data = len(data[1])
df = pd.DataFrame(data[1:], columns=data[0][:num_columns_in_data])
today = pd.to_datetime('today').strftime('%Y-%m-%d')
df.to_csv(f'hdxgruesa2021_v_{today}.csv', index=False)
