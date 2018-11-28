"""
Copyright (C) 2018 ElexonDataManager contributors listed in AUTHORS.
Licensed under the Apache 2.0 License (see LICENSE file).

data_processing_test.py
~~~~~~~~
Unit tests for the data processing functions

"""

import unittest
import datetime as dt
from upload_functions import message_to_dict, message_part_to_points

unittest.TestCase.maxDiff = None

class DataProcessingTestCase(unittest.TestCase):
    """
    Tests data processing functions
    """
    def test_data_subset_to_dict_single(self):
        """
        test single datapoint subset to dict conversion
        """
        input_str = 'TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,\
        SP=1,VD=23700.0'
        expected_dict = {1:
                         {'TP' : dt.datetime(2017, 4, 20, 22, 45),
                          'SD' : dt.datetime(2017, 4, 21),
                          'SP' : 1,
                          'VD' : 23700.0}}
        self.assertEqual(message_part_to_points(input_str,
                                                1,
                                                'SYSTEM',
                                                'INDO'),
                         expected_dict)

    def test_data_subset_to_dict_double(self):
        """
        test double datapoint subset to dict conversion
        """
        input_str = 'TS=2017:03:29:01:00:00:GMT,VP=0.0,\
        TS=2017:03:29:01:30:00:GMT,VP=0.0'
        expected_dict = {1:
                         {'TS' : dt.datetime(2017, 3, 29, 1),
                          'VP' : 0.0},
                         2:
                         {'TS' : dt.datetime(2017, 3, 29, 1, 30),
                          'VP' : 0.0}}
        self.assertEqual(message_part_to_points(input_str,
                                                2,
                                                'BM',
                                                'FPN'),
                         expected_dict)

    def test_data_subset_to_dict_multiple(self):
        """
        test multiple datapoint subset to dict conversion
        """
        input_str = 'SD=2017:04:21:00:00:00:GMT,SP=5,LP=0.0,DR=15175.511,\
        SD=2017:04:21:00:00:00:GMT,SP=7,LP=0.0,DR=15777.266,\
        SD=2017:04:21:00:00:00:GMT,SP=11,LP=0.0,DR=14245.876,\
        SD=2017:04:21:00:00:00:GMT,SP=19,LP=0.0,DR=6852.614'
        expected_dict = {1:
                         {'SD' : dt.datetime(2017, 4, 21),
                          'SP' : 5,
                          'LP' : 0.0,
                          'DR' : 15175.511},
                         2:
                         {'SD' : dt.datetime(2017, 4, 21),
                          'SP' : 7,
                          'LP' : 0.0,
                          'DR' : 15777.266},
                         3:
                         {'SD' : dt.datetime(2017, 4, 21),
                          'SP' : 11,
                          'LP' : 0.0,
                          'DR' : 14245.876},
                         4:
                         {'SD' : dt.datetime(2017, 4, 21),
                          'SP' : 19,
                          'LP' : 0.0,
                          'DR' : 6852.614}}
        self.assertEqual(message_part_to_points(input_str,
                                                4,
                                                'SYSTEM',
                                                'LOLP'),
                         expected_dict)

    def test_fpn_to_dict(self):
        """
        test conversion of FPN raw data string to dictionary
        """
        input_str = '2017:03:29:00:02:03:GMT: subject=BMRA.BM.T_ABTH9.FPN, \
            message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,\
            TS=2017:03:29:01:00:00:GMT,VP=0.0,TS=2017:03:29:01:30:00:GMT,VP=0.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 2, 3),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_ABTH9',
                         'message_subtype' : 'FPN',
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 5,
                         'data_points':
                         {1:
                          {'TS' : dt.datetime(2017, 3, 29, 1),
                           'VP' : 0.0},
                          2:
                          {'TS' : dt.datetime(2017, 3, 29, 1, 30),
                           'VP' : 0.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_qpn_to_dict(self):
        """
        test conversion of QPN raw data string to dictionary
        """
        input_str = '2017:03:29:00:02:17:GMT: subject=BMRA.BM.E_ABERDARE.QPN, \
        message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,\
        TS=2017:03:29:01:00:00:GMT,VP=0.0,TS=2017:03:29:01:30:00:GMT,VP=0.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 2, 17),
                         'message_type' : 'BM',
                         'bmu_id' : 'E_ABERDARE',
                         'message_subtype' : 'QPN',
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 5,
                         'data_points':
                         {1:
                          {'TS' : dt.datetime(2017, 3, 29, 1),
                           'VP' : 0.0},
                          2:
                          {'TS' : dt.datetime(2017, 3, 29, 1, 30),
                           'VP' : 0.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_mel_to_dict(self):
        """
        test conversion of MEL raw data string to dictionary
        """
        input_str = '2017:03:29:00:02:16:GMT: subject=BMRA.BM.T_SIZB-2.MEL, \
        message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,\
        TS=2017:03:29:01:00:00:GMT,VE=602.0,TS=2017:03:29:01:30:00:GMT,VE=602.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 2, 16),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_SIZB-2',
                         'message_subtype' : 'MEL',
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 5,
                         'data_points':
                         {1:
                          {'TS' : dt.datetime(2017, 3, 29, 1),
                           'VE' : 602.0},
                          2:
                          {'TS' : dt.datetime(2017, 3, 29, 1, 30),
                           'VE' : 602.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_mil_to_dict(self):
        """
        test conversion of MIL raw data string to dictionary
        """
        input_str = '2017:03:29:00:01:51:GMT: subject=BMRA.BM.T_DRAXX-1.MIL, \
        message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,\
        TS=2017:03:29:01:00:00:GMT,VF=0.0,TS=2017:03:29:01:30:00:GMT,VF=0.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 1, 51),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_DRAXX-1',
                         'message_subtype' : 'MIL',
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 5,
                         'data_points':
                         {1:
                          {'TS' : dt.datetime(2017, 3, 29, 1),
                           'VF' : 0.0},
                          2:
                          {'TS' : dt.datetime(2017, 3, 29, 1, 30),
                           'VF' : 0.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_bod_to_dict(self):
        """
        test conversion of BOD raw data string to dictionary
        """
        input_str = '2017:03:29:00:02:02:GMT: subject=BMRA.BM.T_DRAXX-1.BOD.-4, \
        message={SD=2017:03:29:00:00:00:GMT,SP=5,NN=-4,OP=45.0,\
        BP=-250.0,NP=2,TS=2017:03:29:01:00:00:GMT,VB=-645.0,\
        TS=2017:03:29:01:30:00:GMT,VB=-645.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 2, 2),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_DRAXX-1',
                         'message_subtype' : 'BOD',
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 5,
                         'NN' : -4,
                         'BP' : -250.0,
                         'OP' : 45.0,
                         'data_points':
                         {1:
                          {'TS' : dt.datetime(2017, 3, 29, 1),
                           'VB' : -645.0},
                          2:
                          {'TS' : dt.datetime(2017, 3, 29, 1, 30),
                           'VB' : -645.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_mid_to_dict(self):
        """
        test conversion of MID raw data string to dictionary
        """
        input_str = '2017:03:29:00:00:37:GMT: subject=BMRA.SYSTEM.MID, \
        message={MI=APXMIDP,SD=2017:03:29:00:00:00:GMT,SP=2,M1=34.58,M2=223.7}'

        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 0, 37),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'MID',
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 2,
                         'MI' : 'APXMIDP',
                         'M1' : 34.58,
                         'M2' : 223.7
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_freq_to_dict(self):
        """
        test conversion of FREQ raw data string to dictionary
        """
        input_str = '2017:03:29:00:00:52:GMT: subject=BMRA.SYSTEM.FREQ, \
        message={TS=2017:03:28:23:58:00:GMT,SF=50.058}'

        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 0, 52),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'FREQ',
                         'TS' : dt.datetime(2017, 3, 28, 23, 58, 0),
                         'SF' : 50.058
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_boalf_to_dict(self):
        """
        test conversion of BOALF raw data string to dictionary
        """
        input_str = '2017:04:21:00:00:43:GMT: subject=BMRA.BM.T_SCCL-1.BOALF, \
        message={NK=52908,SO=T,PF=F,TA=2017:04:20:23:59:00:GMT,AD=F,NP=4,\
        TS=2017:04:21:00:05:00:GMT,VA=367.0,TS=2017:04:21:00:09:00:GMT,\
        VA=310.0,TS=2017:04:21:00:35:00:GMT,VA=310.0,\
        TS=2017:04:21:00:39:00:GMT,VA=367.0'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 0, 43),
                         'message_type' : 'BM',
                         'message_subtype' : 'BOALF',
                         'bmu_id' : 'T_SCCL-1',
                         'NK' : 52908,
                         'SO' : True,
                         'PF' : False,
                         'TA' : dt.datetime(2017, 4, 20, 23, 59, 00),
                         'AD' : False,
                         'data_points':
                         {1:
                          {'TS' : dt.datetime(2017, 4, 21, 0, 5, 0),
                           'VA' : 367.0},
                          2:
                          {'TS' : dt.datetime(2017, 4, 21, 0, 9, 0),
                           'VA' : 310.0},
                          3:
                          {'TS' : dt.datetime(2017, 4, 21, 0, 35, 0),
                           'VA' : 310.0},
                          4:
                          {'TS' : dt.datetime(2017, 4, 21, 0, 39, 0),
                           'VA' : 367.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_fuelhh_to_dict(self):
        """
        test conversion of FUELHH raw data string to dictionary
        """
        input_str = '2017:04:21:00:00:58:GMT: subject=BMRA.SYSTEM.FUELHH, \
        message={TP=2017:04:21:00:00:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,\
        FT=CCGT,FG=11427}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 0, 58),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'FUELHH',
                         'TP' : dt.datetime(2017, 4, 21),
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 2,
                         'FT' : 'CCGT',
                         'FG' : 11427
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_disbsad_to_dict(self):
        """
        test conversion of DISBSAD raw data string to dictionary
        """
        input_str = '2017:04:21:00:09:12:GMT: subject=BMRA.SYSTEM.DISBSAD, \
        message={SD=2017:04:21:00:00:00:GMT,SP=5,AI=4,SO=T,PF=F,JC=9360.0,\
        JV=120.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 9, 12),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'DISBSAD',
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 5,
                         'AI' : 4,
                         'SO' : True,
                         'PF' : False,
                         'JC' : 9360.0,
                         'JV' : 120.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_netbsad_to_dict(self):
        """
        test conversion of NETBSAD raw data string to dictionary
        """
        input_str = '2017:04:21:00:09:13:GMT: subject=BMRA.SYSTEM.NETBSAD, \
        message={SD=2017:04:21:00:00:00:GMT,SP=5,A7=0.0,A8=0.0,A11=0.0,\
        A3=0.0,A9=0.0,A10=0.0,A12=0.0,A6=0.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 9, 13),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'NETBSAD',
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 5,
                         'A7' : 0.0,
                         'A8' : 0.0,
                         'A11' : 0.0,
                         'A3' : 0.0,
                         'A9' : 0.0,
                         'A10' : 0.0,
                         'A12' : 0.0,
                         'A6' : 0.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_soso_to_dict(self):
        """
        test conversion of SOSO raw data string to dictionary
        """
        input_str = '2017:04:21:00:10:51:GMT: subject=BMRA.SYSTEM.SOSO, \
        message={TT=EWIC_NG,ST=2017:04:21:02:00:00:GMT,TD=A02,\
        IC=NG_20170421_0200_1,TQ=25.0,PT=39.75}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 10, 51),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'SOSO',
                         'TT' : 'EWIC_NG',
                         'ST' : dt.datetime(2017, 4, 21, 2),
                         'TD' : 'A02',
                         'IC' : 'NG_20170421_0200_1',
                         'TQ' : 25.0,
                         'PT' : 39.75
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_fuelinst_to_dict(self):
        """
        test conversion of FUELINST raw data string to dictionary
        """
        input_str = '2017:03:29:00:01:10:GMT: subject=BMRA.SYSTEM.FUELINST, \
        message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,SP=2,\
        TS=2017:03:28:23:55:00:GMT,FT=CCGT,FG=10374}'

        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 1, 10),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'FUELINST',
                         'TP' : dt.datetime(2017, 3, 29),
                         'SD' : dt.datetime(2017, 3, 29),
                         'TS' : dt.datetime(2017, 3, 28, 23, 55),
                         'SP' : 2,
                         'FT' : 'CCGT',
                         'FG' : 10374
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_indo_to_dict(self):
        """
        test conversion of INDO raw data string to dictionary
        """
        input_str = '2017:03:29:00:01:08:GMT: subject=BMRA.SYSTEM.INDO, \
        message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,\
        SP=2,VD=24016.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 1, 8),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'INDO',
                         'TP' : dt.datetime(2017, 3, 29),
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 2,
                         'VD' : 24016.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_nonbm_to_dict(self):
        """
        test conversion of NONBM raw data string to dictionary
        """
        input_str = '2017:03:29:00:01:24:GMT: subject=BMRA.SYSTEM.NONBM, \
        message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,\
        SP=2,NB=0}'

        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 1, 24),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'NONBM',
                         'TP' : dt.datetime(2017, 3, 29),
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 2,
                         'NB' : 0.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_itsdo_to_dict(self):
        """
        test conversion of ITSDO raw data string to dictionary
        """
        input_str = '2017:03:29:00:01:09:GMT: subject=BMRA.SYSTEM.ITSDO, \
        message={TP=2017:03:29:00:00:00:GMT,SD=2017:03:29:00:00:00:GMT,SP=2,\
        VD=26085.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 1, 9),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'ITSDO',
                         'TP' : dt.datetime(2017, 3, 29),
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 2,
                         'VD' : 26085.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_tsdf_to_dict(self):
        """
        test conversion of TSDF raw data string to dictionary
        """
        input_str = '2017:04:21:00:16:40:GMT: subject=BMRA.SYSTEM.TSDF.B1,\
        message={ZI=B1,NR=58,\
        TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VD=218.0,\
        TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VD=211.0,\
        TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VD=217.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VD=217.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VD=215.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VD=212.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VD=209.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VD=207.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VD=205.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VD=205.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VD=211.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VD=219.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VD=238.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VD=258.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VD=284.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VD=297.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VD=304.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VD=304.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VD=303.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VD=300.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VD=294.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VD=291.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VD=287.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VD=285.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VD=283.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VD=280.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VD=273.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VD=269.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VD=266.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VD=263.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VD=261.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VD=265.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VD=272.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VD=281.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VD=290.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VD=294.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VD=295.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VD=295.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VD=293.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VD=297.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VD=303.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VD=309.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VD=301.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VD=289.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VD=273.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VD=259.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VD=242.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VD=228.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VD=220.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VD=214.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VD=214.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VD=217.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VD=212.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VD=208.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VD=203.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VD=199.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VD=196.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VD=194.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 16, 40),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'TSDF',
                         'ZI' : 'B1',
                         'data_points' : {1: {'TP': dt.datetime(2017, 4, 20, 22, 45), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 1, 'VD': 218.0}, 2: {'TP': dt.datetime(2017, 4, 20, 23, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 2, 'VD': 211.0}, 3: {'TP': dt.datetime(2017, 4, 20, 23, 45), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 3, 'VD': 217.0}, 4: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 4, 'VD': 217.0}, 5: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 5, 'VD': 215.0}, 6: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 6, 'VD': 212.0}, 7: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 7, 'VD': 209.0}, 8: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 8, 'VD': 207.0}, 9: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 9, 'VD': 205.0}, 10: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 10, 'VD': 205.0}, 11: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 11, 'VD': 211.0}, 12: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 12, 'VD': 219.0}, 13: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 13, 'VD': 238.0}, 14: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 14, 'VD': 258.0}, 15: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 15, 'VD': 284.0}, 16: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 16, 'VD': 297.0}, 17: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 17, 'VD': 304.0}, 18: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 18, 'VD': 304.0}, 19: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 19, 'VD': 303.0}, 20: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 20, 'VD': 300.0}, 21: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 21, 'VD': 294.0}, 22: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 22, 'VD': 291.0}, 23: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 23, 'VD': 287.0}, 24: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 24, 'VD': 285.0}, 25: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 25, 'VD': 283.0}, 26: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 26, 'VD': 280.0}, 27: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 27, 'VD': 273.0}, 28: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 28, 'VD': 269.0}, 29: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 29, 'VD': 266.0}, 30: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 30, 'VD': 263.0}, 31: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 31, 'VD': 261.0}, 32: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 32, 'VD': 265.0}, 33: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 33, 'VD': 272.0}, 34: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 34, 'VD': 281.0}, 35: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 35, 'VD': 290.0}, 36: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 36, 'VD': 294.0}, 37: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 37, 'VD': 295.0}, 38: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 38, 'VD': 295.0}, 39: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 39, 'VD': 293.0}, 40: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 40, 'VD': 297.0}, 41: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 41, 'VD': 303.0}, 42: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 42, 'VD': 309.0}, 43: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 43, 'VD': 301.0}, 44: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 44, 'VD': 289.0}, 45: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 45, 'VD': 273.0}, 46: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 46, 'VD': 259.0}, 47: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 47, 'VD': 242.0}, 48: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 48, 'VD': 228.0}, 49: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 1, 'VD': 220.0}, 50: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 2, 'VD': 214.0}, 51: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 3, 'VD': 214.0}, 52: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 4, 'VD': 217.0}, 53: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 5, 'VD': 212.0}, 54: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 6, 'VD': 208.0}, 55: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 7, 'VD': 203.0}, 56: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 8, 'VD': 199.0}, 57: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 9, 'VD': 196.0}, 58: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 10, 'VD': 194.0}}


                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_lolp_to_dict(self):
        """
        test conversion of LOLP raw data string to dictionary
        """
        input_str = '2017:04:21:00:12:37:GMT: subject=BMRA.SYSTEM.LOLP, \
        message={TP=2017:04:21:00:12:31:GMT,NR=4,SD=2017:04:21:00:00:00:GMT,\
        SP=5,LP=0.0,DR=15175.511,SD=2017:04:21:00:00:00:GMT,SP=7,LP=0.0,\
        DR=15777.266,SD=2017:04:21:00:00:00:GMT,SP=11,LP=0.0,DR=14245.876,\
        SD=2017:04:21:00:00:00:GMT,SP=19,LP=0.0,DR=6852.614}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 12, 37),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'LOLP',
                         'TP' : dt.datetime(2017, 4, 21, 0, 12, 31),
                         'data_points':
                         {1:
                          {'SD' : dt.datetime(2017, 4, 21, 0, 0, 0),
                           'SP' : 5,
                           'LP' : 0.0,
                           'DR' : 15175.511},
                          2:
                          {'SD' : dt.datetime(2017, 4, 21, 0, 0, 0),
                           'SP' : 7,
                           'LP' : 0.0,
                           'DR' : 15777.266},
                          3:
                          {'SD' : dt.datetime(2017, 4, 21, 0, 0, 0),
                           'SP' : 11,
                           'LP' : 0.0,
                           'DR' : 14245.876},
                          4:
                          {'SD' : dt.datetime(2017, 4, 21, 0, 0, 0),
                           'SP' : 19,
                           'LP' : 0.0,
                           'DR' : 6852.614}
                         }}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ndf_to_dict(self):
        """
        test conversion of LOLP raw data string to dictionary
        """
        input_str = '2017:04:21:00:16:29:GMT: subject=BMRA.SYSTEM.NDF.N,\
         message={ZI=N,NR=58,\
         TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VD=23700.0,\
         TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VD=22969.0,\
         TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VD=23644.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VD=23600.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VD=23347.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VD=23045.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VD=22730.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VD=22467.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VD=22300.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VD=22299.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VD=22994.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VD=23820.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VD=25906.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VD=28202.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VD=31034.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VD=32506.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VD=33300.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VD=33235.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VD=33200.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VD=32808.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VD=32155.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VD=31800.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VD=31388.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VD=31159.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VD=30972.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VD=30570.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VD=29828.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VD=29440.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VD=29081.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VD=28710.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VD=28500.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VD=28920.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VD=29769.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VD=30771.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VD=31738.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VD=32200.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VD=32327.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VD=32283.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VD=32100.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VD=32452.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VD=33155.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VD=33800.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VD=32987.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VD=31570.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VD=29874.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VD=28257.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VD=26412.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VD=24800.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VD=23900.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VD=23300.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VD=23328.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VD=23600.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VD=23052.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VD=22566.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VD=22072.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VD=21644.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VD=21227.0,\
         TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VD=21000.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 16, 29),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'NDF',
                         'ZI': 'N',
                         'data_points':
                         {1: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 1,
                              'TP': dt.datetime(2017, 4, 20, 22, 45), 'VD': 23700.0},
                          2: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 2,
                              'TP': dt.datetime(2017, 4, 20, 23, 15), 'VD': 22969.0},
                          3: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 3, 'TP': dt.datetime(2017, 4, 20, 23, 45),
'VD': 23644.0}, 4: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 4, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 23600.0}, 5: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 5, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 23347.0}, 6:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 6, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 23045.0}, 7: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 7, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 22730.0}, 8: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 8, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 22467.0}, 9:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 9, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 22300.0}, 10: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 10,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 22299.0}, 11: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 11, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 22994.0}, 12: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 12, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 23820.0}, 13: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 13, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 25906.0}, 14:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 14, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 28202.0}, 15: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 15,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 31034.0}, 16: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 16, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 32506.0}, 17: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 17, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 33300.0}, 18: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 18, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 33235.0}, 19:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 19, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 33200.0}, 20: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 20,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 32808.0}, 21: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 21, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 32155.0}, 22: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 22, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 31800.0}, 23: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 23, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 31388.0}, 24:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 24, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 31159.0}, 25: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 25,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 30972.0}, 26: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 26, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 30570.0}, 27: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 27, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 29828.0}, 28: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 28, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 29440.0}, 29:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 29, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 29081.0}, 30: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 30,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 28710.0}, 31: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 31, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 28500.0}, 32: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 32, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 28920.0}, 33: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 33, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 29769.0}, 34:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 34, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 30771.0}, 35: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 35,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 31738.0}, 36: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 36, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 32200.0}, 37: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 37, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 32327.0}, 38: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 38, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 32283.0}, 39:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 39, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 32100.0}, 40: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 40,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 32452.0}, 41: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 41, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 33155.0}, 42: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 42, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 33800.0}, 43: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 43, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 32987.0}, 44:
{'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 44, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 31570.0}, 45: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 45,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 29874.0}, 46: {'SD':
dt.datetime(2017, 4, 21, 0, 0), 'SP': 46, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 28257.0}, 47: {'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 47, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 26412.0}, 48: {'SD': dt.datetime(2017, 4,
21, 0, 0), 'SP': 48, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 24800.0}, 49:
{'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 1, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 23900.0}, 50: {'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 2,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 23300.0}, 51: {'SD':
dt.datetime(2017, 4, 22, 0, 0), 'SP': 3, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 23328.0}, 52: {'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 4, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 23600.0}, 53: {'SD': dt.datetime(2017, 4,
22, 0, 0), 'SP': 5, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 23052.0}, 54:
{'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 6, 'TP': dt.datetime(2017, 4, 21,
0, 15), 'VD': 22566.0}, 55: {'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 7,
'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 22072.0}, 56: {'SD':
dt.datetime(2017, 4, 22, 0, 0), 'SP': 8, 'TP': dt.datetime(2017, 4, 21, 0, 15),
'VD': 21644.0}, 57: {'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 9, 'TP':
dt.datetime(2017, 4, 21, 0, 15), 'VD': 21227.0}, 58: {'SD': dt.datetime(2017, 4,
22, 0, 0), 'SP': 10, 'TP': dt.datetime(2017, 4, 21, 0, 15), 'VD': 21000.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_imbalngc_to_dict(self):
        """
        test conversion of IMBALNGC raw data string to dictionary
        """
        input_str = '2017:04:21:00:17:42:GMT: subject=BMRA.SYSTEM.IMBALNGC.B1, \
        message={ZI=B1,NR=58,\
        TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VI=636.0,\
        TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VI=660.0,\
        TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VI=634.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VI=634.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VI=652.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VI=672.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VI=685.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VI=692.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VI=695.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VI=687.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VI=664.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VI=639.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VI=629.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VI=646.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VI=676.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VI=659.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VI=646.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VI=648.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VI=659.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VI=692.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VI=698.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VI=698.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VI=680.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VI=704.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VI=689.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VI=719.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VI=742.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VI=758.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VI=758.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VI=764.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VI=790.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VI=795.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VI=809.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VI=819.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VI=805.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VI=778.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VI=749.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VI=715.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VI=678.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VI=627.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VI=562.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VI=499.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VI=467.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VI=436.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VI=345.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VI=321.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VI=315.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VI=313.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VI=304.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VI=299.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VI=288.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VI=267.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VI=265.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VI=260.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VI=254.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VI=251.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VI=248.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VI=240.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 17, 42),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'IMBALNGC',
                         'ZI': 'B1',
                         'data_points': {1: {'TP': dt.datetime(2017, 4, 20, 22, 45), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 1, 'VI': 636.0}, 2: {'TP': dt.datetime(2017, 4, 20, 23, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 2, 'VI': 660.0}, 3: {'TP': dt.datetime(2017, 4, 20, 23, 45), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 3, 'VI': 634.0}, 4: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 4, 'VI': 634.0}, 5: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 5, 'VI': 652.0}, 6: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 6, 'VI': 672.0}, 7: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 7, 'VI': 685.0}, 8: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 8, 'VI': 692.0}, 9: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 9, 'VI': 695.0}, 10: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 10, 'VI': 687.0}, 11: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 11, 'VI': 664.0}, 12: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 12, 'VI': 639.0}, 13: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 13, 'VI': 629.0}, 14: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 14, 'VI': 646.0}, 15: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 15, 'VI': 676.0}, 16: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 16, 'VI': 659.0}, 17: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 17, 'VI': 646.0}, 18: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 18, 'VI': 648.0}, 19: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 19, 'VI': 659.0}, 20: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 20, 'VI': 692.0}, 21: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 21, 'VI': 698.0}, 22: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 22, 'VI': 698.0}, 23: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 23, 'VI': 680.0}, 24: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 24, 'VI': 704.0}, 25: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 25, 'VI': 689.0}, 26: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 26, 'VI': 719.0}, 27: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 27, 'VI': 742.0}, 28: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 28, 'VI': 758.0}, 29: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 29, 'VI': 758.0}, 30: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 30, 'VI': 764.0}, 31: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 31, 'VI': 790.0}, 32: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 32, 'VI': 795.0}, 33: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 33, 'VI': 809.0}, 34: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 34, 'VI': 819.0}, 35: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 35, 'VI': 805.0}, 36: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 36, 'VI': 778.0}, 37: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 37, 'VI': 749.0}, 38: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 38, 'VI': 715.0}, 39: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 39, 'VI': 678.0}, 40: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 40, 'VI': 627.0}, 41: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 41, 'VI': 562.0}, 42: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 42, 'VI': 499.0}, 43: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 43, 'VI': 467.0}, 44: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 44, 'VI': 436.0}, 45: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 45, 'VI': 345.0}, 46: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 46, 'VI': 321.0}, 47: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 47, 'VI': 315.0}, 48: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 21, 0, 0), 'SP': 48, 'VI': 313.0}, 49: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 1, 'VI': 304.0}, 50: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 2, 'VI': 299.0}, 51: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 3, 'VI': 288.0}, 52: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 4, 'VI': 267.0}, 53: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 5, 'VI': 265.0}, 54: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 6, 'VI': 260.0}, 55: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 7, 'VI': 254.0}, 56: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 8, 'VI': 251.0}, 57: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 9, 'VI': 248.0}, 58: {'TP': dt.datetime(2017, 4, 21, 0, 15), 'SD': dt.datetime(2017, 4, 22, 0, 0), 'SP': 10, 'VI': 240.0}}
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

if __name__ == '__main__':
    unittest.main()
