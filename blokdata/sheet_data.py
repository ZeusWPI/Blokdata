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
    errors = []
    for i, row in enumerate(data[1:]):
        try:
            point = create_point(i+1, row)
            if point is not None:
                ret.append(point)
        except Exception as e:
            errors.append({ "type": "error", "row": i+1, "message": "\n".join(e.args) })
    return json.dumps({ "points": ret, "errors": errors })

def create_point(rowIndex, rowContent):
    if (len(rowContent) < 19):
        raise Exception(f"Row {rowIndex} does not have the correct format.", f"It is too short: a length of 19 was expected, but the length found was {len(rowContent)}.")

    #    0    1    2     3        4         5          6        7  8  9  10 11 12 13 14     15             16    17          18
    active, lat, lon, name, address, capacity, startdate, enddate, _, _, _, _, _, _, _, extra, location_type, wifi, wheelchair = rowContent[0:19]

    if active == "FALSE":
        return None

    hours = [x.replace("</br>", "\n") for x in rowContent[8:15]]

    try:
        coordinates = [f"{parse_coordinate(lon)}", f"{parse_coordinate(lat)}"]
    except Exception as a:
        raise Exception(f"Row {rowIndex} does not have the correct format.", f"One of the coordinates failed to parse.", *a.args)

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coordinates,
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
            "wheelchair": (wheelchair.lower() == "ja"),
            "wifi": (wifi.lower() == "ja"),
        }
    }

# Function to parse a coordinate
# Should be able to handle both English and Dutch locales
# If it can't parse the number, throw a clear error
def parse_coordinate(coord):
    if coord == "":
        raise Exception("Coord value is empty.")

    comma_fixed_coord = coord.replace(",", ".")

    try:
        return float(comma_fixed_coord)
    except:
        raise Exception(f"Coord is not a float: {comma_fixed_coord}")