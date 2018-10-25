import datetime as dt
import downloadFunctions as dF
import urllib.request
import socket
import configparser

startDate = dt.date(2018,9,15)
endDate = dt.date(2018,9,15)

config = configparser.ConfigParser()
config.read('config.ini')

filename_list = dF.getTibcoDailyFilenames(startDate, endDate)

print(filename_list)

print(socket.gethostname())

print(config[socket.gethostname()]['host'])

urllib.request.urlretrieve('https://downloads.elexonportal.co.uk/bmradataarchive/download?key=8bjll9hlkqh7gb8&filename=tib_messages.2018-09-15.gz',config[socket.gethostname()]['dataDirectory']+'test')


for filename in filename_list:
    try:
        remote_url = (config['Elexon']['urlBase']
            + '?key='
            + config['Elexon']['key']
            + '&filename='
            + filename)
        urllib.request.urlretrieve(
            remote_url,
            config[socket.gethostname()]['dataDirectory'] + filename)
        print('Downloading:' + filename)
    except:
        print('Failed to Open URL: ' + remote_url)


#https://downloads.elexonportal.co.uk/bmradataarchive/download?key=8bjll9hlkqh7gb8&filename=tib_messages.2018-09-15.gz
#https://downloads.elexonportal.co.uk/bmradataarchive/download?key=8bjll9hlkqh7gb8&filename=tib_messages.2018-01-01.gz
