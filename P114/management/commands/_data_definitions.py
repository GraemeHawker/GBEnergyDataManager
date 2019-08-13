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
    'ABP' : ['sp', 'ei', 'metered_vol', 'ie_ind'],
    'ABV' : ['bmu_id', 'sd', 'sr_type', 'run_no', 'agg_date'],
    'AGV' : ['gsp_group', 'sd', 'sr_type', 'run_no', 'agg_date'],
    'AGP' : ['sp', 'ei', 'ii', 'gt_vol'],
    'APB' : [],
    'APC' : [],
    'APD' : [],
    'BO2' : [],
    'BO3' : [],
    'BO4' : [],
    'BO6' : [],
    'BP7' : [],
    'BPH' : [],
    'BPI' : [],
    'DB1' : [],
    'DB2' : [],
    'FP2' : [],
    'GMP' : ['sp', 'ei', 'metered_vol', 'ie_ind'],
    'GP9' : ['gsp_id'],
    'IMP' : ['sp', 'ei', 'metered_vol', 'ie_ind'],
    'IPD' : ['inter_gsp_group'],
    'MD1' : [],
    'MD2' : [],
    'MEL' : [],
    'MIL' : [],
    'MPD' : ['gsp_group', 'sd', 'sr_type', 'run_no', 'agg_date'],
    'MVR' : [],
    'PPC' : [],
    'SP7' : [],
    'SPI' : [],
    'SRH' : ['sd', 'sr_type', 'saa_run_no', 'saa_cdca_run_no', 'svaa_cdca_sd',
             'svaa_cdca_run_no', 'svaa_ssr_run_no', 'bsc_party'],
    'SSD' : [],
    'TRA' : [],

}

#custom functions for converting raw message strings to required datatypes
FIELD_CASTING_FUNCS = {
    'agg_date' : lambda x: dt.date(x[:4], x[4:6], x[6:8]),
    'bmu_id' : lambda x: x.strip(),
    'bsc_party' : lambda x: x.strip(),
    'cdca_sd' : lambda x: dt.date(x[:4], x[4:6], x[6:8]),
    'ei' : lambda x: True if x == 'T' else False,
    'gsp_group' : lambda x: x.strip()[-1],
    'gsp_id' : lambda x: x.strip(),
    'gt_vol' : lambda x: float(x),
    'ie_ind' : lambda x: x.strip(),
    'ii' : lambda x: True if x == 'I' else False,
    'inter_gsp_group' : lambda x: x.strip(),
    'metered_vol' : lambda x: float(x),
    'saa_run_no' : lambda x: int(x),
    'saa_cdca_run_no' : lambda x: int(x),
    'sd' : lambda x: dt.date(x[:4], x[4:6], x[6:8]),
    'sp' : lambda x: int(x),
    'sr_type' : lambda x: x.strip(),
    'svaa_cdca_sd' : lambda x: dt.date(x[:4], x[4:6], x[6:8]),
    'svaa_cdca_run_no' : lambda x: int(x),
    'svaa_ssr_run_no' : lambda x: int(x),
    'run_no' : lambda x: int(x),



}
