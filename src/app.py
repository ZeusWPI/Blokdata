from sheet_data import google_sheet_to_json

from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import configparser
CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")

SPREADSHEET_ID = CONFIG["Google"]["SHEET_ID"]
RANGE_NAME = CONFIG["Google"]["RANGE_NAME"]

@app.route('/data.json')
@cross_origin()
def data_json():
    return google_sheet_to_json(SPREADSHEET_ID, RANGE_NAME)

if __name__ == "__main__":
    app.run()
