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
    Bid-offer acceptance level (prior to P217 implementation on 2009-11-09)
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    NK = models.IntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(2147483647)],
                             verbose_name='Acceptance number')
    TA = models.DateTimeField(verbose_name='Acceptance time',
                              validators=[check_dates])
    AD = models.BooleanField(verbose_name='Deemed bid-offer flag',
                             help_text='True for an acceptance of a bid-offer')
    class Meta:
        index_together = ('bmu', 'TA')

class BOALlevel(models.Model):
    """
    Timestamped element of a bid-offer acceptance level
    """
    boal = models.ForeignKey(BOAL, on_delete=models.CASCADE)
    TS = models.DateTimeField(verbose_name='Acceptance level timestamp',
                              validators=[check_dates])
    VA = models.FloatField(verbose_name='Acceptance level value',
                           help_text='MW')
    class Meta:
        index_together = ('boal', 'TS')


class BOALF(models.Model):
    """
    Bid-offer acceptance level flagged (following P217 implementation on 2009-11-09)
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    NK = models.IntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(2147483647)],
                             verbose_name='Acceptance number')
    TA = models.DateTimeField(verbose_name='Acceptance time',
                              validators=[check_dates])
    AD = models.BooleanField(verbose_name='Deemed Bid-Offer Flag',
                             help_text='True for an acceptance of a bid-offer')
    SO = models.BooleanField(verbose_name='SO Flag',
                             help_text='True where potentially impacted by \
                             transmission constraints')
    PF = models.BooleanField(verbose_name='STOR Flag',
                             help_text='True for relating to a STOR provider')
    class Meta:
        index_together = ('bmu', 'TA')

class BOALFlevel(models.Model):
    """
    Timestamped element of a bid-offer acceptance level flagged
    """
    boalf = models.ForeignKey(BOALF, on_delete=models.CASCADE)
    TS = models.DateTimeField(verbose_name='Acceptance level timestamp',
                              validators=[check_dates])
    VA = models.FloatField(verbose_name='Acceptance level value',
                           help_text='MW')
    class Meta:
        index_together = ('boalf', 'TS')


class BOD(models.Model):
    """
    Bid-offer datum
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    NN = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    OP = models.FloatField(verbose_name='Offer price',
                           help_text='£/MWh')
    BP = models.FloatField(verbose_name='Bid price',
                           help_text='£/MWh')
    TS1 = models.DateTimeField(verbose_name='Period start time',
                               validators=[check_dates])
    VB1 = models.FloatField(verbose_name='Period start bid-offer level',
                            help_text='MW')
    TS2 = models.DateTimeField(verbose_name='Period end time',
                               validators=[check_dates])
    VB2 = models.FloatField(verbose_name='Period end bid-offer level',
                            help_text='MW')
    class Meta:
        index_together = ('bmu', 'SD', 'SP')

class BOAV(models.Model):
    """
    Bid-offer acceptance volume
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    NK = models.IntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(2147483647)],
                             verbose_name='Acceptance number')
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    NN = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    OV = models.FloatField(verbose_name='Offer volume',
                           help_text='MWh')
    BV = models.FloatField(verbose_name='Bid volume',
                           help_text='MWh')
    SA = models.BooleanField(verbose_name='Short acceptance flag',
                             help_text='True indicates acceptance was short duration')
    class Meta:
        index_together = ('bmu', 'SD', 'SP')

class DISPTAV(models.Model):
    """
    Disaggregated period total bid-offer acceptance volumes
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    NN = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    OV = models.FloatField(verbose_name='Total offer volume accepted',
                           help_text='MWh')
    BV = models.FloatField(verbose_name='Total bid volume accepted',
                           help_text='MWh')
    P1 = models.FloatField(verbose_name='Period tagged BMU offer volume',
                           help_text='MWh')
    P2 = models.FloatField(verbose_name='Period repriced BMU offer volume',
                           help_text='MWh')
    P3 = models.FloatField(verbose_name='Period originally-priced BMU offer volume',
                           help_text='MW')
    P4 = models.FloatField(verbose_name='Period repriced BMU offer volume',
                           help_text='MWh')
    P5 = models.FloatField(verbose_name='Period repriced BMU bid volume',
                           help_text='MWh')
    P6 = models.FloatField(verbose_name='Period originally-priced BMU bid volume',
                           help_text='MWh')
    class Meta:
        index_together = ('bmu', 'SD', 'SP')


class EBOCF(models.Model):
    """
    Estimated bid-offer cash flows
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    NN = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    OC = models.FloatField(verbose_name='Offer cashflow',
                           help_text='£')
    BC = models.FloatField(verbose_name='Bid cashflow',
                           help_text='£')
    class Meta:
        index_together = ('bmu', 'SD', 'SP')

class FPN(models.Model):
    """
    Final physical notification
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])

    class Meta:
        index_together = ('bmu', 'SD', 'SP')

class FPNlevel(models.Model):
    """
    Spot point relating to an FPN submission
    """
    fpn = models.ForeignKey(FPN, on_delete=models.CASCADE, db_index=True)
    TS = models.DateTimeField(verbose_name='Spot time',
                              validators=[check_dates])
    VP = models.FloatField(verbose_name='Spot power',
                           help_text='MW')
    class Meta:
        index_together = ('fpn', 'TS')

class MEL(models.Model):
    """
    Maximum export limit
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    class Meta:
        index_together = ('bmu', 'SD', 'SP')

class MELlevel(models.Model):
    """
    Spot point relating to a MEL submission
    """
    mel = models.ForeignKey(MEL, on_delete=models.CASCADE, db_index=True)
    TS = models.DateTimeField(verbose_name='Spot time',
                              validators=[check_dates])
    VE = models.FloatField(verbose_name='Spot power',
                           help_text='MW')
    class Meta:
        index_together = ('mel', 'TS')

class MIL(models.Model):
    """
    Minimum import limit
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    class Meta:
        index_together = ('bmu', 'SD', 'SP')

class MILlevel(models.Model):
    """
    Spot point relating to a MIL submission
    """
    mil = models.ForeignKey(MIL, on_delete=models.CASCADE, db_index=True)
    TS = models.DateTimeField(verbose_name='Spot time',
                              validators=[check_dates])
    VF = models.FloatField(verbose_name='Spot power',
                           help_text='MW')
    class Meta:
        index_together = ('mil', 'TS')

class PTAV(models.Model):
    """
    Period total bid-offer acceptance volumes
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    NN = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    OV = models.FloatField(verbose_name='Total offer volume accepted',
                           help_text='MWh')
    BV = models.FloatField(verbose_name='Total bid volume accepted',
                           help_text='MWh')
    class Meta:
        index_together = ('bmu', 'SD', 'SP')

class QAS(models.Model):
    """
    BMU applicable balancing services volume
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    SV = models.FloatField(verbose_name='Energy volume',
                           help_text='MWh')

class QPN(models.Model):
    """
    Quiescent physical notification
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    TS = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    SD = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    SP = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    class Meta:
        index_together = ('bmu', 'SD', 'SP')

class QPNlevel(models.Model):
    """
    Spot point relating to an QPN submission
    """
    qpn = models.ForeignKey(QPN, on_delete=models.CASCADE, db_index=True)
    TS = models.DateTimeField(verbose_name='Spot time',
                              validators=[check_dates])
    VP = models.FloatField(verbose_name='Spot power',
                           help_text='MW')
    class Meta:
        index_together = ('qpn', 'TS')
