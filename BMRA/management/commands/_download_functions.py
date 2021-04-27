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

def download_bmra_file(filename, overwrite):
    """
    downloads single BMRA file corresponding to given filename
    checks if file already exists, does not download if so

    Parameters
    ----------
    filename : str
        the filename to be downloaded

    overwrite: bool
        whether to overwrite existing files

    """
    from GBEnergyDataManager.settings import ELEXON_BASEURL, ELEXON_KEY, BMRA_INPUT_DIR

    if (not os.path.isfile(BMRA_INPUT_DIR + filename)) or (os.path.isfile(BMRA_INPUT_DIR + filename and overwrite)):
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
    download_bmra_file(filename, True)
    file = gzip.open(BMRA_INPUT_DIR + filename, 'rb')
    file_content = file.read().decode('utf-8', 'ignore')
    file_rows = [entry for entry in file_content.split('}')]
    count = 0
    combined_insert_log = {'new_bmus' : [],
                           'inserts' : {},
                           'unprocessed_msg' : {},
                           'duplicate_msg' : {},
                           }
    for message in file_rows:
        if len(message.strip()) > 0:
            message_dict = message_to_dict(message+'}')
            if message_dict is not None:
                if message_dict['message_subtype'] not in []:
                    insert_log = insert_data(message_dict)
                    if 'new_bmu' in insert_log:
                        combined_insert_log['new_bmus'].append(insert_log['new_bmu'])
                    if 'new_entries' in insert_log:
                        for key,value in insert_log['new_entries'].items():
                            if key in combined_insert_log['inserts']:
                                combined_insert_log['inserts'][key] += value
                            else:
                                combined_insert_log['inserts'][key] = value
                    if 'unprocessed_msg' in insert_log:
                        for key,value in insert_log['unprocessed_msg'].items():
                            if key in combined_insert_log['unprocessed_msg']:
                                combined_insert_log['unprocessed_msg'][key] += value
                            else:
                                combined_insert_log['unprocessed_msg'][key] = value
                    if 'duplicate_msg' in insert_log:
                        for key,value in insert_log['duplicate_msg'].items():
                            if key in combined_insert_log['duplicate_msg']:
                                combined_insert_log['duplicate_msg'][key] += value
                            else:
                                combined_insert_log['duplicate_msg'][key] = value
            count += 1
    combined_insert_log['count'] = count
    file.close()
    return combined_insert_log
