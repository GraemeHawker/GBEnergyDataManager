# -*- coding: utf-8 -*-
"""
Models relating to BMRA system-level data
"""
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from BMRA.models.balancing import check_dates
from .core import LDSO


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
    ai = models.IntegerField(verbose_name='Adjustment identifier',
                             help_text='The unique identifier allocated to a \
                             single Balancing Services Adjustment Action item \
                             - unique within each settlement period')
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
    px = models.CharField(max_length=100,
                          blank=True,
                          verbose_name='The name or unique identifier of the person who provides Balancing Services outside of the Balancing Mechanism',
                          help_text='')
    ax = models.CharField(max_length=100,
                          blank=True,
                          verbose_name='The name or unique identifier of the asset providing the relevant Balancing Services Adjustment Action',
                          help_text='')
    tx = models.CharField(max_length=100,
                          blank=True,
                          verbose_name='Whether the Balancing Service was procured by NETSO through a tender',
                          help_text='')
    sx = models.CharField(max_length=100,
                          blank=True,
                          verbose_name='The type of Balancing Service procured',
                          help_text='')

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
                              help_text='£/MWh',
                              blank=True,
                              null=True)
    rp = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Replacement Price',
                             help_text='£/MWh',
                             blank=True,
                             null=True)
    rv = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Replacement Price Calculation Volume',
                             help_text='MWh',
                             blank=True,
                             null=True)
    bd = models.BooleanField(verbose_name='BSAD Defaulted',
                             help_text='If True A1 to A6 are default values')
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


class SOSO(models.Model):
    """
    So to SO prices
    """
    tt = models.CharField(max_length=10,
                          verbose_name='SO-SO trade type',
                          help_text='Indicating parties trading as an underscore separated string')
    st = models.DateTimeField(verbose_name='Start time',
                              validators=[check_dates])
    td = models.CharField(max_length=3,
                          verbose_name='Trade direction',
                          help_text='‘A01’ (up) or ‘A02’ (down)')
    ic = models.CharField(max_length=30,
                          verbose_name='Contract identifier')
    tq = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Trade quantity offered',
                             help_text='MW')
    pt = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Trade price offered',
                             help_text='£/MWh')

    class Meta:
        db_table = 'bmra_soso'
        index_together = ('tt', 'st')


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
                             decimal_places=2,
                             verbose_name='Market Index Price',
                             help_text='£/MWh')
    m2 = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Market Index Volume',
                             help_text='MWh')

    class Meta:
        db_table = 'bmra_mid'
        index_together = ('mi', 'sd', 'sp')


class ISPSTACK(models.Model):
    """
    Indicative System Price Stack
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    bo = models.CharField(max_length=1,
                          verbose_name='Bid/Offer Indicator',
                          help_text='Bid (B) or Offer (O)')
    sn = models.IntegerField(verbose_name='Stack index number',
                             help_text='indicating relative position within \
                             the related stack')
    ci = models.CharField(max_length=30,
                          verbose_name='Component identifier',
                          help_text='associated BMU ID, or for Balancing \
                          Services Adjustment items the unique ID allocated \
                          by the SO, or for Demand Control Volume stack a \
                          unique ID from that BSC Agents system')
    nk = models.IntegerField(blank=True,
                             null=True,
                             verbose_name='Acceptance number',
                             help_text='not included for Balancing Services \
                             Adjustment items')
    nn = models.IntegerField(verbose_name='Bid-offer pair no.',
                             validators=[MinValueValidator(-5),
                                         MaxValueValidator(5)],
                             null=True,
                             blank=True)
    cf = models.BooleanField(verbose_name='CADL Flag',
                             help_text='A value of True indicates that an \
                             Acceptance is considered to be a Short Duration acceptance')
    so = models.BooleanField(verbose_name='SO Flag',
                             help_text='A value of True indicates that an \
                             Acceptance or BS Adjustment Action should be \
                             considered to be potentially impacted by \
                             transmission constraints')
    pf = models.BooleanField(verbose_name='STOR Provider Flag',
                             help_text='A value of True Indicates the item \
                             relates to a STOR Provider')
    ri = models.BooleanField(verbose_name='Repriced Indicator',
                             help_text='True indicates the item has been \
                             repriced')
    up = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Bid-offer Original Price',
                             help_text='£/MWh')
    rsp = models.DecimalField(max_digits=10,
                              decimal_places=3,
                              verbose_name='Reserve Scarcity Price',
                              help_text='£/MWh',
                              blank=True,
                              null=True)
    ip = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Stack Item Original Price',
                             help_text='£/MWh')
    iv = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Stack Item Volume',
                             help_text='MWh')
    da = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='DMAT Adjusted Volume',
                             help_text='MWh')
    av = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Arbitrage Adjusted Volume',
                             help_text='MWh')
    nv = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='NIV Adjusted Volume',
                             help_text='MWh')
    pv = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='PAR Adjusted Volume',
                             help_text='MWh')
    fp = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Stack Item Final Price',
                             help_text='£/MWh')
    tm = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='Transmission Loss Multiplier Value',
                             help_text='MWh')
    tv = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='TLM Adjusted Volume',
                             help_text='MWh')
    tc = models.DecimalField(max_digits=10,
                             decimal_places=3,
                             verbose_name='TLM Adjusted Cost',
                             help_text='£')

    class Meta:
        db_table = 'bmra_ispstack'
        index_together = ('sd', 'sp', 'ci', 'nn')


class TBOD(models.Model):
    """
    Total Bid-Offer Data
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    ot = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='System wide total offer volume',
                             help_text='MWh')
    bt = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='System wide total bid volume',
                             help_text='MWh')

    class Meta:
        db_table = 'bmra_tbod'
        index_together = ('sd', 'sp')


class SYSMSG(models.Model):
    """
    System Message
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Published time',
                              validators=[check_dates])
    mt = models.CharField(max_length=6,
                          verbose_name='Message type')
    sm = models.TextField(verbose_name='System warning message')

    class Meta:
        db_table = 'bmra_sysmsg'


class SYSWARN(models.Model):
    """
    System warning
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Published time',
                              validators=[check_dates])
    sw = models.TextField(verbose_name='System warning message')

    class Meta:
        db_table = 'bmra_syswarn'


class DCONTROL(models.Model):
    """
    Demand Control Instruction Notification
    """
    tp = models.DateTimeField(primary_key=True,
                              verbose_name='Published time',
                              validators=[check_dates])

    class Meta:
        db_table = 'bmra_dcontrol'


class DCONTROLlevel(models.Model):
    """
    Individual control instruction to an LDSO
    """
    dcontrol = models.ForeignKey(DCONTROL, on_delete=models.CASCADE)
    ds = models.ForeignKey(LDSO,
                           verbose_name='Affected LDSO',
                           on_delete=models.PROTECT)
    dcid = models.IntegerField(verbose_name='Demand Control ID')
    sq = models.IntegerField(verbose_name='Instruction sequence no.')
    ev = models.CharField(max_length=1,
                          verbose_name='Demand control event flag',
                          help_text='I indicates instruction by the SO or \
                          emergency manual disconnection. L indicates \
                          automatic low frequency demand disconnection')
    tf = models.DateTimeField(verbose_name='Time from',
                              validators=[check_dates])
    ti = models.DateTimeField(verbose_name='Time to',
                              validators=[check_dates])
    vo = models.DecimalField(max_digits=10,
                             decimal_places=2,
                             verbose_name='Demand control level',
                             help_text='MW')
    so = models.BooleanField(verbose_name='SO flag',
                             help_text='True indicates that an instruction \
                             should be considered to be potentially impacted \
                             by transmission constraints')
    am = models.CharField(max_length=3,
                          verbose_name='Amendment flag',
                          help_text='ORI : Original, INS : Insert, UPD : Update')

    class Meta:
        db_table = 'bmra_dcontrollevel'
        index_together = ['dcontrol', 'tf', 'ds']
