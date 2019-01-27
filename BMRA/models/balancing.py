# -*- coding: utf-8 -*-
"""
Models relating to Balancing Mechanism Unit-level data
"""
from __future__ import unicode_literals

import datetime as dt
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from ElexonDataManager.settings import BMRA_start_date
from .core import BMU

def check_dates(value):
    """
    Validates if date or datetime is within the range of historical BMRA data
    """
    if value < BMRA_start_date or value > dt.date.today():
        raise ValidationError('Date or timestamp not in valid BMRA range')

class BOAL(models.Model):
    """
    Bid-Offer Acceptance Level (prior to P217 implementation on 2009-11-09)
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    NK = models.IntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(2147483647)],
                             verbose_name='Acceptance number')
    TA = models.DateTimeField(verbose_name='Acceptance time',
                              validators=[check_dates])
    AD = models.BooleanField(verbose_name='Deemed bid-offer flag',
                             help_text='True for an acceptance of a bid-offer')

class BOALentry(models.Model):
    """
    Timestamped element of a Bid-Offer Acceptance Level
    """
    BOAL = models.ForeignKey(BOAL, on_delete=models.CASCADE)
    TS = models.DateTimeField(verbose_name='Acceptance level timestamp',
                              validators=[check_dates])
    VA = models.FloatField(verbose_name='Acceptance level value (MW)')

class BOALF(models.Model):
    """
    Bid-Offer Acceptance Level Flagged (following P217 implementation on 2009-11-09)
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    NK = models.IntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(2147483647)],
                             verbose_name='Acceptance number')
    TA = models.DateTimeField(verbose_name='Acceptance time')
    AD = models.BooleanField(verbose_name='Deemed Bid-Offer Flag',
                             help_text='True for an acceptance of a bid-offer')
    SO = models.BooleanField(verbose_name='SO Flag',
                             help_text='True where potentially impacted by \
                             transmission constraints')
    PF = models.BooleanField(verbose_name='STOR Flag',
                             help_text='True for relating to a STOR provider')

class BOALFentry(models.Model):
    """
    Timestamped element of a Bid-Offer Acceptance Level Flagged
    """
    BOALF = models.ForeignKey(BOAL, on_delete=models.CASCADE)
    TS = models.DateTimeField(verbose_name='Acceptance level timestamp',
                              validators=[check_dates])
    VA = models.FloatField(verbose_name='Acceptance level value (MW)')

class BOD(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    NN = models.IntegerField(verbose_name='Bid-offer pair no.')
    OP = models.FloatField()
    BP = models.FloatField()
    TS1 = models.DateTimeField()
    VB1 = models.FloatField()
    TS2 = models.DateTimeField()
    VB2 = models.FloatField()

class DISPTAV(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    NN = models.IntegerField(verbose_name='Bid-offer pair no.')
    OV = models.FloatField()
    BV = models.FloatField()
    P1 = models.FloatField()
    P2 = models.FloatField()
    P3 = models.FloatField()
    P4 = models.FloatField()
    P5 = models.FloatField()
    P6 = models.FloatField()

class EBOCF(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    NN = models.IntegerField(verbose_name='Bid-offer pair no.')
    OC = models.FloatField()
    BC = models.FloatField()

class FPN(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    VP1 = models.FloatField(verbose_name='Power (MW) at period start')
    VP2 = models.FloatField(verbose_name='Power (MW) at period end')

class MEL(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    VE1 = models.FloatField()
    VE2 = models.FloatField()

class MIL(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    VE1 = models.FloatField()
    VE2 = models.FloatField()

class PTAV(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    NN = models.IntegerField(verbose_name='Bid-offer pair no.')
    OV = models.FloatField()
    BV = models.FloatField()

class QAS(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    NN = models.IntegerField(verbose_name='Bid-offer pair no.')

class QPN(models.Model):
    """

    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField(verbose_name='Settlement Date')
    SP = models.IntegerField(verbose_name='Settlement Period')
    VP1 = models.FloatField(verbose_name='Power (MW) at period start')
    VP2 = models.FloatField(verbose_name='Power (MW) at period end')
