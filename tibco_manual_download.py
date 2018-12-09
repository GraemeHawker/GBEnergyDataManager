"""
Manual download/process script for daily tibco files
"""

import datetime as dt
import urllib.request
import socket
import configparser
import gzip
import pymysql
import download_functions as df
import upload_functions as uf

DOWNLOAD_FILES = False  #whether to download files (True) or just process (False)
UPLOAD_TO_DB = False    #whether to process files to db (True) or not (False)

START_DATE = dt.date(2017, 4, 21)
END_DATE = dt.date(2017, 4, 21)

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')
LOCAL_CONFIG = CONFIG[socket.gethostname()]

if UPLOAD_TO_DB is True:    #connect to db
    DB_CONN = pymysql.connect(host=LOCAL_CONFIG['host'],
                              port=int(LOCAL_CONFIG['port']),
                              user=LOCAL_CONFIG['db_user'],
                              passwd=LOCAL_CONFIG['db_passwd'],
                              db=LOCAL_CONFIG['db_tibcodata'])
    DB_CURSOR = DB_CONN.cursor()

FILENAME_LIST = df.get_tibco_daily_filenames(START_DATE, END_DATE)

if DOWNLOAD_FILES is True:
    for filename in FILENAME_LIST:
        print("downloading: " + filename)
        try:
            remote_url = (CONFIG['Elexon']['urlBase']
                          + '?key='
                          + CONFIG['Elexon']['key']
                          + '&filename='
                          + filename)
            urllib.request.urlretrieve(
                remote_url,
                LOCAL_CONFIG['dataDirectory'] + filename)
            print('Downloading:' + filename)
        except urllib.error.URLError as error:
            print('Failed to Open URL: ' + remote_url +' ' + error.reason)
'''
#for the purposes of reviewing file contents
subjects = set()
tibco_types = set()
BMUIDs = set()
BM_data_types = set()
system_data_types = set()
'''

for filename in FILENAME_LIST:
    print('Processing:' + filename)
    f = gzip.open(LOCAL_CONFIG['dataDirectory'] + filename, 'rb')
    file_content = f.read().decode('utf-8', 'ignore')
    dataArray = [entry for entry in file_content.split('}')]
    for message in dataArray:
        message_dict = uf.message_to_dict(message+'}')
    f.close()

if UPLOAD_TO_DB is True:
    DB_CONN.close()
