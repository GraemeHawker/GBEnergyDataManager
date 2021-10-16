# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.shortcuts import render
import csv
import requests
from django.core import serializers
from BMRA.models import BMU, FPN, FPNlevel
import pandas as pd
from GBEnergyDataManager.settings import ELEXON_KEY, LIVE_BOA_URL


def test_chart(request):
    return render(request, 'regional_generation_bytype.html')


def d3_test(request):
    return render(request, 'd3_test.html')


def d3_test2(request):
    return render(request, 'd3_test2.html')


def vega_test(request):
    return render(request, 'vega_test.html')


def test_chart_data(request):
    return JsonResponse({
        'title': f'Sales in 2020',
        'data': {
            'labels': ['this', 'that', 'tother'],
            'datasets': [{
                'label': 'Amount ($)',
                'data': [10, 20, 50],
            }]
        },
    })


# Create your views here.
def list_unused_BMUs(request):
    unused_BMUs = BMU.objects.filter(powerstationbmu__isnull=True).order_by('id')
    return HttpResponse("<br />".join([str(x) for x in unused_BMUs]))


def regional_generation_bytype(request):
    """
    generates list of
    """
    fpns = FPNlevel.objects.filter(vp__gte=0,
                                   fpn__sd='2020-01-01',
                                   fpn__sp=1).values('fpn__bmu__type__supertype',
                                                     'fpn__bmu__gsp_group__name').annotate(total=Sum('vp'))
    print(fpns)
    # post_list = serializers.serialize('json', fpns)
    # return HttpResponse(post_list, content_type="text/json-comment-filtered")

    response = HttpResponse(
        content_type='text/csv',
        # headers={'Content-Disposition': 'attachment; filename="regional_generation_bytype.csv"'},
    )

    gsp_group_ordering = ['North Scotland', 'South Scotland', 'Northern', 'North Western', 'Yorkshire',
                          'Merseyside and North Wales', 'South Wales', 'Midlands', 'East Midlands', 'Eastern',
                          'South Western', 'Southern', 'London', 'Southern Eastern']

    writer = csv.writer(response, quoting=csv.QUOTE_NONE)
    writer.writerow(['gsp_group', 'bmu_type', 'total'])
    for x in fpns:
        writer.writerow([x['fpn__bmu__gsp_group__name'],
                         x['fpn__bmu__type__supertype'],
                         x['total']])

    return response


def regional_demand(request):
    """
    generates list of
    """
    fpns = FPNlevel.objects.filter(vp__lt=0,
                                   fpn__sd='2020-01-03',
                                   fpn__sp=1).values('fpn__bmu__type__supertype',
                                                     'fpn__bmu__gsp_group__name').annotate(total=Sum('vp'))
    print(fpns)
    # post_list = serializers.serialize('json', fpns)
    # return HttpResponse(post_list, content_type="text/json-comment-filtered")

    response = HttpResponse(
        content_type='text/csv',
        # headers={'Content-Disposition': 'attachment; filename="regional_generation_bytype.csv"'},
    )

    writer = csv.writer(response, quoting=csv.QUOTE_NONE)
    writer.writerow(['gsp_group', 'bmu_type', 'total'])
    for x in fpns:
        writer.writerow([x['fpn__bmu__gsp_group__name'],
                         x['fpn__bmu__type__supertype'],
                         x['total']])

    return response


def live_boas(request):
    """
    generates list of Bid-Offer Acceptances from live BMRS datafeed
    """
    boa_feed = requests.get(LIVE_BOA_URL.format(ELEXON_KEY))
    current_boas = pd.read_xml(boa_feed.text, xpath=".//item")

    response = HttpResponse(
        content_type='text/csv',
        # headers={'Content-Disposition': 'attachment; filename="regional_generation_bytype.csv"'},
    )
    writer = csv.writer(response, quoting=csv.QUOTE_NONE)
    writer.writerow(['bmu_id', 'bmu_type', 'intensity'])
    for key, current_BOA in current_boas.to_dict(orient='index').items():
        bmu = BMU.objects.get(id=current_BOA['bmuName'])
        writer.writerow([current_BOA['bmuName'],
                         bmu.ft,
                         0])
    return response
