"""
list of corrupt messages to be ignored

"""

CORRUPT_MESSAGES = [
    '2006:10:13:15:13:26:GMT: subject=BMRA.BM.T_DIDCB6.BOAL',
    '2022:05:31:19:29:53:GMT: subject=BMRA.BM.E_BURWB-1.MIL', # inconsistent number of point values
    '2022:05:31:19:30:16:GMT: subject=BMRA.BM.E_BURWB-1.MIL', # inconsistent number of point values
    '2022:06:29:22:28:58:GMT: subject=BMRA.BM.E_BURWB-1.MIL', # inconsistent number of point values
]
