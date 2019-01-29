# -*- coding: utf-8 -*-
"""
common helper functions
"""
import datetime as dt

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
    if period_start:
        return dt.datetime(SD.year, SD.month, SD.day,
                           SP//2,
                           (SP%2)*30)
    return dt.datetime(SD.year, SD.month, SD.day,
                       SP//2,
                       (SP%2)*30)+dt.timedelta(mins=30)

def dt_to_sp(datetime, period_start=True):
    """
    Converts a timezone-aware datetime object to a settlement date and
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
