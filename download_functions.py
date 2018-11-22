"""
Helper functions for managing downloads

"""
import datetime as dt

def get_tibco_daily_filenames(date_start, date_end=None):
    """
    Generates filenames for daily tibco files between two dates (inclusive)
    if no end date specified, only returns single filename for given date

    Parameters
    ----------
    date_start : datetime
        the date of the first filename to be generated
    date_end : datetime
        the date of the last filename to be generated

    Returns
    -------
    list
        list of strings containing filenames for HH files

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
