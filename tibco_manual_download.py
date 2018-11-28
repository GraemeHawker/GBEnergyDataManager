"""

"""

import datetime as dt
import urllib.request
import socket
import configparser
import gzip
#import pymysql
import download_functions as df
import upload_functions as uf


START_DATE = dt.date(2017, 4, 21)
END_DATE = dt.date(2017, 4, 21)

config = configparser.ConfigParser()
config.read('config.ini')
local_config = config[socket.gethostname()]
'''
conn = pymysql.connect(host=local_config['host'],
                       port=int(local_config['port']),
                       user=local_config['db_user'],
                       passwd=local_config['db_passwd'],
                       db=local_config['db_tibcodata'])
cur = conn.cursor()
'''
filename_list = df.get_tibco_daily_filenames(START_DATE, END_DATE)

'''
for filename in filename_list:
    try:
        remote_url = (config['Elexon']['urlBase']
                      + '?key='
                      + config['Elexon']['key']
                      + '&filename='
                      + filename)
        urllib.request.urlretrieve(
            remote_url,
            local_config['dataDirectory'] + filename)
        print('Downloading:' + filename)
    except:
        print('Failed to Open URL: ' + remote_url)
'''

#for the purposes of reviewing file contents
subjects = set()
tibco_types = set()
BMUIDs = set()
BM_data_types = set()
system_data_types = set()

for filename in filename_list:
    print('Processing:' + filename)
    f = gzip.open(local_config['dataDirectory'] + filename, 'rb')
    file_content = f.read().decode('utf-8', 'ignore')
    dataArray = [entry for entry in file_content.split('}')]
    for message in dataArray:
        message_dict = uf.message_to_dict(message+'}')
    f.close()
#conn.close()
