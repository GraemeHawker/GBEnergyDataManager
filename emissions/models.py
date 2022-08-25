from django.db import models
from BMRA.models.core import BMU
from Physical.models.stations import StationType

# Create your models here.
class StationTypeEmissions(models.Model):
    """
    the emissions data associated with a particular BMU type
    """
    station_type = models.ForeignKey(StationType, on_delete=models.PROTECT)
    base_fuel_ei = models.FloatField(verbose_name='Base fuel emissions intensity (kgCO2/kWh)')
    efficiency_max = models.FloatField(verbose_name='Maximum efficiency (between 0 and 1)')
    efficiency_max_temp = models.FloatField(verbose_name='Temperature in C at which maximum efficiency is achieved')
    efficiency_min = models.FloatField(verbose_name='Minimum efficiency (between 0 and 1)')
    efficiency_min_temp = models.FloatField(verbose_name='Temperature in C at which minimum efficiency is achieved')
    extrapolate_min = models.BooleanField(
        verbose_name='Whether to extrapolate efficiency below minimum outside of defined temp range (True), or use constant minimum value (False)')
    extrapolate_max = models.BooleanField(
        verbose_name='Whether to extrapolate efficiency above maximum outside of defined temp range (True), or use constant maximum value (False)')


    class Meta:
        db_table = 'emissions_station_type'
        verbose_name_plural = "station type emissions"

    def __str__(self):
        return '{}'.format(self.station_type)

class BMUEmissions(models.Model):
    """
    the emissions data associated with a particular BMU type
    """
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    base_fuel_ei = models.FloatField(verbose_name='Base fuel emissions intensity (gCO2/kWh)')
    efficiency_max = models.FloatField(verbose_name='Maximum efficiency (between 0 and 1)')
    efficiency_max_temp = models.FloatField(verbose_name='Temperature in C at which maximum efficiency is achieved')
    efficiency_min = models.FloatField(verbose_name='Minimum efficiency (between 0 and 1)')
    efficiency_min_temp = models.FloatField(verbose_name='Temperature in C at which minimum efficiency is achieved')
    extrapolate_min = models.BooleanField(
        verbose_name='Whether to extrapolate efficiency below minimum outside of defined temp range (True), or use constant minimum value (False)')
    extrapolate_max = models.BooleanField(
        verbose_name='Whether to extrapolate efficiency above maximum outside of defined temp range (True), or use constant maximum value (False)')


    class Meta:
        db_table = 'emissions_bmu'
        verbose_name_plural = "bmu emissions"

    def __str__(self):
        return '{}'.format(self.bmu)