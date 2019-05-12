"""
Helper functions for uploading data to database

"""
import datetime as dt
from django.utils import timezone
from ._data_definitions import FIELDNAMES, FIELD_CASTING_FUNCS

def message_to_dict(raw_message, associated_params=None):
    """
    Converts a raw message string to a dictionary with
    key/value pairs and metadata

    Parameters
    ----------
    raw_message : string
        the BM data string
    associated_params : dictionary
        associated parameters derived from previously created message objects

    Returns
    -------
    message_dict: dict
        a dictionary containing key/value pairs

    """
    message_values = raw_message.split('|')
    message_type = message_values[0].strip()
    message_keys = FIELDNAMES[message_type]
    casted_message_values = [FIELD_CASTING_FUNCS[key](value.strip()) for
                             key, value in zip(message_keys,
                                               message_values)]
    return dict(zip(message_keys, casted_message_values))

def insert_data(message_dict):
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
                              sd=message_dict['SD'],
                              sp=message_dict['SP']).exists():
            return 0
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
        return 1



    raise ValueError('Insert function not available for message subtype %s'
                     % message_dict['message_subtype'])
