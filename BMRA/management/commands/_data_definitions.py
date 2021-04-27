"""
Definitions of expected BMRA message types/fields
for datachecking and type casting

See example_BM_data.txt for description of fields
"""

import datetime as dt
from django.utils import timezone

# messages which will be processed, all others ignored
PROCESSED_MESSAGES = {
    'BM': ['BOAL', 'BOALF', 'BOAV', 'BOD',
           'DISPTAV', 'EBOCF', 'FPN', 'MEL', 'MIL',
           'PTAV', 'QAS', 'QPN'],
    'BP': [],
    'SYSTEM': ['BSAD', 'DCONTROL', 'DF', 'DISBSAD', 'DISEBSP', 'EBSP', 'FOU2T14D', 'FOU2T52W',
               'FOU2T3YW', 'FREQ', 'FUELHH', 'FUELINST', 'IMBALNGC', 'INDDEM', 'INDGEN', 'INDO',
               'INDOD', 'ISPSTACK', 'ITSDO', 'LOLP', 'MELNGC', 'MID', 'NDF', 'NDFD', 'NDFW',
               'NETBSAD', 'NETEBSP', 'NONBM', 'NOU2T14D', 'NOU2T52W', 'NOU2T3YW', 'OCNMFD',
               'OCNMF3Y', 'OCNMF3Y2', 'OCNMFD2', 'OCNMFW', 'OCNMFW2', 'SOSO', 'SYSMSG', 'SYSWARN',
               'TBOD', 'TEMP', 'TSDF', 'TSDFD', 'TSDFW', 'UOU2T14D', 'UOU2T52W', 'UOU2T3YW', 'WINDFOR'
               ],
    'DYNAMIC': ['MDP', 'MDV', 'MNZT', 'MZT', 'NDZ', 'NTB', 'NTO', 'RDRE', 'RDRI', 'RURE', 'RURI', 'SEL', 'SIL'],
    'INFO': []
}
'''
# messages which will be ignored (not actually used, just for note keeping)
UNPROCESSED_MESSAGES = {
    'BM' : [],
    'BP' : [],
    'SYSTEM' : [],
    'DYNAMIC' : [],
    'INFO' : ['TEST', 'MSG']
}
'''
# accepted message fields by message type and message_subtype
# entries here will be used in validation if being processed
ACCEPTED_MESSAGES = {
    'BM': {
        'BOAL': ['NK', 'TA', 'TS', 'AD', 'VA'],
        'BOALF': ['NK', 'SO', 'PF', 'RN', 'SC', 'TA', 'TS', 'AD', 'VA'],
        'BOAV': ['SD', 'SP', 'NN', 'NK', 'OV', 'BV', 'SA'],
        'BOD': ['SD', 'SP', 'NN', 'BP', 'OP', 'TS', 'VB'],
        'DISPTAV': ['SD', 'SP', 'NN', 'OV', 'BV', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
        'EBOCF': ['SD', 'SP', 'NN', 'BC', 'OC'],
        'FPN': ['SD', 'SP', 'TS', 'VP'],
        'MEL': ['SD', 'SP', 'TS', 'VE'],
        'MIL': ['SD', 'SP', 'TS', 'VF'],
        'PTAV': ['SD', 'SP', 'NN', 'OV', 'BV'],
        'QAS': ['SD', 'SP', 'SV'],
        'QPN': ['SD', 'SP', 'TS', 'VP'],
    },
    'BP': {
        'CDN': ['DL', 'ED', 'EP', 'CD', 'CP', 'CT']
    },
    'SYSTEM': {
        'BSAD': ['SD', 'SP', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6'],
        'DF': ['ZI', 'TP', 'SD', 'SP', 'VD'],
        'DISBSAD': ['SD', 'SP', 'AI', 'SO', 'PF', 'JC', 'JV'],
        'DISEBSP': ['SD', 'SP', 'PB', 'PS', 'PD', 'RSP', 'RP', 'RV', 'BD',
                    'A3', 'A6', 'NI', 'AO', 'AB', 'T1', 'T2', 'PP', 'PC',
                    'J1', 'J2', 'J3', 'J4'],
        'DCONTROL': ['TP', 'DS', 'ID', 'SQ', 'EV', 'TF', 'TI', 'VO', 'SO', 'AM'],
        'EBSP': ['SD', 'SP', 'PB', 'PS', 'AO', 'AB', 'AP', 'AC', 'PP',
                 'PC', 'BD', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6'],
        'FOU2T14D': ['TP', 'SD', 'FT', 'OU'],
        'FOU2T52W': ['TP', 'WN', 'CY', 'FT', 'OU'],
        'FOU2T3YW': ['TP', 'WN', 'CY', 'FT', 'OU'],
        'FREQ': ['TS', 'SF'],
        'FUELHH': ['SD', 'SP', 'TP', 'FG', 'FT'],
        'FUELINST': ['SD', 'SP', 'TP', 'TS', 'FG', 'FT'],
        'IMBALNGC': ['SD', 'SP', 'ZI', 'TP', 'VI'],
        'INDDEM': ['SD', 'SP', 'ZI', 'TP', 'VD'],
        'INDGEN': ['SD', 'SP', 'ZI', 'TP', 'VG'],
        'INDO': ['SD', 'SP', 'TP', 'VD'],
        'INDOD': ['TP', 'SD', 'EO', 'EL', 'EH', 'EN'],
        'ISPSTACK': ['SD', 'SP', 'BO', 'SN', 'CI', 'NK', 'NN', 'CF', 'SO',
                     'PF', 'RI', 'UP', 'RSP', 'IP', 'IV', 'DA', 'AV', 'NV',
                     'PV', 'FP', 'TM', 'TV', 'TC'],
        'ITSDO': ['SD', 'SP', 'TP', 'VD'],
        'LOLP': ['TP', 'SD', 'SP', 'LP', 'DR'],
        'MELNGC': ['SD', 'SP', 'ZI', 'TP', 'VM'],
        'MID': ['SD', 'SP', 'MI', 'M1', 'M2'],
        'NDF': ['ZI', 'TP', 'SD', 'SP', 'VD'],
        'NDFD': ['TP', 'SD', 'SP', 'VD'],
        'NDFW': ['TP', 'WN', 'WD', 'VD'],
        'NETBSAD': ['SD', 'SP', 'A7', 'A8', 'A11', 'A3', 'A9', 'A10', 'A12', 'A6'],
        'NETEBSP': ['SD', 'SP', 'PB', 'PS', 'PD', 'AO', 'AB', 'AC', 'PP', 'PC', 'NI', 'BD',
                    'AP', 'A7', 'A8', 'A11', 'A3', 'A9', 'A10', 'A12', 'A6'],
        'NONBM': ['SD', 'SP', 'TP', 'NB'],
        'NOU2T14D': ['SD', 'TP', 'SP', 'OU'],
        'NOU2T52W': ['TP', 'WN', 'CY', 'OU'],
        'NOU2T3YW': ['TP', 'WN', 'CY', 'OU'],
        'OCNMFD': ['SD', 'TP', 'SP', 'VM'],
        'OCNMFD2': ['SD', 'TP', 'DM'],
        'OCNMF3Y': ['TP', 'WN', 'CY', 'VM'],
        'OCNMFW': ['TP', 'WN', 'WD', 'VM'],
        'OCNMFW2': ['TP', 'WN', 'CY', 'DM'],
        'OCNMF3Y2': ['TP', 'WN', 'CY', 'DM'],
        'SOSO': ['TT', 'ST', 'TD', 'IC', 'TQ', 'PT'],
        'SYSWARN': ['TP', 'SW'],
        'SYSMSG': ['TP', 'MT', 'SM'],
        'TBOD': ['SD', 'SP', 'OT', 'BT'],
        'TEMP': ['TP', 'TS', 'TL', 'TH', 'TN', 'TO'],
        'TSDF': ['ZI', 'TP', 'SD', 'SP', 'VD'],
        'TSDFD': ['TP', 'SD', 'SP', 'VD'],
        'TSDFW': ['TP', 'WN', 'WD', 'VD'],
        'UOU2T14D': ['TP', 'SD', 'FT', 'OU'],
        'UOU2T52W': ['TP', 'WN', 'CY', 'FT', 'OU'],
        'UOU2T3YW': ['TP', 'WN', 'CY', 'FT', 'OU'],
        'WINDFOR': ['SD', 'SP', 'TP', 'VG', 'TR']
    },
    'DYNAMIC': {
        'MDP': ['TE', 'DP'],
        'MDV': ['TE', 'DV'],
        'MNZT': ['TE', 'MN'],
        'MZT': ['TE', 'MZ'],
        'NDZ': ['TE', 'DZ'],
        'NTB': ['TE', 'DB'],
        'NTO': ['TE', 'DO'],
        'RDRE': ['TE', 'R1', 'RB', 'R2', 'RC', 'R3'],
        'RDRI': ['TE', 'R1', 'RB', 'R2', 'RC', 'R3'],
        'RURE': ['TE', 'U1', 'UB', 'U2', 'UC', 'U3'],
        'RURI': ['TE', 'U1', 'UB', 'U2', 'UC', 'U3'],
        'SEL': ['TE', 'SE'],
        'SIL': ['TE', 'SI']
    },
    'INFO': {
        'TEST': ['DATA'],
        'MSG': ['DATA', 'TP', 'IN']
    },
}

# messages (including some weird ones) that have appeared with no useful information
IGNORED_MESSAGES = ['TEST', 'test', 'text', 'Duber']

# custom functions for converting raw message strings to required datatypes
FIELD_CASTING_FUNCS = {
    'A1': lambda value: float(value),
    'A2': lambda value: float(value),
    'A3': lambda value: float(value),
    'A4': lambda value: float(value),
    'A5': lambda value: float(value),
    'A6': lambda value: float(value),
    'A7': lambda value: float(value),
    'A8': lambda value: float(value),
    'A9': lambda value: float(value),
    'A10': lambda value: float(value),
    'A11': lambda value: float(value),
    'A12': lambda value: float(value),
    'AB': lambda value: float(value),
    'AC': lambda value: float(value),
    'AD': lambda value: True if value == 'T' else False,
    'AI': lambda value: int(value),
    'AM': lambda value: value.strip(),
    'AO': lambda value: float(value),
    'AP': lambda value: float(value),
    'AV': lambda value: float(value),
    'BC': lambda value: float(value),
    'BD': lambda value: True if value == 'T' else False,
    'BO': lambda value: value.strip(),
    'BP': lambda value: float(value),
    'BT': lambda value: float(value),
    'BV': lambda value: float(value),
    'CD': lambda value: dt.date(*[int(x) for x in value.split(':')[:3]]),
    'CF': lambda value: True if value == 'T' else False,
    'CI': lambda value: value.strip(),
    'CP': lambda value: int(value),
    'CT': lambda value: value.strip(),
    'CY': lambda value: int(value),
    'DA': lambda value: float(value),
    'DATA': lambda value: value.strip(),
    'DB': lambda value: int(value),
    'DL': lambda value: int(value),
    'DM': lambda value: float(value),
    'DO': lambda value: int(value),
    'DP': lambda value: int(value),
    'DR': lambda value: float(value),
    'DS': lambda value: value.strip(),
    'DV': lambda value: float(value),
    'DZ': lambda value: int(value),
    'ED': lambda value: dt.date(*[int(x) for x in value.split(':')[:3]]),
    'EH': lambda value: int(value),
    'EL': lambda value: int(value),
    'EN': lambda value: int(value),
    'EO': lambda value: int(value),
    'EP': lambda value: int(value),
    'EV': lambda value: value.strip(),
    'FG': lambda value: int(value),
    'FT': lambda value: value.strip(),
    'FP': lambda value: float(value),
    'IC': lambda value: value.strip(),
    'ID': lambda value: int(value),
    'IN': lambda value: value.strip(),
    'IP': lambda value: float(value),
    'IV': lambda value: float(value),
    'J1': lambda value: float(value),
    'J2': lambda value: float(value),
    'J3': lambda value: float(value),
    'J4': lambda value: float(value),
    'JC': lambda value: float(value),
    'JV': lambda value: float(value),
    'LP': lambda value: float(value),
    'MI': lambda value: value.strip(),
    'M1': lambda value: float(value),
    'M2': lambda value: float(value),
    'MN': lambda value: int(value),
    'MT': lambda value: value.strip(),
    'MZ': lambda value: int(value),
    'NB': lambda value: float(value),
    'NI': lambda value: float(value),
    'NK': lambda value: int(value),
    'NN': lambda value: int(value),
    'NV': lambda value: float(value),
    'OC': lambda value: float(value),
    'OP': lambda value: float(value),
    'OT': lambda value: float(value),
    'OU': lambda value: float(value),
    'OV': lambda value: float(value),
    'PB': lambda value: float(value),
    'PC': lambda value: float(value),
    'PD': lambda value: value.strip(),
    'PF': lambda value: True if value == 'T' else False,
    'PP': lambda value: float(value),
    'PS': lambda value: float(value),
    'PT': lambda value: float(value),
    'PV': lambda value: float(value),
    'P1': lambda value: float(value),
    'P2': lambda value: float(value),
    'P3': lambda value: float(value),
    'P4': lambda value: float(value),
    'P5': lambda value: float(value),
    'P6': lambda value: float(value),
    'PC': lambda value: float(value),
    'PP': lambda value: float(value),
    'R1': lambda value: float(value),
    'R2': lambda value: float(value),
    'R3': lambda value: float(value),
    'RB': lambda value: int(value),
    'RC': lambda value: int(value),
    'RI': lambda value: True if value == 'T' else False,
    'RN': lambda value: True if value == 'T' else False,
    'RP': lambda value: float(value),
    'RSP': lambda value: float(value),
    'RV': lambda value: float(value),
    'SA': lambda value: True if value == 'S' else False,
    'SC': lambda value: True if value == 'T' else False,
    'SD': lambda value: dt.date(*[int(x) for x in value.split(':')[:3]]),
    'SE': lambda value: float(value),
    'SF': lambda value: float(value),
    'SI': lambda value: float(value),
    'SM': lambda value: value.strip(),
    'SN': lambda value: int(value),
    'SO': lambda value: True if value == 'T' else False,
    'SP': lambda value: int(value),
    'SQ': lambda value: int(value),
    'ST': lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]], tzinfo=timezone.utc),
    'SV': lambda value: float(value),
    'SW': lambda value: value.strip(),
    'T1': lambda value: float(value),
    'T2': lambda value: float(value),
    'TA': lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]], tzinfo=timezone.utc),
    'TC': lambda value: float(value),
    'TD': lambda value: value.strip(),
    'TE': lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]], tzinfo=timezone.utc),
    'TF': lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]], tzinfo=timezone.utc),
    'TH': lambda value: float(value),
    'TI': lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]], tzinfo=timezone.utc),
    'TL': lambda value: float(value),
    'TM': lambda value: float(value),
    'TN': lambda value: float(value),
    'TO': lambda value: float(value),
    'TP': lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]], tzinfo=timezone.utc),
    'TQ': lambda value: float(value),
    'TR': lambda value: int(value),
    'TS': lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]], tzinfo=timezone.utc),
    'TT': lambda value: value.strip(),
    'TV': lambda value: float(value),
    'U1': lambda value: float(value),
    'U2': lambda value: float(value),
    'U3': lambda value: float(value),
    'UB': lambda value: int(value),
    'UC': lambda value: int(value),
    'UP': lambda value: float(value),
    'VA': lambda value: float(value),
    'VB': lambda value: float(value),
    'VD': lambda value: float(value),
    'VE': lambda value: float(value),
    'VF': lambda value: float(value),
    'VG': lambda value: float(value),
    'VI': lambda value: float(value),
    'VM': lambda value: float(value),
    'VO': lambda value: float(value),
    'VP': lambda value: float(value),
    'WD': lambda value: dt.date(*[int(x) for x in value.split(':')[:3]]),
    'WN': lambda value: int(value),
    'ZI': lambda value: value.strip()
}
