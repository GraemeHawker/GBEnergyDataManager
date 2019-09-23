"""
Helper functions for managing P114 file downloads

"""
import urllib.request
import os.path
import json
import requests
from GBEnergyDataManager.settings import ELEXON_KEY, P114_INPUT_DIR, P114_LIST_URL, P114_DOWNLOAD_URL
from ._upload_functions import file_to_message_list, insert_data
from ._data_definitions import PROCESSED_FEEDS, IGNORED_FEEDS
from tqdm import tqdm

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

    if len(json_data)>0:
        unrecognised_feeds = [x for x in json_data if x.split('_')[0] not in PROCESSED_FEEDS+IGNORED_FEEDS]
        if len(unrecognised_feeds)>0:
            raise ValueError('Feed type not recognised for files: '+unrecognised_feeds)
        files_to_be_processed = [x for x in json_data if x.split('_')[0] in PROCESSED_FEEDS]
        if len(files_to_be_processed)>0:
            return files_to_be_processed
    return None

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
    #print(filename)
    if not os.path.isfile(P114_INPUT_DIR + filename) or overwrite:
        remote_url = (P114_DOWNLOAD_URL.format(ELEXON_KEY, filename))
        urllib.request.urlretrieve(remote_url,
                                   P114_INPUT_DIR + filename)

def process_p114_date(p114_date):
    """
    Retrieves data for nominated day and processes it

    Parameters
    ----------
    p114_date : date
        the date for which filenames are to be retrieved

    Returns
    -------

    Raises
    ------
    """
    filenames = get_p114_filenames_for_date(p114_date)
    if filenames is not None:
        print('{} relevant files found'.format(len(filenames)))
        for filename in tqdm(filenames):
            get_p114_file(filename, overwrite=True)
            insert_data(file_to_message_list(filename))
    else:
        print('No relevant files found')
