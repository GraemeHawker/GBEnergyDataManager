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


class SIL(models.Model):
    """
    Stable Import Limit
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    si = models.FloatField(verbose_name='Stable Import Limit',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_sil'
        index_together = ('bmu', 'te')


class SEL(models.Model):
    """
    Stable Export Limit
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    se = models.FloatField(verbose_name='Stable Export Limit',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_sel'
        index_together = ('bmu', 'te')


class MNZT(models.Model):
    """
    Minimum Non-zero Time
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    mn = models.FloatField(verbose_name='Minimum non-zero time',
                           help_text='minutes?')

    class Meta:
        db_table = 'bmra_mnzt'
        index_together = ('bmu', 'te')


class NDZ(models.Model):
    """
    Notice to deviate from zero
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    dz = models.FloatField(verbose_name='Notice to deviate from zero',
                           help_text='minutes?')

    class Meta:
        db_table = 'bmra_ndz'
        index_together = ('bmu', 'te')


class RURE(models.Model):
    """
    Run-up rate export
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    u1 = models.FloatField(verbose_name='Run up rate 1',
                           help_text='MW/minute')
    ub = models.FloatField(verbose_name='Run up elbow 2',
                           help_text='MW/minute')
    u2 = models.FloatField(verbose_name='Run up rate 2',
                           help_text='MW/minute')
    uc = models.FloatField(verbose_name='Run up elbow 3',
                           help_text='MW/minute')
    u3 = models.FloatField(verbose_name='Run up rate 3',
                           help_text='MW/minute')

    class Meta:
        db_table = 'bmra_rure'
        index_together = ('bmu', 'te')


class RURI(models.Model):
    """
    Run-up rate import
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    u1 = models.FloatField(verbose_name='Run up rate 1',
                           help_text='MW/minute')
    ub = models.FloatField(verbose_name='Run up elbow 2',
                           help_text='MW/minute')
    u2 = models.FloatField(verbose_name='Run up rate 2',
                           help_text='MW/minute')
    uc = models.FloatField(verbose_name='Run up elbow 3',
                           help_text='MW/minute')
    u3 = models.FloatField(verbose_name='Run up rate 3',
                           help_text='MW/minute')

    class Meta:
        db_table = 'bmra_ruri'
        index_together = ('bmu', 'te')


class RDRE(models.Model):
    """
    Run-down rate export
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    r1 = models.FloatField(verbose_name='Run down rate 1',
                           help_text='MW/minute')
    rb = models.FloatField(verbose_name='Run down elbow 2',
                           help_text='MW/minute')
    r2 = models.FloatField(verbose_name='Run down rate 2',
                           help_text='MW/minute')
    rc = models.FloatField(verbose_name='Run down elbow 3',
                           help_text='MW/minute')
    r3 = models.FloatField(verbose_name='Run down rate 3',
                           help_text='MW/minute')

    class Meta:
        db_table = 'bmra_rdre'
        index_together = ('bmu', 'te')


class RDRI(models.Model):
    """
    Run-down rate import
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    r1 = models.FloatField(verbose_name='Run down rate 1',
                           help_text='MW/minute')
    rb = models.FloatField(verbose_name='Run down elbow 2',
                           help_text='MW/minute')
    r2 = models.FloatField(verbose_name='Run down rate 2',
                           help_text='MW/minute')
    rc = models.FloatField(verbose_name='Run down elbow 3',
                           help_text='MW/minute')
    r3 = models.FloatField(verbose_name='Run down rate 3',
                           help_text='MW/minute')

    class Meta:
        db_table = 'bmra_rdri'
        index_together = ('bmu', 'te')


class MDV(models.Model):
    """
    Maximum delivery volume
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    dv = models.FloatField(verbose_name='Maximum delivery volume',
                           help_text='MW')

    class Meta:
        db_table = 'bmra_mdv'
        index_together = ('bmu', 'te')

class MDP(models.Model):
    """
    Maximum delivery period
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    dp = models.FloatField(verbose_name='Maximum delivery period',
                           help_text='minutes')

    class Meta:
        db_table = 'bmra_mdp'
        index_together = ('bmu', 'te')

class MZT(models.Model):
    """
    Minimum zero time
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    mz = models.FloatField(verbose_name='Minimum zero time',
                           help_text='minutes')

    class Meta:
        db_table = 'bmra_mzt'
        index_together = ('bmu', 'te')

class NTB(models.Model):
    """
    Notice to deliver bids
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    db = models.FloatField(verbose_name='Notice to deliver bids',
                           help_text='minutes')

    class Meta:
        db_table = 'bmra_ntb'
        index_together = ('bmu', 'te')

class NTO(models.Model):
    """
    Notice to deliver offers
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    te = models.DateTimeField(verbose_name='Effective time',
                              validators=[check_dates])
    do = models.FloatField(verbose_name='Notice to deliver offers',
                           help_text='minutes')

    class Meta:
        db_table = 'bmra_nto'
        index_together = ('bmu', 'te')
