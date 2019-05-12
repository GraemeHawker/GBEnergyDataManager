"""
Definitions of expected P114 message types/fields
for datachecking and type casting
"""
import datetime as dt

#definitions of accepted message tags, with hierarchical
#dictionary to reflect data structure
ACCEPTED_MESSAGES = {
    'C0291' : {'AGV' : ['AGP']},
    'C0301' : {'MPD' : None,
               'GP9' : ['GMP'],
               'EPD' : ['EMP'],
               'IPD' : ['IMP']},
    'C0421' : {'ABV' : ['ABP']},
    'S0142' : {},
}

#message types which are ignored and not further processed
IGNORED_MESSAGES = {
    'C0291' : ['AAA', 'ZZZ'],
    'C0301' : ['AAA', 'ZZZ'],
    'C0421' : ['AAA', 'ZZZ'],
    'S0142' : [],
}

#list of ordered fieldnames for each message type
#(needed as not labelled in raw data)
FIELDNAMES = {
    'ABP' : [],
    'ABV' : ['bmu_id', 'sd', 'sr_type', 'run_no', 'agg_date'],
    'AGV' : ['gsp_group', 'sd', 'sr_type', 'run_no', 'agg_date'],
    'AGP' : ['sp', 'ei', 'ii', 'gt_vol'],
}

#custom functions for converting raw message strings to required datatypes
FIELD_CASTING_FUNCS = {
    'agg_date' : lambda x: dt.date(x[:4],x[4:6],x[6:8]),
    'bmu_id' : lambda x: x.strip(),
    'ei' : lambda x: True if x == 'T' else False,
    'gsp_group' : lambda x: x.strip(),
    'gt_vol' : lambda x: float(x),
    'ii' : lambda x: True if x == 'I' else False,
    'sd' : lambda x: dt.date(x[:4],x[4:6],x[6:8]),
    'sp' : lambda x: int(x),
    'sr_type' : lambda x: x.strip(),
    'run_no' : lambda x: int(x),



}
