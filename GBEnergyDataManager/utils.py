# -*- coding: utf-8 -*-
"""
common helper functions
"""
import numpy as np
import datetime as dt
import pytz

def is_dst(datetime):
    """
    determines if a (timezone-aware) datetime object is within UK daylight savings

    parameters
    ----------
    datetime : datetime object
        timezone-aware datetime

    Returns
    -------
    is_dst : boolean
        True if datetime in UK daylight savings, False if not
    """
    return datetime.astimezone(pytz.timezone('Europe/London')).dst() > dt.timedelta(0)


def sp_to_dt(SD, SP, period_start=True):
    """
    Converts a settlement date and settlement period to a timezone-aware
    datetime object

    Parameters
    ----------
    SD : datetime.date object
        the settlement date
    SP : int
        the settlement period (in range 1 to 50)
    period_start : bool
        whether the desired datetime object should relate to the start (True)
        or end (False) of the settlement period

    Returns
    -------
    datetime : datetime.datetime
        a timezone-aware datetime object
    """
    #check date object passed - not datetime
    if not isinstance(SD, dt.date):
        raise ValueError('Expected Settlement Date parameter not of type datetime.date')

    #minimum SP value check
    if SP < 1:
        raise ValueError('SP value of %d less than minimum value of 1' % SP)

    #maximum SP value check, taking into account transition days
    transition_days = [dt.date(x.year, x.month, x.day)
                       for x in pytz.timezone('Europe/London')._utc_transition_times]
    if SD in [x for x in transition_days if x.month<6]: #clocks go forward
        if SP > 46:
            raise ValueError('SP value of %d exceeds maximum value of 46 \
                             for forward clock change date' % SP)
    elif SD in [x for x in transition_days if x.month>6]: #clocks go back
        if SP > 50:
            raise ValueError('SP value of %d exceeds maximum value of 50 \
                             for backward clock change date' % SP)
    elif SP > 48:
        raise ValueError('SP value of %d exceeds maximum value of 48 for \
                         non-clock change date' % SP)

    '''
    #previous attempt using native timezone calc, preserved for posterity
    #SD and SP are in BST, so calculate datetime for that timezone
    datetime = dt.datetime(SD.year, SD.month, SD.day, tzinfo=pytz.timezone('Europe/London'))
    print(datetime)
    datetime += dt.timedelta(minutes=(SP-1)*30)
    print(datetime)
    #if period end, add half an hour
    if not period_start:
        datetime += dt.timedelta(minutes=30)
    return pytz.utc.normalize(datetime.astimezone(pytz.utc))
    '''

    datetime = dt.datetime(SD.year, SD.month, SD.day, tzinfo=pytz.utc)
    datetime += dt.timedelta(minutes=(SP-1)*30)
    if not period_start:
        datetime += dt.timedelta(minutes=30)

    # DST shift should only be applied on days after transition day
    # (as does not impact calculation until SP resets to 1)
    if SD in [x for x in transition_days if x.month<6]:
        pass
    elif SD in [x for x in transition_days if x.month>6] and SP > 2:
        datetime -= dt.timedelta(hours=1)
    else:
        datetime -= datetime.astimezone(pytz.timezone('Europe/London')).dst()
    return datetime

def dt_to_sp(datetime, period_start=True):
    """
    Converts a timezone-aware datetime object to a settlement date (BST) and
    settlement period

    Parameters
    ----------
    datetime : datetime.datetime object
        the settlement date
    period_start : bool
        whether the passed datetime object relates to the start (True)
        or end (False) of the settlement period, if the datetime object falls
        exactly on a half-hour period and is ambiguous. If the datetime object
        falls within a half-hour period (i.e. is unambiguous) this argument is
        ignored

    Returns
    -------
    SD : datetime.date
        the settlement date
    SP : int
        the settlement period
    """

    # DST transition dates
    # clocks go forward on transition_days[::2], 46 settlement periods
    # clocks go back on transition_days[1::2], 50 settlement periods
    transition_days = [dt.date(x.year, x.month, x.day)
                       for x in pytz.timezone('Europe/London')._utc_transition_times]

    # initally set SD and SP ignoring DST
    sd_raw = dt.date(datetime.year, datetime.month, datetime.day)
    sp_raw = (datetime.hour*60+datetime.minute) // 30 + 1

    # adjust SP for DST
    # note that impact on SP does not immediately take effect until day after transition
    # So:
    # if on day clocks got forward, do not adjust
    # if on day clocks go back, adjust both within and without BST period
    if (datetime.astimezone(pytz.timezone('Europe/London')).dst() != dt.timedelta(0)\
    and sd_raw not in [x for x in transition_days if x.month<6])\
    or (datetime.astimezone(pytz.timezone('Europe/London')).dst() == dt.timedelta(0)\
    and sd_raw in [x for x in transition_days if x.month>6]):
        sp_raw += 2

    # shift period by 1 if datetime is ambiguous and to be treated as period end
    # rather than start
    if not period_start and (datetime.hour*60+datetime.minute) % 30 == 0:
        sp_raw -= 1

    # now deal with cases where SP is now shifted to previous settlement date
    # allowing for variable number of SPs on DST transition dates
    if sp_raw < 1:
        sd_raw -= dt.timedelta(days=1)
        if sd_raw in [x for x in transition_days if x.month<6]:
            sp_raw = 46 - sp_raw
        elif sd_raw in [x for x in transition_days if x.month>6]:
            sp_raw = 50 - sp_raw
        else:
            sp_raw = 48 - sp_raw

    # now deal with cases where SP is shifted to next settlement date, allowing
    # for variable number of SPs on DST transition dates
    if sp_raw > 48 and sd_raw not in transition_days:
        sd_raw += dt.timedelta(days=1)
        sp_raw -= 48
    if sp_raw > 46 and sd_raw in [x for x in transition_days if x.month<6]:
        sd_raw += dt.timedelta(days=1)
        sp_raw -= 46
    if sp_raw > 50 and sd_raw in [x for x in transition_days if x.month>6]:
        sd_raw += dt.timedelta(days=1)
        sp_raw -= 50

    return sd_raw, sp_raw

def get_sp_list(sd_start, sd_end, sp_start=None, sp_end=None):
    """
    Gives a list of tuples of settlement dates and periods between two
    given settlement dates/periods

    Parameters
    ----------
    sd_start : datetime.date object
        the first settlement date
    sd_end : datetime.date object
        the last settlement date
    sp_start : int
        the settlement period to begin with on the first settlement date
        (assumed 1 if no argument provided)
    sp_end : int
        the settlement period to end with on the last settlement date
        (assumed final settlement period if no argument provided)

    Returns
    -------
    a list of (SD,SP) tuples where:
    SD : datetime.date
        the settlement date
    SP : int
        the settlement period
    """
    sp_list = []
    curr_sd = sd_start
    while curr_sd <= sd_end:
        if curr_sd == sd_start and sp_start is not None:
            first_sp = sp_start
        else:
            first_sp = 1

        #maximum SP value check, taking into account transition days
        transition_days = [dt.date(x.year, x.month, x.day)
                           for x in pytz.timezone('Europe/London')._utc_transition_times]
        if curr_sd in [x for x in transition_days if x.month<6]: #clocks go forward
            last_sp = 46
        elif curr_sd in [x for x in transition_days if x.month>6]: #clocks go back
            last_sp = 50
        else:
            last_sp = 48
        if (curr_sd == sd_end and sp_end is not None) and sp_end < last_sp:

            last_sp = sp_end
        for curr_sp in np.arange(first_sp, last_sp+1):
            sp_list.append((curr_sd, curr_sp))

        curr_sd += dt.timedelta(days=1)

    return sp_list
