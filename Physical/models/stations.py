"""
models relating to physical power station entities
"""

from django.db import models
from BMRA.models.core import BMU
from Physical.models.zones import ConnectionSite, TO_zone, OC2_zone

class StationType(models.Model):
    """
    the type of power station
    """
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'physical_station_type'

    def __str__(self):
        return self.name

class PowerStation(models.Model):
    """
    a physical electricity generating station
    """
    name = models.CharField(max_length=100)
    to_zone = models.ForeignKey(TO_zone, on_delete=models.PROTECT, null=True)
    OC2_zone = models.ForeignKey(OC2_zone, on_delete=models.PROTECT, null=True)
    connection_site = models.ForeignKey(ConnectionSite, on_delete=models.PROTECT, null=True)
    station_type = models.ForeignKey(StationType, on_delete=models.PROTECT, null=True)
    embedded = models.BooleanField()
    latitude = models.FloatField(blank=True,
                                 null=True)
    longitude = models.FloatField(blank=True,
                                  null=True)
    comments = models.TextField(blank=True,
                                null=True)
    class Meta:
        db_table = 'physical_power_station'

    def __str__(self):
        return self.name

class PowerStationOwner(models.Model):
    """
    a commercial entity owning power stations
    """
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'physical_power_station_owner'

class PowerStationOwnership(models.Model):
    """
    a period of ownership of a power station by an owner
    """
    power_station = models.ForeignKey(PowerStation, on_delete=models.PROTECT)
    power_station_owner = models.ForeignKey(PowerStationOwner, on_delete=models.PROTECT)
    start_date = models.DateField()
    class Meta:
        db_table = 'physical_power_station_ownership'

class PowerStationBMU(models.Model):
    """
    a BMU associated with a physical power station
    """
    power_station = models.ForeignKey(PowerStation, on_delete=models.PROTECT)
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    class Meta:
        db_table = 'physical_power_station_bmu'

    def __str__(self):
        return '{} {}'.format(self.bmu, self.power_station)

class ProjectStatus(models.Model):
    """
    a defined state of project lifecycle
    """
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'physical_project_status'

class PowerStationStatus(models.Model):
    """
    a change in status or registered power output
    """
    power_station = models.ForeignKey(PowerStation, on_delete=models.PROTECT)
    effective_date = models.DateField()
    rating = models.FloatField()
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.PROTECT)
    class Meta:
        db_table = 'physical_power_station_status'
