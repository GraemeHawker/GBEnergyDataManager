# -*- coding: utf-8 -*-
"""
Models relating to BMRA system-level data
"""
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from BMRA.models.balancing import check_dates

class FREQ(models.Model):
    """
    System Frequency Data
    """
    ts = models.DateTimeField(primary_key=True,
                              verbose_name='Received time',
                              validators=[check_dates])
    sf = models.DecimalField(max_digits=10,
                             decimal_places = 3,
                             verbose_name='System Frequency',
                             help_text='Hz')

    class Meta:
        db_table = 'bmra_freq'


class MID(models.Model):
    """
    Market Index Data
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    mi = models.CharField(max_length=11,
                          verbose_name='Market Index Data Provider')
    m1 = models.DecimalField(max_digits=10,
                             decimal_places = 2,
                             verbose_name='Market Index Price',
                             help_text='£/MWh')
    m2 = models.DecimalField(max_digits=10,
                             decimal_places = 2,
                             verbose_name='Market Index Volume',
                             help_text='MWh')
    class Meta:
        db_table = 'bmra_mid'
        index_together = ('mi', 'sd', 'sp')
