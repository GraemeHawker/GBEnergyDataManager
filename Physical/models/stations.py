"""
models relating to physical power station entities
"""

from django.db import models
from BMRA.models.core import BMU
from Physical.models.zones import ConnectionSite, TOZone, OC2Zone

class PowerStation(models.Model):
    """
    a physical electricity generating station
    """
    name = models.CharField(max_length=100)

class StationType(models.Model):
    """
    the type of power station
    """
    name = models.CharField(max_length=100)
    connection_site = models.ForeignKey(ConnectionSite, on_delete=models.PROTECT)
    OC2_zone = models.ForeignKey(OC2Zone, on_delete=models.PROTECT)
    TO_zone = models.ForeignKey(TOZone, on_delete=models.PROTECT)

class PowerStationOwner(models.Model):
    """
    a commercial entity owning power stations
    """
    name = models.CharField(max_length=100)

class PowerStationOwnership(models.Model):
    """
    a period of ownership of a power station by an owner
    """
    power_station = models.ForeignKey(PowerStation, on_delete=models.PROTECT)
    power_station_owner = models.ForeignKey(PowerStationOwner, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(null=True) #null indicates current ownership

class PowerStationBMU(models.Model):
    """
    a BMU associated with a physical power station
    """
    power_station = models.ForeignKey(PowerStation, on_delete=models.PROTECT)
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)

class ProjectStatus(models.Model):
    """
    a defined state of project lifecycle
    """
    name = models.CharField(max_length=100)

class PowerStationStatus(models.Model):
    """
    a change in status or registered power output
    """
    power_station = models.ForeignKey(PowerStation, on_delete=models.PROTECT)
    effective_date = models.DateField()
    rating = models.FloatField()
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.PROTECT)
