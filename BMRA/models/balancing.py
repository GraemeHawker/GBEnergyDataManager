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
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    nk = models.IntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(2147483647)],
                             verbose_name='Acceptance number')
    ta = models.DateTimeField(verbose_name='Acceptance time',
                              validators=[check_dates])
    ad = models.BooleanField(verbose_name='Deemed bid-offer flag',
                             help_text='True for an acceptance of a bid-offer')
    class Meta:
        db_table = 'bmra_boal'
        index_together = ('bmu', 'ta')

class BOALlevel(models.Model):
    """
    Timestamped element of a bid-offer acceptance level
    """
    boal = models.ForeignKey(BOAL, on_delete=models.CASCADE)
    ts = models.DateTimeField(verbose_name='Acceptance level timestamp',
                              validators=[check_dates])
    va = models.FloatField(verbose_name='Acceptance level value',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_boallevel'
        index_together = ('boal', 'ts')


class BOALF(models.Model):
    """
    Bid-offer acceptance level flagged (following P217 implementation on 2009-11-09)
    """
    bmu = models.ForeignKey(BMU,
                            on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    nk = models.IntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(2147483647)],
                             verbose_name='Acceptance number')
    ta = models.DateTimeField(verbose_name='Acceptance time',
                              validators=[check_dates])
    ad = models.BooleanField(verbose_name='Deemed Bid-Offer Flag',
                             help_text='True for an acceptance of a bid-offer')
    so = models.BooleanField(verbose_name='SO Flag',
                             help_text='True where potentially impacted by \
                             transmission constraints')
    pf = models.BooleanField(verbose_name='STOR Flag',
                             help_text='True for relating to a STOR provider')
    class Meta:
        db_table = 'bmra_boalf'
        index_together = ('bmu', 'ta')

class BOALFlevel(models.Model):
    """
    Timestamped element of a bid-offer acceptance level flagged
    """
    boalf = models.ForeignKey(BOALF, on_delete=models.CASCADE)
    ts = models.DateTimeField(verbose_name='Acceptance level timestamp',
                              validators=[check_dates])
    va = models.FloatField(verbose_name='Acceptance level value',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_boalflevel'
        index_together = ('boalf', 'ts')


class BOD(models.Model):
    """
    Bid-offer datum
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    nn = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    op = models.FloatField(verbose_name='Offer price',
                           help_text='£/MWh')
    bp = models.FloatField(verbose_name='Bid price',
                           help_text='£/MWh')
    ts1 = models.DateTimeField(verbose_name='Period start time',
                               validators=[check_dates])
    vb1 = models.FloatField(verbose_name='Period start bid-offer level',
                            help_text='MW')
    ts2 = models.DateTimeField(verbose_name='Period end time',
                               validators=[check_dates])
    vb2 = models.FloatField(verbose_name='Period end bid-offer level',
                            help_text='MW')
    class Meta:
        db_table = 'bmra_bod'
        index_together = ('bmu', 'sd', 'sp')

class BOAV(models.Model):
    """
    Bid-offer acceptance volume
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    nk = models.IntegerField(validators=[MinValueValidator(1),
                                         MaxValueValidator(2147483647)],
                             verbose_name='Acceptance number')
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    nn = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    ov = models.FloatField(verbose_name='Offer volume',
                           help_text='MWh')
    bv = models.FloatField(verbose_name='Bid volume',
                           help_text='MWh')
    sa = models.BooleanField(verbose_name='Short acceptance flag',
                             help_text='True indicates acceptance was short duration')
    class Meta:
        db_table = 'bmra_boav'
        index_together = ('bmu', 'sd', 'sp')

class DISPTAV(models.Model):
    """
    Disaggregated period total bid-offer acceptance volumes
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    nn = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    ov = models.FloatField(verbose_name='Total offer volume accepted',
                           help_text='MWh')
    bv = models.FloatField(verbose_name='Total bid volume accepted',
                           help_text='MWh')
    p1 = models.FloatField(verbose_name='Period tagged BMU offer volume',
                           help_text='MWh')
    p2 = models.FloatField(verbose_name='Period repriced BMU offer volume',
                           help_text='MWh')
    p3 = models.FloatField(verbose_name='Period originally-priced BMU offer volume',
                           help_text='MW')
    p4 = models.FloatField(verbose_name='Period repriced BMU offer volume',
                           help_text='MWh')
    p5 = models.FloatField(verbose_name='Period repriced BMU bid volume',
                           help_text='MWh')
    p6 = models.FloatField(verbose_name='Period originally-priced BMU bid volume',
                           help_text='MWh')
    class Meta:
        db_table = 'bmra_disptav'
        index_together = ('bmu', 'sd', 'sp')


class EBOCF(models.Model):
    """
    Estimated bid-offer cash flows
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    nn = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    oc = models.FloatField(verbose_name='Offer cashflow',
                           help_text='£')
    bc = models.FloatField(verbose_name='Bid cashflow',
                           help_text='£')
    class Meta:
        db_table = 'bmra_ebocf'
        index_together = ('bmu', 'sd', 'sp')

class FPN(models.Model):
    """
    Final physical notification
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])

    class Meta:
        db_table = 'bmra_fpn'
        index_together = ('bmu', 'sd', 'sp')

class FPNlevel(models.Model):
    """
    Spot point relating to an FPN submission
    """
    fpn = models.ForeignKey(FPN, on_delete=models.CASCADE, db_index=True)
    ts = models.DateTimeField(verbose_name='Spot time',
                              validators=[check_dates])
    vp = models.FloatField(verbose_name='Spot power',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_fpnlevel'
        index_together = ('fpn', 'ts')

class MEL(models.Model):
    """
    Maximum export limit
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    class Meta:
        db_table = 'bmra_mel'
        index_together = ('bmu', 'sd', 'sp')

class MELlevel(models.Model):
    """
    Spot point relating to a MEL submission
    """
    mel = models.ForeignKey(MEL, on_delete=models.CASCADE, db_index=True)
    ts = models.DateTimeField(verbose_name='Spot time',
                              validators=[check_dates])
    ve = models.FloatField(verbose_name='Spot power',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_mellevel'
        index_together = ('mel', 'ts')

class MIL(models.Model):
    """
    Minimum import limit
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    class Meta:
        db_table = 'bmra_mil'
        index_together = ('bmu', 'sd', 'sp')

class MILlevel(models.Model):
    """
    Spot point relating to a MIL submission
    """
    mil = models.ForeignKey(MIL, on_delete=models.CASCADE, db_index=True)
    ts = models.DateTimeField(verbose_name='Spot time',
                              validators=[check_dates])
    vf = models.FloatField(verbose_name='Spot power',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_millevel'
        index_together = ('mil', 'ts')

class PTAV(models.Model):
    """
    Period total bid-offer acceptance volumes
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    nn = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)])
    ov = models.FloatField(verbose_name='Total offer volume accepted',
                           help_text='MWh')
    bv = models.FloatField(verbose_name='Total bid volume accepted',
                           help_text='MWh')
    class Meta:
        db_table = 'bmra_ptav'
        index_together = ('bmu', 'sd', 'sp')

class QAS(models.Model):
    """
    BMU applicable balancing services volume
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    sv = models.FloatField(verbose_name='Energy volume',
                           help_text='MWh')
    class Meta:
        db_table = 'bmra_qas'
        index_together = ('bmu', 'sd', 'sp')

class QPN(models.Model):
    """
    Quiescent physical notification
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    ts = models.DateTimeField(verbose_name='Received time',
                              validators=[check_dates])
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    class Meta:
        db_table = 'bmra_qpn'
        index_together = ('bmu', 'sd', 'sp')

class QPNlevel(models.Model):
    """
    Spot point relating to an QPN submission
    """
    qpn = models.ForeignKey(QPN, on_delete=models.CASCADE, db_index=True)
    ts = models.DateTimeField(verbose_name='Spot time',
                              validators=[check_dates])
    vp = models.FloatField(verbose_name='Spot power',
                           help_text='MW')
    class Meta:
        db_table = 'bmra_qpnlevel'
        index_together = ('qpn', 'ts')
