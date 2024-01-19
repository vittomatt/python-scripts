#!/usr/bin/env python3

import signal
import sys
import requests
from termcolor import colored
from googleapiclient.discovery import build

SPREADSHEET_ID = '1-OrwfbOn54ouHVKogaFJ2M44PWNVH51TafsS7RpFpBw'
RANGE_NAME = 'Sheet1!A1:A2'
API_KEY = 'AIzaSyBbbvoqsxHDOHMvwOpBer3xpqI8zfCZAVc'

def def_handler(sig, frame):
    print(colored('Exiting...', 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def main():
    sheets = authenticate_sheets(API_KEY)
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print(f'Values: {values}')
             
def authenticate_sheets(api_key):
    return build('sheets', 'v4', developerKey=api_key).spreadsheets()

if __name__ == '__main__':
    main()
