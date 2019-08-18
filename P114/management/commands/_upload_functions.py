"""
Helper functions for uploading data to database

"""
import datetime as dt
from django.utils import timezone
from ._data_definitions import ACCEPTED_MESSAGES, IGNORED_MESSAGES, \
FIELDNAMES, FIELD_CASTING_FUNCS
from GBEnergyDataManager.settings import P114_INPUT_DIR
import gzip
from tqdm import tqdm

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
                                               message_values[1:])]
    return dict(zip(message_keys, casted_message_values))

def file_to_message_list(filename):
    """
    Converts locally saved file to list of message dictionaries
    Filters for accepted message types and raises errors for
    unrecognised message types

    Parameters
    ----------
    filename : string
        the filename to be Processed

    Returns
    -------
    message_list: list
        a list of message dictionaries containing key/value pairs
    """

    p114_feed = filename.split('_')[0]
    if p114_feed not in ACCEPTED_MESSAGES and p114_feed not in IGNORED_MESSAGES:
        raise ValueError('P114 item {} not recognised'.format(p114_feed))
    file = gzip.open(P114_INPUT_DIR + filename, 'rb')
    file_content = file.read().decode('utf-8', 'ignore')
    message_list = []
    for row in file_content.split('\n'):
        if len(row)>0:
            message_values = row.split('|')
            message_type = message_values[0]
            if message_type in ACCEPTED_MESSAGES[p114_feed]:
                message_keys = FIELDNAMES[message_type]
                casted_message_values = [FIELD_CASTING_FUNCS[key](value.strip()) for
                                         key, value in zip(message_keys,
                                                           message_values[1:])]
                message_list.append(dict(zip(['message_type']+message_keys, [message_type]+casted_message_values)))
            elif message_type not in IGNORED_MESSAGES[p114_feed]:
                print(row)
                raise ValueError('message type {} not recognised'.format(message_type))
    return message_list

def insert_data(message_list):
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
    from P114.models import GSP, GSP_group, Interconnector, InterGSP, SR_type, \
    ABV, ABP, AGV, AGP, MPD, GMP, EMP, IMP

    from BMRA.models import BMU

    # here we rely on message order to be correct in the input files
    # e.g. as ABP datapoints come immediately after the ABV datapoint
    # with which they are associated, we link ABPs to the most recent
    # created ABV object in the loop
    # TODO: add integrity checks e.g. that numbers of and links between
    # each object in a processed file are consistent with this assumption
    for message_dict in tqdm(message_list):
        if message_dict['message_type'] == 'ABV':
            bmu, created = BMU.objects.get_or_create(id=message_dict['bmu_id'])
            sr_type, created = SR_type.objects.get_or_create(id=message_dict['sr_type'])
            abv, created = ABV.objects.get_or_create(bmu=bmu,
                                                     sd=message_dict['sd'],
                                                     sr_type=sr_type,
                                                     run_no=message_dict['run_no'],
                                                     agg_date=message_dict['agg_date'])

        elif message_dict['message_type'] == 'ABP':
            abp, created = ABP.objects.get_or_create(abv=abv,
                                                     sp=message_dict['sp'],
                                                     ei=message_dict['ei'],
                                                     vol=message_dict['vol'],
                                                     ii=message_dict['ii'])

        elif message_dict['message_type'] == 'AGV':
            gsp_group, created = GSP_group.objects.get_or_create(id=message_dict['gsp_group'])
            sr_type, created = SR_type.objects.get_or_create(id=message_dict['sr_type'])
            agv, created = AGV.objects.get_or_create(gsp_group=gsp_group,
                                                     sd=message_dict['sd'],
                                                     sr_type=sr_type,
                                                     run_no=message_dict['run_no'],
                                                     agg_date=message_dict['agg_date'])

        elif message_dict['message_type'] == 'AGP':
            agp, created = AGP.objects.get_or_create(agv=agv,
                                                     sp=message_dict['sp'],
                                                     ei=message_dict['ei'],
                                                     vol=message_dict['vol'],
                                                     ii=message_dict['ii'])

        elif message_dict['message_type'] == 'MPD':
            gsp_group, created = GSP_group.objects.get_or_create(id=message_dict['gsp_group'])
            sr_type, created = SR_type.objects.get_or_create(id=message_dict['sr_type'])
            mpd, created = MPD.objects.get_or_create(gsp_group=gsp_group,
                                                     sd=message_dict['sd'],
                                                     sr_type=sr_type,
                                                     run_no=message_dict['run_no'],
                                                     agg_date=message_dict['agg_date'])

        elif message_dict['message_type'] == 'GP9':
            # in this case we don't create a GP9 object as it only has GSP id
            # instead get/create the GSP object and use it in following GMPs
            gsp, created = GSP.objects.get_or_create(id=message_dict['gsp_id'])

        elif message_dict['message_type'] == 'GMP':
            gmp, created = GMP.objects.get_or_create(gsp=gsp,
                                                     mpd=mpd,
                                                     sp=message_dict['sp'],
                                                     ei=message_dict['ei'],
                                                     vol=message_dict['vol'],
                                                     ii=message_dict['ii'])

        elif message_dict['message_type'] == 'EPD':
            # in this case we don't create a EPD object as it only has Interconnector id
            # instead get/create the Interconnector object and use it in following EMPs
            interconnector, created = Interconnector.objects.get_or_create(id=message_dict['inter_id'])

        elif message_dict['message_type'] == 'EMP':
            emp, created = EMP.objects.get_or_create(interconnector=interconnector,
                                                     mpd=mpd,
                                                     sp=message_dict['sp'],
                                                     ei=message_dict['ei'],
                                                     vol=message_dict['vol'],
                                                     ii=message_dict['ii'])

        elif message_dict['message_type'] == 'IPD':
            # in this case we don't create a IPD object as it only has InterGSP id
            # instead get/create the InterGSP object and use it in following IMPs
            intergsp, created = InterGSP.objects.get_or_create(id=message_dict['intergsp_id'])

        elif message_dict['message_type'] == 'IMP':
            imp, created = IMP.objects.get_or_create(intergsp=intergsp,
                                                     mpd=mpd,
                                                     sp=message_dict['sp'],
                                                     ei=message_dict['ei'],
                                                     vol=message_dict['vol'],
                                                     ii=message_dict['ii'])

    '''
    #check if BMUID already in db, if not insert and log


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
    '''
