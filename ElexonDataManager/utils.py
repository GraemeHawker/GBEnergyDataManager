# -*- coding: utf-8 -*-
"""
common helper functions
"""
import datetime as dt
from django.utils import timezone
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

    #minimum SP value check
    if SP<1:
        raise ValueError('SP value of %d less than minimum value of 1' % SP)

    #maximum SP value check, taking into account transition days
    transition_days = [dt.date(x.year, x.month, x.day) for x in pytz.timezone('Europe/London')._utc_transition_times]
    if SD in transition_days[::2] and SP>46:    #clocks go forward
        raise ValueError('SP value of %d exceeds maximum value of 46 for forward clock change date' % SP)
    elif SD in transition_days[1::2] and SP>50: #clocks go back
        raise ValueError('SP value of %d exceeds maximum value of 50 for backward clock change date' % SP)
    elif SP>48:
        raise ValueError('SP value of %d exceeds maximum value of 48 for non-clock change date' % SP)

    #SD and SP are in BST, so calculate datetime for that timezone
    datetime = dt.datetime(SD.year, SD.month, SD.day, tzinfo=pytz.timezone('Europe/London'))
    datetime += dt.timedelta(minutes=(SP-1)*30)
    print(datetime)
    #if period end, add half an hour
    if not period_start:
        datetime+=dt.timedelta(minutes=30)

    #convert to UTC datetime
    return datetime.astimezone(pytz.utc)

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
        or end (False) of the settlement period

    Returns
    -------
    SD : datetime.date
        the settlement date
    SP : int
        the settlement period
    """
    pass
