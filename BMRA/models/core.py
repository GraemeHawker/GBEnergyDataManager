# -*- coding: utf-8 -*-
"""
Core models relating to BMRA data management and physical plant
"""
from __future__ import unicode_literals

from django.db import models
#from P114.models.models import GSP_group
#from Physical.models import StationType


class ProcessedMessage(models.Model):
    """
    Signature of a BMRA message which has already been processed
    """
    timestamp = models.DateTimeField()
    subject = models.CharField(max_length=50)

    class Meta:
        db_table = 'bmra_processedmessage'
        index_together = ('timestamp', 'subject')


class BMU(models.Model):
    """
    Balancing Mechanism Unit
    """
    id = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    gsp_group = models.ForeignKey('P114.GSP_group',
                                  on_delete=models.PROTECT,
                                  blank=True,
                                  null=True)
    type = models.ForeignKey('Physical.StationType',
                             on_delete=models.PROTECT,
                             blank=True,
                             null=True)

    class Meta:
        db_table = 'bmra_bmu'

    def __str__(self):
        return '{} {}'.format(self.id, self.name)


class ZI(models.Model):
    """
    Zone Indicator
    """
    id = models.CharField(max_length=3, primary_key=True)

    class Meta:
        db_table = 'bmra_zi'


class FT(models.Model):
    """
    Fuel type
    """
    id = models.CharField(max_length=10, primary_key=True)

    class Meta:
        db_table = 'bmra_ft'


class LDSO(models.Model):
    """
    Licensed Distribution System Operator
    """
    id = models.CharField(max_length=10, primary_key=True)

    class Meta:
        db_table = 'bmra_ldso'
