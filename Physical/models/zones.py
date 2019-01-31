from django.db import models
from BMRA.models.core import BMU

class OC2Zone(models.Model):
    """
    an OC2 zone
    """
    name = models.CharField(max_length=100)

class TOZone(models.Model):
    """
    a zone relating to a specific Transmission Owner
    """
    name = models.CharField(max_length=100)

class ConnectionSite(models.Model):
    """
    a connection site on the network
    """
    name = models.CharField(max_length=100)
