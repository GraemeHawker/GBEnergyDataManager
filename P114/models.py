from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ElexonDataManager.settings import P114_DATA_START_DATE

def check_dates(value):
    """
    Validates if date or datetime is within the range of historical BMRA data
    """
    if value < P114_DATA_START_DATE or value > dt.date.today():
        raise ValidationError('Date or timestamp not in valid P114 range')

# Create your models here.
class sr_type(models.Model):
    name = models.CharField(max_length=2, primary_key=True)
    order  = models.IntegerField(verbose_name='Ordinal Value',
                                 help_text='defines time order in which settlement values are derived, 1=first')

class gsp_group(models.Model):
    """
    Grid Supply Point Group
    """
    id = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'p114_gsp_group'

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
