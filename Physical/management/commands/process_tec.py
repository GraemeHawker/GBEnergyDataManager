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
            # if listed owner does not exist, create it
            try:
                owner = PowerStationOwner.objects.get(name=row['Customer Name'])
            except PowerStationOwner.DoesNotExist:
                owner = PowerStationOwner(name=row['Customer Name'])
                owner.save()

            # if listed Connection Site does not exist, create it
            try:
                connection = ConnectionSite.objects.get(name=row['ConnectionSite'])
            except PowerStationOwner.DoesNotExist:
                connection = ConnectionSite(name=row['ConnectionSite'])
                connection.save()

            #if listed TO Zone does not exist, create it
            try:
                to_zone = TOZone.objects.get(name=row['HOST TO'])
            except PowerStationOwner.DoesNotExist:
                to_zone = TOZone(name=row['HOST TO'])
                to_zone.save()

            # if listed plant type does not exist, create it
            try:
                station_type = StationType.objects.get(name=row['Plant Type'])
            except PlantType.DoesNotExist:
                station_type = StationType(name=row['Plant Type'])
                station_type.save()

            # if power station entry does not exist, create it and bind to zone objects
            try:
                power_station = PowerStation.objects.get(name=row['Project Name'])
            except PlantType.DoesNotExist:
                power_station = PowerStation(name = row['Project Name'],
                                             station_type = station_type,
                                             to_zone = to_zone,
                                             OC2_zone = None,
                                             connection_site = connection_site
                                             )
                power_station.save()

            # check if current owner known, if not create new relationship
            # TODO: add date handling
            # TODO: edge case of site being taken back by a previous owner
            try:
                power_station_ownership = PowerStationOwnership.objects.get(power_station = power_station,
                                                                            power_station_owner = owner)
            except PlantType.DoesNotExist:
                power_station_ownership = PowerStationOwnership(power_station = power_station,
                                                                power_station_owner = owner,
                                                                start_date = None,
                                                                )
                power_station_ownership.save()

            # update / create power station status
            try:
                power_station_status = PowerStationStatus.objects.get(power_station = power_station,
                                                                      effective_date = row['MW Effective Date']
                                                                      rating = row['MW Total']
                                                                      project_status = project_status
                                                                      )
            except PowerStationStatus.DoesNotExist:
                power_station_status = PowerStationStatus(power_station = power_station,
                                                          effective_date = row['MW Effective Date']
                                                          rating = row['MW Connected']
                                                          project_status = project_status
                                                          )
                power_station_status.save()
            self.stdout.write(str(row))
