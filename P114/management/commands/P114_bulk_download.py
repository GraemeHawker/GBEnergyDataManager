# -*- coding: utf-8 -*-
"""
command to download and process BMRA data for specified date rahge
"""
import datetime as dt
from django.core.management.base import BaseCommand, CommandError
from ._download_functions import process_p114_date

class Command(BaseCommand):
    help = 'downloads P114 data for specific date range, expected 2 arguments of form yyyy-m-d'

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Started: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        start_date = dt.datetime(*[int(x) for x in options['date'][0].split('-')[:3]])
        end_date = dt.datetime(*[int(x) for x in options['date'][1].split('-')[:3]])
        date = start_date
        while date <= end_date:
            self.stdout.write('{:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
            self.stdout.write("downloading data for "
                              + '{:%Y-%m-%d}'.format(date))
            process_p114_date(date)
            date += dt.timedelta(days=1)
        self.stdout.write('Finished: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
