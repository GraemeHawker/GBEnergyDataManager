# -*- coding: utf-8 -*-
"""
command to download and process BMRA data for specific date
"""
import datetime as dt
from django.core.management.base import BaseCommand, CommandError
from ._aggregate_functions import get_BMU_timeseries

class Command(BaseCommand):
    help = 'downloads BMRA data for specific date, expected argument yyyy-m-d'

    def add_arguments(self, parser):
        parser.add_argument('bmu')
        parser.add_argument('date', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Started: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        bmu = options['bmu']
        start_date = dt.datetime(*[int(x) for x in options['date'][0].split('-')[:3]])
        end_date = dt.datetime(*[int(x) for x in options['date'][1].split('-')[:3]])
        self.stdout.write('Generating aggregate timeseries for BMU %s' % bmu)
        self.stdout.write('Start date: {:%Y-%m-%d %H:%M:%S}'.format(start_date))
        self.stdout.write('Start date: {:%Y-%m-%d %H:%M:%S}'.format(end_date))
        dataframe = get_BMU_timeseries(bmu, start_date, end_date)
        self.stdout.write(dataframe.to_string())
