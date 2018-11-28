"""
Definitions of expected BMRA message types/fields
for datachecking and type casting

See example_BM_data.txt for description of fields
"""

import datetime as dt

ACCEPTED_MESSAGES = {
    'BM' : {
        'BOALF' : ['NK', 'SO', 'PF', 'TA', 'TS', 'AD', 'VA'],
        'BOD' : ['SD', 'SP', 'NN', 'BP', 'OP', 'TS', 'VB'],
        'FPN' : ['SD', 'SP', 'TS', 'VP'],
        'MEL' : ['SD', 'SP', 'TS', 'VE'],
        'MIL' : ['SD', 'SP', 'TS', 'VF'],
        'QPN' : ['SD', 'SP', 'TS', 'VP'],
        },
    'SYSTEM' : {
        'DISBSAD' : ['SD', 'SP', 'AI', 'SO', 'PF', 'JC', 'JV'],
        'FREQ' : ['TS', 'SF'],
        'FUELHH' : ['SD', 'SP', 'TP', 'FG', 'FT'],
        'FUELINST' : ['SD', 'SP', 'TP', 'TS', 'FG', 'FT'],
        'IMBALNGC' : ['SD', 'SP', 'ZI', 'TP', 'VI'],
        'INDO' : ['SD', 'SP', 'TP', 'VD'],
        'ITSDO' : ['SD', 'SP', 'TP', 'VD'],
        'LOLP' : ['TP', 'SD', 'SP', 'LP', 'DR'],
        'MID' : ['SD', 'SP', 'MI', 'M1', 'M2'],
        'NDF' : ['ZI', 'TP', 'SD', 'SP', 'VD'],
        'NETBSAD' : ['SD', 'SP', 'A7', 'A8', 'A11', 'A3', 'A9', 'A10', 'A12', 'A6'],
        'NONBM' : ['SD', 'SP', 'TP', 'NB'],
        'SOSO' : ['TT', 'ST', 'TD', 'IC', 'TQ', 'PT'],
        'TSDF' : ['ZI', 'TP', 'SD', 'SP', 'VD']
        },
    'DYNAMIC' : {}
}

FIELD_CASTING_FUNCS = {
    'A3' : lambda value: float(value),
    'A6' : lambda value: float(value),
    'A7' : lambda value: float(value),
    'A8' : lambda value: float(value),
    'A9' : lambda value: float(value),
    'A10' : lambda value: float(value),
    'A11' : lambda value: float(value),
    'A12' : lambda value: float(value),
    'AD' : lambda value: True if value == 'T' else False,
    'AI' : lambda value: int(value),
    'BP' : lambda value: float(value),
    'DR' : lambda value: float(value),
    'FG' : lambda value: int(value),
    'FT' : lambda value: value.strip(),
    'IC' : lambda value: value.strip(),
    'JC' : lambda value: float(value),
    'JV' : lambda value: float(value),
    'LP' : lambda value: float(value),
    'MI' : lambda value: value.strip(),
    'M1' : lambda value: float(value),
    'M2' : lambda value: float(value),
    'NB' : lambda value: float(value),
    'NK' : lambda value: int(value),
    'NN' : lambda value: int(value),
    'OP' : lambda value: float(value),
    'PF' : lambda value: True if value == 'T' else False,
    'PT' : lambda value: float(value),
    'SD' : lambda value: dt.datetime(*[int(x) for x in value.split(':')[:3]]),
    'SF' : lambda value: float(value),
    'SO' : lambda value: True if value == 'T' else False,
    'SP' : lambda value: int(value),
    'ST' : lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]]),
    'TA' : lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]]),
    'TD' : lambda value: value.strip(),
    'TP' : lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]]),
    'TQ' : lambda value: float(value),
    'TS' : lambda value: dt.datetime(*[int(x) for x in value.split(':')[:-1]]),
    'TT' : lambda value: value.strip(),
    'VA' : lambda value: float(value),
    'VB' : lambda value: float(value),
    'VD' : lambda value: float(value),
    'VE' : lambda value: float(value),
    'VF' : lambda value: float(value),
    'VI' : lambda value: float(value),
    'VP' : lambda value: float(value),
    'ZI' : lambda value: value.strip()
}
