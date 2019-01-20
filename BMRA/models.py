# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Processed_Messages(models.Model):
    timestamp = models.DateTimeField()
    subject = models.CharField(max_length=50)

class BMU(models.Model):
    bmu_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

class BM_party(models.Model):
    name = models.CharField(max_length=100)

class BOAL(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    NK = models.IntegerField()
    TA = models.DateTimeField()
    AD = models.BooleanField()

class BOAL_entry(models.Model):
    BOAL = models.ForeignKey(BOAL, on_delete=models.CASCADE)
    TS = models.DateTimeField()
    VA = models.FloatField()

class BOALF(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)

class BOD(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)

class DISPTAV(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)

class EBOCF(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)

class FPN(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField()
    SP = models.IntegerField()
    VP1 = models.FloatField()
    VP2 = models.FloatField()

class MEL(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField()
    SP = models.IntegerField()
    VE1 = models.FloatField()
    VE2 = models.FloatField()

class MIL(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField()
    SP = models.IntegerField()
    VE1 = models.FloatField()
    VE2 = models.FloatField()

class PTAV(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)

class QAS(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)

class QPN(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField()
    SP = models.IntegerField()
    VP1 = models.FloatField()
    VP2 = models.FloatField()
