import gzip
import pymysql
import dbEntry as db
import dbEntry_SYSTEM as sdb
import tibcoDownloads as tdl
import bmDayToExcel_3 as bmExcel_3
import datetime as dt
import os
import re


""" SCRIPT TO AUTOMATICALLY UPDATE THE VARIOUS BALANCING MECHANISM DATABASES . UPDATED TO DOWNLOAD HALF HOURLY"""

### Initial housekeeping

addBMU = """
INSERT INTO tibcodata.bmu (bmu_id) VALUES (%s)
"""

fetchMels = """
SELECT GREATEST(start_level,end_level)
FROM tibcodata.mel
WHERE
bmu_id = %s AND
settlement_day = %s AND
settlement_period = %s
"""

writePeriodMel ="""
INSERT INTO p114data.periodmel (bmuId, settlementDay, settlementPeriod, settlementDateTime, periodMel)
VALUES (%s, %s, %s, %s, %s)
"""

bmuL = [] #List of existing BMUs in database

urlBase = 'https://downloads.elexonportal.co.uk/bmradataarchive/download?key=***REMOVED***&filename=tib_messages_hh.'
dataDirectory = 'D:\\bmrs\\'
proccesedDirectory = 'D:\\bmrs processed\\'


failedToInsert = [] # log of records which could not be inserted into the database
downloadErrors = []

rowCount = 0
nFails = 0


#Open database connection
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='***REMOVED***', db='tibcodata')
cur = conn.cursor()

connSys = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='***REMOVED***', db='tibcosystem')
curSys = connSys.cursor()

#Errors and logs
errorLog = []  #Complete list of lines that did not insert
tDownloadFails = 0  #Total Failures to insert

##Get list of existing BMUs

cur.execute("SELECT bmu_id FROM tibcodata.bmu")

bmuL=[]


for bmu in cur.fetchall(): 
    bmuL.append(bmu[0])
    
    


## Get dates to update

# Look up latest file processed
processedFiles = os.listdir(proccesedDirectory)
processedFiles.sort()
lastProcessedDate = processedFiles[-1][-25:-15]
lastProcessedDate = dt.datetime.strptime(lastProcessedDate,'%Y-%m-%d').date()

# Look up todays date
today = dt.date.today()
#today = dt.date(2015,11,5)
yesterday = today - dt.timedelta(days=1)
# Calcualte list of dates to update (By default should only be today) if ongoing automatic processing is working
datesToProcess = [lastProcessedDate + dt.timedelta(days=d) for d in range((today - lastProcessedDate).days+1)]


## Download files

for d in datesToProcess:
     err = tdl.tibcoDownloadHH(d, urlBase, dataDirectory, proccesedDirectory)
     downloadErrors.append(err)
     if err == 1:
         tDownloadFails += 1
    
    
    
## For each HH folder downloaded
for dfile in os.listdir(dataDirectory):
    f = gzip.open(dataDirectory+dfile,'rb')
    file_content = f.read().decode('utf-8','ignore')
    dataArray = [entry for entry in file_content.split('}')]
    le = len(dataArray)
    tm = dt.datetime.now()
    print(dfile+' HH contains: '+str(le)+' rows. Time is: '+str(tm.time()))
    t=0
    rowCount = 0
    
    for r in dataArray:
        rowCount += 1
        #print(rowCount)
        #Check if row is empty (will usually designate end of the file)
        if r not in ('', '\n', '\r\n'):
            #If line starts with newline character: remove
            if r[0:1] is '\n': r = r[1:]
            if r[0:2] == '\r\n': r = r[2:]
            recieved = r[0:19]
            gmt = r[20:23]
            subject  =  r[r.find('subject=')+8:r.find(',',r.find('subject=')+8,len(r))]
            message  =  r[r.find('message={')+9:len(r)]
            subjectPart = subject.split('.')
            
            if gmt != 'GMT':
                print('hold')
                
            e = 1
    ##          Process BMU specific data
            if subjectPart[1] == 'BM':
                subjectShort = subjectPart[2:]
            
                # Check if BMU ID already existists in database
                if subjectShort[0] not in bmuL:
                    try:
                        cur.execute(addBMU, subjectShort[0])
                        bmuL.append(subjectShort[0])
                    except: 
                        print('Cant insert new BMU into Database')
    
            
                
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
    

## Prcess system data
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
                    

    ## Update Period Mels in the p114 database



    #Committ Values
    conn.commit()
    connSys.commit()
    f.close()
    os.rename(dataDirectory+dfile, proccesedDirectory+dfile)
    
bmuQuerry = """SELECT bmu_id from bmu WHERE bmu_id LIKE 'T_%' OR bmu_id LIKE 'E_%'OR bmu_id LIKE 'M_%' """

cur.execute(bmuQuerry)
bmus = cur.fetchall()

bmuL = []
for b in bmus: 
    bmuL.append(b[0])


reviewFolder = "D:\\USERS\\***REMOVED***\\ShareFile\\My Files & Folders\\BM Daily Reviews\\csv\\"

bmExcel_3.createDailyCsv(bmuL, yesterday, cur, curSys, reviewFolder)

