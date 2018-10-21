import sys
sys.path.append('../')

import time
import datetime as dt
import pymysql
import bisect
from bmraTimes import bmraDT 
################################################################################
## Main function 1: fpnPowerSerries                                           ##
## Returns a serries of spot times and spot levels for FPN from the           ##
## tibcodata database.                                                        ##
## Spot times are at least at the start and end of each settlement period     ##
## and any intermediate points submitted                                      ##
################################################################################


def fpnPowerSeries(bmu, startDate, endDate, cur):
    """ Retrurns easily plotably time-serries of power set points 
    """
    
    ## Querry and variables
    
    dateList = [startDate + dt.timedelta(days=x) for x in range((endDate-startDate).days + 1)]
    
    fpnQuery = """ 
        Select start_time, start_level, end_time, end_level, settlement_period 
        FROM fpn 
        WHERE bmu_id = %s AND settlement_day = %s
        """
        
    countQuerry= """
        SELECT COUNT(1) FROM fpn
        WHERE bmu_id = %s AND settlement_day >= %s AND settlement_day <= %s
        """
    
    
    
    
    
    #Check if there is any data to find
    cur.execute(countQuerry, [bmu, dateList[0], dateList[-1]])
    nn = cur.fetchall()
    if nn[0][0] == 0: 
        return [], []
    
    power = []
    sDateTime = []
    
    
    ## For each day in the list find the relevant points and appends them to lists which are returned
    for d in dateList:
        try:
            cur.execute(fpnQuery, [bmu, str(d)])
        except:
            print('Failed to access data from databased in fpnPowerSerries')
            return None, 1
        
        rr = cur.fetchall()
        
        for r in rr: 
        
        
            #Only use start time and power for first entry and if there is a step change
            if len(power) is 0 or power[-1] != r[1]:
                if r[4] in [1, 2] and r[0].seconds > 82799:
                    sDateTime.append(dt.datetime.combine(d,dt.time(0))+r[0]-dt.timedelta(seconds=60*60*24))
                else: 
                    sDateTime.append(dt.datetime.combine(d,dt.time(0))+r[0])
                power.append(r[1])
    
            #And always use end time and power the rest of the time
            
            #Special case for point at the end of period 48 which requires manually adding a full day to the time serries
            #During BST the settlment periods are out of date with the listed times which remain in GMT. So the day the clocks
            #go forward their are only 46 settlment periods and 50 on the day the clocks go forward. 
            #Therefore in the sumer either the end period 46 or the start of period 47 could be out of phase of period 

            
            if r[4] in [1, 2] and r[2].seconds > 82799:
                sDateTime.append(dt.datetime.combine(d,dt.time(0))+r[2]-dt.timedelta(seconds=60*60*24))
            elif r[4] in [48, 50] and r[2].seconds is 0:
                sDateTime.append(dt.datetime.combine(d,dt.time(0))+dt.timedelta(seconds=60*60*24))
            elif r[4] is 2 and r[2].seconds is 0: 
                sDateTime.append(dt.datetime.combine(d,dt.time(0)))
            else:
                sDateTime.append(dt.datetime.combine(d,dt.time(0))+r[2])
            power.append(r[3])
    

    
            if sDateTime[-1] < sDateTime[-2]:
                    print('hold')
                    
    
    return sDateTime, power

################################################################################
## Main function 2: fpnEnergySeries                                           ##
## Returns a set of energies per settlement period between the date range     ##
## specified (inclusive of both start and end date)                           ##
## This makes use of the function fpnPeriod Energy which calculates the       ##
## energy in a particular period                                              ##
##                                                                            ##
## The calculation assumes linear interpolation between levels and spot times ##
################################################################################  

    
def fpnEnergySeries(bmu, startDate, endDate, cur):
    
    """ Function to produce a time serries of Energy scheduled under FPNs for each settlement period between two dates (inclusive)  
    """
    ## Variables
    
    dateList, sDate, sPeriod, sDatetime = bmraDT.spList(startDate, endDate)
    energy = []
    
    for d in sDate: 
        e, err = fpnPeriodEnergy(bmu, sDate[d], sPeriod[d], cur)
        energy.append(e)
    
    return sDate, sPeriod, sDateTime, energy
 
################################################################################
## Main function 3: powerToEnergy                                             ##
## Returns a set of energies per settlement period for all periods included   ##
## in a time series of spot powers and spot times                             ##
## unlike fpnEnergySerries this requires an existing power serries as input   ##
## and does not query the databse itself                                      ##
################################################################################  
 
def powerToEnergy(dt_series, power, dt_energy):
    """ Function to take a time serries of power together with assotiated datetime serries
        and return a time serries of energy per settlement period
    """
    
    #1. Create list of dates covering the range of the input series
    
    energy = []


    #for each data and for each period within that date
    for i in range (len(dt_energy)):
        # if not the last element
###        if i+1 < len(dt_energy):
            #bisect the power time serries
        settlement_P = power[bisect.bisect_left(dt_series,dt_energy[i]):bisect.bisect_right(dt_series,dt_energy[i]+dt.timedelta(minutes=30))]
        settlement_dt = dt_series[bisect.bisect_left(dt_series,dt_energy[i]):bisect.bisect_right(dt_series,dt_energy[i]+dt.timedelta(minutes=30))]
        
        # if it is the last element
###        elif i+1 == len(dt_energy):
###              #Take the last segment 
###              settlement_P = power[bisect.bisect_left(dt_series,dt_energy[i]):]
###              settlement_dt = dt_series[bisect.bisect_left(dt_series,dt_energy[i]):bisect.bisect_right(dt_series,dt_energy[i] + dt.timedelta(minutes=30))]
    
        settlement_T = [0]
        e = 0
      
        for i in range(1,len(settlement_dt)):
            #Length of setment between two consecutive points in seconds:
            settlement_T.append((settlement_dt[i]-settlement_dt[0]).seconds/(60*60))
            #Calculate energy of segment and add to e:
            e += 0.5 * (settlement_P[i-1]+settlement_P[i]) * (settlement_T[i] - settlement_T[i-1])
        energy.append(e)
    
    
        
    
    return energy 
 
 
################################################################################
## Main function 4:fpnAddBoals                                                ##
## Function to take an existing spot-power time serries representing the      ##
## fpns submitted for a BMU and adjust to produce a time series with the      ##
## result: FPN +/- BOAL                                                       ##
##                                                                            ##
## The resultant time serries is a power time serries                         ##
################################################################################ 
 
def fpnAddBoals(bmu, fpn_P, fpn_dt, cur):
     
    ## BOAL Query 
    boalQuery= """
    SELECT 
    acceptance_no, acceptance_time, start_time, start_level, end_time, end_level, so_flag, settlement_day, settlement_period
    FROM boal
    WHERE bmu_id = %s
    AND settlement_day >= %s
    AND settlement_day <= %s
    ORDER BY acceptance_no, boal_id
    """ 
     
    ## Variable definition
    pastMidnightS = 0 #Flag used when adjusting a BOAL to identify when we move to the next day 
    pastMidnightE = 0 
    
    ## Query database and define variable
    
    cur.execute(boalQuery, [bmu, str(fpn_dt[0].date()), str(fpn_dt[-1].date())])
    boals = cur.fetchall()
    n = len(boals)
    
    #Define variables
    an = [0] * n # Acceptance No: used to group together all BOALS across multiple periods beloning to same acceptance
    at = [0] * n # Date and Time accepted
    st = [0] * n # Start time of BOAL in GMT
    sl = [0] * n # Start level of BOAL (absolute level - NOT relative to existing time series)
    sd = [0] * n # Settlement day of entry
    sp = [0] * n # Settlement period of entry
    et = [0] * n # end time of entry 
    el = [0] * n # end level of entry 
    sof = [0] * n # SO flag of entry (either 0 or 1)
   
   ## NOTE: the way the data has been entered to the database means that 
   ## although the original BOALS do not neccessaraly have entries on the start / end
   ## of a settlment period. An entry for each start / end of a period has been calculated
   ## when data is entered to the database.  
    
    
    #And enter values from querry into specific variables
    for i,b in enumerate(boals): 
        an[i] = b[0]
        at[i] = b[1]
        st[i] = b[2]
        sl[i] = b[3]
        et[i] = b[4]
        el[i] = b[5]
        sof[i] = b[6]
    
    #Find unique values of acceptances
    acceptances = list(set(an))  #Note there are multiple entries per acceptance: this finds list of unique acceptances
    acceptances.sort()
    
    ## Go thorugh acceptances each time adjusting the existing time serries (fpn)
    for a in acceptances:
        

        
        #Find number of entries for particular acceptance and row numbers
        nItems = an.count(a)
        first = an.index(a)
        rows = [first+i for i in range(0,nItems)] #list of rows in BOAL variables relevant to this specific acceptance
        
        #Find location in fpn of time and power variables
        accAccTime = at[rows[0]]
        pastMidnight = 0 # Flag to note the move to a new day
        newDay = dt.timedelta(days=0)
        
     ##  (((A))) Create the time-series snipet to insert based on the BOALs
    
        if st[rows[0]] < TimeToTimeDelta(accAccTime): 
            #If the first start time is smaller than the acceptance time assume that they are 
            #seperated by mignight, and therefore when dealing with time -> datatime conversion
            #will need to add an extra day into the calculations
            pastMidnight = 1
            newDay = dt.timedelta(days=pastMidnight)
        
        #Set the first datatime value to the snippet:
        replacedt = [dt.datetime.combine(accAccTime.date(), dt.time(0,0))+ st[rows[0]]+ \
        newDay]
        
        #First power value to add to the snippet: 
        replacep = [sl[rows[0]]]
        
        #Then the rest of the datetime and power values to add to the snippet
        for rr in rows:
        
            #If the next entry timedelta value is less than the last - assume past midnight and need to add 
            #extra day onto the code. 
            
            if et[rr] < TimeToTimeDelta(replacedt[-1]):
                pastMidnight += 1
                newDay = dt.timedelta(days=pastMidnight)
            
            #Continue to add values 
            replacedt.append(dt.datetime.combine(accAccTime.date(), dt.time(0,0))+ et[rr] + \
            newDay)
            
            replacep.append(el[rr])
        
    ## (((B)))) Find values in existing FPN time-seris to overwrite

        i1s = bisect.bisect_left(fpn_dt, replacedt[0])
        i2s = bisect.bisect_right(fpn_dt, replacedt[0])
        i1e = bisect.bisect_left(fpn_dt, replacedt[-1])
        i2e = bisect.bisect_right(fpn_dt, replacedt[-1])
        nExist_s = i2s - i1s
        nExist_e = i2e - i1e

        #Find point of insertion into existing list of start point for new datapoint
        if nExist_s == 0:
            iInst_s = i1s
        elif nExist_s == 1 and fpn_P[i1s] == replacep[0]:
            iInst_s = i1s
        elif nExist_s == 1 and fpn_P[i1s] != replacep[0]:
            iInst_s = i1s+1
        elif nExist_s == 2:
            iInst_s = i1s + 1
        else:
            print('4 Error: There apears to be more than two points in time series with the same time')



        #Find point of insertion into existing list of end point for new datapoint
        if nExist_e == 0: 
            iInst_e = i1e
        elif nExist_e == 1 and  fpn_P[i1e] == replacep[-1]:
            iInst_e = i1e+1
        elif nExist_e ==1 and fpn_P[i1e] != replacep[-1]:
            iInst_e = i1e
        elif nExist_e in [1,2]:
            iInst_e = i1e+1
        else:
            print('5 Error: There apears to be more than two points in time series with the same time')

    
        #Now delete obselette entries in the existing time serries (ets_dt and ets_p) and splice
        #in the snipped created from the BOALs. 
        
        
        del fpn_dt[iInst_s:iInst_e]
        del fpn_P[iInst_s:iInst_e]
        
        fpn_dt[iInst_s:iInst_s]=replacedt
        fpn_P[iInst_s:iInst_s]=replacep   
    
    ## END (for loop based on acceptances)
    
    return fpn_dt, fpn_P

################################################################################
## Main function 5:timeAtZero                                                 ##
## Function takes a time series of spot power points and finds the amount     ##
## of time the time series is at zero and a list of those zero times          ##
################################################################################  
    
def timeAtZero(dt, levels):
    
    #Overview information 
    start = dt[0]
    end = dt[-1]
    deltaT = (end - start).days*60*60*24 + (end - start).seconds
    
    startTimes = []
    length = []
    
    
    #Each time level goes to zero find the length of that zero period
    i=0
    while i < len(levels):
        #When level becomes zero...
        if levels[i] == 0:
            #Add time of occurance to list
            startTimes.append(dt[i])
            
            #Continue until level becomes non-zero again 
            while levels[i] == 0 and i < len(levels)-1:
                 i += 1                 
            #Caclulate length in seconds at zero and attache to list of lengths
            length.append((dt[i]-startTimes[-1]).seconds + (dt[i]-startTimes[-1]).days*60*60*24)
        i += 1
    
    #Calculate summary statistics
    zeroLength = sum(length)
    fraction = zeroLength / deltaT
    
    return startTimes, length, zeroLength, fraction
    
################################################################################
## Main function 6:boPairSubmitted                                            ##
## Function builds the bid/offer curve for a BMU for each settlement_period   ##
## in the time range                                                          ##
################################################################################  
   
def boPairSubmitted(bmu, st, et, cur):
    ### Variable
    bodQuery = """
    SELECT settlement_day, settlement_period, bod_no, offer_price, bid_price, start_time, start_level, end_time, end_level
    FROM
    tibcodata.bod
    WHERE
    bmu_id = %s AND
    settlement_day >= %s AND
    settlement_day <= %s
    """
    
    #list of dates through time period
    d = st
    dateList = []
    while d <= et:
        dateList.append(d)
        d += dt.timedelta(days=1)
    
    #Preallocate some variables to be filled in
    
    sd = [0 for x in range(48*len(dateList))]
    sp = [0 for x in range(48*len(dateList))]
    i=0
    for d in dateList: 
        for p in range(1,49):
            sd[i] = d
            sp[i] = p
            i += 1
    

    bod_mainPrice =[[0 for x in range(12)]for x in range(48*len(dateList))]
    bod_level =[[0 for x in range(12)]for x in range(48*len(dateList))]
    bod_reversePrice =[[0 for x in range(12)]for x in range(48*len(dateList))]
    
    #The database query 
    queryData = [bmu, str(st), str(et)]
    cur.execute(bodQuery, queryData)
    
    bod = cur.fetchall()
    
    
    for b in bod: 
        dd = b[0]
        pp = b[1]
        rrow = (dd-st).days*48+pp-1
        
        
        if b[2] < 0:
            ccol = b[2]+6
            bod_mainPrice[rrow][ccol] = b[4]
            bod_reversePrice[rrow][ccol]  = b[3]
            bod_level[rrow][ccol] = b[6]
        else:
            ccol = b[2]+5
            bod_mainPrice[rrow][ccol] = b[3]
            bod_reversePrice[rrow][ccol] = b[4]
          
            bod_level[rrow][ccol] = b[6]
        
        if b[6] != b[8]:		
            print('hold')
            
    return sd, sp, bod_mainPrice, bod_level, bod_reversePrice
                    
        
    
################################################################################
## Main function 7:boaEnergyAndCash                                           ##
## Function produces HH time serries of total energy and cash flow for a BMU  ##
## per settlement period. This summs over all BOAs                            ##
################################################################################  
    
def boaEnergyAndCash(bmu, sd, sp, settlement_dt, cur):
    
    ## Querries
    
    boavQuery = """
    SELECT  
        sum(bid_vol), sum(offer_vol)
    FROM
        tibcodata.boav
    WHERE
        bmu_id = %s AND
        settlement_day = %s AND
        settlement_period = %s
    """
    
    ebocfQuery = """
    SELECT  
        sum(bid_cf), sum(offer_cf)
    FROM
        tibcodata.ebocf
    WHERE
        bmu_id = %s AND
        settlement_day = %s AND
        settlement_period = %s
    """

    

    boavs_offers = [0 for x in range(len(sd))]
    boavs_bids = [0 for x in range(len(sd))]
    ebocfs_offers = [0 for x in range(len(sd))]
    ebocfs_bids = [0 for x in range(len(sd))]
    

    for p in range(len(sd)):
        queryData = [bmu, str(sd[p]), str(sp[p])]
        n = cur.execute(boavQuery, queryData)
        bb = cur.fetchall()
        bb = bb[0]
        
        if bb ==(None, None): 
            bb = (0,0)
            cf = (0,0)
        else:
            cur.execute(ebocfQuery, queryData)
            cf = cur.fetchall()
            cf=cf[0]
        
        boavs_bids[p] = bb[0]
        if boavs_bids[p] == None:
            print('hold')
        boavs_offers[p] = bb[1]
        ebocfs_bids[p] = cf[0]
        ebocfs_offers[p] = cf[1]

    return boavs_bids, boavs_offers, ebocfs_bids, ebocfs_offers

################################################################################
## Main function 8:melPowerSeries                                             ##
## Takes FPN time-series and checks if any values need to be capped by MEL    ##
################################################################################    
    
def melPowerSeries(bmu,sdL, spL, cur):

    melQuery = """
    SELECT settlement_day, settlement_period, start_time, start_level, end_time, end_level, recieved	
    FROM tibcodata.mel
    WHERE
    bmu_id = %s
    AND settlement_day >= %s AND settlement_day <= %s 
    ORDER BY settlement_day, settlement_period
    """
    
    t1 = time.time()
    
    mel_dt = []
    mel_level = []
    mel_rdt = []
    
    
    countQuerry= """
        SELECT COUNT(1) FROM mel
        WHERE bmu_id = %s AND settlement_day >= %s AND settlement_day <= %s
        """
    
    #Check if there is any data to find
    cur.execute(countQuerry, [bmu, sdL[0], sdL[-1]])
    nn = cur.fetchall()
    if nn[0][0] == 0: 
        return [], [], []
    
    cur.execute(melQuery, [bmu, sdL[0], sdL[-1]])
    mels = cur.fetchall()
    mels = list(mels)
    
    melsS = sorted(mels, key = lambda mel: (mel[0], mel[1], mel[6]))
    
    for m in melsS:

        m_bmraDT_start = bmraDT.from_dpdt(m[0], m[1], m[2])
        m_bmraDT_end = bmraDT.from_dpdt(m[0], m[1], m[4])
        if mel_dt == []:

            #Deal with first Entry: add start and end
            
            
            
            mel_dt.append(m_bmraDT_start.datetime)
            mel_dt.append(m_bmraDT_end.datetime)
            mel_level.append(m[3])
            mel_level.append(m[5])
            mel_rdt.append(m[6])
            mel_rdt.append(m[6])

        else:
        
            i1s = bisect.bisect_left(mel_dt, m_bmraDT_start.datetime)
            i2s = bisect.bisect_right(mel_dt, m_bmraDT_start.datetime)

            nExist_s = i2s - i1s

            i1e = bisect.bisect_left(mel_dt, m_bmraDT_end.datetime)
            i2e = bisect.bisect_right(mel_dt, m_bmraDT_end.datetime)
            
            nExist_e = i2e - i1e
            
            
            #Find point of insertion into existing list of start point for new datapoint
            if nExist_s == 0:
                iInst_s = i1s
            elif nExist_s == 1 and mel_level[i1s] == m[3]:
                iInst_s = i1s
            elif nExist_s == 1 and mel_level[i1s] != m[3]:
                iInst_s = i1s+1
            elif nExist_s == 2:
                iInst_s = i1s + 1
            else:
                print('2 Error: There apears to be more than two points in time series with the same time')
            
            
            #Find point of insertion into existing list of end point for new datapoint
            if nExist_e == 0: 
                iInst_e = i1e
            elif nExist_e == 1 and  mel_level[i1e] == m[5]:
                iInst_e = i1e+1
            elif nExist_e ==1 and mel_level[i1e] != m[5]:
                iInst_e = i1e
            elif nExist_e in [1,2]:
                iInst_e = i1e+1
            else:
                print('3 Error: There apears to be more than two points in time series with the same time')
            
            #One correction: If a new step change is replacing either 1 or two existing data point (that is either
            # and existing normal data poitn or an existing step change. Need to adjust the above forumlas
            # And the new data point is replacing both this will show up as: 
            # nExist_s = nExist_e = 2 and t_s = t_e
            # Currently it assumes that the two existing data points at the start time and the two existing data points
            # at the end time are different sets of points and therefore delete the inside one of each. However if they
            # are actually the same sets of points we need to delete both of them
            
            if nExist_e == 1 and m_bmraDT_start.datetime == m_bmraDT_end.datetime:
                iInst_e += 1
            
            if nExist_e == 2 and nExist_s ==2 and m_bmraDT_start.datetime == m_bmraDT_end.datetime:
                iInst_s -= 1
                iInst_e += 1
            
            
            #Delete section to be replaced
            del mel_dt[iInst_s:iInst_e]
            del mel_level[iInst_s:iInst_e]
            del mel_rdt[iInst_s:iInst_e]
            
            #Inster new section
            mel_dt[iInst_s:iInst_s] = [m_bmraDT_start.datetime, m_bmraDT_end.datetime]
            mel_level[iInst_s:iInst_s] = [m[3], m[5]]
            mel_rdt[iInst_s:iInst_s] = [m[6], m[6]]
            
            if mel_dt[-1] < mel_dt[-2]:
                print('hold')
            
    return mel_dt, mel_level, mel_rdt


################################################################################
## Main function 8:capFpnByMel                                             ##
## Takes FPN time-series and checks if any values need to be capped by MEL    ##
################################################################################

#To be done
    
    

        
################################################################################
## Support function 1: fpnPeriodEnergy                                        ##
## Queries fpn table in tibcodata database for all entries relevant to a      ##
## particular bmu for a particular settlement period                          ##
## Calculates the energy under the power line assuming linear interpolation   ##
## Due to the structure of the data there will always be an entry for the     ##
## start and end of a period                                                  ##
################################################################################



def fpnPeriodEnergy(bmu, sd, sp, cur):
    """ Function to sum up the enegy for a settlement period from (potentially) multiple entries in the database
    """
    ## Querry and variables
    fpnQuery = """ 
        Select settlement_day, settlement_period, start_time, start_level, end_time, end_level 
        FROM fpn 
        WHERE bmu_id = %s AND settlement_day = %s AND settlement_period = %s
        """
    energy = 0
    
    ##Access Database
    try: 
        cur.execute(fpnQuery, [bmu, str(sd), str(sp)])
    except:
        print('Failed to complete database querry in fpnPerioEnergy')
        return None, 1
    
    ## Process data returned
    rr = cur.fetchall()
    
    for r in rr: 
        ps=dt.time((r[1]-1)//2, 30*((r[1]-1)%2)) #Converts period start time to time object
        st =  (r[2].seconds/3600) - (ps.hour) - (ps.minute / 60)  #Dif between start of period and start time
        
        #The following if block adjusts the situation that an end time occures at midnight (and can be represetented by time = 0) 
        if r[4].seconds == 0:
            et = 24 - (ps.hour) - (ps.minute / 60) 
        else:
            et =  (r[4].seconds/3600) - (ps.hour) - (ps.minute / 60)  #Dif between start of period and start time
        energy += 0.5 * (et -st) * (r[3] + r[5])  #Area of region is 1/2 * length * height1 * height2
    
    return energy, 0
    
################################################################################
## Support function 2: timeToTimeDelta                                        ##
## creates a time-delta object which represents time since the previous       ##
## midnight. Useful for creating object to add to date to give datetime       ##
################################################################################
    
def TimeToTimeDelta(t):
    """ Takes in a time or date time variable and converts it to a time-delta object where the output
        is in seconds from the previous midnight"""
        
    if type(t) in [dt.datetime, dt.time]:
        dt_seconds = t.hour*60*60 + t.minute*60 + t.second
    else:
        print("Incompatable data type provided to TimeToDelta - only datetime and time objects allowed")
        return None
    return dt.timedelta(seconds=dt_seconds)
    

################################################################################
## Support function 3: clockChangeAdjust                                      ##
## Adjusts times to GMT from local time, which either:                        ##
##  - Does nothing during the winter                                          ##
##  - Subtracts 1 hour and returns in BST                                     ##
################################################################################

def clockChangeAdjust(in_dt): 
    
    ## Historical Clock Change Days
    clocksForward= [dt.date(2000, 3, 26), 
                    dt.datetime(2001, 3, 26, 0), 
                    dt.datetime(2002, 4, 1, 0), 
                    dt.datetime(2003, 3, 31, 0), 
                    dt.datetime(2004, 3, 29, 0), 
                    dt.datetime(2005, 3, 28, 0), 
                    dt.datetime(2006, 3, 27, 0), 
                    dt.datetime(2007, 3, 26, 0), 
                    dt.datetime(2008, 3, 31, 0), 
                    dt.datetime(2009, 3, 30, 0), 
                    dt.datetime(2010, 3, 29, 0), 
                    dt.datetime(2011, 3, 28, 0), 
                    dt.datetime(2012, 3, 26, 0), 
                    dt.datetime(2013, 4, 1, 0), 
                    dt.datetime(2014, 3, 31, 0), 
                    dt.datetime(2015, 3, 30, 0)]
    
    clocksBack=    [dt.datetime(2000, 10, 30,0), 
                    dt.datetime(2001, 10, 29,0), 
                    dt.datetime(2002, 10, 28,0),            
                    dt.datetime(2003, 10, 27,0),            
                    dt.datetime(2004, 11, 1,0), 
                    dt.datetime(2005, 10, 31,0), 
                    dt.datetime(2006, 10, 30,0), 
                    dt.datetime(2007, 10, 29,0), 
                    dt.datetime(2008, 10, 27,0), 
                    dt.datetime(2009, 10, 26,0), 
                    dt.datetime(2010, 11, 1,0), 
                    dt.datetime(2011, 10, 31,0), 
                    dt.datetime(2012, 10, 29,0), 
                    dt.datetime(2013, 10, 28,0), 
                    dt.datetime(2014, 10, 27,0), 
                    dt.datetime(2015, 10, 26,0)]
    
    yearRow = in_dt.year - 2000
    
    if (in_dt-clocksForward[yearRow]).days < 0 or  (in_dt-clocksBack[yearRow]).days > 0: 
        out_dt = in_dt
    else:
        out_dt = in_dt - dt.timedelta(seconds = 60*60)
    return out_dt
    
    
################################################################################
## Support function 4: periodTimeSeries                                       ##
## time Series of dates, periods and starting datetime                        ##
################################################################################

def periodTimeSeries(st, et):
    d = st
    dateList = []
    

    
    while d <= et:
        dateList.append(d)
        d += dt.timedelta(days=1)

    sd = [0 for x in range(48*len(dateList))]
    sp = [0 for x in range(48*len(dateList))]
    settlement_dt = [0 for x in range(48*len(dateList))]

    i=0
    for d in dateList: 
        for p in range(1,49):
            sd[i] = d
            sp[i] = p
            timeUnadjusted= dt.datetime.combine(d, dt.time(int((p-1)/2), 30*((p-1)%2)))
            settlement_dt[i] = clockChangeAdjust(timeUnadjusted)
            i += 1 
    
    return sd, sp, settlement_dt
