"""
Helper functions for managing downloads

"""
import datetime as dt
import urllib.request
import gzip
import os.path
from django.db import transaction
from tqdm import tqdm

from ._upload_functions import message_to_dict, insert_data

def get_tibco_daily_filenames(date_start, date_end=None):
    """
    Generates filenames for daily tibco files between two dates (inclusive)
    if no end date specified, only returns single filename for given date

    Example url:
https://downloads.elexonportal.co.uk/bmradataarchive/download?\
key=INSERT_KEY&filename=tib_messages.2018-09-15.gz

    Parameters
    ----------
    date_start : datetime
        the date of the first filename to be generated
    date_end : datetime
        the date of the last filename to be generated

    Returns
    -------
    list
        list of strings containing filenames for daily files

    Raises
    ------

    """

    if date_end is None:
        date_end = date_start

    filename_list = []
    curr_date = date_start
    while curr_date <= date_end:
        filename_list.append(
            'tib_messages.'
            +str(curr_date.year)
            +'-'+str('%02d' %(int(curr_date.month),))
            +'-'+str('%02d' %(int(curr_date.day),))+'.gz')
        curr_date += dt.timedelta(days=1)

    return filename_list

def download_bmra_file(filename):
    """
    downloads single BMRA file corresponding to given filename
    checks if file already exists, does not download if so

    Parameters
    ----------
    filename : str
        the filename to be downloaded

    """
    from GBEnergyDataManager.settings import ELEXON_BASEURL, ELEXON_KEY, BMRA_INPUT_DIR

    if not os.path.isfile(BMRA_INPUT_DIR + filename):
        remote_url = (ELEXON_BASEURL
                      + '?key='
                      + ELEXON_KEY
                      + '&filename='
                      + filename)
        urllib.request.urlretrieve(
            remote_url,
            BMRA_INPUT_DIR + filename)

@transaction.atomic #all succeeds for single day or rollback
def process_bmra_file(date):
    """
    downloads and processes single BMRA file corresponding to given date

    Parameters
    ----------
    date : datetime
        the date of the datafile to be downloaded and processed
    """
    from GBEnergyDataManager.settings import BMRA_INPUT_DIR


    filename = get_tibco_daily_filenames(date)[0]
    download_bmra_file(filename)
    file = gzip.open(BMRA_INPUT_DIR + filename, 'rb')
    file_content = file.read().decode('utf-8', 'ignore')
    file_rows = [entry for entry in file_content.split('}')]
    count = 0
    for message in tqdm(file_rows):
        if len(message.strip()) > 0:
            message_dict = message_to_dict(message+'}')
            if message_dict is not None:
                insert_data(message_dict)
            count += 1
    file.close()
