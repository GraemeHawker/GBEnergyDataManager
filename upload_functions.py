"""
Helper functions for uploading data to database

"""
import datetime as dt

def message_to_dict(raw_message):
    """
    Converts a raw message string to a dictionary with
    key/value pairs and metadata

    Parameters
    ----------
    raw_message : string
        the BM data string

    Returns
    -------
    message_dict: dict
        a dictionary containing key/value pairs and metadata:
            received_time: datetime
                the timestamp of the message
            message_type: string
                the tibco message type, one of ['BM','SYSTEM','DYNAMIC']
            message_subtype: string
                the subtype of the message
                for message_type == 'BM', one of
                    ['FPN','QPN','MEL','MIL']
                for message_type == 'SYSTEM', one of
                    []
                for message_type == 'DYNAMIC', one of
                    []
            data_pairs: dict
                time/value pairs ordered by integer key
                each consisting of a timestamp and float value

    """
    message_dict = dict()

    message_parts = raw_message.split(',')
    received_time_string = message_parts[0].split(' ')[0]
    message_dict['received_time'] = dt.datetime(
        *[int(x) for x in received_time_string.split(':')[:-2]])

    message_type_list = message_parts[0].split(' ')[1].split('.')
    message_dict['message_type'] = message_type_list[1]
    if message_dict['message_type'] == 'BM':
        message_dict['bmu_id'] = message_type_list[2]
        message_dict['message_subtype'] = message_type_list[3]
    elif message_dict['message_type'] == 'SYSTEM':
        message_dict['message_subtype'] = message_type_list[2]
    else:
        raise ValueError('message type %s not recognised' % message_dict['message_type'])

    key_values = raw_message[raw_message.find('{')+1:raw_message.rfind('}')]
    for key_value in key_values.split(','):
        key, value = key_value.split('=')
        key = key.strip()
        if key == 'SD':     #settlement date
            message_dict['SD'] = dt.datetime(*[int(x) for x in value.split(':')[:3]])
        elif key == 'SP':   #settlement period
            message_dict['SP'] = int(value)
        elif message_dict['message_subtype'] == 'BOD' and key == 'NN':
            message_dict['NN'] = int(value)
        elif message_dict['message_subtype'] == 'BOD' and key == 'BP':
            message_dict['BP'] = float(value)
        elif message_dict['message_subtype'] == 'BOD' and key == 'OP':
            message_dict['OP'] = float(value)
        elif key == 'NP':   #process data pairs
            message_dict['data_pairs'] = dict()
            pair_count = 1
            for pair_timestamp, pair_value in zip(
                    key_values.split(',')[-2*int(value):][0::2],
                    key_values.split(',')[-2*int(value):][1::2]):
                message_dict['data_pairs'][pair_count] = {
                    'timestamp' : dt.datetime(
                        *[int(x) for x in pair_timestamp.split('=')[1]
                          .split(':')[:-2]]),
                    pair_value.split('=')[0]: float(pair_value.split('=')[1])}
                pair_count += 1
            break   #pairs should be the final part of the message
        else:
            raise ValueError('message key %s not recognised for \
                             message type %s and message subtype %s' %
                             (key, message_dict['message_type'],
                              message_dict['message_subtype']))
    return message_dict


def split_message(raw_message):
    """
    Takes a BM relevant message
    and splits into a list of fields and a list of values

    Parameters
    ----------
    raw_message : string
        the BM data string

    Returns
    -------
    fields: list
        a list of strings containing field names

    values: list
        a list of strings containing field values

    Raises
    ------

    """
    message_parts = raw_message.split(',')
    fields = []
    values = []
    for message in message_parts:
        message_pair = message.split('=')
        fields.append(message_pair[0])
        if message_pair[0] == 'SD':
            values.append(dtStringToDT(message_pair[1], False))
        elif message_pair[0] in ['TS', 'TA']:
            values.append(dtStringToDT(message_pair[1], True))
        else:
            values.append(message_pair[1])
    return fields, values

def dtStringToDT(raw_string, type):
    """
    Converts BMRA string which represents a date to a datetime object

    Parameters
    ----------
    raw_string : string
        the BM date/time string

    type: Boolean
        whether the string contains date and time (True) or date only (False)

    Returns
    -------
    processed_datetime: list
        a list of strings containing field names

    Raises
    ------

    """
    date_parts = raw_string.split(':')

    if type is True:
        processed_datetime = dt.datetime(year=int(date_parts[0]),
                                         month=int(date_parts[1]),
                                         day=int(date_parts[2]),
                                         hour=int(date_parts[3]),
                                         minute=int(date_parts[4]),
                                         second=int(date_parts[5]))
    else:
        processed_datetime = dt.datetime(year=int(date_parts[0]),
                                         month=int(date_parts[1]),
                                         day=int(date_parts[2]))

    return processed_datetime



def insert_bm_data(BMUID, BM_data_type, received, gmt, message, cur):
    """
    Inserts a row of BMUID-level data

    Parameters
    ----------
    BMUID : string
        the ID code for the BM unit concerned
    BM_data_type : string
        the sub-type of BM data being processed, corresponding
        to the SQL table to be inserted INTO

        should be one of:
            'FPN' : Final Physical Notification
            'QPN' : Quiescent Physical Notification
            'MEL' : Maximum Import Limit
            'MIL' : Minimum Import Limit

    received :

    Returns
    -------
    None

    Raises
    ------

    """
    if BM_data_type in ['FPN', 'QPN', 'MEL', 'MIL']:
        #e = db.enterBMphys(subjectShort[0], subjectShort[-1], recieved, gmt, message, cur)
        query_part_1 = "INSERT INTO tibcodata."+BM_data_type.lower()
        query_part_2 = """
        (bmu_id, recieved, settlement_day, settlement_period, start_time, start_level, end_time, end_level)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        insert_query = query_part_1 + query_part_2

        #Split message into consituent parts, extract settlement date/period
        message_fields, message_values = split_message(message)
        sDate = message_values[0]
        sPeriod = message_values[1]

        #For each pair of values
        for i in range(0, int(mV[2])-1):

            #Extract relevant data
            sTime = message_values[3+(2*i)]
            sLevel = message_values[4+(2*i)]
            eTime = message_values[5+(2*i)]
            eLevel = message_values[6+(2*i)]

            #Pull together data for query
            queryData = [BMUID, received, sDate, sPeriod, sTime.strftime('%H:%M:%S'), sLevel, eTime.strftime('%H:%M:%S'), eLevel]

            #carry out querry
            cur.execute(insert_query, queryData)

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
