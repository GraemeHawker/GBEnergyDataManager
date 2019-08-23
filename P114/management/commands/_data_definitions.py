"""
Definitions of expected P114 message types/fields
for datachecking and type casting
"""
import datetime as dt

#feeds to process, used to filter input files
PROCESSED_FEEDS = ['C0301','C0291','C0421']

#feeds to ignore (error raised if file found
#relating to feed not in either of these 2 lists)
IGNORED_FEEDS = ['C0291', 'C0421', 'S0142']

#definitions of accepted message tags, with hierarchical
#dictionary to reflect data structure
ACCEPTED_MESSAGES = {
    'C0291' : ['AGV', 'AGP'],
    'C0301' : ['MPD', 'GP9', 'GMP', 'EPD', 'EMP', 'IPD', 'IMP'],
    'C0421' : ['ABV', 'ABP'],
    'S0142' : [],
}

#message types which are ignored and not further processed
IGNORED_MESSAGES = {
    'C0291' : ['AAA', 'ZZZ'],
    'C0301' : ['AAA', 'ZZZ'],
    'C0421' : ['AAA', 'ZZZ'],
    'S0142' : ['AAA', 'APB', 'APC', 'APD', 'BO2', 'BO3', 'BO4', 'BO6', 'BO7',
               'BP7', 'BPH', 'BPI', 'DB1', 'DB2', 'FP2', 'MD1', 'MD2', 'MEL',
               'MIL', 'MVR', 'PPC', 'SPI', 'SP7', 'SRH', 'SSD', 'TRA', 'ZZZ'],
}

#list of ordered fieldnames for each message type
#(needed as not labelled in raw data)
FIELDNAMES = {
    'ABP' : ['sp', 'ei', 'vol', 'ii'],
    'ABV' : ['bmu_id', 'sd', 'sr_type', 'run_no', 'agg_date'],
    'AGV' : ['gsp_group', 'sd', 'sr_type', 'run_no', 'agg_date'],
    'AGP' : ['sp', 'ei', 'ii', 'vol'],
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
    'EPD' : ['inter_id'],
    'EMP' : ['sp', 'ei', 'vol', 'ii'],
    'FP2' : [],
    'GMP' : ['sp', 'ei', 'vol', 'ii'],
    'GP9' : ['gsp_id'],
    'IMP' : ['sp', 'ei', 'vol', 'ii'],
    'IPD' : ['intergsp_id'],
    'MD1' : [],
    'MD2' : [],
    'MEL' : [],
    'MIL' : [],
    'MPD' : ['gsp_group', 'sd', 'sr_type', 'run_no', 'agg_date'],
    'MVR' : [],
    'PPC' : [],
    'SP7' : [],
    'SPI' : ['sp', 'sbp', 'ssp', 'pdc', 'tot_dem', 'tot_gen', 'tot_bsc_vol',
             'info_imb1', 'info_imb2', 'not_res', 'tot_niv_vol', 'arbitrage',
             'cadl', 'dmat', 'nebpca', 'nebpva', 'nsbpva', 'bppa',
             'nespca', 'nespva', 'nsspva', 'sppa', 'stabv', 'staov',
             'tstabv', 'tstaov', 'tsrabv', 'tsraov', 'tsoabv', 'tsoaov',
             'tsasv', 'tsabv', 'tstasv', 'tstabv', 'tsrasv', 'tsrabv',
             'tsoasv', 'tsoabv', 'rep_price', 'rep_price_vol'],
    'SRH' : ['sd', 'sr_type', 'saa_run_no', 'saa_cdca_run_no', 'svaa_cdca_sd',
             'svaa_cdca_run_no', 'svaa_ssr_run_no', 'bsc_party'],
    'SSD' : [],
    'TRA' : [],

}

#custom functions for converting raw message strings to required datatypes
FIELD_CASTING_FUNCS = {
    'agg_date' : lambda x: dt.date(int(x[:4]), int(x[4:6]), int(x[6:8])),
    'arbitrage' : lambda x: True if x == 'T' else False,
    'bmu_id' : lambda x: x.strip(),
    'bppa' : lambda x: float(x),
    'bsc_party' : lambda x: x.strip(),
    'cdca_sd' : lambda x: dt.date(int(x[:4]), int(x[4:6]), int(x[6:8])),
    'cadl' : lambda x: int(x),
    'dmat' : lambda x: float(x),
    'ei' : lambda x: True if x == 'T' else False,
    'gsp_group' : lambda x: x.strip()[-1],
    'gsp_id' : lambda x: x.strip(),
    'gt_vol' : lambda x: float(x),
    'ie_ind' : lambda x: x.strip(),
    'ii' : lambda x: True if x == 'I' else False,
    'info_imb1' : lambda x: float(x),
    'info_imb2' : lambda x: float(x),
    'inter_id' : lambda x: x.strip(),
    'intergsp_id' : lambda x: x.strip(),
    'nebpca': lambda x: float(x),
    'nebpva': lambda x: float(x),
    'nsbpva': lambda x: float(x),
    'nespca': lambda x: float(x),
    'nespva': lambda x: float(x),
    'nsspva': lambda x: float(x),
    'not_res' : lambda x: float(x),
    'pdc' : lambda x: x.strip(),
    'run_no' : lambda x: int(x),
    'saa_run_no' : lambda x: int(x),
    'saa_cdca_run_no' : lambda x: int(x),
    'sbp' : lambda x: float(x),
    'sd' : lambda x: dt.date(int(x[:4]), int(x[4:6]), int(x[6:8])),
    'sp' : lambda x: int(x),
    'sppa': lambda x: float(x),
    'sr_type' : lambda x: x.strip(),
    'ssp' : lambda x: float(x),
    'stabv': lambda x: float(x),
    'staov': lambda x: float(x),
    'svaa_cdca_sd' : lambda x: dt.date(int(x[:4]), int(x[4:6]), int(x[6:8])),
    'svaa_cdca_run_no' : lambda x: int(x),
    'svaa_ssr_run_no' : lambda x: int(x),
    'tot_bsc_vol' : lambda x: float(x),
    'tot_dem' : lambda x: float(x),
    'tot_gen' : lambda x: float(x),
    'tot_niv_vol' : lambda x: float(x),
    'tsoabv': lambda x: float(x),
    'tsoaov': lambda x: float(x),
    'tsrabv': lambda x: float(x),
    'tsraov': lambda x: float(x),
    'tstabv': lambda x: float(x),
    'tstaov': lambda x: float(x),
    'vol' : lambda x: float(x),
}
