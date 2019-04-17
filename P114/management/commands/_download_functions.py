"""
Helper functions for managing P114 file downloads

"""
import datetime as dt
import urllib.request
import gzip
import os.path
import json
import requests
from ElexonDataManager.settings import ELEXON_KEY, P114_INPUT_DIR, P114_LIST_URL, P114_DOWNLOAD_URL

def get_filenames_for_date(p114_date):
    """

    """
    response = requests.get(P114_LIST_URL.format(ELEXON_KEY,
                                                 P114_date.year,
                                                 P114_date.month,
                                                 P114_date.day))
    json_data = json.loads(response.text)
    return json_data.items()
