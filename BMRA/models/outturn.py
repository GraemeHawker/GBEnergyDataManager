# -*- coding: utf-8 -*-
"""
Models relating to System Out-turn Data
"""
from __future__ import unicode_literals

import datetime as dt
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from BMRA.models.balancing import check_dates
from .core import FT

class FREQ(models.Model):
    """
    System Frequency Data
    """
    ts = models.DateTimeField(primary_key=True,
                              verbose_name='Received time',
                              validators=[check_dates])
    sf = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='System Frequency',
                             help_text='Hz')

    class Meta:
        db_table = 'bmra_freq'

class TEMP(models.Model):
    """
    Temperature Data
    """
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    to = models.DecimalField(max_digits=5,
                             decimal_places=3,
                             verbose_name='Outturn Temperature',
                             help_text='Celsius')
    tn = models.DecimalField(max_digits=5,
                             decimal_places=3,
                             verbose_name='Normal Reference Temperature',
                             help_text='Celsius')
    tl = models.DecimalField(max_digits=5,
                             decimal_places=3,
                             verbose_name='Low Reference Temperature',
                             help_text='Celsius')
    th = models.DecimalField(max_digits=5,
                             decimal_places=3,
                             verbose_name='High Reference Temperature',
                             help_text='Celsius')

    class Meta:
        db_table = 'bmra_temp'
        index_together = ['ts', 'tp']

class INDO(models.Model):
    """
    Initial National Demand Out-Turn
    """
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.DecimalField(max_digits=10,
                             decimal_places = 2,
                             verbose_name='Demand level',
                             help_text='MW')

    class Meta:
        db_table = 'bmra_indo'
        index_together = ['sd', 'sp', 'tp']

class ITSDO(models.Model):
    """
    Initial Transmission System Demand Outturn
    """
    tp = models.DateTimeField(verbose_name='Published time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    vd = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Demand level',
                             help_text='MW')

    class Meta:
        db_table = 'bmra_itsdo'
        index_together = ['sd', 'sp', 'tp']


class LOLP(models.Model):
    """
    Loss of Load Probability and De-rated Margin
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Message time',
                              validators=[check_dates])
    class Meta:
        db_table = 'bmra_lolp'

class LOLPlevel(models.Model):
    """
    Timestamped element of a weekly BMU fuel type forecast
    """
    lolp = models.ForeignKey(LOLP, on_delete=models.CASCADE)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    lp = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Loss of Load Probability')
    dr = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='De-rated Margin',
                             help_text='MW')
    class Meta:
        db_table = 'bmra_lolplevel'
        index_together = ('lolp', 'sd', 'sp')

class NONBM(models.Model):
    """
    Non-BM STOR Out-Turn
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    nb = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Non-BM STOR Volume',
                             help_text='MWh')

    class Meta:
        db_table = 'bmra_nonbm'
        index_together = ['sd', 'sp', 'tp']

class INDOD(models.Model):
    """
    Daily Energy Volume Data
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    eo = models.DecimalField(max_digits=10,
                             decimal_places = 3,
                             verbose_name='Energy Volume Out-turn',
                             help_text='MWh')
    el = models.DecimalField(max_digits=10,
                             decimal_places = 3,
                             verbose_name='Energy Volume Low Reference',
                             help_text='MWh')
    eh = models.DecimalField(max_digits=10,
                             decimal_places = 3,
                             verbose_name='Energy Volume High Reference',
                             help_text='MWh')
    en = models.DecimalField(max_digits=10,
                             decimal_places = 3,
                             verbose_name='Energy Normal Reference Volume	',
                             help_text='MWh')

    class Meta:
        db_table = 'bmra_indod'
        index_together = ['sd', 'tp']

class FUELINST(models.Model):
    """
    Instantaneous Generation by Fuel Type
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    ts = models.DateTimeField(verbose_name='Level time',
                              validators=[check_dates])
    ft = models.ForeignKey(FT, on_delete=models.PROTECT)
    fg = models.DecimalField(max_digits=10,
                             decimal_places = 2,
                             verbose_name='Total generation level',
                             help_text='MW')
    class Meta:
        db_table = 'bmra_fuelinst'
        index_together = ['sd', 'sp', 'ts', 'tp']

class FUELHH(models.Model):
    """
    Instantaneous Generation by Fuel Type
    """
    tp = models.DateTimeField(verbose_name='Message time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    ft = models.ForeignKey(FT, on_delete=models.PROTECT)
    fg = models.DecimalField(max_digits=10,
                             decimal_places = 2,
                             verbose_name='Total generation level',
                             help_text='MW')
    class Meta:
        db_table = 'bmra_fuelhh'
        index_together = ['sd', 'sp', 'tp']
