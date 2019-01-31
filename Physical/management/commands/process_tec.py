# -*- coding: utf-8 -*-
"""
command to download and process BMRA data for specific date
"""
from pathlib import Path, PurePath

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from Physical.models.stations import PowerStation, PowerStationOwner

class Command(BaseCommand):
    help = 'processes TEC register file into power station and associated objects'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write('opening file %s' % options['filename'][0])
        path = Path(__file__).parents[2]
        raw_tec_data = pd.read_excel(PurePath(path,
                                              'unit_data/',
                                              options['filename'][0]),
                                     skiprows=[0])
        self.stdout.write(str(raw_tec_data.columns))
        for index, row in raw_tec_data.iterrows():
            try:
                owner = PowerStationOwner.objects.get(name=row['Customer Name'])
            except PowerStationOwner.DoesNotExist:
                owner = PowerStationOwner(name=row['Customer Name'])
                owner.save()
            self.stdout.write(str(row))
