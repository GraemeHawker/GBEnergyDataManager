"""
generator type and gsp group mappings for converting
data in Physical/unit_data to BMU objects

used by ./update_BMUs.py
"""

type_mapping = {
    'CHP' : 'CHP',
    'Battery' : 'BATT',
    'Metalworks' : 'METAL',
    'Wind (Onshore)' : 'WON',
    'CCGT' : 'CCGT',
    'EfW' : 'EFW',
    'Hydro' : 'HYDRO',
    'PV' : 'PV',
    'Biomass' : 'BIO',
    'Transformer' : 'TX',
    'Peaker' : 'PEAK',
    'Demand' : 'DEM',
    'Wind (Offshore)' : 'WOFF',
    'Nuclear' : 'NUC',
    'Rail' : 'RAIL',
    'Flywheel' : 'FLY',
    'Coal' : 'COAL',
    'PS' : 'PS',
    'Virtual parties' : 'VIRT',
    'GSP: East Midlands' : 'GSP',
    'GSP: Eastern' : 'GSP',
    'GSP: London' : 'GSP',
    'GSP: Merseyside and North Wales' : 'GSP',
    'GSP: Midlands' : 'GSP',
    'GSP: North East England' : 'GSP',
    'GSP: North Scotland' : 'GSP',
    'GSP: North West England' : 'GSP',
    'GSP: South East England' : 'GSP',
    'GSP: South Scotland' : 'GSP',
    'GSP: South Wales' : 'GSP',
    'GSP: South West England' : 'GSP',
    'GSP: Southern England' : 'GSP',
    'GSP: Yorkshire' : 'GSP',
    'GSP: North Western' : 'GSP',
    'GSP: South Eastern' : 'GSP',
    'GSP: South Western' : 'GSP',
    'IC: Manx' : 'ICMAN',
    'IC: BritNed (Demand)' : 'ICBN',
    'IC: ElecLink (Demand)' : 'ICEL',
    'IC: East/West (Demand)' : 'ICEW',
    'IC: IFA (Demand)' : 'ICIFA',
    'IC: Moyle (Demand)' : 'ICMOY',
    'IC: Nemo (Demand)' : 'ICNEM',
    'IC: Scottish (Demand)' : 'ICSCO',
    'IC: BritNed (Generation)' : 'ICBN',
    'IC: ElecLink (Generation)' : 'ICEL',
    'IC: East/West (Generation)' : 'ICEW',
    'IC: IFA (Generation)' : 'ICIFA',
    'IC: Moyle (Generation)' : 'ICMOY',
    'IC: Nemo (Generation)' : 'ICNEM',
    'IC: Scottish (Generation)' : 'ICSCO',
    'IC: North Sea Link (Generation)' : 'ICNOR',
    'IC: North Sea Link (Demand)' : 'ICNOR',
    'Unclassified' : 'UNKNO',
    'Unknown' : 'UNKNO'
}

gsp_mapping = {'Merseyside and North Wales' : 'D',
               'North East England' : 'F',
               'South East England' : 'J',
               'South Wales' : 'K',
               'South West England' : 'L',
               'Yorkshire' : 'M',
               'South Scotland' : 'N',
               'North Scotland' : 'P',
               'Eastern' : 'A',
               'Southern England' : 'H',
               'Midlands' : 'E',
               'East Midlands' : 'B',
               'North West England' : 'G',
               'London' : 'C',
               'Unknown' : 'U'
}