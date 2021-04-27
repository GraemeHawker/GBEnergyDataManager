"""
Helper functions for uploading data to database

"""
import datetime as dt
from itertools import zip_longest
from django.utils import timezone
from django.core.mail import send_mail
from ._data_definitions import PROCESSED_MESSAGES, ACCEPTED_MESSAGES, IGNORED_MESSAGES, FIELD_CASTING_FUNCS
from ._corrupt_message_list import CORRUPT_MESSAGES
from ._ignored_message_list import IGNORED_SYSMSG, IGNORED_SYSWARN
from GBEnergyDataManager.settings import SYS_WARN_EMAIL_RECIPIENTS, EMAIL_HOST_USER


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

    if no_points == 0:  # some cases where there is no data
        return data_dict
    # subdivide into iterables each containing single set of key,value pairs
    # see https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    if len(raw_message_part.split(',')) % no_points != 0:
        raise ValueError("Unexpected number of key/value pairs %s"
                         % raw_message_part)
    data_length = len(raw_message_part.split(',')) // no_points
    for data_set in zip_longest(*[iter(raw_message_part.split(','))] * data_length,
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
    if len(message_type_list) < 2:
        # occasional badly-formatted messages
        print('Not able to parse message type for message: {}'.format(raw_message))
        return None
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
            # for the system messages which also have an associated BMU ID
            # in the header
            message_subtype = message_type_list[3]
            message_dict['bmu_id'] = message_type_list[2]
        else:
            raise ValueError('Valid subtype not found for message type %s %s' %
                             (message_type, raw_message))
        message_dict['message_subtype'] = message_subtype
    elif message_type in IGNORED_MESSAGES:
        return None
    else:
        raise ValueError('message type %s not recognised %s' % (message_type,
                                                                raw_message))

    if message_subtype not in ACCEPTED_MESSAGES[message_type]:
        raise ValueError('message subtype %s not recognised for \
                         message type %s %s' %
                         (message_subtype,
                          message_type,
                          raw_message))

    key_values = raw_message[raw_message.find('{') + 1:raw_message.rfind('}')]

    for key_value in key_values.split(','):
        key = key_value[:key_value.find('=')].strip()
        if key == 'SW':  # edge case where commas can appear in field
            value = key_values[key_values.rfind(key) + 3:].strip()
            message_dict[key] = value
            return message_dict
        value = key_value[key_value.find('=') + 1:].strip()
        # key, value = key_value.split('=')
        # key = key.strip()
        if key in ['NP', 'NR']:  # process multiple datapoints
            raw_message_part = raw_message[raw_message.rfind(key):-1]
            raw_message_part = raw_message_part[raw_message_part.find(',') + 1:]
            message_dict['data_points'] = message_part_to_points(
                raw_message_part,
                int(value.strip()),
                message_type,
                message_subtype)
            break  # datapoints should be the final part of the message
        elif key in ACCEPTED_MESSAGES[message_type][message_subtype]:
            message_dict[key] = FIELD_CASTING_FUNCS[key](value)
        else:
            raise ValueError('message key %s not recognised for \
            message type %s and message subtype %s %s' %
                             (key, message_dict['message_type'],
                              message_dict['message_subtype'],
                              raw_message))
    # if message_subtype=='BOALF' and 'PF' not in message_dict: print(raw_message)
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
    '''
    if message_dict['message_subtype']=='SOSO':
        if message_dict['IC'] == 'EG_20200502_0100_1':
            print(message_dict)
    return {'unprocessed_msg' : {message_dict['message_subtype'] : 1}}
    '''

    if message_dict['message_subtype'] not in PROCESSED_MESSAGES[message_dict['message_type']]:
        return {'unprocessed_msg': {message_dict['message_subtype']: 1}}

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
    from BMRA.models.balancing import FPN, FPNlevel, MEL, MELlevel, MIL, MILlevel, \
        BOAL, BOALlevel, BOALF, BOALFlevel, BOD, DISPTAV, EBOCF, PTAV, QAS, QPN, QPNlevel, \
        BOAV

    from BMRA.models.core import BMU

    # dictionary of log messages
    insert_log = {}

    # check if BMUID already in db, if not insert and log
    try:
        bmu = BMU.objects.get(id=message_dict['bmu_id'])
    except BMU.DoesNotExist:
        insert_log['new_bmu'] = message_dict['bmu_id']
        bmu = BMU(id=message_dict['bmu_id'])
        bmu.save()

    # construct associated BM object
    if message_dict['message_subtype'] in ['FPN']:
        if FPN.objects.filter(bmu=bmu,
                              sd=message_dict['SD'],
                              sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        fpn = FPN(bmu=bmu,
                  ts=message_dict['received_time'],
                  sd=message_dict['SD'],
                  sp=message_dict['SP'])
        fpn.save()
        for data_point in message_dict['data_points'].values():
            fpn_level = FPNlevel(fpn=fpn,
                                 ts=data_point['TS'],
                                 vp=data_point['VP'])
            fpn_level.save()
        insert_log['new_entries'] = {'fpn': 1}
        return insert_log

    if message_dict['message_subtype'] in ['MEL']:
        if MEL.objects.filter(bmu=bmu,
                              ts=message_dict['received_time'],
                              sd=message_dict['SD'],
                              sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        mel = MEL(bmu=bmu,
                  ts=message_dict['received_time'],
                  sd=message_dict['SD'],
                  sp=message_dict['SP'])
        mel.save()
        for data_point in message_dict['data_points'].values():
            mel_level = MELlevel(mel=mel,
                                 ts=data_point['TS'],
                                 ve=data_point['VE'])
            mel_level.save()
        insert_log['new_entries'] = {'mel': 1}
        return insert_log

    if message_dict['message_subtype'] in ['MIL']:
        if MIL.objects.filter(bmu=bmu,
                              ts=message_dict['received_time'],
                              sd=message_dict['SD'],
                              sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        mil = MIL(bmu=bmu,
                  ts=message_dict['received_time'],
                  sd=message_dict['SD'],
                  sp=message_dict['SP'])
        mil.save()
        for data_point in message_dict['data_points'].values():
            mil_level = MILlevel(mil=mil,
                                 ts=data_point['TS'],
                                 vf=data_point['VF'])
            mil_level.save()
        insert_log['new_entries'] = {'mil': 1}
        return insert_log

    if message_dict['message_subtype'] in ['BOAL']:
        if BOAL.objects.filter(bmu=bmu,
                               ts=message_dict['received_time'],
                               nk=message_dict['NK']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        boal = BOAL(bmu=bmu,
                    ts=message_dict['received_time'],
                    nk=message_dict['NK'],
                    ta=message_dict['TA'],
                    ad=message_dict['AD'])
        boal.save()
        for data_point in message_dict['data_points'].values():
            boal_level = BOALlevel(boal=boal,
                                   ts=data_point['TS'],
                                   va=data_point['VA'])
            boal_level.save()
        insert_log['new_entries'] = {'boal': 1}
        return insert_log

    if message_dict['message_subtype'] in ['BOALF']:
        if BOALF.objects.filter(bmu=bmu,
                                ts=message_dict['received_time'],
                                nk=message_dict['NK']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        boalf = BOALF(bmu=bmu,
                      ts=message_dict['received_time'],
                      nk=message_dict['NK'],
                      ta=message_dict['TA'],
                      ad=message_dict['AD'],
                      so=message_dict['SO'],
                      pf=message_dict.get('PF'),
                      rn=message_dict.get('RN'),
                      sc=message_dict.get('SC'))
        boalf.save()
        for data_point in message_dict['data_points'].values():
            boalf_level = BOALFlevel(boalf=boalf,
                                     ts=data_point['TS'],
                                     va=data_point['VA'])
            boalf_level.save()
        insert_log['new_entries'] = {'boalf': 1}
        return insert_log

    if message_dict['message_subtype'] in ['BOD']:
        if BOD.objects.filter(bmu=bmu,
                              ts=message_dict['received_time'],
                              sd=message_dict['SD'],
                              sp=message_dict['SP'],
                              nn=message_dict['NN']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        # expecting 2 data pairs, raise error if note
        if len(message_dict['data_points']) != 2:
            raise ValueError('2 data points expected for BOD entry, %d found' %
                             len(message_dict['data_points']))
        bod = BOD(bmu=bmu,
                  ts=message_dict['received_time'],
                  sd=message_dict['SD'],
                  sp=message_dict['SP'],
                  nn=message_dict['NN'],
                  op=message_dict['OP'],
                  bp=message_dict['BP'],
                  ts1=message_dict['data_points'][1]['TS'],
                  vb1=message_dict['data_points'][1]['VB'],
                  ts2=message_dict['data_points'][2]['TS'],
                  vb2=message_dict['data_points'][2]['VB'])
        bod.save()
        insert_log['new_entries'] = {'bod': 1}
        return insert_log

    if message_dict['message_subtype'] in ['BOAV']:
        if BOAV.objects.filter(bmu=bmu,
                               nk=message_dict['NK'],
                               sd=message_dict['SD'],
                               sp=message_dict['SP'],
                               nn=message_dict['NN']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        boav = BOAV(bmu=bmu,
                    ts=message_dict['received_time'],
                    nk=message_dict['NK'],
                    sd=message_dict['SD'],
                    sp=message_dict['SP'],
                    nn=message_dict['NN'],
                    ov=message_dict['OV'],
                    bv=message_dict['BV'],
                    sa=message_dict['SA'])
        boav.save()
        insert_log['new_entries'] = {'boav': 1}
        return insert_log

    if message_dict['message_subtype'] in ['DISPTAV']:
        if DISPTAV.objects.filter(bmu=bmu,
                                  sd=message_dict['SD'],
                                  sp=message_dict['SP'],
                                  nn=message_dict['NN'],
                                  ts=message_dict['received_time']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        disptav = DISPTAV(bmu=bmu,
                          ts=message_dict['received_time'],
                          sd=message_dict['SD'],
                          sp=message_dict['SP'],
                          nn=message_dict['NN'],
                          ov=message_dict['OV'],
                          bv=message_dict['BV'],
                          p1=message_dict['P1'],
                          p2=message_dict['P2'],
                          p3=message_dict['P3'],
                          p4=message_dict['P4'],
                          p5=message_dict['P5'],
                          p6=message_dict['P6'])
        disptav.save()
        insert_log['new_entries'] = {'disptav': 1}
        return insert_log

    if message_dict['message_subtype'] in ['EBOCF']:
        if EBOCF.objects.filter(bmu=bmu,
                                sd=message_dict['SD'],
                                sp=message_dict['SP'],
                                nn=message_dict['NN']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        ebocf = EBOCF(bmu=bmu,
                      ts=message_dict['received_time'],
                      sd=message_dict['SD'],
                      sp=message_dict['SP'],
                      nn=message_dict['NN'],
                      oc=message_dict['OC'],
                      bc=message_dict['BC'])
        ebocf.save()
        insert_log['new_entries'] = {'ebocf': 1}
        return insert_log

    if message_dict['message_subtype'] in ['PTAV']:
        if PTAV.objects.filter(bmu=bmu,
                               sd=message_dict['SD'],
                               sp=message_dict['SP'],
                               nn=message_dict['NN']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        ptav = PTAV(bmu=bmu,
                    ts=message_dict['received_time'],
                    sd=message_dict['SD'],
                    sp=message_dict['SP'],
                    nn=message_dict['NN'],
                    ov=message_dict['OV'],
                    bv=message_dict['BV'])
        ptav.save()
        insert_log['new_entries'] = {'ptav': 1}
        return insert_log

    if message_dict['message_subtype'] in ['QAS']:
        if QAS.objects.filter(bmu=bmu,
                              sd=message_dict['SD'],
                              sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        qas = QAS(bmu=bmu,
                  ts=message_dict['received_time'],
                  sd=message_dict['SD'],
                  sp=message_dict['SP'],
                  sv=message_dict['SV'])
        qas.save()
        insert_log['new_entries'] = {'qas': 1}
        return insert_log

    if message_dict['message_subtype'] in ['QPN']:
        if QPN.objects.filter(bmu=bmu,
                              sd=message_dict['SD'],
                              sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        qpn = QPN(bmu=bmu,
                  ts=message_dict['received_time'],
                  sd=message_dict['SD'],
                  sp=message_dict['SP'])
        qpn.save()
        for data_point in message_dict['data_points'].values():
            qpn_level = QPNlevel(qpn=qpn,
                                 ts=data_point['TS'],
                                 vp=data_point['VP'])
            qpn_level.save()
        insert_log['new_entries'] = {'qpn': 1}
        return insert_log

    raise ValueError('Insert function not available for message subtype %s'
                     % message_dict['message_subtype'])


def insert_system_data(message_dict):
    """
    Generates and saves Django ORM object from message dictionary
    in order to insert a row of SYSTEM-level data to DB

    Parameters
    ----------
    message_dict: message dictionary

    Returns
    -------
    None

    Raises
    ------

    """
    from BMRA.models import BMU, BSAD, DISBSAD, NETBSAD, MID, EBSP, NETEBSP, \
        DISEBSP, SOSO, ISPSTACK, TBOD, FREQ, TEMP, INDO, ITSDO, LOLP, \
        LOLPlevel, NONBM, INDOD, FUELINST, FUELHH, SYSMSG, DCONTROL, LDSO, FT, \
        SYSWARN, DCONTROLlevel, DF, ZI, NDF, TSDF, IMBALNGC, INDGEN, INDDEM, \
        MELNGC, NDFD, TSDFD, TSDFW, NDFW, OCNMFW, OCNMFW2, OCNMF3Y2, FOU2T14D, FOU2T52W, \
        UOU2T14D, UOU2T52W, WINDFOR, OCNMFD, OCNMFD2, NOU2T14D, NOU2T52W, NOU2T3YW, \
        OCNMF3Y, FOU2T3YW, UOU2T3YW

    insert_log = {}
    # construct associated SYSTEM object
    if message_dict['message_subtype'] in ['BSAD']:
        if BSAD.objects.filter(sd=message_dict['SD'],
                               sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        bsad = BSAD(sd=message_dict['SD'],
                    sp=message_dict['SP'],
                    a1=message_dict['A1'],
                    a2=message_dict['A2'],
                    a3=message_dict['A3'],
                    a4=message_dict['A4'],
                    a5=message_dict['A5'],
                    a6=message_dict['A6'])
        bsad.save()
        insert_log['new_entries'] = {'bsad': 1}
        return insert_log

    if message_dict['message_subtype'] in ['DCONTROL']:
        if DCONTROL.objects.filter(tp=message_dict['TP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        dcontrol = DCONTROL(tp=message_dict['TP'])
        dcontrol.save()
        for data_point in message_dict['data_points'].values():
            try:
                ldso = LDSO.objects.get(id=data_point['DS'])
            except LDSO.DoesNotExist:
                ldso = LDSO(id=data_point['DS'])
                ldso.save()
            dcontrol_level = DCONTROLlevel(dcontrol=dcontrol,
                                           ds=ldso,
                                           dcid=data_point['ID'],
                                           sq=data_point['SQ'],
                                           ev=data_point['EV'],
                                           tf=data_point['TF'],
                                           ti=data_point['TI'],
                                           vo=data_point['VO'],
                                           so=data_point['SO'],
                                           am=data_point['AM'])
            dcontrol_level.save()
        insert_log['new_entries'] = {'dcontrol': 1}
        return insert_log

    if message_dict['message_subtype'] in ['DF']:
        zi = ZI.objects.get_or_create(id=message_dict['ZI'])[0]
        for data_point in message_dict['data_points'].values():
            if DF.objects.filter(zi=zi,
                                 tp=data_point['TP'],
                                 sd=data_point['SD'],
                                 sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            df = DF(zi=zi,
                    tp=data_point['TP'],
                    sd=data_point['SD'],
                    sp=data_point['SP'],
                    vd=data_point['VD'])
            df.save()
        insert_log['new_entries'] = {'df': 1}
        return insert_log

    if message_dict['message_subtype'] in ['NDF']:
        zi = ZI.objects.get_or_create(id=message_dict['ZI'])[0]
        for data_point in message_dict['data_points'].values():
            if NDF.objects.filter(zi=zi,
                                  tp=data_point['TP'],
                                  sd=data_point['SD'],
                                  sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ndf = NDF(zi=zi,
                      tp=data_point['TP'],
                      sd=data_point['SD'],
                      sp=data_point['SP'],
                      vd=data_point['VD'])
            ndf.save()
        insert_log['new_entries'] = {'ndf': 1}
        return insert_log

    if message_dict['message_subtype'] in ['TSDF']:
        zi = ZI.objects.get_or_create(id=message_dict['ZI'])[0]
        for data_point in message_dict['data_points'].values():
            if TSDF.objects.filter(zi=zi,
                                   tp=data_point['TP'],
                                   sd=data_point['SD'],
                                   sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            tsdf = TSDF(zi=zi,
                        tp=data_point['TP'],
                        sd=data_point['SD'],
                        sp=data_point['SP'],
                        vd=data_point['VD'])
            tsdf.save()
        insert_log['new_entries'] = {'tsdf': 1}
        return insert_log

    if message_dict['message_subtype'] in ['IMBALNGC']:
        zi = ZI.objects.get_or_create(id=message_dict['ZI'])[0]
        for data_point in message_dict['data_points'].values():
            if IMBALNGC.objects.filter(zi=zi,
                                       tp=data_point['TP'],
                                       sd=data_point['SD'],
                                       sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            imbalngc = IMBALNGC(zi=zi,
                                tp=data_point['TP'],
                                sd=data_point['SD'],
                                sp=data_point['SP'],
                                vi=data_point['VI'])
            imbalngc.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['INDGEN']:
        zi = ZI.objects.get_or_create(id=message_dict['ZI'])[0]
        for data_point in message_dict['data_points'].values():
            if INDGEN.objects.filter(zi=zi,
                                     tp=data_point['TP'],
                                     sd=data_point['SD'],
                                     sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            indgen = INDGEN(zi=zi,
                            tp=data_point['TP'],
                            sd=data_point['SD'],
                            sp=data_point['SP'],
                            vg=data_point['VG'])
            indgen.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['MELNGC']:
        zi = ZI.objects.get_or_create(id=message_dict['ZI'])[0]
        for data_point in message_dict['data_points'].values():
            if MELNGC.objects.filter(zi=zi,
                                     tp=data_point['TP'],
                                     sd=data_point['SD'],
                                     sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            melngc = MELNGC(zi=zi,
                            tp=data_point['TP'],
                            sd=data_point['SD'],
                            sp=data_point['SP'],
                            vm=data_point['VM'])
            melngc.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['INDDEM']:
        zi = ZI.objects.get_or_create(id=message_dict['ZI'])[0]
        for data_point in message_dict['data_points'].values():
            if INDDEM.objects.filter(zi=zi,
                                     tp=data_point['TP'],
                                     sd=data_point['SD'],
                                     sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            inddem = INDDEM(zi=zi,
                            tp=data_point['TP'],
                            sd=data_point['SD'],
                            sp=data_point['SP'],
                            vd=data_point['VD'])
            inddem.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['NDFD']:
        for data_point in message_dict['data_points'].values():
            if NDFD.objects.filter(tp=message_dict['TP'],
                                   sd=data_point['SD'],
                                   sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ndfd = NDFD(tp=message_dict['TP'],
                        sd=data_point['SD'],
                        sp=data_point['SP'],
                        vd=data_point['VD'])
            ndfd.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['TSDFD']:
        for data_point in message_dict['data_points'].values():
            if TSDFD.objects.filter(tp=message_dict['TP'],
                                    sd=data_point['SD'],
                                    sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            tsdfd = TSDFD(tp=message_dict['TP'],
                          sd=data_point['SD'],
                          sp=data_point['SP'],
                          vd=data_point['VD'])
            tsdfd.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['TSDFW']:
        for data_point in message_dict['data_points'].values():
            if TSDFW.objects.filter(tp=message_dict['TP'],
                                    wd=data_point['WD'],
                                    wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            tsdfw = TSDFW(tp=message_dict['TP'],
                          wd=data_point['WD'],
                          wn=data_point['WN'],
                          vd=data_point['VD'])
            tsdfw.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['NDFW']:
        for data_point in message_dict['data_points'].values():
            if NDFW.objects.filter(tp=message_dict['TP'],
                                   wd=data_point['WD'],
                                   wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ndfw = NDFW(tp=message_dict['TP'],
                        wd=data_point['WD'],
                        wn=data_point['WN'],
                        vd=data_point['VD'])
            ndfw.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['NOU2T14D']:
        for data_point in message_dict['data_points'].values():
            if NOU2T14D.objects.filter(tp=message_dict['TP'],
                                       sd=data_point['SD'],
                                       sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            nou2t14d = NOU2T14D(tp=message_dict['TP'],
                                sd=data_point['SD'],
                                sp=data_point['SP'],
                                ou=data_point['OU'])
            nou2t14d.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['NOU2T52W']:
        for data_point in message_dict['data_points'].values():
            if NOU2T52W.objects.filter(tp=message_dict['TP'],
                                       cy=data_point['CY'],
                                       wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            nou2t52w = NOU2T52W(tp=message_dict['TP'],
                                cy=data_point['CY'],
                                wn=data_point['WN'],
                                ou=data_point['OU'])
            nou2t52w.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['NOU2T3YW']:
        for data_point in message_dict['data_points'].values():
            if NOU2T3YW.objects.filter(tp=message_dict['TP'],
                                       cy=data_point['CY'],
                                       wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            nou2t3yw = NOU2T3YW(tp=message_dict['TP'],
                                cy=data_point['CY'],
                                wn=data_point['WN'],
                                ou=data_point['OU'])
            nou2t3yw.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['OCNMFD']:
        for data_point in message_dict['data_points'].values():
            if OCNMFD.objects.filter(tp=message_dict['TP'],
                                     sd=data_point['SD'],
                                     sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ocnmfd = OCNMFD(tp=message_dict['TP'],
                            sd=data_point['SD'],
                            sp=data_point['SP'],
                            vm=data_point['VM'])
            ocnmfd.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['OCNMFW']:
        for data_point in message_dict['data_points'].values():
            if OCNMFW.objects.filter(tp=message_dict['TP'],
                                     wd=data_point['WD'],
                                     wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ocnmfw = OCNMFW(tp=message_dict['TP'],
                            wd=data_point['WD'],
                            wn=data_point['WN'],
                            vm=data_point['VM'])
            ocnmfw.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['OCNMF3Y']:
        for data_point in message_dict['data_points'].values():
            if OCNMF3Y.objects.filter(tp=message_dict['TP'],
                                      cy=data_point['CY'],
                                      wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ocnmf3y = OCNMF3Y(tp=message_dict['TP'],
                              cy=data_point['CY'],
                              wn=data_point['WN'],
                              vm=data_point['VM'])
            ocnmf3y.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['OCNMFW2']:
        for data_point in message_dict['data_points'].values():
            if OCNMFW2.objects.filter(tp=message_dict['TP'],
                                      cy=data_point['CY'],
                                      wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ocnmfw2 = OCNMFW2(tp=message_dict['TP'],
                              cy=data_point['CY'],
                              wn=data_point['WN'],
                              dm=data_point['DM'])
            ocnmfw2.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['OCNMF3Y2']:
        for data_point in message_dict['data_points'].values():
            if OCNMF3Y2.objects.filter(tp=message_dict['TP'],
                                      cy=data_point['CY'],
                                      wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ocnmf3y2 = OCNMF3Y2(tp=message_dict['TP'],
                              cy=data_point['CY'],
                              wn=data_point['WN'],
                              dm=data_point['DM'])
            ocnmf3y2.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['WINDFOR']:
        for data_point in message_dict['data_points'].values():
            if WINDFOR.objects.filter(tp=data_point['TP'],
                                      sd=data_point['SD'],
                                      sp=data_point['SP']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            windfor = WINDFOR(tp=data_point['TP'],
                              sd=data_point['SD'],
                              sp=data_point['SP'],
                              vg=data_point['VG'],
                              tr=data_point['TR'])
            windfor.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['OCNMFD2']:
        for data_point in message_dict['data_points'].values():
            if OCNMFD2.objects.filter(tp=message_dict['TP'],
                                      sd=data_point['SD']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            ocnmfd2 = OCNMFD2(tp=message_dict['TP'],
                              sd=data_point['SD'],
                              dm=data_point['DM'])
            ocnmfd2.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['FOU2T14D']:
        for data_point in message_dict['data_points'].values():
            ft = FT.objects.get_or_create(id=data_point['FT'])[0]
            if FOU2T14D.objects.filter(tp=message_dict['TP'],
                                       ft=ft,
                                       sd=data_point['SD']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            fou2t14d = FOU2T14D(tp=message_dict['TP'],
                                ft=ft,
                                sd=data_point['SD'],
                                ou=data_point['OU'])
            fou2t14d.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['FOU2T52W']:
        for data_point in message_dict['data_points'].values():
            ft = FT.objects.get_or_create(id=data_point['FT'])[0]
            if FOU2T52W.objects.filter(tp=message_dict['TP'],
                                       ft=ft,
                                       cy=data_point['CY'],
                                       wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            fou2t52w = FOU2T52W(tp=message_dict['TP'],
                                ft=ft,
                                cy=data_point['CY'],
                                wn=data_point['WN'],
                                ou=data_point['OU'])
            fou2t52w.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['FOU2T3YW']:
        for data_point in message_dict['data_points'].values():
            ft = FT.objects.get_or_create(id=data_point['FT'])[0]
            if FOU2T3YW.objects.filter(tp=message_dict['TP'],
                                       ft=ft,
                                       cy=data_point['CY'],
                                       wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            fou2t52w = FOU2T3YW(tp=message_dict['TP'],
                                ft=ft,
                                cy=data_point['CY'],
                                wn=data_point['WN'],
                                ou=data_point['OU'])
            fou2t52w.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['UOU2T14D']:
        bmu = BMU.objects.get_or_create(id=message_dict['bmu_id'])[0]
        for data_point in message_dict['data_points'].values():
            ft = FT.objects.get_or_create(id=data_point['FT'])[0]
            if UOU2T14D.objects.filter(tp=message_dict['TP'],
                                       bmu=bmu,
                                       ft=ft,
                                       sd=data_point['SD']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            uou2t14d = UOU2T14D(tp=message_dict['TP'],
                                bmu=bmu,
                                ft=ft,
                                sd=data_point['SD'],
                                ou=data_point['OU'])
            uou2t14d.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['UOU2T52W']:
        bmu = BMU.objects.get_or_create(id=message_dict['bmu_id'])[0]
        for data_point in message_dict['data_points'].values():
            ft = FT.objects.get_or_create(id=data_point['FT'])[0]
            if UOU2T52W.objects.filter(tp=message_dict['TP'],
                                       bmu=bmu,
                                       ft=ft,
                                       cy=data_point['CY'],
                                       wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            uou2t52w = UOU2T52W(tp=message_dict['TP'],
                                bmu=bmu,
                                ft=ft,
                                cy=data_point['CY'],
                                wn=data_point['WN'],
                                ou=data_point['OU'])
            uou2t52w.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['UOU2T3YW']:
        bmu = BMU.objects.get_or_create(id=message_dict['bmu_id'])[0]
        for data_point in message_dict['data_points'].values():
            ft = FT.objects.get_or_create(id=data_point['FT'])[0]
            if UOU2T3YW.objects.filter(tp=message_dict['TP'],
                                       bmu=bmu,
                                       ft=ft,
                                       cy=data_point['CY'],
                                       wn=data_point['WN']).exists():
                return {'duplicate_msg': {message_dict['message_subtype']: 1}}
            uou2t3yw = UOU2T3YW(tp=message_dict['TP'],
                                bmu=bmu,
                                ft=ft,
                                cy=data_point['CY'],
                                wn=data_point['WN'],
                                ou=data_point['OU'])
            uou2t3yw.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['DISBSAD']:
        if DISBSAD.objects.filter(sd=message_dict['SD'],
                                  sp=message_dict['SP'],
                                  ai=message_dict['AI']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        disbsad = DISBSAD(sd=message_dict['SD'],
                          sp=message_dict['SP'],
                          ai=message_dict['AI'],
                          so=message_dict['SO'],
                          pf=message_dict['PF'],
                          jc=message_dict['JC'],
                          jv=message_dict['JV'])
        disbsad.save()
        insert_log['new_entries'] = {'disbsad': 1}
        return insert_log

    if message_dict['message_subtype'] in ['DISEBSP']:
        if DISEBSP.objects.filter(sd=message_dict['SD'],
                                  sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        if 'RSP' in message_dict:
            rsp = message_dict['RSP']
        else:
            rsp = None
        if 'RP' in message_dict:
            rp = message_dict['RP']
        else:
            rp = None
        if 'RV' in message_dict:
            rv = message_dict['RV']
        else:
            rv = None
        disebsp = DISEBSP(sd=message_dict['SD'],
                          sp=message_dict['SP'],
                          pb=message_dict['PB'],
                          ps=message_dict['PS'],
                          pd=message_dict['PD'],
                          rsp=rsp,
                          rp=rp,
                          rv=rv,
                          bd=message_dict['BD'],
                          a3=message_dict['A3'],
                          a6=message_dict['A6'],
                          ni=message_dict['NI'],
                          ao=message_dict['AO'],
                          ab=message_dict['AB'],
                          t1=message_dict['T1'],
                          t2=message_dict['T2'],
                          pp=message_dict['PP'],
                          pc=message_dict['PC'],
                          j1=message_dict['J1'],
                          j2=message_dict['J2'],
                          j3=message_dict['J3'],
                          j4=message_dict['J4'])
        disebsp.save()
        insert_log['new_entries'] = {'disebsp': 1}
        return insert_log

    if message_dict['message_subtype'] in ['EBSP']:
        if EBSP.objects.filter(sd=message_dict['SD'],
                               sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        ebsp = EBSP(sd=message_dict['SD'],
                    sp=message_dict['SP'],
                    pb=message_dict['PB'],
                    ps=message_dict['PS'],
                    ao=message_dict['AO'],
                    ab=message_dict['AB'],
                    ap=message_dict['AP'],
                    ac=message_dict['AC'],
                    pp=message_dict['AP'],
                    pc=message_dict['PC'],
                    bd=message_dict['BD'],
                    a1=message_dict['A1'],
                    a2=message_dict['A2'],
                    a3=message_dict['A3'],
                    a4=message_dict['A4'],
                    a5=message_dict['A5'],
                    a6=message_dict['A6'])
        ebsp.save()
        insert_log['new_entries'] = {'ebsp': 1}
        return insert_log

    if message_dict['message_subtype'] in ['FREQ']:
        if FREQ.objects.filter(ts=message_dict['TS']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        freq = FREQ(ts=message_dict['TS'],
                    sf=message_dict['SF'])
        freq.save()
        insert_log['new_entries'] = {'freq': 1}
        return insert_log

    if message_dict['message_subtype'] in ['FUELHH']:
        try:
            ft = FT.objects.get(id=message_dict['FT'])
        except FT.DoesNotExist:
            ft = FT(id=message_dict['FT'])
            ft.save()
        if FUELHH.objects.filter(sd=message_dict['SD'],
                                 sp=message_dict['SP'],
                                 tp=message_dict['TP'],
                                 ft=ft).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        fuelhh = FUELHH(tp=message_dict['TP'],
                        sd=message_dict['SD'],
                        sp=message_dict['SP'],
                        ft=ft,
                        fg=message_dict['FG'])
        fuelhh.save()
        insert_log['new_entries'] = {'fuelhh': 1}
        return insert_log

    if message_dict['message_subtype'] in ['FUELINST']:
        try:
            ft = FT.objects.get(id=message_dict['FT'])
        except FT.DoesNotExist:
            ft = FT(id=message_dict['FT'])
            ft.save()
        if FUELINST.objects.filter(sd=message_dict['SD'],
                                   sp=message_dict['SP'],
                                   ts=message_dict['TS'],
                                   tp=message_dict['TP'],
                                   ft=ft).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        fuelinst = FUELINST(tp=message_dict['TP'],
                            sd=message_dict['SD'],
                            sp=message_dict['SP'],
                            ts=message_dict['TS'],
                            ft=ft,
                            fg=message_dict['FG'])
        fuelinst.save()
        insert_log['new_entries'] = {'fuelinst': 1}
        return insert_log

    if message_dict['message_subtype'] in ['INDO']:
        if INDO.objects.filter(sd=message_dict['SD'],
                               sp=message_dict['SP'],
                               tp=message_dict['TP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        indo = INDO(tp=message_dict['TP'],
                    sd=message_dict['SD'],
                    sp=message_dict['SP'],
                    vd=message_dict['VD'])
        indo.save()
        insert_log['new_entries'] = {'indo': 1}
        return insert_log

    if message_dict['message_subtype'] in ['INDOD']:
        if INDOD.objects.filter(sd=message_dict['SD'],
                                tp=message_dict['TP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        indod = INDOD(tp=message_dict['TP'],
                      sd=message_dict['SD'],
                      eo=message_dict['EO'],
                      el=message_dict['EL'],
                      eh=message_dict['EH'],
                      en=message_dict['EN'])
        indod.save()
        insert_log['new_entries'] = {'indod': 1}
        return insert_log

    if message_dict['message_subtype'] in ['TBOD']:
        if TBOD.objects.filter(sd=message_dict['SD'],
                               sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        tbod = TBOD(sd=message_dict['SD'],
                    sp=message_dict['SP'],
                    ot=message_dict['OT'],
                    bt=message_dict['BT'])
        tbod.save()
        insert_log['new_entries'] = {'tbod': 1}
        return insert_log

    if message_dict['message_subtype'] in ['ISPSTACK']:
        if 'NN' in message_dict:
            nn = message_dict['NN']
        else:
            nn = None
        if 'NK' in message_dict:
            nk = message_dict['NK']
        else:
            nk = None
        if ISPSTACK.objects.filter(sd=message_dict['SD'],
                                   sp=message_dict['SP'],
                                   ci=message_dict['CI'],
                                   bo=message_dict['BO'],
                                   nn=nn,
                                   nk=nk,
                                   sn=message_dict['SN']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        if 'RSP' in message_dict:
            rsp = message_dict['RSP']
        else:
            rsp = None
        ispstack = ISPSTACK(sd=message_dict['SD'],
                            sp=message_dict['SP'],
                            bo=message_dict['BO'],
                            sn=message_dict['SN'],
                            ci=message_dict['CI'],
                            nk=nk,
                            nn=nn,
                            cf=message_dict['CF'],
                            so=message_dict['SO'],
                            pf=message_dict['PF'],
                            ri=message_dict['RI'],
                            up=message_dict['UP'],
                            rsp=rsp,
                            ip=message_dict['IP'],
                            iv=message_dict['IV'],
                            da=message_dict['DA'],
                            av=message_dict['AV'],
                            nv=message_dict['NV'],
                            pv=message_dict['PV'],
                            fp=message_dict['FP'],
                            tm=message_dict['TM'],
                            tv=message_dict['TV'],
                            tc=message_dict['TC'])
        ispstack.save()
        insert_log['new_entries'] = {'ispstack': 1}
        return insert_log

    if message_dict['message_subtype'] in ['ITSDO']:
        if ITSDO.objects.filter(sd=message_dict['SD'],
                                sp=message_dict['SP'],
                                tp=message_dict['TP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        itsdo = ITSDO(tp=message_dict['TP'],
                      sd=message_dict['SD'],
                      sp=message_dict['SP'],
                      vd=message_dict['VD'])
        itsdo.save()
        insert_log['new_entries'] = {'itsdo': 1}
        return insert_log

    if message_dict['message_subtype'] in ['LOLP']:
        if LOLP.objects.filter(tp=message_dict['TP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        lolp = LOLP(tp=message_dict['TP'])
        lolp.save()
        for data_point in message_dict['data_points'].values():
            lolp_level = LOLPlevel(lolp=lolp,
                                   sd=data_point['SD'],
                                   sp=data_point['SP'],
                                   lp=data_point['LP'],
                                   dr=data_point['DR'])
            lolp_level.save()
        insert_log['new_entries'] = {'lolp': 1}
        return insert_log

    if message_dict['message_subtype'] in ['MID']:
        if MID.objects.filter(mi=message_dict['MI'],
                              sd=message_dict['SD'],
                              sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        mid = MID(mi=message_dict['MI'],
                  sd=message_dict['SD'],
                  sp=message_dict['SP'],
                  m1=message_dict['M1'],
                  m2=message_dict['M2'])
        mid.save()
        insert_log['new_entries'] = {'mid': 1}
        return insert_log

    # for unknown reasons, multiple NETBSAD messages can be present
    # for the same SP. If we get a message covering an existing SP,
    # then update the existing object with the new data
    if message_dict['message_subtype'] in ['NETBSAD']:
        netbsad, created = NETBSAD.objects.update_or_create(sd=message_dict['SD'],
                                                            sp=message_dict['SP'],
                                                            defaults={'a7': message_dict['A7'],
                                                                      'a8': message_dict['A8'],
                                                                      'a11': message_dict['A11'],
                                                                      'a3': message_dict['A3'],
                                                                      'a9': message_dict['A9'],
                                                                      'a10': message_dict['A10'],
                                                                      'a12': message_dict['A12'],
                                                                      'a6': message_dict['A6']})
        if created:
            insert_log['new_entries'] = {'netbsad': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['NETEBSP']:
        if NETEBSP.objects.filter(sd=message_dict['SD'],
                                  sp=message_dict['SP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        netebsp = NETEBSP(sd=message_dict['SD'],
                          sp=message_dict['SP'],
                          pb=message_dict['PB'],
                          ps=message_dict['PS'],
                          pd=message_dict['PD'],
                          ao=message_dict['AO'],
                          ab=message_dict['AB'],
                          ap=message_dict['AP'],
                          ac=message_dict['AC'],
                          pp=message_dict['AP'],
                          pc=message_dict['PC'],
                          ni=message_dict['NI'],
                          bd=message_dict['BD'],
                          a7=message_dict['A7'],
                          a8=message_dict['A8'],
                          a11=message_dict['A11'],
                          a3=message_dict['A3'],
                          a9=message_dict['A9'],
                          a10=message_dict['A10'],
                          a12=message_dict['A12'],
                          a6=message_dict['A6'])
        netebsp.save()
        insert_log['new_entries'] = {'netebsp': 1}
        return insert_log

    if message_dict['message_subtype'] in ['NONBM']:
        if NONBM.objects.filter(sd=message_dict['SD'],
                                sp=message_dict['SP'],
                                tp=message_dict['TP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        nonbm = NONBM(tp=message_dict['TP'],
                      sd=message_dict['SD'],
                      sp=message_dict['SP'],
                      nb=message_dict['NB'])
        nonbm.save()
        insert_log['new_entries'] = {'nonbm': 1}
        return insert_log

    if message_dict['message_subtype'] in ['SOSO']:
        if SOSO.objects.filter(ic=message_dict['IC'],
                               tt=message_dict['TT'],
                               st=message_dict['ST'],
                               td=message_dict['TD']).exists():
            #print(message_dict)
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        soso = SOSO(tt=message_dict['TT'],
                    st=message_dict['ST'],
                    td=message_dict['TD'],
                    ic=message_dict['IC'],
                    tq=message_dict['TQ'],
                    pt=message_dict['PT'])
        soso.save()
        insert_log['new_entries'] = {message_dict['message_subtype']: 1}
        return insert_log

    if message_dict['message_subtype'] in ['SYSMSG']:
        if SYSMSG.objects.filter(tp=message_dict['TP'],
                                 mt=message_dict['MT'],
                                 sm=message_dict['SM']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        sysmsg = SYSMSG(tp=message_dict['TP'],
                        mt=message_dict['MT'],
                        sm=message_dict['SM'])
        sysmsg.save()

        # email mailing list with contents if not in ignored list
        if not any(sysmsg in message_dict['SM'] for sysmsg in IGNORED_SYSMSG):
            send_mail(
                'BMRA System Message Received',
                '{:%Y-%m-%d %H:%M:%S} {} {}'.format(message_dict['TP'],
                                                    message_dict['MT'],
                                                    message_dict['SM']),
                EMAIL_HOST_USER,
                SYS_WARN_EMAIL_RECIPIENTS,
                fail_silently=False,
            )
        insert_log['new_entries'] = {'sysmsg': 1}
        return insert_log

    if message_dict['message_subtype'] in ['SYSWARN']:
        if SYSWARN.objects.filter(tp=message_dict['TP'],
                                  sw=message_dict['SW']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        syswarn = SYSWARN(tp=message_dict['TP'],
                          sw=message_dict['SW'])
        syswarn.save()

        # email mailing list with contents if not in ignored list
        if not any(sysmsg in message_dict['SW'] for sysmsg in IGNORED_SYSWARN):
            send_mail(
                'BMRA System Message Received',
                '{:%Y-%m-%d %H:%M:%S} {}'.format(message_dict['TP'],
                                                 message_dict['SW']),
                EMAIL_HOST_USER,
                SYS_WARN_EMAIL_RECIPIENTS,
                fail_silently=False,
            )
        insert_log['new_entries'] = {'syswarn': 1}
        return insert_log

    if message_dict['message_subtype'] in ['TEMP']:
        if TEMP.objects.filter(ts=message_dict['TS'],
                               tp=message_dict['TP']).exists():
            return {'duplicate_msg': {message_dict['message_subtype']: 1}}
        temp = TEMP(ts=message_dict['TS'],
                    tp=message_dict['TP'],
                    to=message_dict['TO'],
                    tn=message_dict['TN'],
                    tl=message_dict['TL'],
                    th=message_dict['TH'])
        temp.save()
        insert_log['new_entries'] = {'temp': 1}
        return insert_log


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
    from BMRA.models.core import BMU
    from BMRA.models.dynamic import SIL, SEL, MNZT, NDZ, RURE, RURI, RDRE, RDRI, \
        MDV, MDP, MZT, NTB, NTO

    insert_log = {}

    # check if BMUID already in db, if not insert and log
    try:
        bmu = BMU.objects.get(id=message_dict['bmu_id'])
    except BMU.DoesNotExist:
        bmu = BMU(id=message_dict['bmu_id'])
        insert_log['new_bmu'] = message_dict['bmu_id']
        bmu.save()

    if message_dict['message_subtype'] in ['SIL']:
        sil, created = SIL.objects.get_or_create(bmu=bmu,
                                                 te=message_dict['TE'],
                                                 si=message_dict['SI'])
        if created:
            insert_log['new_entries'] = {'sil': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['SEL']:
        sel, created = SEL.objects.get_or_create(bmu=bmu,
                                                 te=message_dict['TE'],
                                                 se=message_dict['SE'])
        if created:
            insert_log['new_entries'] = {'sel': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['MNZT']:
        mnzt, created = MNZT.objects.get_or_create(bmu=bmu,
                                                   te=message_dict['TE'],
                                                   mn=message_dict['MN'])
        if created:
            insert_log['new_entries'] = {'mnzt': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['NDZ']:
        ndz, created = NDZ.objects.get_or_create(bmu=bmu,
                                                 te=message_dict['TE'],
                                                 dz=message_dict['DZ'])
        if created:
            insert_log['new_entries'] = {'ndz': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['RURE']:
        rure, created = RURE.objects.get_or_create(bmu=bmu,
                                                   te=message_dict['TE'],
                                                   u1=message_dict['U1'],
                                                   ub=message_dict['UB'],
                                                   u2=message_dict['U2'],
                                                   uc=message_dict['UC'],
                                                   u3=message_dict['U3'])
        if created:
            insert_log['new_entries'] = {'rure': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['RURI']:
        ruri, created = RURI.objects.get_or_create(bmu=bmu,
                                                   te=message_dict['TE'],
                                                   u1=message_dict['U1'],
                                                   ub=message_dict['UB'],
                                                   u2=message_dict['U2'],
                                                   uc=message_dict['UC'],
                                                   u3=message_dict['U3'])
        if created:
            insert_log['new_entries'] = {'ruri': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['RDRE']:
        rdre, created = RDRE.objects.get_or_create(bmu=bmu,
                                                   te=message_dict['TE'],
                                                   r1=message_dict['R1'],
                                                   rb=message_dict['RB'],
                                                   r2=message_dict['R2'],
                                                   rc=message_dict['RC'],
                                                   r3=message_dict['R3'])
        if created:
            insert_log['new_entries'] = {'rdre': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['RDRI']:
        rdri, created = RDRI.objects.get_or_create(bmu=bmu,
                                                   te=message_dict['TE'],
                                                   r1=message_dict['R1'],
                                                   rb=message_dict['RB'],
                                                   r2=message_dict['R2'],
                                                   rc=message_dict['RC'],
                                                   r3=message_dict['R3'])
        if created:
            insert_log['new_entries'] = {'rdri': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['MDV']:
        mdv, created = MDV.objects.get_or_create(bmu=bmu,
                                                 te=message_dict['TE'],
                                                 dv=message_dict['DV'])
        if created:
            insert_log['new_entries'] = {'mdv': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['MDP']:
        mdp, created = MDP.objects.get_or_create(bmu=bmu,
                                                 te=message_dict['TE'],
                                                 dp=message_dict['DP'])
        if created:
            insert_log['new_entries'] = {'mdp': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['MZT']:
        mzt, created = MZT.objects.get_or_create(bmu=bmu,
                                                 te=message_dict['TE'],
                                                 mz=message_dict['MZ'])
        if created:
            insert_log['new_entries'] = {'mzt': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['NTB']:
        ntb, created = NTB.objects.get_or_create(bmu=bmu,
                                                 te=message_dict['TE'],
                                                 db=message_dict['DB'])
        if created:
            insert_log['new_entries'] = {'ntb': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    if message_dict['message_subtype'] in ['NTO']:
        nto, created = NTO.objects.get_or_create(bmu=bmu,
                                                 te=message_dict['TE'],
                                                 do=message_dict['DO'])
        if created:
            insert_log['new_entries'] = {'nto': 1}
            return insert_log
        return {'duplicate_msg': {message_dict['message_subtype']: 1}}

    raise ValueError('Insert function not available for message subtype %s'
                     % message_dict['message_subtype'])


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
    raise ValueError('Insert function not available for message subtype %s'
                     % message_dict['message_subtype'])


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
    raise ValueError('Insert function not available for message subtype %s'
                     % message_dict['message_subtype'])
