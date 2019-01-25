# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Processed_Messages(models.Model):
    timestamp = models.DateTimeField()
    subject = models.CharField(max_length=50)

class BMU(models.Model):
    bmu_id = models.CharField(max_length=11)
    name = models.CharField(max_length=100)

class BOAL(models.Model):
    bmu = models.ForeignKey(
        BMU,
        on_delete=models.PROTECT
        )
    NK = models.IntegerField(
        validators=[MinValueValidator(1),
        MaxValueValidator(2147483647)
        )])
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
    SD = models.DateField()
    SP = models.IntegerField()
    NN = models.IntegerField()
    OP = models.FloatField()
    BP = models.FloatField()
    TS1 = models.DateTimeField()
    VB1 = models.FloatField()
    TS2 = models.DateTimeField()
    VB2 = models.FloatField()

class DISPTAV(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField()
    SP = models.IntegerField()
    NN = models.IntegerField()
    OV = models.FloatField()
    BV = models.FloatField()
    P1 = models.FloatField()
    P2 = models.FloatField()
    P3 = models.FloatField()
    P4 = models.FloatField()
    P5 = models.FloatField()
    P6 = models.FloatField()

class EBOCF(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField()
    SP = models.IntegerField()
    NN = models.IntegerField()
    OC = models.FloatField()
    BC = models.FloatField()

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
    SD = models.DateField()
    SP = models.IntegerField()
    NN = models.IntegerField()
    OV = models.FloatField()
    BV = models.FloatField()

class QAS(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField()
    SP = models.IntegerField()
    NN = models.IntegerField()

class QPN(models.Model):
    bmu = models.ForeignKey(BMU, on_delete=models.PROTECT)
    SD = models.DateField()
    SP = models.IntegerField()
    VP1 = models.FloatField()
    VP2 = models.FloatField()
