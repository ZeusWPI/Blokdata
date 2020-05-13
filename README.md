# Blokdata

Create [blokmap](https://github.com/zeuswpi/blokmap) data from a Google sheet.

## Installation

1. Setup python

```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

2. Setup `config.ini` as follows

```
[Google]

SHEET_ID = #FILLMEIN
RANGE_NAME = #METOO
```

3. [Request a Google service account](https://console.cloud.google.com/iam-admin/serviceaccounts)

4. Store the service account's key as `service_account.json`

5. Give the service account's email (read) access to the sheet

6. `python src/app.py`

## TODO

- Code cleanup: separate files
- Database caching: don't re-request google sheet data every time
- Error handling: it shouldn't ever crash on user input
