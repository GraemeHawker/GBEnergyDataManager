import sys
sys.path.append('D:\\USERS\\***REMOVED***\\ShareFile\\My Files & Folders\\python\\libraries\\sg')

import datetime
import bmraTimes as bm

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
"""




def splitMessage(mess):
    """ Takes a BM relevant message and splits into a list of fields and a list of values """
    message = mess.split(',')
    fields = []
    values = []
    for m in message:
        ms = m.split('=')
        if len(ms) == 2:
            fields.append(ms[0])
            if fields[-1] =='SD':
                values.append(dtStringToDT(ms[1],0))
            elif fields[-1] in ['TS', 'TA', 'TP']:
                values.append(dtStringToDT(ms[1],1))
            else:
                values.append(ms[1])
        elif len(ms) == 1:
            fields.append('')
            values.append(ms[0])
        else:
            fields.append('')
            values.append(''.join(st for st in ms))
        
    return fields, values


def dtStringToDT(dtS, type):
    """ Type to be 0 for date or 1 for date and time """
    dtL = dtS.split(':')
    if type == 0:
        dtDt = datetime.datetime(year=int(dtL[0]), month=int(dtL[1]), day=int(dtL[2]))
    else: 
        dtDt = datetime.datetime(year=int(dtL[0]), month=int(dtL[1]), day=int(dtL[2]), hour=int(dtL[3]), minute=int(dtL[4]), second=int(dtL[5]))
    return dtDt
    

def enterWindForecast(mr, mess, cur):
    
    insertQuery = """ 
    INSERT into tibcosystem.windforecast 
    (message_time, forecast_time, settlement_day, settlement_period, generation, installed_capacity)
    VALUES
    (%s, %s, %s, %s, %s, %s)
    """
    
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)
    
    nr = int(mV[0])
    
    
    
    for n in range(0,nr):
        ft = mV[1+(n*5)]
        sd = mV[2+(n*5)]
        sp = mV[3+(n*5)]
        gen = mV[4+(n*5)]
        cap = mV[5+(n*5)]
        
        #Remove GMT if required
        
        if mr[-3:] in ['GMT', 'gmt']:
            mr = mr[:-4]
        


    
        queryData = [mr, ft, sd, sp, gen, cap]
        
        try:
            cur.execute(insertQuery, queryData)
        except:
            print('Wind Forecast Insert Failed')
            return 0
    
    return 1
    
    
def enterOutturnByFuelType(mess, cur):
    insertQuery = """ INSERT INTO hhgenerationbyfuel (message_recieved, settlement_day, settlement_period, fuel_type, generation)
    VALUES
    (%s, %s, %s, %s, %s)  
    """
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)

    #Remove GMT if required
    


    
    queryData = [mV[0], mV[1], mV[2], mV[3], mV[4]]
    try:
        cur.execute(insertQuery, queryData)
    except:
        print('HH by fuel type insert failed')
        return 0
    
    return 1
    
    
    
def enterOutturnByFuelTypeInst(mess, cur):
    insertQuery = """ INSERT INTO instgenerationbyfuel (message_recieved, settlement_day, settlement_period, spot_time, fuel_type, generation)
    VALUES
    (%s, %s, %s, %s, %s, %s)  
    """
    
    #Split message into consituent parts
    mF, mV = splitMessage(mess)

    #Remove GMT if required




    queryData = [mV[0], mV[1], mV[2], mV[3], mV[4], mV[5]]
    try:
        cur.execute(insertQuery, queryData)
    except:
        print('Inst by fuel type insert failed')
        return 0
    
    return 1
        
    
def enterZoneForecasts(mType, mr, mess, cur):
    """ Function to process forecasts of demand, generation and imbalance that are made nationallly and zonally by NG """
    
    # Querry 
    table = "INSERT INTO tibcosystem."+mType.lower()
    
    q2 = """
    (message_recieved, zone, published_time, settlement_day, settlement_period, level)
    VALUES
    (%s, %s, %s, %s, %s, %s)
    """
    
    c1 = "SELECT count(*) FROM tibcosystem."+mType.lower()
    c2 = """
    WHERE
    published_time = %s AND
    settlement_day = %s AND
    settlement_period = %s AND
    zone = %s
    """
    checkExists = c1+c2
    
    insertQuery = table+q2
    
    mF, mV = splitMessage(mess)
    
    zone = mV[0]
    nr = int(mV[1])
    
    for n in range(0,nr):
        pt = mV[2+(n*4)]
        sd = mV[3+(n*4)]
        sp = mV[4+(n*4)]
        lev = mV[5+(n*4)]
        
        #Remove GMT if required
        


        
        if mr[-3:] in ['GMT', 'gmt']:
            mr = mr[:-4]
        
        queryData = [mr, zone, pt, sd, sp, lev]
        checkData = [pt, sd, sp, zone]

        cur.execute(checkExists, checkData)
        ex = cur.fetchone()
        ex = ex[0]

        
        if ex == 0: 
            try:
                cur.execute(insertQuery, queryData)
            except:
                print('Zone Demand Forecast insert failed')
                return 0
    
    return 1
    
def enterTempData(mess, cur):
    insertQuery = """ INSERT INTO temp (message_received, spot_time, outturn_temp, norm_ref_temp, low_ref_temp, high_ref_temp)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        """
        
        
    #Split message into consituent parts
    mF, mV = splitMessage(mess)
    
    pt = mV[0]
    st = mV[1]
    





    
    querryData = [pt, st, mV[2], mV[3], mV[4], mV[5]]
    try:
        cur.execute(insertQuery, querryData)
    except:
        print('Temperature insert failed')
        return 0
        
    return 1

    
    
    
def enterFrequency(mess, cur):
    insertQuerry  = """INSERT INTO frequency (spot_time, freq) VALUES (%s, %s)"""
    
    mF, mV = splitMessage(mess)
    
    #Remove GMT
    

    
    querryData = [mV[0], mV[1]]
    try:
        cur.execute(insertQuerry, querryData)
    except:
        print('Frequency insert failed')
        return 0
        
    return 1
    

def enterDemandOutTurn(mType, mess, cur):
    if mType == 'INDO':
        insertQuerry = """INSERT INTO indo (message_received, settlement_day, settlement_period, level) VALUES (%s, %s, %s, %s)"""
    elif mType == 'ITSDO':
        insertQuerry = """INSERT INTO itsdo (message_received, settlement_day, settlement_period, level) VALUES (%s, %s, %s, %s)"""
    else:
        print('Incorrect MEssage Type in enterDemandOutTurn')
        return 0
    
    mF, mV = splitMessage(mess)
    
    pt = mV[0]
    sd = mV[1]
    
    querryData = [pt, sd, mV[2], mV[3]]
    try:
        cur.execute(insertQuerry, querryData)

    except:
        print('Demand outturn insert failed')
        return 0
        
    return 1
    

def enterNonBMstor(mess, cur):
    insertQuerry = """ INSERT INTO nonbmstor (message_received, settlement_day, settlement_period, level) VALUES( %s, %s, %s, %s)"""
    
    mF, mV = splitMessage(mess)
    
    pt = mV[0]


    
    querryData = [pt, mV[1], mV[2], mV[3]]
    try:
        cur.execute(insertQuerry, querryData)
    except:
        print('Non-BM insert failed')
        return 0
    return 1
    

def enterEnergyOutTurn(mess, cur):
    insertQuerry = """ INSERT INTO indod (message_received, settlement_day, energy_outturn, low_ref, high_ref, norm_ref)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
    
    mF, mV = splitMessage(mess)
    
    pt = mV[0]

    
    querryData = [pt, mV[1], mV[2], mV[3], mV[4], mV[5]]
    try:
        cur.execute(insertQuerry, querryData)
    except:
        print('Energy Demand insert failed')
        return 0
        
    return 1

def enterSysWarn(mess, cur):
    insertQuerry = """ INSERT INTO systemwarnings (message_received, text) VALUES (%s, %s)"""
    
    mF, mV = splitMessage(mess)
    
    pt = mV[0]
    
    if len(mV) > 2:
        for m in mV[2:]:
            mV[1] = mV[1]+m
        

    
    querryData = [pt, mV[1]]
    try:
        cur.execute(insertQuerry, querryData)

    except:
        print('System Warning insert failed')
        return 0 
        
    return 1
    
def enterSysMsg(mess, cur):
    insertQuerry = """ INSERT INTO systemmessages (type, message_received, text) VALUES (%s, %s, %s)"""
   
    mF, mV = splitMessage(mess) 
    
    pt = mV[1]
    if len(mV) > 3:
        for m in mV[3:]:
            mV[2] = mV[2]+m
        
    querryData = [mV[0], pt, mV[2]]
    
    try:
        cur.execute(insertQuerry, querryData)
    except:
        print('System Messages insert failed')
        return 0
    return 1
    
    
def enterSysTotalBODs(mess, cur):
    insertQuerry = """ INSERT INTO tbod (settlement_day, settlement_period, tov, tbv) VALUES (%s, %s, %s, %s)"""
    
    
    mF, mV = splitMessage(mess)
    sd = mV[0]
 
    
    querryData = [sd, mV[1], mV[2], mV[3]]
    
    try:
        cur.execute(insertQuerry, querryData)
    except:
        print('System Total BODS insert failed')
        return 0
    return 1
    
def enterMid(mess, cur):
    insertQuerry = """INSERT INTO mid (provider, settlement_day, settlement_period, mip, miv) VALUES (%s, %s, %s, %s, %s)"""
    
    mf, mV = splitMessage(mess)
    sd = mV[1].date()


    querryData = [mV[0], sd, mV[2], mV[3], mV[4]]
    
    try:
        cur.execute(insertQuerry, querryData)
    except:
        print('MID insert failed')
        return 0 
    return 1



def enterLolp(mess,cur):
    insertQuerry = """INSERT INTO lolp (message_received, settlement_day, settlement_period, lolp, derated_gen_margin) VALUES (%s, %s,%s, %s, %s)"""
    
    mF, mV = splitMessage(mess)
    
    n = int(mV[1])
    
    for i in range(0,n):
        sd = mV[2+(i*4)]
        sp = mV[3+(i*4)]
        lolp = mV[4+(i*4)]
        drm = mV[5+(i*4)]
        
        querryData = [mV[0], sd, sp, lolp, drm]
        
        try:
            cur.execute(insertQuerry, querryData)
        except:
            print("LOLP insert failed")
            return 0
        
    return 1
    

def enterDisebsp(mess, cur):
    insertQuerry = """
    INSERT INTO disebsp 
    (settlement_day, 
    settlement_period, 
    buy_price, 
    sell_price, 
    price_code, 
    reserve_scarcity_price, 
    replacement_price, 
    replacement_vol, 
    bdsa_default,
    sp_adjustment, 
    bp_adjustement, 
    niv, 
    total_system_accepted_offer_vol, 
    total_system_accepted_bid_vol,  
    total_system_tagged_acceptaned_offer_vol, 
    total_system_tagged_acceptaned_bid_vol,  
    system_total_priced_acceptance_offer_vol, 
    system_total_priced_acceptance_bid_vol, 
    total_system_adjustment_sell_vol,
    total_system_adjustment_buy_vol,
    total_system_tagged_adjustment_sell_vol,
    total_system_tagged_adjustment_buy_vol )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    
    
    
    mF, mV = splitMessage(mess)
    codes = ['SD', 'SP' ,'PB', 'PS', 'PD', 'RSP', 'RP', 'RV', 'BD', 'A3', 'A6', 'NI', 'AO', 'AB', 'T1', 'T2', 'PP', 'PC', 'J1', 'J2', 'J3', 'J4'] 
    dataInputs = [None for c in codes]
    
    
    for j, c in enumerate(mF): 
        if c in mF: 
            i = codes.index(c)
            try:
                dataInputs[i] = str(mV[j])
            except:
                print('hold')
    try:
        cur.execute(insertQuerry, dataInputs)
    except:
        print("failed to input DISEBSP data")
        return 0
        
    return 1
    
def eneterOC2generationData(mess, bmu, received, cur):
        insertQuerry="""
        INSERT INTO oc2bmuavailability
        (message_received, 
        bmu_id,
        published_date,
        year,
        week_no,
        fuel_type,
        availability)
        VALUES (%s, %s, %s, %s, %s, %s, %s) """
        
        mF, mV = splitMessage(mess)
        
        if mF[1] == 'NR':
            nr = int(mV[1])
        else:
            print('hold')
        
        for n in range(0,nr):
            week = mV[2+(4*n)]
            year = mV[3+(4*n)]
            fuel = mV[4+(4*n)]
            output = mV[5+(4*n)]
            
            dataInput = [received, bmu, mV[0], year, week, fuel, output]
            
            try:
                cur.execute(insertQuerry, dataInput)
            except:
                print("failed to input OC2 data")
                return 0
        return 1
                    
