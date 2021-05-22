from django.core.management.base import BaseCommand
import pandas as pd
from ._bmu_mappings import type_mapping, gsp_mapping
from BMRA.models import BMU
from P114.models import GSP_group
from Physical.models import StationType


class Command(BaseCommand):
    help = 'creates and updates BMU entries based on data in Physical/unit_data spreadsheets'

    def handle(self, *args, **options):
        metadata_path = 'C:/Users/graem/code/GBEnergyDataManager/Physical/unit_data/'
        files = ['Generators.csv', 'GSP units.csv', 'Interconnectors.csv', 'Unknown.csv']
        metadata = pd.DataFrame(columns=['Type', 'BMU', 'Name', 'GSP region'])
        for file in files:
            metadata = metadata.append(pd.read_csv(metadata_path + file))
        known = 0
        unknown = 0

        for i, bmu_data in metadata.iterrows():
            #print(bmu_data)
            station_type = StationType.objects.get(id=type_mapping[bmu_data.Type])
            gsp_group = GSP_group.objects.get(id=gsp_mapping[bmu_data['GSP region']])
            obj, created = BMU.objects.update_or_create(id=bmu_data.BMU,
                                                        defaults={'name': bmu_data.Name,
                                                                  'gsp_group': gsp_group,
                                                                  'type': station_type})
            if created:
                print(obj)