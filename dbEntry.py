import sys
sys.path.append('D:\\USERS\\seb09186\\ShareFile\\My Files & Folders\\python\\libraries\\sg')

import datetime
from bmraTimes import bmraDT 

""" This set of functions carries out various processes involved in processing 
    BMRA data from the orginal flat-files into databaseds. This includes: 
    
    splitMessage: Takes the message part of a flat-file entry and splits it into two 
    lists: fieldsa and value
    
    dtStringToDT: Converts a data-time string given in the flat files into a Python Date Time
    object
    
    enterBMphys: Takes one of the following types of message relevant to a specific BMU and adds it to the 
    relevant table in the database: FPN, QPN, MEL, MIL
    
    There are other functions simialr to enterBMphys for entereing other BMUnit specific data: Bid Offers, 
    Bid Offers Accepted and Cash Flows
    
    
    Content: 
Functions for main BMU info:
    1. enterBMphys (Enter Physical data including FPNs, QPN, MEL and MIL)
    2. enterBMbod (Enter the Bids and offers from BM Units)
    3. enterBMboal (Enter the Bid Offer Levels - the instruction from NG as to what level to generate within the submitted bids and offers)
    4. enterBMboav (Enter the total energy per bid-offer pair, per settlement period)
    5. enterBMebocf (Enter the total cash flow by bid-offer pair, per settlement period)
Functions for BMU dynamic data
    6. enterBMdyn2 (Enters Dynamic unit data which comes in the format time: value. This is: 'NDZ', 'NTO', 'NTB', 'MZT', 'MNZT', 'SEL', 'SIL', 'MDV', 'MDP'
    7. enterBMdynRates (Enters Dynamic rate limits for units - Max Ramp Up and Down Rates)
Support Function
    8. splitMessage (Takes message in flat format and splits into to lists: Fields and Value)
    9. dtStringToDT (Converts BMRA string which represents a data and creates a datetime object)
"""


#### 1. enterBMphys (Enter Physical data including FPNs, QPN, MEL and MIL) #####


def enterBMphys(bmu, mType, tr, gmt, mess, cur):
    ## Define Querry
    table = "INSERT INTO tibcodata."+mType.lower()
    
    
    q2 = """
    (bmu_id, recieved, settlement_day, settlement_period, start_time, start_level, end_time, end_level)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    insertQuery = table+q2
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)
    
    #define Dates and times
    sDate = mV[0]
    
    sPeriod =  mV[1]
    
    #Check in GMT

                
    #For each pair of values
    for i in range(0,int(mV[2])-1):
        
        #Etract relevant data
        sTime = mV[3+(2*i)]
        sLevel = mV[4+(2*i)]
        eTime = mV[5+(2*i)]
        eLevel = mV[6+(2*i)]
        
        #Pull together data for query
        queryData = [bmu, tr, sDate, sPeriod, sTime, sLevel, eTime, eLevel] 
        
        #carry out querry
        try: 
            cur.execute(insertQuery, queryData)
        except: 
            print('Not able to insert '+mType+' data')
            print(mess)

        
    return 1


#### 2. enterBMbod (Enter the Bids and offers from BM Units) #####

        
def enterBMbod(bmu, mType, tr, gmt, mess, cur):
    ## Database Query
    table = "INSERT INTO tibcodata."+mType.lower()
    q2 = """
    (bmu_id, recieved, settlement_day, settlement_period, bod_no, offer_price, bid_price, start_time, start_level, end_time, end_level)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    insertQuery = table+q2
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)
    #define Dates and times
    sDate = mV[0]
    sPeriod =  mV[1]

    #Prices
    bodN = mV[2]
    OP = mV[3]
    BP = mV[4]

    #For each pair of times/values
    for i in range(0,int(mV[5])-1):
        #Etract relevant data
        sTime = mV[6+(2*i)]
        sLevel = mV[7+(2*i)]
        eTime = mV[8+(2*i)]
        eLevel = mV[9+(2*i)]
        
        #Pull together data for query
        queryData = [bmu, tr, sDate, sPeriod, bodN, OP, BP, sTime, sLevel, eTime, eLevel] 
        #execute query
        try: 
            cur.execute(insertQuery, queryData)
        except: 
            print('Not able to insert '+mType+' data')

    return 1

######3. enterBMboal (Enter the Bid Offer Levels - the instruction from NG as to what level to generate within the submitted bids and offers) #####

def enterBMboal(bmu, mType, tr, gmt, mess, cur):
    """ This version has the added complication that Bid Offer Acceptances don't adhear to trading periods
        As such, given that the databased is designed based on trading periods, each bid-offer acceptance 
        that ocvers muliple trading periods will be divided so that there is an individual entry based on the
        trading period. This will be carried out by the creating a bmraDT object and using the assotiated
        function in bmraTimes. 
        
        For any bid offer acceptance where two spot times are in different trading periods there will be
          1. One Entry from the "BOA start time" until the end of that trading period
          2. One Entry for each trading period fully insider the period from "BOA start time" to "BOA end time"             
             This entry will have an "entry start time" of the start of the trading period and 
             an "entry end time" of the end of that trading period 
          3. One Entry from the start of the final trading period until the "BOA end time"
          
        There will therefore be N entries where N is the number of trading periods covered 
        (inclusive of start and end periods)
    """
    ## Database Query
    table = "INSERT INTO tibcodata.boal"
    q2 = """
    (bmu_id, recieved, settlement_day, settlement_period, acceptance_no, acceptance_time, start_time, start_level, end_time, end_level, so_flag, deemed_flag, stor)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    insertQuery = table+q2
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)
    
    #Fixed no matter the duration -  THIS CAN BE RETURNED TO LATER
    if mType == 'BOAL':
        mF.insert(1, 'SO')
        mF.insert(3, 'AD')
        mV.insert(1, None)
        mV.insert(3, None)
    boaN = mV[0]
    if mV[1] == 'T': soFlag = str(1) 
    else: soFlag = str(0)
    if mV[3] == 'T': deemedFlag = str(1) 
    else: deemedFlag = str(0)
    
    ## Note that on the 5th November 2015 when the P305 change occured an extra flag was added to the BOALF variable to identify if an action is taken as a STOR action. 
    ## A column was added to the database during November 2015 to track this. It should contain null values for all actions pre 5th November 2015, and contain either 1 or 0 for all actions after
    if mF[2] =='PF':
        mF.append(mF.pop(2))
        mV.append(mV.pop(2))
        if mV[-1] == 'T': stor = str(1)
        else: stor = str(0)
    else:
        stor = None
    TA = mV[2]
    
    ## For each pair of spot times
    
    #For each pair of times/values
    for i in range(0,int(mV[4])-1):
        
        sTime_bmraDT = bmraDT.from_dt(mV[5+(2*i)])
        sLevel = float(mV[6+(2*i)])
        eTime_bmraDT = bmraDT.from_dt(mV[7+(2*i)])
        eLevel =float(mV[8+(2*i)])
        
        dTimes, dLevels = bmraDT.interpolate(sTime_bmraDT, sLevel, eTime_bmraDT, eLevel)
    
        for t in range(0,len(dTimes)-1): 
            sDateI = dTimes[t].sd
            sPeriodI = dTimes[t].sp
            sTimeI = dTimes[t].datetime
            sLevelI = dLevels[t]
            eTimeI = dTimes[t+1].datetime
            eLevelI = dLevels[t+1]
            
            queryData = [bmu, tr, sDateI, sPeriodI, boaN, TA, sTimeI, sLevelI, eTimeI, eLevelI, soFlag, deemedFlag, stor]
        
        
            #execute query
            try: 
                cur.execute(insertQuery, queryData)
            except: 
                print('Not able to insert '+mType+' data')
                print(mess)
                
    return 1
            
            

#####  4. enterBMboav (Enter the total energy per bid-offer pair, per settlement period) ####
            
def enterBMboav(bmu, mType, tr, gmt, mess, cur):
    ## Define Querry
    table = "INSERT INTO tibcodata.boav"
    
    
    q2 = """
    (bmu_id, recieved, settlement_day, settlement_period, bo_pair, offer_vol, bid_vol, short_flag)
    VALUES
    (%s, %s, %s, %s, %s, %s,%s, %s)
    """
    
    insertQuery = table+q2
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)
    
    #define Dates and times
    sDate = mV[0]
    
    sPeriod =  mV[1]
    
    
    #Check in GMT
            
    bon = mV[2]
    offVol = mV[4]
    bidVol = mV[5]
    if len(mV) == 7:
        if mV[6] =='L' : shortFlag = 0
        elif mV[6] =='S' : shortFlag = 1
        else: shortFlag = None   
    else:
        shortFlag = None
    
    #Pull together data for query
    queryData = [bmu, tr, sDate, sPeriod, bon, offVol, bidVol, shortFlag] 
        
        #carry out querry
    try: 
        cur.execute(insertQuery, queryData)
    except: 
        print('Not able to insert '+mType+' data')
        print(mess)

        
    return 1
    

##### 5. enterBMebocf (Enter the total cash flow by bid-offer pair, per settlement period) #######

def enterBMebocf(bmu, mType, tr, gmt, mess, cur):
    ## Define Querry
    table = "INSERT INTO tibcodata.ebocf"
    
    
    q2 = """
    (bmu_id, recieved, settlement_day, settlement_period, bo_pair, offer_cf, bid_cf)
    VALUES
    (%s, %s, %s, %s, %s, %s,%s)
    """
    
    insertQuery = table+q2
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)
    
    #define Dates and times
    sDate = mV[0]
    
    sPeriod =  mV[1]
    

    #Check in GMT
            
    bon = mV[2]
    offcf = mV[3]
    bidcf = mV[4]           
    
    #Pull together data for query
    queryData = [bmu, tr, sDate, sPeriod, bon, offcf, bidcf] 
        
    #carry out querry
    try: 
        cur.execute(insertQuery, queryData)
    except: 
        print('Not able to insert '+mType+' data')
        print(mess)

        
    return 1
    
    
    
    ### DYNAMIC DATA !!!!!!
 
 #######  6. enterBMdyn2 (Enters Dynamic unit data which comes in the format time: value. This is: 'NDZ', 'NTO', 'NTB', 'MZT', 'MNZT', 'SEL', 'SIL', 'MDV', 'MDP')  #####
 
 
    
def enterBMdyn2(bmu, mType, tr, gmt, mess, cur):
    ## Define Querry
    table = "INSERT INTO tibcodata."+mType.lower()
    
    
    q2 = '(bmu_id, recieved, effective_from, '+mType.lower()+') VALUES (%s, %s, %s, %s)'
    
    insertQuery = table+q2
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)
    
    if mV[0][-4:] == ':GMT':
        mV[0] = mV[0][:-4]
    
    queryData = [bmu, str(tr), str(mV[0]), str(mV[1])]
    
    try: 
        cur.execute(insertQuery, queryData)
    except: 
        print('Not able to insert '+mType+' data')
        print(mess)

        
    return 1
        

#####  7. enterBMdynRates (Enters Dynamic rate limits for units - Max Ramp Up and Down Rates) ####
        
def enterBMdynRates(bmu, mType, tr, gmt, mess, cur):
    
    #Preprocess table to use
    
    t = mType[:-1].lower()
    inout = mType[-1].lower()
    
     ## Define Querry
    table = "INSERT INTO tibcodata."+t
    q2 = '(bmu_id, recieved, effective_from, rate_1, elbow_2, rate_2, elbow_3, rate_3, import) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    insertQuery = table+q2
    
    #Split message into parts 
    
    mF, mV = splitMessage(mess)

    #remove 'GMT' from end of time if required 
    
    if mV[0][-4:] == ':GMT':
        mV[0] = mV[0][:-4]
    
    # Vector of rates and elbows
    
    re = [None] * 5
    
    for i, v in enumerate(mV[1:]):
        re[i] = v
    
    queryData = [bmu, tr, mV[0]] + re + [inout]
    
    try: 
        cur.execute(insertQuery, queryData)
    except: 
        print('Not able to insert '+mType+' data')
        print(mess)

        
    return 1
    
  
  
  ######  8. splitMessage (Takes message in flat format and splits into to lists: Fields and Value) #####
    
def splitMessage(mess):
    """ Takes a BM relevant message and splits into a list of fields and a list of values """
    message = mess.split(',')
    fields = []
    values = []
    for m in message:
        ms = m.split('=')
        fields.append(ms[0])
        if fields[-1] =='SD':
            values.append(dtStringToDT(ms[1],0))
        elif fields[-1] in ['TS', 'TA']:
            values.append(dtStringToDT(ms[1],1))
        else:
            values.append(ms[1])
    return fields, values

##############   9. dtStringToDT (Converts BMRA string which represents a data and creates a datetime object) #######

def dtStringToDT(dtS, type):
    """ Type to be 0 for date or 1 for date and time """
    dtL = dtS.split(':')
    if type == 0:
        dtDt = datetime.datetime(year=int(dtL[0]), month=int(dtL[1]), day=int(dtL[2]))
    else: 
        dtDt = datetime.datetime(year=int(dtL[0]), month=int(dtL[1]), day=int(dtL[2]), hour=int(dtL[3]), minute=int(dtL[4]), second=int(dtL[5]))
    return dtDt
    
