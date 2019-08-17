# -*- coding: utf-8 -*-
"""
command to download and process P114 data for specific date
"""
import datetime as dt
from django.core.management.base import BaseCommand, CommandError
from ._download_functions import process_p114_date

class Command(BaseCommand):
    help = 'downloads P114 data for specific date, expected argument yyyy-m-d'

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Started: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        self.stdout.write("downloading data for %s" % options['date'][0])
        date = dt.datetime(*[int(x) for x in options['date'][0].split('-')[:3]])
        process_p114_date(date)
        self.stdout.write('Finished: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
