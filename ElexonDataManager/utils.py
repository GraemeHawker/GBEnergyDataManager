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
    if SD in transition_days[::2]: #clocks go forward
        if SP > 46:
            raise ValueError('SP value of %d exceeds maximum value of 46 \
                             for forward clock change date' % SP)
    elif SD in transition_days[1::2]: #clocks go back
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
    if SD in transition_days[::2]:
        pass
    elif SD in transition_days[1::2] and SP > 2:
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
    transition_days = [dt.date(x.year, x.month, x.day)
                       for x in pytz.timezone('Europe/London')._utc_transition_times]

    if datetime.astimezone(pytz.timezone('Europe/London')).dst() != dt.timedelta(0):
        datetime = datetime+dt.timedelta(hours=1)
    if period_start or datetime.minute%30 != 0:
        if dt.date(datetime.year, datetime.month, datetime.day) in transition_days[::2]\
        and ((datetime.hour*60+datetime.minute) // 30 + 1) > 2:
            return (dt.date(datetime.year, datetime.month, datetime.day),
                    (datetime.hour*60+datetime.minute) // 30 - 1)
        if dt.date(datetime.year, datetime.month, datetime.day) in transition_days[1::2]\
        and datetime.hour >= 1:
            print(datetime.hour)
            if datetime.hour >= 2:
                return (dt.date(datetime.year, datetime.month, datetime.day),
                        (datetime.hour*60+datetime.minute) // 30 + 5)
            return (dt.date(datetime.year, datetime.month, datetime.day),
                    (datetime.hour*60+datetime.minute) // 30 + 1)
        return (dt.date(datetime.year, datetime.month, datetime.day),
                (datetime.hour*60+datetime.minute) // 30 + 1)
    if (datetime.hour*60+datetime.minute) // 30 == 0:
        return (dt.date(datetime.year, datetime.month, datetime.day) - dt.timedelta(days=1),
                48)
    if dt.date(datetime.year, datetime.month, datetime.day) in transition_days[::2]\
    and ((datetime.hour*60+datetime.minute) // 30 + 1) > 2:
        return (dt.date(datetime.year, datetime.month, datetime.day),
                (datetime.hour*60+datetime.minute) // 30 - 2)
    return (dt.date(datetime.year, datetime.month, datetime.day),
            (datetime.hour*60+datetime.minute) // 30)

def get_sp_list(sd_start, sd_end):
    """
    Gives a list of settlement dates and periods between two dates inclusive
    """
    sp_list = []
    curr_sd = sd_start
    while curr_sd <= sd_end:
        #maximum SP value check, taking into account transition days
        transition_days = [dt.date(x.year, x.month, x.day)
                           for x in pytz.timezone('Europe/London')._utc_transition_times]
        if curr_sd in transition_days[::2]: #clocks go forward
            no_sp = 46
        elif curr_sd in transition_days[1::2]: #clocks go back
            no_sp = 50
        else:
            no_sp = 48
        for curr_sp in np.arange(no_sp):
            sp_list.append((curr_sd, curr_sp))
    return sp_list
