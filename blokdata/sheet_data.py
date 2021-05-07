from apiclient.discovery import build
from httplib2 import Http
from google.oauth2 import service_account
import json

def get_google_sheet(spreadsheet_id, range_name):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    credentials = service_account.Credentials.from_service_account_file('service_account.json')
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=scoped_credentials)

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet

def google_sheet_to_json(spreadsheet_id, range_name):
    sheet = get_google_sheet(spreadsheet_id, range_name)
    data = sheet["values"]
    ret = []
    for row in data[1:]:
        point = create_point(row)
        if point is not None:
            ret.append(point)
    return json.dumps(ret)

def create_point(row):
    if (len(row) < 19):
        return None

    #    0    1    2     3        4         5          6        7  8  9  10 11 12 13 14     15             16          17    18
    active, lat, lon, name, address, capacity, startdate, enddate, _, _, _, _, _, _, _, extra, location_type, wheelchair, wifi = row[0:19]

    if active == "FALSE":
        return None

    hours = [x.replace("</br>", "\n") for x in row[8:15]]

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
            # We give dict an iterable of pairs, dict gives us a dict
            "hours": dict(zip(
                ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
                hours
            )),
            "extra": extra,
            "type": location_type,
            "wheelchair": wheelchair,
            "wifi": wifi,
        }
    }
