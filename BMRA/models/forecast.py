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
        db_table = 'bmra_df'
        index_together = ('zi', 'sd', 'sp', 'tp')


class NDF(models.Model):
    """
    National Demand Forecast
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
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
        db_table = 'bmra_ndf'
        index_together = ('zi', 'sd', 'sp', 'tp')


class TSDF(models.Model):
    """
    Transmission System Demand Forecast
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
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
        db_table = 'bmra_tsdf'
        index_together = ('zi', 'sd', 'sp', 'tp')


class IMBALNGC(models.Model):
    """
    Indicated imbalance
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
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
        db_table = 'bmra_imbalngc'
        index_together = ('zi', 'sd', 'sp', 'tp')


class INDGEN(models.Model):
    """
    Indicated generation
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
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
        db_table = 'bmra_indgen'
        index_together = ('zi', 'sd', 'sp', 'tp')


class MELNGC(models.Model):
    """
    Indicated margin
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
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
        db_table = 'bmra_melngc'
        index_together = ('zi', 'sd', 'sp', 'tp')


class INDDEM(models.Model):
    """
    Indicated demand
    """
    zi = models.ForeignKey(ZI,
                           on_delete=models.PROTECT)
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
        db_table = 'bmra_inddem'
        index_together = ('zi', 'sd', 'sp', 'tp')


class NDFD(models.Model):
    """
    Demand forecast, 2-14 days ahead
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_ndfd'
        index_together = ('tp', 'sd', 'sp')


class TSDFD(models.Model):
    """
    Transmission system demand forecast
    """
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
        db_table = 'bmra_tsdfd'
        index_together = ('tp', 'sd', 'sp')


class TSDFW(models.Model):
    """
    Transmission System Demand Forecast, 2-52 weeks
    """
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    wd = models.DateField(verbose_name='Week start date',
                              validators=[check_forecast_dates])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_tsdfw'
        index_together = ('wd', 'tp')


class NDFW(models.Model):
    """
    Demand Forecast, 2-52 weeks
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    wd = models.DateField(verbose_name='Week start date',
                              validators=[check_forecast_dates])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    vd = models.FloatField(verbose_name='Demand level',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_ndfw'
        index_together = ('wd', 'tp')


class NOU2T14D(models.Model):
    """
    National Output Usable, 2-14 days ahead
    """
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    ou = models.FloatField(verbose_name='Output usable',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_nou2t14d'
        index_together = ('tp', 'sd', 'sp')


class NOU2T52W(models.Model):
    """
    Generating Plant Demand Margin, 2-52 weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    cy = models.IntegerField(verbose_name='Calendar year',
                             validators=[MinValueValidator(2000),
                                         MaxValueValidator(3000)])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    ou = models.FloatField(verbose_name='Output Usable',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_nou2t52w'
        index_together = ('cy', 'wn', 'tp')


class NOU2T3YW(models.Model):
    """
    Generating Plant Demand Margin, 2-156 weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    cy = models.IntegerField(verbose_name='Calendar year',
                             validators=[MinValueValidator(2000),
                                         MaxValueValidator(3000)])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    ou = models.FloatField(verbose_name='Output Usable',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_nou2t3yw'
        index_together = ('cy', 'wn', 'tp')


class OCNMFW(models.Model):
    """
    Surplus forecast 2-52 weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    wd = models.DateField(verbose_name='Week start date',
                              validators=[check_forecast_dates])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    vm = models.FloatField(verbose_name='Surplus level',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_ocnmfw'
        index_together = ('wd', 'tp')


class OCNMF3Y(models.Model):
    """
    Surplus forecast 2-52 weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    cy = models.IntegerField(verbose_name='Calendar year',
                             validators=[MinValueValidator(2000),
                                         MaxValueValidator(3000)])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    vm = models.FloatField(verbose_name='Surplus level',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_ocnmf3y'
        index_together = ('cy', 'wn', 'tp')


class OCNMFW2(models.Model):
    """
    Generating Plant Demand Margin, 2-52 weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    cy = models.IntegerField(verbose_name='Calendar year',
                             validators=[MinValueValidator(2000),
                                         MaxValueValidator(3000)])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    dm = models.FloatField(verbose_name='Demand margin',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_ocnmfw2'
        index_together = ('cy', 'wn', 'tp')


class OCNMF3Y2(models.Model):
    """
    Generating Plant Demand Margin, 2-156 weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    cy = models.IntegerField(verbose_name='Calendar year',
                             validators=[MinValueValidator(2000),
                                         MaxValueValidator(3000)])
    wn = models.IntegerField(verbose_name='Week number',
                             validators=[MinValueValidator(0),
                                         MaxValueValidator(53)])
    dm = models.FloatField(verbose_name='Demand margin',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_ocnmf3y2'
        index_together = ('cy', 'wn', 'tp')


class WINDFOR(models.Model):
    """
    Forecast peak wind generation
    """
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
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
        db_table = 'bmra_windfor'
        index_together = ('sd', 'sp', 'tp')


class OCNMFD(models.Model):
    """
    Surplus forecast 2-14 days ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vm = models.FloatField(verbose_name='Surplus',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_ocnmfd'
        index_together = ('sd', 'sp', 'tp')


class OCNMFD2(models.Model):
    """
    Generating Plant margin, 2-14 days ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    dm = models.FloatField(verbose_name='Generating plant margin',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_ocnmfd2'
        index_together = ('sd', 'tp')


class FOU2T14D(models.Model):
    """
    National Output Usable by Fuel Type, 2-14 Days ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    ft = models.ForeignKey(FT, on_delete=models.PROTECT)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    ou = models.FloatField(verbose_name='Output usable',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_fou2t14d'
        index_together = ('ft', 'sd', 'tp')


class FOU2T52W(models.Model):
    """
    National Output Usable by Fuel Type, 2-52 Weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
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
        db_table = 'bmra_fou2t52w'
        index_together = ('ft', 'cy', 'wn', 'tp')


class FOU2T3YW(models.Model):
    """
    National Output Usable by Fuel Type, 2-52 Weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
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
        db_table = 'bmra_fou2t3yw'
        index_together = ('ft', 'cy', 'wn', 'tp')


class UOU2T14D(models.Model):
    """
    National Output Usable by Fuel Type and BM Unit, 2-14 Days ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    ft = models.ForeignKey(FT, on_delete=models.PROTECT)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_forecast_dates])
    ou = models.FloatField(verbose_name='Output usable',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_uou2t14d'
        index_together = ('bmu', 'ft', 'sd', 'tp')


class UOU2T52W(models.Model):
    """
    National Output Usable by Fuel Type and BM Unit, 2-52 Weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
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
        db_table = 'bmra_uou2t52w'
        index_together = ('bmu', 'ft', 'cy', 'wn', 'tp')


class UOU2T3YW(models.Model):
    """
    National Output Usable by Fuel Type and BM Unit, 2-156 Weeks ahead
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
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
        db_table = 'bmra_uou2t3yw'
        index_together = ('bmu', 'ft', 'cy', 'wn', 'tp')