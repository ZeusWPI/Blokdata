from .sheet_data import google_sheet_to_json

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_caching import Cache

import configparser

# Setup Flask app
app = Flask(__name__)

# Add CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Add caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Read the config file
CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")

SPREADSHEET_ID = CONFIG["Google"]["SHEET_ID"]
RANGE_NAME = CONFIG["Google"]["RANGE_NAME"]
CACHE_TIMEOUT = int(CONFIG["Cache"]["TIMEOUT"])

@app.route('/data.json')
@cache.cached(timeout=CACHE_TIMEOUT)
@cross_origin()
def data_json():
    return google_sheet_to_json(SPREADSHEET_ID, RANGE_NAME)

if __name__ == "__main__":
    app.run()
