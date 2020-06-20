from django.db import models
from BMRA.models.core import BMU

class TO_zone(models.Model):
    """
    a zone relating to a specific Transmission Owner
    """
    id = models.CharField(max_length=10,
                          primary_key=True)
    class Meta:
        verbose_name = 'TO Zone'
        db_table = 'physical_to_zone'

    def __str__(self):
        return self.id


class OC2_zone(models.Model):
    """
    an OC2 zone
    """
    id = models.CharField(max_length=10,
                          primary_key=True)
    to_zone = models.ForeignKey(TO_zone,
                                on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'OC2 Zone'
        db_table = 'physical_oc2_zone'

    def __str__(self):
        return self.id

class ConnectionSite(models.Model):
    """
    a connection site on the network
    """
    name = models.CharField(max_length=100)
    oc2_zone = models.ForeignKey(OC2_zone,
                                 on_delete=models.PROTECT)
    latitude = models.FloatField(blank=True,
                                 null=True)
    longitude = models.FloatField(blank=True,
                                  null=True)
    class Meta:
        verbose_name = 'connection site'
        db_table = 'physical_connection_site'

    def __str__(self):
        return self.name
