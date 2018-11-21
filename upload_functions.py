"""
Helper functions for uploading data to database

"""
import datetime as dt

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

##############   9. dtStringToDT (Converts BMRA string which represents a date and creates a datetime object) #######

def dtStringToDT(dtS, type):
    """ Type to be 0 for date or 1 for date and time """
    dtL = dtS.split(':')
    if type == 0:
        dtDt = dt.datetime(year=int(dtL[0]), month=int(dtL[1]), day=int(dtL[2]))
    else:
        dtDt = dt.datetime(year=int(dtL[0]), month=int(dtL[1]), day=int(dtL[2]), hour=int(dtL[3]), minute=int(dtL[4]), second=int(dtL[5]))
    return dtDt



def insert_bm_data(BMUID, BM_data_type, received, gmt, message, cur):
    """

    """
    if BM_data_type in ['FPN', 'QPN', 'MEL', 'MIL']:
        #e = db.enterBMphys(subjectShort[0], subjectShort[-1], recieved, gmt, message, cur)
        table = "INSERT INTO tibcodata."+BM_data_type.lower()


        q2 = """
        (bmu_id, recieved, settlement_day, settlement_period, start_time, start_level, end_time, end_level)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        insertQuery = table+q2

        #Split message into consituent parts
        mF, mV = splitMessage(message)

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
            queryData = [BMUID, received, sDate, sPeriod, sTime.strftime('%H:%M:%S'), sLevel, eTime.strftime('%H:%M:%S'), eLevel]

            #carry out querry
            cur.execute(insertQuery, queryData)

            '''
            except:
                print('Not able to insert '+mType+' data')
                print(mess)
            '''


        return 1
    '''
    elif BM_data_type in ['BOD']:
        e = db.enterBMbod(subjectShort[0], subjectShort[-2], recieved, gmt, message, cur)
    elif BM_data_type in ['BOALF', 'BOAL']:
        e = db.enterBMboal(subjectShort[0], subjectShort[-1], recieved, gmt, message, cur)
    elif BM_data_type in ['BOAV']:
        e =db.enterBMboav(subjectShort[0], subjectShort[-2], recieved, gmt, message, cur)
    elif BM_data_type in ['EBOCF']:
        e =db.enterBMebocf(subjectShort[0], subjectShort[-2], recieved, gmt, message, cur)
    '''


def insert_system_data(message):
    """
    """
    pass

def insert_dynamic_data(BMUID, BM_data_type, message):
    """
    """
    pass
