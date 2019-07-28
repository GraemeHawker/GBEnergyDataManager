# -*- coding: utf-8 -*-
"""
Models relating to System Forecasting Data
"""
from __future__ import unicode_literals

import datetime as dt
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from GBEnergyDataManager.settings import BMRA_DATA_START_DATE
from .core import BMU, ZI, FT
from BMRA.models.balancing import check_dates

def check_forecast_dates(value):
    """
    Validates if date or datetime is within the range of historical BMRA data
    """
    if value < BMRA_DATA_START_DATE or value > dt.date.today() + dt.timedelta(years=1):
        raise ValidationError('Date or timestamp not in valid BMRA range')

class DF(models.Model):
    """
    Demand Forecast (ceased publication Q1 2009)
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Message time',
                              validators=[check_forecast_dates])
    class Meta:
        db_table = 'bmra_df'
        index_together = ('zi', 'ts')

class DFlevel(models.Model):
    """
    Timestamped element of a demand forecast
    """
    df = models.ForeignKey(DF, on_delete=models.CASCADE)
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_dflevel'
        index_together = ('df', 'sd', 'sp')

class NDF(models.Model):
    """
    National Demand Forecast
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_ndf'
        index_together = ('zi', 'ts')

class NDFlevel(models.Model):
    """
    Timestamped element of a national demand forecast
    """
    ndf = models.ForeignKey(NDF, on_delete=models.CASCADE)
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_ndflevel'
        index_together = ('ndf', 'sd', 'sp')

class TSDF(models.Model):
    """
    Transmission System Demand Forecast
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_tsdf'
        index_together = ('zi', 'ts')

class TSDFlevel(models.Model):
    """
    Timestamped element of a transmission system demand forecast
    """
    tsdf = models.ForeignKey(TSDF, on_delete=models.CASCADE)
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_tsdflevel'
        index_together = ('tsdf', 'sd', 'sp')

class IMBALNGC(models.Model):
    """
    Indicated imbalance
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_imbalngc'
        index_together = ('zi', 'ts')

class IMBALNGClevel(models.Model):
    """
    Timestamped element of an indicated imbalance forecast
    """
    imbalngc = models.ForeignKey(IMBALNGC, on_delete=models.CASCADE)
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vi = models.FloatField(verbose_name='Imbalance value',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_imbalngclevel'
        index_together = ('imbalngc', 'sd', 'sp')

class INDGEN(models.Model):
    """
    Indicated generation
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_indgen'
        index_together = ('zi', 'ts')

class INDGENlevel(models.Model):
    """
    Timestamped element of an indicated generation forecast
    """
    indgen = models.ForeignKey(INDGEN, on_delete=models.CASCADE)
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vg = models.FloatField(verbose_name='Generation value',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_indgenlevel'
        index_together = ('indgen', 'sd', 'sp')

class MELNGC(models.Model):
    """
    Indicated margin
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_melngc'
        index_together = ('zi', 'ts')

class MELNGClevel(models.Model):
    """
    Timestamped element of an indicated margin forecast
    """
    melngc = models.ForeignKey(MELNGC, on_delete=models.CASCADE)
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vm = models.FloatField(verbose_name='Sum of MELs within zone',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_melngclevel'
        index_together = ('melngc', 'sd', 'sp')

class INDDEM(models.Model):
    """
    Indicated demand
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_inddem'
        index_together = ('zi', 'ts')

class INDDEMlevel(models.Model):
    """
    Timestamped element of an indicated demand forecast
    """
    inddem = models.ForeignKey(INDDEM, on_delete=models.CASCADE)
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_inddemlevel'
        index_together = ('inddem', 'sd', 'sp')

class NDFD(models.Model):
    """
    Demand forecast, 2-14 days ahead
    """
    ts = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_ndfd'

class NDFDlevel(models.Model):
    """
    Timestamped element of a demand forecast
    """
    ndfd = models.ForeignKey(NDFD, on_delete=models.CASCADE)
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_ndfdlevel'
        index_together = ('ndfd', 'sd', 'sp')

class TSDFD(models.Model):
    """
    Transmission system demand forecast
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_tsdfd'

class TSDFDlevel(models.Model):
    """
    Timestamped element of a transmission system demand forecast
    """
    tsdfd = models.ForeignKey(TSDFD, on_delete=models.CASCADE)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_tsdfdlevel'
        index_together = ('tsdfd', 'sd', 'sp')

class TSDFW(models.Model):
    """
    Transmission System Demand Forecast, 2-52 weeks
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Published time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_tsdfw'

class TSDFWlevel(models.Model):
    """
    Timestamped element of a weekly transmission system demand forecast
    """
    tsdfw = models.ForeignKey(TSDFW, on_delete=models.CASCADE)
    wd = models.DateTimeField(verbose_name='Week start date',
                              validators=[check_forecast_dates])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_tsdfwlevel'
        index_together = ('tsdfw', 'wn')

class NDFW(models.Model):
    """
    Transmission System Demand Forecast, 2-52 weeks
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_ndfw'

class NDFWlevel(models.Model):
    """
    Timestamped element of a weekly transmission system demand forecast
    """
    ndfw = models.ForeignKey(NDFW, on_delete=models.CASCADE)
    wd = models.DateTimeField(verbose_name='Week start date',
                              validators=[check_forecast_dates])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_ndfwlevel'
        index_together = ('ndfw', 'wn')

class OCNMFW(models.Model):
    """
    Surplus forecast 2-52 weeks ahead
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_ocnmfw'

class OCNMFWlevel(models.Model):
    """
    Timestamped element of a surplus forecast
    """
    ocnmfw = models.ForeignKey(OCNMFW, on_delete=models.CASCADE)
    wd = models.DateTimeField(verbose_name='Week start date',
                              validators=[check_forecast_dates])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_ocnmfwlevel'
        index_together = ('ocnmfw', 'wn')

class OCNMFW2(models.Model):
    """
    Generating Plant Demand Margin, 2-52 weeks ahead
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_ocnmfw2'

class OCNMFW2level(models.Model):
    """
    Timestamped element of a plant demand margin forecast
    """
    ocnmfw = models.ForeignKey(OCNMFW2, on_delete=models.CASCADE)
    cy = models.IntegerField(verbose_name='Calendar year',
                             validators=[MinValueValidator(2000),
                                         MaxValueValidator(3000)])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    vd = models.FloatField(verbose_name='Demand margin',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_ocnmfw2level'
        index_together = ('ocnmfw', 'cy', 'wn')

class WINDFOR(models.Model):
    """
    Forecast peak wind generation
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_windfor'

class WINDFORlevel(models.Model):
    """
    Timestamped element of a wind forecast
    """
    windfor = models.ForeignKey(WINDFOR, on_delete=models.CASCADE)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vg = models.FloatField(verbose_name='Generation',
                           help_text='MW')
    tr = models.FloatField(verbose_name='Total capacity',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_windforlevel'
        index_together = ('windfor', 'sd', 'sp')

class OCNMFD(models.Model):
    """
    Surplus forecast 2-14 days ahead
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_ocnmfd'

class OCNMFDlevel(models.Model):
    """
    Timestamped element of a surplus forecast
    """
    ocnmfd = models.ForeignKey(OCNMFD, on_delete=models.CASCADE)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vm = models.FloatField(verbose_name='Surplus',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_ocnmfdlevel'
        index_together = ('ocnmfd', 'sd', 'sp')

class OCNMFD2(models.Model):
    """
    Generating Plant margin, 2-14 days ahead
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_ocnmfd2'

class OCNMFD2level(models.Model):
    """
    Timestamped element of a plant margin forecast
    """
    ocnmfd2 = models.ForeignKey(OCNMFD2, on_delete=models.CASCADE)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    dm = models.FloatField(verbose_name='Generating plant margin',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_ocnmfd2level'
        index_together = ['ocnmfd2', 'sd']

class FOU2T14D(models.Model):
    """
    National Output Usable by Fuel Type, 2-14 Days ahead
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_fou2t14d'

class FOU2T14Dlevel(models.Model):
    """
    Timestamped element of a fuel type output forecast
    """
    fou2t14d = models.ForeignKey(FOU2T14D, on_delete=models.CASCADE)
    ft = models.ForeignKey(FT, on_delete=models.PROTECT)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    ou = models.FloatField(verbose_name='Output usable',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_fou2t14dlevel'
        index_together = ('fou2t14d', 'sd')

class UOU2T14D(models.Model):
    """
    National Output Usable by Fuel Type and BM Unit, 2-14 Days ahead
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    class Meta:
        db_table = 'bmra_uou2t14d'

class UOU2T14Dlevel(models.Model):
    """
    Timestamped element of a daily BMU fuel type forecast
    """
    uou2t14d = models.ForeignKey(UOU2T14D, on_delete=models.CASCADE)
    ft = models.ForeignKey(FT, on_delete=models.PROTECT)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    ou = models.FloatField(verbose_name='Output usable',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_uou2t14dlevel'
        index_together = ('uou2t14d', 'sd')

class UOU2T52W(models.Model):
    """
    National Output Usable by Fuel Type and BM Unit, 2-52 Weeks ahead
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    class Meta:
        db_table = 'bmra_uou2t52w'

class UOU2T52Wlevel(models.Model):
    """
    Timestamped element of a weekly BMU fuel type forecast
    """
    uou2t52w = models.ForeignKey(UOU2T52W, on_delete=models.CASCADE)
    ft = models.ForeignKey(FT, on_delete=models.PROTECT)
    cy = models.IntegerField(verbose_name='Calendar year',
                             validators=[MinValueValidator(2000),
                                         MaxValueValidator(3000)])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    ou = models.FloatField(verbose_name='Output usable',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_uou2t52wlevel'
        index_together = ('uou2t52w', 'cy', 'wn')
