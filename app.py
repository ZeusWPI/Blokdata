from apiclient.discovery import build
from httplib2 import Http
from google.oauth2 import service_account
import json

import configparser
CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")


SPREADSHEET_ID = CONFIG["Google"]["SHEET_ID"]
RANGE_NAME = CONFIG["Google"]["RANGE_NAME"]

def get_google_sheet():
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    credentials = service_account.Credentials.from_service_account_file('service_account.json')
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=scoped_credentials)

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    return gsheet

def google_sheet_to_json():
    sheet = get_google_sheet()
    data = sheet["values"]
    return json.dumps([create_point(row) for row in data[1:]])

def create_point(row):
    lat, lon, name, address, capacity, startdate, enddate, hours_monday, hours_tuesday, hours_wednesday, hours_thursday, hours_friday, hours_saturday, hours_sunday, extra, location_type = row
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat],
        },
        "properties": {
            "name": name,
            "address": address,
            "capacity": capacity,
            "period": {
                "start": startdate,
                "end": enddate,
            },
            "hours": {
                "monday": hours_monday,
                "tuesday": hours_tuesday,
                "wednesday": hours_wednesday,
                "thursday": hours_thursday,
                "friday": hours_friday,
                "saturday": hours_saturday,
                "sunday": hours_sunday,
            },
            "extra": extra,
            "type": location_type,
        }
    }

print(google_sheet_to_json())
