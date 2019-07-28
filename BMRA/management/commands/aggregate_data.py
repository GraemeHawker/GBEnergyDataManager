# -*- coding: utf-8 -*-
"""
command to download and process BMRA data for specific date
"""
import datetime as dt
from django.core.management.base import BaseCommand, CommandError
from ._aggregate_functions import get_BMU_timeseries
from GBEnergyDataManager.utils import get_sp_list

class Command(BaseCommand):
    help = 'downloads BMRA data for specific date, expected argument yyyy-m-d'

    def add_arguments(self, parser):
        parser.add_argument('bmu')
        parser.add_argument('date', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Started: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        bmu = options['bmu']
        start_date = dt.date(*[int(x) for x in options['date'][0].split('-')[:3]])
        end_date = dt.date(*[int(x) for x in options['date'][1].split('-')[:3]])
        self.stdout.write('Generating aggregate timeseries for BMU %s' % bmu)
        self.stdout.write('Start date: {:%Y-%m-%d %H:%M:%S}'.format(start_date))
        self.stdout.write('Start date: {:%Y-%m-%d %H:%M:%S}'.format(end_date))
        sp_list = get_sp_list(start_date, end_date)
        #self.stdout.write(str(sp_list))
        df = get_BMU_timeseries(bmu, start_date, end_date)
        for curr_sd, curr_sp in sp_list:
            self.stdout.write(str(curr_sd)+" "+str(curr_sp))
            fpns = df[(df.SD == curr_sd) & (df.SP == curr_sp)]['VP']
            self.stdout.write(str(fpns))
            #fpn_mwh = fpns[0]
            #self.stdout.write(str(fpn_mwh))

        self.stdout.write(df.to_string())
