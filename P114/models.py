from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from GBEnergyDataManager.settings import P114_DATA_START_DATE

def check_dates(value):
    """
    Validates if date or datetime is within the range of historical BMRA data
    """
    if value < P114_DATA_START_DATE or value > dt.date.today():
        raise ValidationError('Date or timestamp not in valid P114 range')

# Create your models here.
class sr_type(models.Model):
    name = models.CharField(max_length=2, primary_key=True)
    order = models.IntegerField(verbose_name='Ordinal Value',
                                help_text='defines time order in which \
                                settlement values are derived, 1=first')

class gsp_group(models.Model):
    """
    Grid Supply Point Group
    """
    id = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'p114_gsp_group'

class gsp(models.Model):
    """
    Grid Supply Point
    """
    id = models.CharField(max_length=11, primary_key=True)
    gsp_group = models.ForeignKey(gsp_group,
                                  on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'p114_gsp'

class bsc_party(models.Model):
    """
    BSC party
    """
    id = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'p114_bsc_party'

class agv(models.Model):
    """
    Aggregated GSP Group Take Volumes
    """
    gsp_group = models.ForeignKey(gsp_group,
                                  on_delete=models.PROTECT)
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sr_type = models.ForeignKey(sr_type,
                                on_delete=models.PROTECT)
    run_no = models.IntegerField(verbose_name='CDCA run number')
    agg_date = models.DateField(verbose_name='Aggregation date',
                                validators=[check_dates])

    class Meta:
        db_table = 'p114_agv'
        index_together = ('gsp_group', 'sd', 'sr_type')

class agp(models.Model):
    """
    Aggregated GSP Group Take - Period
    """
    agv = models.ForeignKey(agv,
                            on_delete=models.PROTECT)
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    ei = models.BooleanField(verbose_name='Estimate indicator',
                             help_text='True for an estimated value')
    ii = models.BooleanField(verbose_name='Import/Export indicator',
                             help_text='True for import, False for export')
    gt_vol = models.FloatField(verbose_name='Group Take Volume',
                               help_text='MWh')

    class Meta:
        db_table = 'p114_agp'
        index_together = ('agv', 'sp')

class srh(models.Model):
    """
    Settlement Report Header
    """
    sd = models.DateField(verbose_name='Settlement date',
                          validators=[check_dates])
    sr_type = models.ForeignKey(sr_type,
                                on_delete=models.PROTECT)
    saa_run_no = models.IntegerField(verbose_name='SAA Run Number',
                                     validators=[MinValueValidator(1),
                                                 MaxValueValidator(50)])
    saa_cdca_run_no = models.IntegerField(verbose_name='SAA CDCA Run Number',
                                          validators=[MinValueValidator(1),
                                                      MaxValueValidator(50)])
    svaa_cdca_sd = models.DateField(verbose_name='SVAA CDCA Settlement date',
                                    validators=[check_dates])
    svaa_cdca_run_no = models.IntegerField(verbose_name='SAA CDCA Run Number',
                                           validators=[MinValueValidator(1),
                                                       MaxValueValidator(50)])
    svaa_ssr_run_no = models.IntegerField(verbose_name='SAA CDCA Run Number',
                                          validators=[MinValueValidator(1),
                                                      MaxValueValidator(50)])
    bsc_party = models.ForeignKey(bsc_party,
                                  on_delete=models.PROTECT)
    class Meta:
        db_table = 'p114_srh'
        index_together = ('bsc_party', 'sd', 'sr_type')

class spi(models.Model):
    """
    Settlement Period Information
    """
    sp = models.IntegerField(verbose_name='Settlement period',
                             validators=[MinValueValidator(1),
                                         MaxValueValidator(50)])
    srh = models.ForeignKey(srh,
                            on_delete=models.PROTECT)
    pdc = models.CharField(max_length=2,
                           verbose_name='Price Derivation Code')
    tot_dem = models.DecimalField(max_digits=10,
                                  decimal_places=3,
                                  verbose_name='Total Demand',
                                  help_text='MWh')
    tot_gen = models.DecimalField(max_digits=10,
                                  decimal_places=3,
                                  verbose_name='Total Generation',
                                  help_text='MWh')
    tot_bsc_vol = models.DecimalField(max_digits=10,
                                      decimal_places=3,
                                      verbose_name='Total Period Applicable \
                                      Balancing Services Volume',
                                      help_text='MWh')
    info_imb1 = models.DecimalField(max_digits=10,
                                    decimal_places=5,
                                    verbose_name='Information Imbalance Price 1',
                                    help_text='£/MWh')
    info_imb2 = models.DecimalField(max_digits=10,
                                    decimal_places=5,
                                    verbose_name='Information Imbalance Price 2',
                                    help_text='£/MWh')
    not_res = models.DecimalField(max_digits=10,
                                  decimal_places=3,
                                  verbose_name='Notional Reserve Limit',
                                  null=True,
                                  blank=True)
    tot_niv_vol = models.DecimalField(max_digits=10,
                                      decimal_places=3,
                                      verbose_name='Total NIV Tagged Volume',
                                      help_text='MWh')
    arbitrage = models.BooleanField(verbose_name='Arbitrage Flag')
    cadl = models.IntegerField(verbose_name='Continuous Acceptance \
                               Duration Limit',
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(99)])
    dmat = models.DecimalField(max_digits=10,
                               decimal_places=3,
                               verbose_name='De Minimis Acceptance \
                               Threshold',
                               help_text='MWh')



    class Meta:
        db_table = 'p114_spi'
        index_together = ('srh', 'sd', 'sr_type')
