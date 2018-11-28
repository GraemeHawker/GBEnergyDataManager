"""

"""

import datetime as dt
import urllib.request
import socket
import configparser
import gzip
import pymysql
import download_functions as df
import upload_functions as uf


START_DATE = dt.date(2017, 4, 21)
END_DATE = dt.date(2018, 11, 15)

config = configparser.ConfigParser()
config.read('config.ini')
local_config = config[socket.gethostname()]


conn = pymysql.connect(host=local_config['host'],
                       port=int(local_config['port']),
                       user=local_config['db_user'],
                       passwd=local_config['db_passwd'],
                       db=local_config['db_tibcodata'])


cur = conn.cursor()

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
    le = len(dataArray)
    tm = dt.datetime.now()
    t = 0
    rowCount = 0
    for r in dataArray:
        rowCount += 1
        #print(rowCount)
        #Check if row is empty (will usually designate end of the file)
        if r not in ('', '\n', '\r\n'):
            #If line starts with newline character: remove
            if r[0:1] == '\n':
                r = r[1:]
            if r[0:2] == '\r\n':
                r = r[2:]
            received = r[0:19]
            gmt = r[20:23]
            subject = r[r.find('subject=')+8:r.find(',',
                                                    r.find('subject=')+8,
                                                    len(r))]
            message = r[r.find('message={')+9:len(r)]
            subjectPart = subject.split('.')
            subjectShort = subjectPart[2:]
            subjects.add(str(subjectPart))

            subject_list = subject.split('.')
            tibco_type = subject_list[1] #should be 'BM' or 'SYSTEM'
            tibco_types.add(tibco_type)
            if tibco_type == 'BM':
                BMUID = subject_list[2]
                BMUIDs.add(BMUID)
                BM_data_type = subject_list[3]
                BM_data_types.add(BM_data_type)
                '''
                if 'CNQPS-4' in BMUID and BM_data_type == 'FPN':
                    message_list = message.split(',')
                    print(#message_list[0].split('=')[1],
                          message_list[4].split('=')[1],
                          )
                '''
                uf.insert_bm_data(BMUID, BM_data_type, received, gmt, message, cur)
            elif tibco_type == 'SYSTEM':
                #print(subject_list)
                system_data_type = subject_list[2]
                system_data_types.add(system_data_type)
                uf.insert_system_data(message)
            elif tibco_type == 'DYNAMIC':
                BMUID = subject_list[2]
                BMUIDs.add(BMUID)
                dynamic_data_type = subject_list[1]
                uf.insert_dynamic_data(BMUID, BM_data_type, message)
            elif tibco_type == 'BP':
                pass
            else:
                raise ValueError('Tibco message subject type %s not found' % tibco_type)
    f.close()
    conn.commit()
    #connSys.commit()

#print(BM_data_types)
#print(system_data_types)




#print(sorted(BM_data_types))
"""
            if gmt != 'GMT':
                print('hold')

            e = 1
    ##          Process BMU specific data
            if subjectPart[1] == 'BM':


                # Check if BMU ID already existists in database
                if subjectShort[0] not in bmuL:
                    try:
                        cur.execute(addBMU, subjectShort[0])
                        bmuL.append(subjectShort[0])
                    except:
                        print('Can\'t insert new BMU into Database')



                # Find the table in which data must be put
                if subjectShort[-1] in ['FPN', 'QPN', 'MEL', 'MIL']:
                    e = db.enterBMphys(subjectShort[0], subjectShort[-1], recieved, gmt, message, cur)
                elif subjectShort[-2] in ['BOD']:
                    e = db.enterBMbod(subjectShort[0], subjectShort[-2], recieved, gmt, message, cur)
                elif subjectShort[-1] in ['BOALF', 'BOAL']:
                    e = db.enterBMboal(subjectShort[0], subjectShort[-1], recieved, gmt, message, cur)
                elif subjectShort[-2] in ['BOAV']:
                    e =db.enterBMboav(subjectShort[0], subjectShort[-2], recieved, gmt, message, cur)
                elif subjectShort[-2] in ['EBOCF']:
                    e =db.enterBMebocf(subjectShort[0], subjectShort[-2], recieved, gmt, message, cur)


            # Prcess system data
            elif subjectPart[1] == 'SYSTEM':
                subjectShort = subjectPart[2:]


                if subjectShort[0] in ['WINDFOR']:
                    e = sdb.enterWindForecast(recieved, message, curSys)
                elif subjectShort[0] in ['FUELHH']:
                    e = sdb.enterOutturnByFuelType(message, curSys)
                elif subjectShort[0] in ['FUELINST']:
                    e = sdb.enterOutturnByFuelTypeInst(message, curSys)
                elif subjectShort[0] in ['NDF', 'TSDF', 'MELNGC', 'IMBALNGC', 'INDGEN','INDDEM']:
                    e = sdb.enterZoneForecasts(subjectShort[0], recieved, message, curSys)
                elif subjectShort[0] in ['TEMP']:
                    e = sdb.enterTempData(message, curSys)
                elif subjectShort[0] in ['FREQ']:
                    e = sdb.enterFrequency(message, curSys)
                elif subjectShort[0] in ['INDO', 'ITSDO']:
                    e = sdb.enterDemandOutTurn(subjectShort[0], message, curSys)
                elif subjectShort[0] in ['NONBM']:
                    e = sdb.enterNonBMstor(message, curSys)
                elif subjectShort[0] in ['INDOD']:
                    e = sdb.enterEnergyOutTurn(message, curSys)
                elif subjectShort[0] in ['SYSWARN']:
                    e = sdb.enterSysWarn(message, curSys)
                elif subjectShort[0] in ['SYSMSG']:
                    e = sdb.enterSysMsg(message, curSys)
                elif subjectShort[0] in ['TBOD']:
                    e = sdb.enterSysTotalBODs(message, curSys)
                elif  subjectShort[0] in ['MID']:
                    e = sdb.enterMid(message, curSys)
                elif  subjectShort[0] in ['LOLP']:
                    e = sdb.enterLolp(message, curSys)
                elif subjectShort[0] in ['DISEBSP']:
                    e = sdb.enterDisebsp(message, curSys)
                elif len(subjectShort)>1:
                    if subjectShort[1] in ['UOU2T52W']:
                        e = sdb.eneterOC2generationData(message, subjectShort[0], recieved, cur)

# Still need to work out format of SOSO
#                elif  subjectShort[0] in ['SOSO']:
#                   e = db.enterSoSo(mess, cur)
                if e == 0:
                    print('hold')
                    input('Hold...')
                    print('holding')
"""
#https://downloads.elexonportal.co.uk/bmradataarchive/download?key=8bjll9hlkqh7gb8&filename=tib_messages.2018-09-15.gz
#https://downloads.elexonportal.co.uk/bmradataarchive/download?key=8bjll9hlkqh7gb8&filename=tib_messages.2018-01-01.gz
