import datetime as dt

def getTibcoDailyFilenames(date_start, date_end = None):
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
            str(curr_date.year)
            +'-'+str('%02d' %(int(curr_date.month),))
            +'-'+str('%02d' %(int(curr_date.day),))+'.gz')
        curr_date += dt.timedelta(days=1)

    return filename_list


def downloadTibcoDailyFile(dateIn, urlBase, fileBase):
    """ Function to download Tibco Relay data from elexon and parse it to base raw format in MySQL database """

    ##1 download and open data from Elexon
    #Add specified data onto the base URL
    dateStr = str(dateIn.year)+'-'+str('%02d' %(int(dateIn.month),))+'-'+str('%02d' %(int(dateIn.day),))+'.gz'
    url1 = urlBase+dateStr
    fileName = fileBase+dateStr
    #Try downloading file
    try:
        u = urllib.request.urlopen(url1)
        urllib.request.urlretrieve(url1, fileName)
        print('Downloading:'+dateStr)
    except:
        print('Failed to Open URL: '+url1)
        l = len(url1)
        return 1
    return 0
