"""
Helper functions for managing P114 file downloads

"""
import urllib.request
import os.path
import json
import requests
from ElexonDataManager.settings import ELEXON_KEY, P114_INPUT_DIR, P114_LIST_URL, P114_DOWNLOAD_URL

def get_p114_filenames_for_date(p114_date):
    """
    Returns a list of p114 filenames generated on a specific date

    Parameters
    ----------
    p114_date : date
        the date for which filenames are to be retrieved

    Returns
    -------
    list
        list of strings containing filenames

    Raises
    ------


    """
    response = requests.get(P114_LIST_URL.format(ELEXON_KEY,
                                                 p114_date.year,
                                                 p114_date.month,
                                                 p114_date.day))
    json_data = json.loads(response.text)
    return json_data.items()

def get_p114_file(filename, overwrite=True):
    """
    downloads specified P114 file

    Parameters
    ----------
    filename : string
        the filename to be retrieved
    overwrite : boolean
        if the file already exists, whether to overwrite or keep

    Returns
    -------

    Raises
    ------

    """

    if not os.path.isfile(P114_INPUT_DIR + filename) or overwrite:
        remote_url = (P114_DOWNLOAD_URL.format(ELEXON_KEY, filename))
        urllib.request.urlretrieve(remote_url,
                                   P114_INPUT_DIR + filename)
