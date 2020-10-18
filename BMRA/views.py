# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from BMRA.models import BMU
from Physical.models import PowerStationBMU

# Create your views here.
def list_unused_BMUs(request):
    unused_BMUs = BMU.objects.filter(powerstationbmu__isnull=True).order_by('id')
    return HttpResponse("<br />".join([str(x) for x in unused_BMUs]))
