import urllib.request
import csv
import gzip
import pymysql
import sys
from datetime import date, timedelta
import os
import time

""" This script to download gzfiles on the BMRA data from elexonportal website for a specified date range.
"""


def tibcoDownload(dateIn, urlBase, fileBase):
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


def tibcoDownloadHH(dateIn, urlBase, fileBase, filesProcessed):
    """ Function to download Tibco Relay data from elexon and parse it to base raw format in MySQL database """
    dateStr = str(dateIn.year)+'-'+str('%02d' %(int(dateIn.month),))+'-'+str('%02d' %(int(dateIn.day),))
    hhFileExt = listOfHHfileExtentions()
    processedFiles = os.listdir(filesProcessed)

    f = 0

    for hh in hhFileExt:
        fullFileName = dateStr+hh
        filePath = fileBase+fullFileName
        if fullFileName not in processedFiles:
            try:
                url1 = urlBase+fullFileName
                u = urllib.request.urlopen(url1)
                urllib.request.urlretrieve(url1, filePath)
                print('Downloading:'+fullFileName)
                if os.path.getsize(filePath) < 200: os.remove(filePath)
            except:
                print('Failed to Open URL: '+ulr1)
                f =+ 1

    return 0



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

if  __name__ == "__main__":
    ## Variables

    #Dates are inclusive and will download daily tibco file for each day between the two dates
    sdate = date(2015,6,10)
    edate = date(2015,11,11)

    #url
    urlBase = 'https://downloads.elexonportal.co.uk/bmradataarchive/download?key=***REMOVED***&filename=tib_messages.'

    #Folder to which gzip files are saved

    fileBase = 'D:\\bmrs Tibco Raw\\'

    #Set up list of dates to extract
    dates = []
    dates.append(edate)
    while dates[len(dates)-1] >= sdate:
        dates.append(dates[len(dates)-1] - timedelta(days =1))

    errorLog = []  #Complete list of lines that did not insert
    tFails = 0  #Total Failures to insert



    ## Loop through Days in dates varibale
    errors = []
    for d in dates:
        err = tibcoDownload(d, urlBase, fileBase)
        errors.append(err)
        if err == 1:
            tFails += 1
        #time.sleep(10)

def listOfHHfileExtentions():
    hhFiles = [ '.00.00-00.30.gz',
                '.00.30-01.00.gz',
                '.01.00-01.30.gz',
                '.01.30-02.00.gz',
                '.02.00-02.30.gz',
                '.02.30-03.00.gz',
                '.03.00-03.30.gz',
                '.03.30-04.00.gz',
                '.04.00-04.30.gz',
                '.04.30-05.00.gz',
                '.05.00-05.30.gz',
                '.05.30-06.00.gz',
                '.06.00-06.30.gz',
                '.06.30-07.00.gz',
                '.07.00-07.30.gz',
                '.07.30-08.00.gz',
                '.08.00-08.30.gz',
                '.08.30-09.00.gz',
                '.09.00-09.30.gz',
                '.09.30-10.00.gz',
                '.10.00-10.30.gz',
                '.10.30-11.00.gz',
                '.11.00-11.30.gz',
                '.11.30-12.00.gz',
                '.12.00-12.30.gz',
                '.12.30-13.00.gz',
                '.13.00-13.30.gz',
                '.13.30-14.00.gz',
                '.14.00-14.30.gz',
                '.14.30-15.00.gz',
                '.15.00-15.30.gz',
                '.15.30-16.00.gz',
                '.16.00-16.30.gz',
                '.16.30-17.00.gz',
                '.17.00-17.30.gz',
                '.17.30-18.00.gz',
                '.18.00-18.30.gz',
                '.18.30-19.00.gz',
                '.19.00-19.30.gz',
                '.19.30-20.00.gz',
                '.20.00-20.30.gz',
                '.20.30-21.00.gz',
                '.21.00-21.30.gz',
                '.21.30-22.00.gz',
                '.22.00-22.30.gz',
                '.22.30-23.00.gz',
                '.23.00-23.30.gz',
                '.23.30-00.00.gz',]

    return hhFiles
