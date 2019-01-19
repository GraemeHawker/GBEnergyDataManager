# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class BMU(models.Model):
    bmu_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

class BM_party(models.Model):
    name = models.CharField(max_length=100)

class FPN(models.Model):
    bmu = models.ForeignKey(BMU)
    SD = models.DateField()
    SP = models.IntegerField()
