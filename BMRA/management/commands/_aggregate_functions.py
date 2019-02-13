"""
helper functions to collate and aggregate raw data

"""
from BMRA.models.core import BMU
from BMRA.models.balancing import FPN, FPNlevel
import pandas as pd

def get_BMU_timeseries(bmu_id, SD_start, SD_end):
    """

    """
    #get raw list of FPN objects
    bmu = BMU.objects.get(id=bmu_id)
    fpns = pd.DataFrame.from_records(FPN.objects.filter(bmu=bmu,
                                                        SD=SD_start).values())

    df_fpn = pd.DataFrame(columns=['SD','SP','TS'])

    fpn_levels = FPNlevel.objects.filter(
        fpn__bmu=bmu,
        fpn__SD=SD_start,
        fpn__SD__lte=SD_end).order_by('TS','fpn__SD','fpn__SP')

    for fpn_level in fpn_levels:
        df_fpn = df_fpn.append([{'TS':fpn_level.TS,
                                 'SD':fpn_level.fpn.SD,
                                 'SP':fpn_level.fpn.SP,
                                 'VP':fpn_level.VP}])


    return df_fpn
