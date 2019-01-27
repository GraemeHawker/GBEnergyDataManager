# -*- coding: utf-8 -*-
"""
Core models relating to BMRA data management and physical plant
"""
from __future__ import unicode_literals

from django.db import models

class ProcessedMessage(models.Model):
    """
    Signature of a BMRA message which has already been processed
    """
    timestamp = models.DateTimeField()
    subject = models.CharField(max_length=50)

class BMU(models.Model):
    """
    Balancing Mechanism Unit
    """
    bmu_id = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
