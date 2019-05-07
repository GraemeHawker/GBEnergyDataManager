# -*- coding: utf-8 -*-
"""
Models relating to BMRA system-level data
"""
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from BMRA.models.balancing import check_dates

class BSAD(models.Model):
    """
    Balancing Services Adjustment Data
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    a1 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Sell price cost adjustment',
                             help_text='£')
    a2 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Sell price volume adjustment',
                             help_text='MWh')
    a3 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Sell price price adjustment',
                             help_text='£/MWh')
    a4 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Buy price cost adjustment',
                             help_text='£')
    a5 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Buy price volume adjustment',
                             help_text='MWh')
    a6 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Buy price price adjustment',
                             help_text='£/MWh')
    class Meta:
        db_table = 'bmra_bsad'
        index_together = ('sd', 'sp')

class DISBSAD(models.Model):
    """
    Balancing Services Adjustment Action Data
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    ai = models.IntegerField(verbose_name='Adjustment identifier')
    so = models.BooleanField(verbose_name='System Operator Flag',
                             help_text='A value of ‘T’ indicates where an \
                             Acceptance or Balancing Services Adjustment \
                             Action item should be considered to be \
                             potentially impacted by transmission constraints')
    pf = models.BooleanField(verbose_name='STOR Flag',
                             help_text='A value of ‘T’ indicates where an \
                             Acceptance or Balancing Services Adjustment \
                             Action item should be considered being \
                             related to a STOR Provider')
    jc = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Adjustment cost',
                             help_text='£')
    jv = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Adjustment volume',
                             help_text='MWh')
    class Meta:
        db_table = 'bmra_disbsad'
        index_together = ('sd', 'sp')

class NETBSAD(models.Model):
    """
    Balancing Services Adjustment Data
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    a7 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Net Energy Sell Price Cost Adjustment (ESCA)',
                             help_text='£')
    a8 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Net Energy Sell Price Volume Adjustment (ESVA)',
                             help_text='MWh')
    a11 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Net System Sell Price Volume Adjustment (SSVA)',
                             help_text='MWh')
    a3 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Sell Price Price Adjustment (SPA)',
                             help_text='£')
    a9 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Net Energy Buy Price Cost Adjustment (EBCA)',
                             help_text='£')
    a10 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Net Energy Buy Price Volume Adjustment (EBVA)',
                             help_text='MWh')
    a12 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Net System Buy Price Volume Adjustment (SBVA)',
                             help_text='MWh')
    a6 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Buy Price Price Adjustment (BPA)',
                             help_text='£')
    class Meta:
        db_table = 'bmra_netbsad'
        index_together = ('sd', 'sp')

class EBSP(models.Model):
    """
    Estimated buy and sell price
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    pb = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Buy price - the price that must be \
                             paid for electricity which is out of balance',
                             help_text='£')
    ps = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Sell Price - the price received \
                             for electricity which is out of balance',
                             help_text='£')
    ao = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Accepted Offer Volume - \
                             System wide total Accepted Offer Volume for \
                             the Settlement Period',
                             help_text='MWh')
    ab = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Accepted Bid Volume - \
                             System wide total Accepted Bid Volume for \
                             the Settlement Period',
                             help_text='MWh')
    ap = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Unpriced Accepted Offer \
                             Volume - System wide total Unpriced Accepted \
                             Offer Volume for the Settlement Period',
                             help_text='MWh')
    ac = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Unpriced Accepted Bid \
                             Volume - System wide total Unpriced Accepted \
                             Bid Volume for the Settlement Period',
                             help_text='MWh')
    pp = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Priced Accepted Offer Volume \
                             - System wide total Priced Accepted Offer Volume \
                             for the Settlement Period',
                             help_text='MWh')
    pc = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Priced Accepted Bid Volume \
                             - System wide total Priced Accepted Bid Volume \
                             for the Settlement Period',
                             help_text='MWh')
    bd = models.BooleanField(verbose_name='BSAD Defaulted',
                             help_text='If True A1 to A6 are default values')
    a1 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Sell price cost adjustment',
                             help_text='£')
    a2 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Sell price volume adjustment',
                             help_text='MWh')
    a3 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Sell price price adjustment',
                             help_text='£/MWh')
    a4 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Buy price cost adjustment',
                             help_text='£')
    a5 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Buy price volume adjustment',
                             help_text='MWh')
    a6 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Buy price price adjustment',
                             help_text='£/MWh')
    class Meta:
        db_table = 'bmra_ebsp'
        index_together = ('sd', 'sp')

class NETEBSP(models.Model):
    """
    Estimated buy and sell price
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    pb = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Buy price - the price that must be \
                             paid for electricity which is out of balance',
                             help_text='£')
    ps = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Sell Price - the price received \
                             for electricity which is out of balance',
                             help_text='£')
    pd = models.CharField(max_length=2,
                          verbose_name='Price Derivation Code - A code that \
                          describes the way in which SSP and SBP were calculated',
                          help_text='Valid values defined in BMRA-I006')
    ao = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Accepted Offer Volume - \
                             System wide total Accepted Offer Volume for \
                             the Settlement Period',
                             help_text='MWh')
    ab = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Accepted Bid Volume - \
                             System wide total Accepted Bid Volume for \
                             the Settlement Period',
                             help_text='MWh')
    ap = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Unpriced Accepted Offer \
                             Volume - System wide total Unpriced Accepted \
                             Offer Volume for the Settlement Period',
                             help_text='MWh')
    ac = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Unpriced Accepted Bid \
                             Volume - System wide total Unpriced Accepted \
                             Bid Volume for the Settlement Period',
                             help_text='MWh')
    pp = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Priced Accepted Offer Volume \
                             - System wide total Priced Accepted Offer Volume \
                             for the Settlement Period',
                             help_text='MWh')
    pc = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Total Priced Accepted Bid Volume \
                             - System wide total Priced Accepted Bid Volume \
                             for the Settlement Period',
                             help_text='MWh')
    ni = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Indicative Net Imbalance Volume',
                             help_text='MWh')
    bd = models.BooleanField(verbose_name='BSAD Defaulted',
                             help_text='If True A1 to A6 are default values')
    a7 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Net Energy Sell Price Cost Adjustment (ESCA)',
                             help_text='£')
    a8 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Net Energy Sell Price Volume Adjustment (ESVA)',
                             help_text='MWh')
    a11 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Net System Sell Price Volume Adjustment (SSVA)',
                             help_text='MWh')
    a3 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Sell Price Price Adjustment (SPA)',
                             help_text='£')
    a9 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Net Energy Buy Price Cost Adjustment (EBCA)',
                             help_text='£')
    a10 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Net Energy Buy Price Volume Adjustment (EBVA)',
                             help_text='MWh')
    a12 = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Net System Buy Price Volume Adjustment (SBVA)',
                             help_text='MWh')
    a6 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Buy Price Price Adjustment (BPA)',
                             help_text='£')
    class Meta:
        db_table = 'bmra_netebsp'
        index_together = ('sd', 'sp')

class DISEBSP(models.Model):
    """
    Disaggregated Estimated Buy and Sell Price
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    pb = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Buy price - the price that must be \
                             paid for electricity which is out of balance',
                             help_text='£')
    ps = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Sell Price - the price received \
                             for electricity which is out of balance',
                             help_text='£')
    pd = models.CharField(max_length=2,
                          verbose_name='Price Derivation Code - A code that \
                          describes the way in which SSP and SBP were calculated',
                          help_text='Valid values defined in BMRA-I006')
    rsp = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Reserve Scarcity Price',
                             help_text='£/MWh')
    a3 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Sell Price Price Adjustment (SPA)',
                             help_text='£')
    a6 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Buy Price Price Adjustment (BPA)',
                             help_text='£')
    ni = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Indicative Net Imbalance Volume',
                             help_text='MWh')
    ao = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Total Accepted Offer Volume - \
                             System wide total Accepted Offer Volume for \
                             the Settlement Period',
                             help_text='MWh')
    ab = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='Total Accepted Bid Volume - \
                             System wide total Accepted Bid Volume for \
                             the Settlement Period',
                             help_text='MWh')
    t1 = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='System wide total tagged Accepted \
                             Offer Volume for Settlement period',
                             help_text='MWh')
    t2 = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='System wide total tagged Accepted \
                             Bid Volume for Settlement period',
                             help_text='MWh')
    pp = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='System wide total priced Accepted \
                             Offer Volume for Settlement period',
                             help_text='MWh')
    pc = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='System wide total priced Accepted \
                             Bid Volume for Settlement period',
                             help_text='MWh')
    j1 = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='System wide total Adjustment Sell \
                             Volume for Settlement period',
                             help_text='MWh')
    j2 = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='System wide total Adjustment Buy \
                             Volume for Settlement periodd',
                             help_text='MWh')
    j3 = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='System wide total tagged Adjustment \
                             Sell Volume for Settlement period',
                             help_text='MWh')
    j4 = models.DecimalField(max_digits=10,
                             decimal_places=5,
                             verbose_name='System wide total tagged Adjustment \
                             Buy Volume for Settlement period',
                             help_text='MWh')

    class Meta:
        db_table = 'bmra_disebsp'
        index_together = ('sd', 'sp')

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
