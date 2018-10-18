import sys
sys.path.append('D:\\USERS\\seb09186\\ShareFile\\My Files & Folders\\python\\libraries\\sg')

import bmraTimes as bt
import csvProcess as csv2
import pymysql
import datetime as dt
import os
import dataManipulation as dm

def createDailyCsv(bmuList, today, cur, curSys, fd):    


    boavQuerry = """
            SELECT  
                sum(bid_vol), sum(offer_vol)
            FROM
                tibcodata.boav
            WHERE
                bmu_id = %s AND
                settlement_day = %s AND
                settlement_period = %s
            """


    nsp = bt.noOfPeriods(today)
    sp = [i+1 for i,n in enumerate(range(0,nsp))]
    fpnOutput = []
    melOutput = [] 
    boavOutput = []
    indoOutput =[]
    bmuLastGen = []
    bmuLastAvail = []
    hhFuelOutput = [[] for i in range(0,13)]  
    balancingOutput = [[] for i in range(0,3)]
    hhFuelKey = ['CCGT','COAL', 'INTEW','INTFR', 'INTIRL', 'INTNED', 'NPSHYD', 'NUCLEAR', 'OCGT', 'OIL', 'OTHER', 'PS', 'WIND']
    
    
    dList, sd_series, sp_series, dt_series = dm.bmraDT.spList(today, today)
    
    for bmu in bmuList:
        print(bmu)
        fpn_P_dt, fpn_P = dm.fpnPowerSeries(bmu, today, today, cur)
        fpn_E = dm.powerToEnergy(fpn_P_dt, fpn_P, dt_series)

        fpnOutput.append(fpn_E)
        
#         cur.execute("SELECT settlement_day, settlement_period FROM fpn WHERE bmu_id = %s AND end_level > 0 ORDER BY settlement_day DESC , settlement_period DESC LIMIT 1", [bmu])
#         lastGen = cur.fetchall()
#         lastGendt = bt.bmraDT.from_dp(lastGen[0][0], lastGen[0][1])
#         bmuLastGen.append(lastGendt)
        
        
        mel_P_dt,  mel_P, mel_P_dt_recieved = dm.melPowerSeries(bmu, sd_series, sp_series, cur)
        mel_E =  dm.powerToEnergy(mel_P_dt, mel_P, dt_series)
        melOutput.append(mel_E)
        
        
        
#         cur.execute("SELECT settlement_day, settlement_period FROM mel WHERE bmu_id = %s AND end_level > 0 ORDER BY settlement_day DESC , settlement_period DESC LIMIT 1", [bmu])
#         lastAvail = cur.fetchall()
#         lastAvaildt = bt.bmraDT.from_dp(lastAvail[0][0], lastAvail[0][1])
#         bmuLastAvail.append(lastAvaildt)
        
        boav_E = [None for s in range(0,len(sp))]
        for i, s in enumerate(sp):
            boavData = [bmu, today, s]
            try:
                cur.execute(boavQuerry, boavData)
            except:
                print('Failed to return BOAV querry os settlement Period '+str(s))
                return
            boavs = cur.fetchall()
            if len(boavs)<2: boavs = boavs[0]
            try:
                boav_E[i] = sum(boavs)
            except:
                boav_E[i] = 0 
        boavOutput.append(boav_E)
        
        
    
    
    csv2.listToCsv(fd+'daily_fpn.csv', [sp]+fpnOutput, ['SP']+ bmuList)
    csv2.listToCsv(fd+'daily_mel.csv', [sp]+melOutput, ['SP']+ bmuList)
    csv2.listToCsv(fd+'daily_boav.csv', [sp]+boavOutput, ['SP']+ bmuList)
    #csv2.listToCsv(fd+'last_gen_avail.csv', [bmuL]+[bmuLastGen]+[bmuLastAvail], ['BMU', 'Last Gen', 'LastAvail'])
    
    ## System Warnings and System Messages
    
    curSys.execute("SELECT * FROM systemwarnings WHERE message_received > %s AND message_received <%s", [today, today + dt.timedelta(days=1)])
    warns = curSys.fetchall()
    wTimes = []
    wMess = []
    for w in warns:
        wTimes.append(w[1])
        wMess.append(w[2].replace('\n', ' '))
    

    saveWarn = [wTimes]+[wMess]

         
    csv2.listToCsv(fd+'daily_warns.csv', saveWarn, ['Warning Issued', ''])
  
    curSys.execute("SELECT * FROM systemmessages WHERE message_received > %s AND message_received <%s", [today, today + dt.timedelta(days=1)])
    message = curSys.fetchall()
    mTimes = []
    mMess = []
    for m in message:
        mTimes.append(m[2])
        mMess.append(m[3].replace('\n', ' '))
    
    saveMess = [mTimes]+[mMess]

         
    csv2.listToCsv(fd+'daily_messages.csv', saveMess, ['Message Issued', ''])
    
    ## System data
    
    curSys.execute("SELECT settlement_period, level FROM indo WHERE settlement_day = %s ORDER BY settlement_period", [today])
    nd = curSys.fetchall()
    for n in nd: 
        indoOutput.append(float(n[1]))
    
    if len(indoOutput) < 48:
        nLeft = 48 - len(indoOutput)
        for n in range (0,nLeft):
            indoOutput.append(None)
    
    curSys.execute("SELECT settlement_period, fuel_type, generation FROM hhgenerationbyfuel WHERE settlement_day = %s ORDER BY settlement_period, fuel_type", [today])
    hhft = curSys.fetchall()
    
    for g in hhft:
        i = hhFuelKey.index(g[1])
        hhFuelOutput[i].append(float(g[2]))
        
    if len(hhFuelOutput[0]) < 48:
        nLeft = 48 - len(hhFuelOutput[0])
        for n in range (0,nLeft):
            for f in hhFuelOutput:
                f.append(None)
    
    ## Non SP based information: Extremes of Instantaneous generation and Frequency 
    instGenT = []
    instGenSP = []
    instGenG = []
    curSys.execute("SELECT spot_time, settlement_period, SUM(generation) FROM tibcosystem.instgenerationbyfuel WHERE spot_time >= %s AND spot_time < %s  GROUP BY spot_time ORDER BY SUM(generation) DESC LIMIT 1", [today, today+dt.timedelta(days=1)])
    maxInstGen = curSys.fetchall()
    instGenT.append(maxInstGen[0][0].time())
    instGenSP.append(maxInstGen[0][1])
    instGenG.append(maxInstGen[0][2])
    
    curSys.execute("SELECT spot_time, settlement_period, SUM(generation) FROM tibcosystem.instgenerationbyfuel WHERE spot_time >= %s AND spot_time < %s  GROUP BY spot_time ORDER BY SUM(generation) ASC LIMIT 1", [today, today+dt.timedelta(days=1)])
    minInstGen = curSys.fetchall()

    instGenT.append(minInstGen[0][0].time())
    instGenSP.append(minInstGen[0][1])
    instGenG.append(minInstGen[0][2])
    
    csv2.listToCsv(fd+'instGen.csv', [instGenT, instGenSP, instGenG], ['DateTime', 'SP', 'Generation(MW)'])
    
    curSys.execute("SELECT spot_time, freq FROM tibcosystem.frequency WHERE spot_time >=%s AND spot_time < %s", [today, today+dt.timedelta(days=1)])
    freq = curSys.fetchall()
    freqT = []
    freqF = []
    for f in freq: 
        freqT.append(f[0].time())
        freqF.append(f[1])
        
    csv2.listToCsv(fd+'freq.csv', [freqT, freqF],  ['Time', 'Frequency (Hz)'])
        
    
    
    ## BalancingData
    curSys.execute("SELECT settlement_period, buy_price, niv FROM tibcosystem.disebsp WHERE settlement_day = %s GROUP BY settlement_period ORDER BY settlement_period", [today])
    bd = curSys.fetchall()

    for b in(bd): 
        balancingOutput[0].append(b[1])
        balancingOutput[1].append(b[2])
    
    curSys.execute("SELECT settlement_period, mip, miv FROM tibcosystem.mid WHERE settlement_day = %s AND provider = 'APXMIDP' GROUP BY settlement_period ORDER BY settlement_period", [today])
    mid = curSys.fetchall()
    for m in mid: 
        balancingOutput[2].append(m[1])
    
    
    csv2.listToCsv(fd+'system_data.csv', [sp]+[indoOutput]+hhFuelOutput, ['SP', 'INDO']+hhFuelKey)
    csv2.listToCsv(fd+'market_data.csv', [sp]+balancingOutput, ['SP', 'System Price (£/MWh)', 'NIV(MW)', 'MIP - APX (£/MWh)'])
    
    csv2.listToCsv(fd+'date.csv', [[today]], ['Date'])
    
    return 
    
## Main section


if __name__ == "__main__":
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='imGoingToCambridge2015', db='tibcodata')
    cur = conn.cursor()
    
    connSys = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='imGoingToCambridge2015', db='tibcosystem')
    curSys = connSys.cursor()
    
    bmuQuerry = """SELECT bmu_id from bmu WHERE bmu_id LIKE 'T_%' OR bmu_id LIKE 'E_%' """
    
    cur.execute(bmuQuerry)
    bmus = cur.fetchall()
    
    bmuL = []
    for b in bmus: 
        bmuL.append(b[0])
    
    
    fd = "D:\\USERS\\seb09186\\ShareFile\\My Files & Folders\\BM Daily Reviews\\csv\\"
    
    #createDailyCsv(bmuL, dt.date(2015,12,13), cur, curSys, fd)
    
    createDailyCsv(['T_LOAN-1', 'T_LOAN-2','T_COCK-1'], dt.date(2015,11,20), cur, curSys, fd)

    