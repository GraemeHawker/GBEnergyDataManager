"""
Helper functions for uploading data to database

"""
import datetime as dt
from itertools import zip_longest
from django.utils import timezone
from ._data_definitions import PROCESSED_MESSAGES, ACCEPTED_MESSAGES, FIELD_CASTING_FUNCS
from ._corrupt_message_list import CORRUPT_MESSAGES


def message_part_to_points(raw_message_part,
                           no_points,
                           message_type,
                           message_subtype):
    """
    For part of a message string containing multiple datapoints
    splits string into individual datapoints and inserts
    key,value pairs into dictionary

    Parameters
    ----------
    raw_message_part : string
        the BM datapoints substring

    no_points: integer
        the number of datapoints contained

    message_type: string
        the BMRA message type (e.g. 'BM')

    message_subtype: string
        the BMRA message sub-type (e.g. 'FPN')
    """

    data_dict = dict()
    data_set_count = 1

    if no_points == 0:  #some cases where there is no data
        return data_dict
    #subdivide into iterables each containing single set of key,value pairs
    #see https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    if len(raw_message_part.split(','))%no_points != 0:
        raise ValueError("Unexpected number of key/value pairs %s"
                         % raw_message_part)
    data_length = len(raw_message_part.split(','))//no_points
    for data_set in zip_longest(*[iter(raw_message_part.split(','))]*data_length,
                                fillvalue='error'):
        data_dict[data_set_count] = dict()
        for data_point in data_set:
            if data_point == 'error':
                raise ValueError("Unexpected number of key/value pairs %s"
                                 % raw_message_part)
            key, value = data_point.split('=')
            if key.strip() in ACCEPTED_MESSAGES[message_type][message_subtype]:
                data_dict[data_set_count][key.strip()] = FIELD_CASTING_FUNCS[
                    key.strip()](value.strip())
            else:
                raise ValueError('message key %s not recognised for \
                message type %s and message subtype %s %s' %
                                 (key, message_type,
                                  message_subtype,
                                  raw_message_part))
        data_set_count += 1
    return data_dict


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
                the tibco message type, e.g. one of ['BM','SYSTEM','DYNAMIC']
            message_subtype: string
                the subtype of the message, e.g. 'FPN'
            data_pairs: dict
                time/value pairs ordered by integer key
                each consisting of a timestamp and float value

    """
    message_dict = dict()

    message_parts = raw_message.split(',')
    if message_parts[0].strip() in CORRUPT_MESSAGES:
        return None
    received_time_string = message_parts[0].split(' ')[0]
    message_dict['received_time'] = dt.datetime(
        *[int(x) for x in received_time_string.split(':')[:6]], tzinfo=timezone.utc)

    message_type_list = message_parts[0].split(' ')[1].split('.')
    message_type = message_type_list[1]
    message_dict['subject'] = message_parts[0].split(' ')[1].split('=')[1]
    message_dict['message_type'] = message_type
    if message_type in ['BM', 'BP', 'DYNAMIC']:
        message_dict['bmu_id'] = message_type_list[2]
        message_subtype = message_type_list[3]
        message_dict['message_subtype'] = message_subtype
    elif message_type in ['SYSTEM', 'INFO']:
        if message_type_list[2] in ACCEPTED_MESSAGES[message_type]:
            message_subtype = message_type_list[2]
        elif len(message_type_list) > 3 and message_type_list[3] in ACCEPTED_MESSAGES[message_type]:
            #for the system messages which also have an associated BMU ID
            #in the header
            message_subtype = message_type_list[3]
            message_dict['bmu_id'] = message_type_list[2]
        else:
            raise ValueError('Valid subtype not found for message type %s %s' %
                             (message_type, raw_message))
        message_dict['message_subtype'] = message_subtype
    else:
        raise ValueError('message type %s not recognised %s' % (message_type,
                                                                raw_message))

    if message_subtype not in ACCEPTED_MESSAGES[message_type]:
        raise ValueError('message subtype %s not recognised for \
                         message type %s %s' %
                         (message_subtype,
                          message_type,
                          raw_message))

    key_values = raw_message[raw_message.find('{')+1:raw_message.rfind('}')]


    for key_value in key_values.split(','):
        key = key_value[:key_value.find('=')].strip()
        if key == 'SW': #edge case where commas can appear in field
            value = key_values[key_values.rfind(key)+3:].strip()
            message_dict[key] = value
            return message_dict
        value = key_value[key_value.find('=') + 1:].strip()
        #key, value = key_value.split('=')
        #key = key.strip()
        if key in ['NP', 'NR']:   #process multiple datapoints
            raw_message_part = raw_message[raw_message.rfind(key):-1]
            raw_message_part = raw_message_part[raw_message_part.find(',')+1:]
            message_dict['data_points'] = message_part_to_points(
                raw_message_part,
                int(value.strip()),
                message_type,
                message_subtype)
            break   #datapoints should be the final part of the message
        elif key in ACCEPTED_MESSAGES[message_type][message_subtype]:
            message_dict[key] = FIELD_CASTING_FUNCS[key](value)
        else:
            raise ValueError('message key %s not recognised for \
            message type %s and message subtype %s %s' %
                             (key, message_dict['message_type'],
                              message_dict['message_subtype'],
                              raw_message))
    return message_dict

def insert_data(message_dict):
    """
    Converts a message dictionary to Django ORM object, checking first
    if message has already been processed

    Parameters
    ----------
    message_dict : dict
        the BM data dictionary

    Returns
    -------
    0: Message already processed, no further action taken
    1: Message processed successfully
    2: Message not currently in accepted message list, no further action taken
    """
    if message_dict['message_subtype'] not in PROCESSED_MESSAGES[message_dict['message_type']]:
        return 2

    if message_dict['message_type'] == 'SYSTEM':
        return insert_system_data(message_dict)
    if message_dict['message_type'] == 'BM':
        return insert_bm_data(message_dict)
    if message_dict['message_type'] == 'DYNAMIC':
        return insert_dynamic_data(message_dict)
    if message_dict['message_type'] == 'INFO':
        return insert_info_data(message_dict)
    if message_dict['message_type'] == 'BP':
        return insert_bp_data(message_dict)
    raise ValueError('Insert function not available for message type %s'
                     % message_dict['message_type'])

def insert_bm_data(message_dict):
    """
    Generates and saves Django ORM object from message dictionary
    in order to insert a row of BMUID-level data to DB

    Parameters
    ----------
    message: message dictionary

    Returns
    -------
    None

    Raises
    ------

    """
    from BMRA.models.balancing import FPN, FPNlevel, MEL, MELlevel, MIL, MILlevel,\
    BOAL, BOALlevel, BOALF, BOALFlevel, BOD, DISPTAV, EBOCF, PTAV, QAS, QPN, QPNlevel,\
    BOAV

    from BMRA.models.core import BMU

    #check if BMUID already in db, if not insert and log
    try:
        bmu = BMU.objects.get(id=message_dict['bmu_id'])
    except BMU.DoesNotExist:
        bmu = BMU(id=message_dict['bmu_id'])
        bmu.save()

    #construct associated BM object
    if message_dict['message_subtype'] in ['FPN']:
        if FPN.objects.filter(bmu=bmu,
                              TS=message_dict['received_time']).exists():
            return 0
        fpn = FPN(bmu=bmu,
                  TS=message_dict['received_time'],
                  SD=message_dict['SD'],
                  SP=message_dict['SP'])
        fpn.save()
        for data_point in message_dict['data_points'].values():
            fpn_level = FPNlevel(fpn=fpn,
                                 TS=data_point['TS'],
                                 VP=data_point['VP'])
            fpn_level.save()
        return 1

    if message_dict['message_subtype'] in ['MEL']:
        if MEL.objects.filter(bmu=bmu,
                              TS=message_dict['received_time']).exists():
            return 0
        mel = MEL(bmu=bmu,
                  TS=message_dict['received_time'],
                  SD=message_dict['SD'],
                  SP=message_dict['SP'])
        mel.save()
        for data_point in message_dict['data_points'].values():
            mel_level = MELlevel(mel=mel,
                                 TS=data_point['TS'],
                                 VE=data_point['VE'])
            mel_level.save()
        return 1

    if message_dict['message_subtype'] in ['MIL']:
        if MIL.objects.filter(bmu=bmu,
                              TS=message_dict['received_time']).exists():
            return 0
        mil = MIL(bmu=bmu,
                  TS=message_dict['received_time'],
                  SD=message_dict['SD'],
                  SP=message_dict['SP'])
        mil.save()
        for data_point in message_dict['data_points'].values():
            mil_level = MILlevel(mil=mil,
                                 TS=data_point['TS'],
                                 VF=data_point['VF'])
            mil_level.save()
        return 1

    if message_dict['message_subtype'] in ['BOAL']:
        if BOAL.objects.filter(bmu=bmu,
                               TS=message_dict['received_time']).exists():
            return 0
        boal = BOAL(bmu=bmu,
                    TS=message_dict['received_time'],
                    NK=message_dict['NK'],
                    TA=message_dict['TA'],
                    AD=message_dict['AD'])
        boal.save()
        for data_point in message_dict['data_points'].values():
            boal_level = BOALlevel(boal=boal,
                                   TS=data_point['TS'],
                                   VA=data_point['VA'])
            boal_level.save()
        return 1

    if message_dict['message_subtype'] in ['BOALF']:
        if BOALF.objects.filter(bmu=bmu,
                                TS=message_dict['received_time']).exists():
            return 0
        boalf = BOALF(bmu=bmu,
                      TS=message_dict['received_time'],
                      NK=message_dict['NK'],
                      TA=message_dict['TA'],
                      AD=message_dict['AD'],
                      SO=message_dict['SO'],
                      PF=message_dict['PF'])
        boalf.save()
        for data_point in message_dict['data_points'].values():
            boalf_level = BOALFlevel(boalf=boalf,
                                     TS=data_point['TS'],
                                     VA=data_point['VA'])
            boalf_level.save()
        return 1

    if message_dict['message_subtype'] in ['BOD']:
        if BOD.objects.filter(bmu=bmu,
                              TS=message_dict['received_time']).exists():
            return 0
        #expecting 2 data pairs, raise error if note
        if len(message_dict['data_points']) != 2:
            raise ValueError('2 data points expected for BOD entry, %d found' %
                             len(message_dict['data_points']))
        bod = BOD(bmu=bmu,
                  TS=message_dict['received_time'],
                  SD=message_dict['SD'],
                  SP=message_dict['SP'],
                  NN=message_dict['NN'],
                  OP=message_dict['OP'],
                  BP=message_dict['BP'],
                  TS1=message_dict['data_points'][1]['TS'],
                  VB1=message_dict['data_points'][1]['VB'],
                  TS2=message_dict['data_points'][2]['TS'],
                  VB2=message_dict['data_points'][2]['VB'])
        bod.save()
        return 1

    if message_dict['message_subtype'] in ['BOAV']:
        if BOAV.objects.filter(bmu=bmu,
                               TS=message_dict['received_time']).exists():
            return 0
        boav = BOAV(bmu=bmu,
                    TS=message_dict['received_time'],
                    NK=message_dict['NK'],
                    SD=message_dict['SD'],
                    SP=message_dict['SP'],
                    NN=message_dict['NN'],
                    OV=message_dict['OV'],
                    BV=message_dict['BV'],
                    SA=message_dict['SA'])
        boav.save()
        return 1


    if message_dict['message_subtype'] in ['DISPTAV']:
        if DISPTAV.objects.filter(bmu=bmu,
                                  TS=message_dict['received_time']).exists():
            return 0
        disptav = DISPTAV(bmu=bmu,
                          TS=message_dict['received_time'],
                          SD=message_dict['SD'],
                          SP=message_dict['SP'],
                          NN=message_dict['NN'],
                          OV=message_dict['OV'],
                          BV=message_dict['BV'],
                          P1=message_dict['P1'],
                          P2=message_dict['P2'],
                          P3=message_dict['P3'],
                          P4=message_dict['P4'],
                          P5=message_dict['P5'],
                          P6=message_dict['P6'])
        disptav.save()
        return 1

    if message_dict['message_subtype'] in ['EBOCF']:
        if EBOCF.objects.filter(bmu=bmu,
                                TS=message_dict['received_time']).exists():
            return 0
        ebocf = EBOCF(bmu=bmu,
                      TS=message_dict['received_time'],
                      SD=message_dict['SD'],
                      SP=message_dict['SP'],
                      NN=message_dict['NN'],
                      OC=message_dict['OC'],
                      BC=message_dict['BC'])
        ebocf.save()
        return 1

    if message_dict['message_subtype'] in ['PTAV']:
        if PTAV.objects.filter(bmu=bmu,
                               TS=message_dict['received_time']).exists():
            return 0
        ptav = PTAV(bmu=bmu,
                    TS=message_dict['received_time'],
                    SD=message_dict['SD'],
                    SP=message_dict['SP'],
                    NN=message_dict['NN'],
                    OV=message_dict['OV'],
                    BV=message_dict['BV'])
        ptav.save()
        return 1

    if message_dict['message_subtype'] in ['QAS']:
        if QAS.objects.filter(bmu=bmu,
                              TS=message_dict['received_time']).exists():
            return 0
        qas = QAS(bmu=bmu,
                  TS=message_dict['received_time'],
                  SD=message_dict['SD'],
                  SP=message_dict['SP'],
                  SV=message_dict['SV'])
        qas.save()
        return 1

    if message_dict['message_subtype'] in ['QPN']:
        if QPN.objects.filter(bmu=bmu,
                              TS=message_dict['received_time']).exists():
            return 0
        qpn = QPN(bmu=bmu,
                  TS=message_dict['received_time'],
                  SD=message_dict['SD'],
                  SP=message_dict['SP'])
        qpn.save()
        for data_point in message_dict['data_points'].values():
            qpn_level = QPNlevel(qpn=qpn,
                                 TS=data_point['TS'],
                                 VP=data_point['VP'])
            qpn_level.save()
        return 1

    raise ValueError('Insert function not available for message subtype %s'
                     % message_dict['message_subtype'])




def insert_system_data(message_dict):
    """
    Generates and saves Django ORM object from message dictionary
    in order to insert a row of SYSTEM-level data to DB

    Parameters
    ----------
    message: message dictionary

    Returns
    -------
    None

    Raises
    ------

    """
    pass

def insert_dynamic_data(message_dict):
    """
    Generates and saves Django ORM object from message dictionary
    in order to insert a row of BMUID-level dynamic data to DB

    Parameters
    ----------
    message: message dictionary

    Returns
    -------
    None

    Raises
    ------

    """
    pass

def insert_info_data(message_dict):
    """
    Generates and saves Django ORM object from message dictionary
    in order to insert a row of info data to DB

    Parameters
    ----------
    message: message dictionary

    Returns
    -------
    None

    Raises
    ------

    """
    pass

def insert_bp_data(message_dict):
    """
    Generates and saves Django ORM object from message dictionary
    in order to insert a row of BP-level data to DB

    Parameters
    ----------
    message: message dictionary

    Returns
    -------
    None

    Raises
    ------

    """
    pass
