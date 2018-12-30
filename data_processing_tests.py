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

    def test_test_to_dict(self):
        """
        test conversion of TEST raw data string to dictionary
        """
        input_str = '2002:08:14:11:59:48:GMT: subject=BMRA.INFO.TEST, \
        message={DATA=TEST - ignore}'

        expected_dict = {'received_time' : dt.datetime(2002, 8, 14, 11, 59, 48),
                         'message_type' : 'INFO',
                         'message_subtype' : 'TEST',
                         'DATA' : 'TEST - ignore'
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_msg_to_dict(self):
        """
        test conversion of msg raw data string to dictionary
        """
        input_str = '2002:10:08:16:11:05:GMT: subject=BMRA.INFO.MSG, \
        message={DATA=This is a test message}'

        expected_dict = {'received_time' : dt.datetime(2002, 10, 8, 16, 11, 5),
                         'message_type' : 'INFO',
                         'message_subtype' : 'MSG',
                         'DATA' : 'This is a test message'
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_msg_to_dict2(self):
        """
        test conversion of other form of msg raw data string to dictionary
        """
        input_str = '2006:05:16:07:20:01:GMT+00:00: subject=BMRA.INFO.MSG, \
        message={TP=2006:05:16:07:20:00:GMT,IN=The current date and time is Tue May 16 07:20:00 GMT 2006}'

        expected_dict = {'received_time' : dt.datetime(2006, 5, 16, 7, 20, 1),
                         'message_type' : 'INFO',
                         'message_subtype' : 'MSG',
                         'TP' : dt.datetime(2006,5,16,7,20),
                         'IN' : 'The current date and time is Tue May 16 07:20:00 GMT 2006'
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

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
        input_str = '2017:03:29:00:02:16:GMT: subject=BMRA.BM.T_SIZB2.MEL, \
        message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,\
        TS=2017:03:29:01:00:00:GMT,VE=602.0,TS=2017:03:29:01:30:00:GMT,VE=602.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 2, 16),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_SIZB2',
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
        input_str = '2017:03:29:00:01:51:GMT: subject=BMRA.BM.T_DRAXX1.MIL, \
        message={SD=2017:03:29:00:00:00:GMT,SP=5,NP=2,\
        TS=2017:03:29:01:00:00:GMT,VF=0.0,TS=2017:03:29:01:30:00:GMT,VF=0.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 1, 51),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_DRAXX1',
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
        input_str = '2017:03:29:00:02:02:GMT: subject=BMRA.BM.T_DRAXX1.BOD.4, \
        message={SD=2017:03:29:00:00:00:GMT,SP=5,NN=4,OP=45.0,\
        BP=250.0,NP=2,TS=2017:03:29:01:00:00:GMT,VB=645.0,\
        TS=2017:03:29:01:30:00:GMT,VB=645.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 3, 29, 0, 2, 2),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_DRAXX1',
                         'message_subtype' : 'BOD',
                         'SD' : dt.datetime(2017, 3, 29),
                         'SP' : 5,
                         'NN' : 4,
                         'BP' : 250.0,
                         'OP' : 45.0,
                         'data_points':
                         {1:
                          {'TS' : dt.datetime(2017, 3, 29, 1),
                           'VB' : 645.0},
                          2:
                          {'TS' : dt.datetime(2017, 3, 29, 1, 30),
                           'VB' : 645.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ebocf_to_dict(self):
        """
        test conversion of EBOCF raw data string to dictionary
        """
        input_str = '2017:04:21:00:21:54:GMT: subject=BMRA.BM.T_EECL-1.EBOCF.1,\
         message={SD=2017:04:21:00:00:00:GMT,SP=2,NN=1,OC=4.95,BC=0.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 21, 54),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_EECL-1',
                         'message_subtype' : 'EBOCF',
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 2,
                         'NN' : 1,
                         'OC' : 4.95,
                         'BC' : 0.0
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_boav_to_dict(self):
        """
        test conversion of BOAV raw data string to dictionary
        """
        input_str = '2017:04:21:00:21:54:GMT: subject=BMRA.BM.T_EECL-1.BOAV.1, \
        message={SD=2017:04:21:00:00:00:GMT,SP=2,NN=1,NK=88365,OV=0.0833,BV=0.0,SA=L}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 21, 54),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_EECL-1',
                         'message_subtype' : 'BOAV',
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 2,
                         'NN' : 1,
                         'NK' : 88365,
                         'OV' : 0.0833,
                         'BV' : 0.0,
                         'SA' : False
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_disptav_to_dict(self):
        """
        test conversion of DISPTAV raw data string to dictionary
        """
        input_str = '2017:04:21:00:21:54:GMT: subject=BMRA.BM.T_EECL-1.DISPTAV.1, \
        message={SD=2017:04:21:00:00:00:GMT,SP=2,NN=1,OV=0.0833,\
        P1=0.0833,P2=0.0,P3=0.0,BV=0.0,P4=0.0,P5=0.0,P6=0.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 21, 54),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_EECL-1',
                         'message_subtype' : 'DISPTAV',
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 2,
                         'NN' : 1,
                         'OV' : 0.0833,
                         'BV' : 0.0,
                         'P1' : 0.0833,
                         'P2' : 0.0,
                         'P3' : 0.0,
                         'P4' : 0.0,
                         'P5' : 0.0,
                         'P6' : 0.0
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ptav_to_dict(self):
        """
        test conversion of PTAV raw data string to dictionary
        """
        input_str = '2009:01:01:00:20:20:GMT: subject=BMRA.BM.T_DAMC-1.PTAV.-1, \
        message={SD=2008:12:31:00:00:00:GMT,SP=48,NN=-1,OV=1.5833334,BV=-8.333333}'

        expected_dict = {'received_time' : dt.datetime(2009, 1, 1, 0, 20, 20),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_DAMC-1',
                         'message_subtype' : 'PTAV',
                         'SD' : dt.datetime(2008, 12, 31),
                         'SP' : 48,
                         'NN' : -1,
                         'OV' : 1.5833334,
                         'BV' : -8.333333,
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_qas_to_dict(self):
        """
        test conversion of QAS raw data string to dictionary
        """
        input_str = '2017:04:21:07:12:49:GMT: subject=BMRA.BM.T_BAGE-1.QAS, \
        message={SD=2017:04:20:00:00:00:GMT,SP=1,SV=1.621}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 7, 12, 49),
                         'message_type' : 'BM',
                         'bmu_id' : 'T_BAGE-1',
                         'message_subtype' : 'QAS',
                         'SD' : dt.datetime(2017, 4, 20),
                         'SP' : 1,
                         'SV' : 1.621
                         }
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

    def test_tbod_to_dict(self):
        """
        test conversion of MID raw data string to dictionary
        """
        input_str = '2017:04:21:00:21:54:GMT: subject=BMRA.SYSTEM.TBOD, \
        message={SD=2017:04:21:00:00:00:GMT,SP=2,OT=49472.0,BT=-48434.5}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 21, 54),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'TBOD',
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 2,
                         'OT' : 49472.0,
                         'BT' : -48434.5
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_disebsp_to_dict(self):
        """
        test conversion of DISEBSP raw data string to dictionary
        """
        input_str = '2017:04:21:00:21:54:GMT: subject=BMRA.SYSTEM.DISEBSP, \
        message={SD=2017:04:21:00:00:00:GMT,SP=2,PB=29.83277,PS=29.83277,PD=N,\
        BD=F,A3=0.0,A6=0.0,NI=-18.3724,AO=223.2374,AB=-221.4425,T1=223.2374,\
        T2=-203.0701,PP=222.5202,PC=-80.051,J1=-225.0,J2=205.0,J3=-225.0,\
        J4=205.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 21, 54),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'DISEBSP',
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 2,
                         'PB' : 29.83277,
                         'PS' : 29.83277,
                         'PD' : 'N',
                         'BD' : False,
                         'A3' : 0.0,
                         'A6' : 0.0,
                         'NI' : -18.3724,
                         'AO' : 223.2374,
                         'AB' : -221.4425,
                         'T1' : 223.2374,
                         'T2' : -203.0701,
                         'PP' : 222.5202,
                         'PC' : -80.051,
                         'J1' : -225.0,
                         'J2' : 205.0,
                         'J3' : -225.0,
                         'J4' : 205.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_sel_to_dict(self):
        """
        test conversion of SEL raw data string to dictionary
        """
        input_str = '2017:04:21:01:21:21:GMT: subject=BMRA.DYNAMIC.T_ROCK-1.SEL, \
        message={TE=2017:04:21:01:20:00:GMT,SE=240.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 1, 21, 21),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'SEL',
                         'bmu_id' : 'T_ROCK-1',
                         'TE' : dt.datetime(2017, 4, 21, 1, 20),
                         'SE' : 240.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_sil_to_dict(self):
        """
        test conversion of SEL raw data string to dictionary
        """
        input_str = '2018:01:02:11:56:15:GMT: subject=BMRA.DYNAMIC.2__MPGEN002.SIL, \
        message={TE=2018:01:02:11:54:00:GMT,SI=0.0}'

        expected_dict = {'received_time' : dt.datetime(2018, 1, 2, 11, 56, 15),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'SIL',
                         'bmu_id' : '2__MPGEN002',
                         'TE' : dt.datetime(2018, 1, 2, 11, 54),
                         'SI' : 0.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_mnzt_to_dict(self):
        """
        test conversion of MNZT raw data string to dictionary
        """
        input_str = '2017:04:21:01:21:54:GMT: subject=BMRA.DYNAMIC.T_STAY-2.MNZT, \
        message={TE=2017:04:21:01:21:00:GMT,MN=360}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 1, 21, 54),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'MNZT',
                         'bmu_id' : 'T_STAY-2',
                         'TE' : dt.datetime(2017, 4, 21, 1, 21),
                         'MN' : 360
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ndz_to_dict(self):
        """
        test conversion of NDZ raw data string to dictionary
        """
        input_str = '2017:04:21:01:21:55:GMT: subject=BMRA.DYNAMIC.T_STAY-2.NDZ, \
        message={TE=2017:04:21:01:21:00:GMT,DZ=58}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 1, 21, 55),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'NDZ',
                         'bmu_id' : 'T_STAY-2',
                         'TE' : dt.datetime(2017, 4, 21, 1, 21),
                         'DZ' : 58
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_rure_to_dict(self):
        """
        test conversion of RURE raw data string to dictionary
        """
        input_str = '2017:04:21:01:22:19:GMT: subject=BMRA.DYNAMIC.T_STAY-2.RURE, \
        message={TE=2017:04:21:01:21:00:GMT,U1=8.4,UB=45,U2=0.2,UC=48,U3=17.5}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 1, 22, 19),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'RURE',
                         'bmu_id' : 'T_STAY-2',
                         'TE' : dt.datetime(2017, 4, 21, 1, 21),
                         'U1' : 8.4,
                         'UB' : 45,
                         'U2' : 0.2,
                         'UC' : 48,
                         'U3' : 17.5
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ruri_to_dict(self):
        """
        test conversion of RURI raw data string to dictionary
        """
        input_str = '2002:01:02:17:02:01:GMT: subject=BMRA.DYNAMIC.2__JYELG001.RURI, \
        message={TE=2002:01:02:17:00:00:GMT,U1=900.0,UB=0,U2=0.0,UC=0,U3=0.0}'

        expected_dict = {'received_time' : dt.datetime(2002, 1, 2, 17, 2, 1),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'RURI',
                         'bmu_id' : '2__JYELG001',
                         'TE' : dt.datetime(2002, 1, 2, 17),
                         'U1' : 900.0,
                         'UB' : 0,
                         'U2' : 0.0,
                         'UC' : 0,
                         'U3' : 0.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_rdre_to_dict(self):
        """
        test conversion of RDRE raw data string to dictionary
        """
        input_str = '2017:04:21:05:04:39:GMT: subject=BMRA.DYNAMIC.T_ROCK-1.RDRE, \
        message={TE=2017:04:21:05:04:00:GMT,R1=25.0,RB=220,R2=47.5,RC=125,R3=55.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 5, 4, 39),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'RDRE',
                         'bmu_id' : 'T_ROCK-1',
                         'TE' : dt.datetime(2017, 4, 21, 5, 4),
                         'R1' : 25.0,
                         'RB' : 220,
                         'R2' : 47.5,
                         'RC' : 125,
                         'R3' : 55.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_rdri_to_dict(self):
        """
        test conversion of RDRI raw data string to dictionary
        """
        input_str = '2002:01:02:17:01:50:GMT: subject=BMRA.DYNAMIC.2__JYELG001.RDRI, \
        message={TE=2002:01:02:17:00:00:GMT,R1=900.0,RB=0,R2=0.0,RC=0,R3=0.0}'

        expected_dict = {'received_time' : dt.datetime(2002, 1, 2, 17, 1, 50),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'RDRI',
                         'bmu_id' : '2__JYELG001',
                         'TE' : dt.datetime(2002, 1, 2, 17),
                         'R1' : 900.0,
                         'RB' : 0,
                         'R2' : 0.0,
                         'RC' : 0,
                         'R3' : 0.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_mdv_to_dict(self):
        """
        test conversion of MDV raw data string to dictionary
        """
        input_str = '2002:01:02:17:01:13:GMT: subject=BMRA.DYNAMIC.2__JYELG001.MDV, \
        message={TE=2002:01:02:17:00:00:GMT,DV=-44.0}'

        expected_dict = {'received_time' : dt.datetime(2002, 1, 2, 17, 1, 13),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'MDV',
                         'bmu_id' : '2__JYELG001',
                         'TE' : dt.datetime(2002, 1, 2, 17),
                         'DV' : -44.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_mdp_to_dict(self):
        """
        test conversion of MDP raw data string to dictionary
        """
        input_str = '2002:01:02:17:01:14:GMT: subject=BMRA.DYNAMIC.2__JYELG001.MDP, \
        message={TE=2002:01:02:17:00:00:GMT,DP=239}'

        expected_dict = {'received_time' : dt.datetime(2002, 1, 2, 17, 1, 14),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'MDP',
                         'bmu_id' : '2__JYELG001',
                         'TE' : dt.datetime(2002, 1, 2, 17),
                         'DP' : 239
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_mzt_to_dict(self):
        """
        test conversion of MZT raw data string to dictionary
        """
        input_str = '2017:04:21:02:20:27:GMT: subject=BMRA.DYNAMIC.T_FOYE-2.MZT, \
        message={TE=2017:04:21:02:19:00:GMT,MZ=30}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 2, 20, 27),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'MZT',
                         'bmu_id' : 'T_FOYE-2',
                         'TE' : dt.datetime(2017, 4, 21, 2, 19),
                         'MZ' : 30
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ntb_to_dict(self):
        """
        test conversion of NTB raw data string to dictionary
        """
        input_str = '2017:04:21:02:20:44:GMT: subject=BMRA.DYNAMIC.T_FOYE-2.NTB, \
        message={TE=2017:04:21:02:19:00:GMT,DB=2}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 2, 20, 44),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'NTB',
                         'bmu_id' : 'T_FOYE-2',
                         'TE' : dt.datetime(2017, 4, 21, 2, 19),
                         'DB' : 2
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_nto_to_dict(self):
        """
        test conversion of NTO raw data string to dictionary
        """
        input_str = '2017:04:21:02:20:44:GMT: subject=BMRA.DYNAMIC.T_FOYE-2.NTO, \
        message={TE=2017:04:21:02:19:00:GMT,DO=2}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 2, 20, 44),
                         'message_type' : 'DYNAMIC',
                         'message_subtype' : 'NTO',
                         'bmu_id' : 'T_FOYE-2',
                         'TE' : dt.datetime(2017, 4, 21, 2, 19),
                         'DO' : 2
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

    def test_ispstack_to_dict(self):
        """
        test conversion of ISPSTACK raw data string to dictionary
        """
        input_str = '2017:04:21:00:21:54:GMT: subject=BMRA.SYSTEM.ISPSTACK, \
        message={SD=2017:04:21:00:00:00:GMT,SP=2,BO=O,SN=1,CI=T_HUMR-1,\
        NK=112149,NN=1,CF=F,SO=F,PF=F,RI=F,UP=49.49,IP=49.49,IV=12.6424,\
        DA=12.6424,AV=12.6424,NV=0.0,PV=0.0,FP=49.49,TM=1.0,TV=0.0,TC=0.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 21, 54),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'ISPSTACK',
                         'SD' : dt.datetime(2017, 4, 21),
                         'SP' : 2,
                         'BO' : 'O',
                         'SN' : 1,
                         'CI' : 'T_HUMR-1',
                         'NK' : 112149,
                         'NN' : 1,
                         'CF' : False,
                         'SO' : False,
                         'PF' : False,
                         'RI' : False,
                         'UP' : 49.49,
                         'IP' : 49.49,
                         'IV' : 12.6424,
                         'DA' : 12.6424,
                         'AV' : 12.6424,
                         'NV' : 0.0,
                         'PV' : 0.0,
                         'FP' : 49.49,
                         'TM' : 1.0,
                         'TV' : 0.0,
                         'TC' : 0.0
                        }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_boalf_to_dict(self):
        """
        test conversion of BOALF raw data string to dictionary
        """
        input_str = '2017:04:21:00:00:43:GMT: subject=BMRA.BM.T_SCCL1.BOALF, \
        message={NK=52908,SO=T,PF=F,TA=2017:04:20:23:59:00:GMT,AD=F,NP=4,\
        TS=2017:04:21:00:05:00:GMT,VA=367.0,TS=2017:04:21:00:09:00:GMT,\
        VA=310.0,TS=2017:04:21:00:35:00:GMT,VA=310.0,\
        TS=2017:04:21:00:39:00:GMT,VA=367.0'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 0, 43),
                         'message_type' : 'BM',
                         'message_subtype' : 'BOALF',
                         'bmu_id' : 'T_SCCL1',
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

    def test_boal_to_dict(self):
        """
        test conversion of BOAL raw data string to dictionary
        """
        input_str = '2009:01:01:00:09:41:GMT: subject=BMRA.BM.T_SHBA-1.BOAL, \
        message={NK=59073,TA=2009:01:01:00:09:00:GMT,AD=F,NP=4,\
        TS=2009:01:01:00:11:00:GMT,VA=597.0,\
        TS=2009:01:01:00:13:00:GMT,VA=560.0,\
        TS=2009:01:01:00:28:00:GMT,VA=560.0,\
        TS=2009:01:01:00:30:00:GMT,VA=498.0}'

        expected_dict = {'received_time' : dt.datetime(2009, 1, 1, 0, 9, 41),
                         'message_type' : 'BM',
                         'message_subtype' : 'BOAL',
                         'bmu_id' : 'T_SHBA-1',
                         'NK' : 59073,
                         'TA' : dt.datetime(2009, 1, 1, 0, 9),
                         'AD' : False,
                         'data_points':
                         {1:
                          {'TS' : dt.datetime(2009, 1, 1, 0, 11, 0),
                           'VA' : 597.0},
                          2:
                          {'TS' : dt.datetime(2009, 1, 1, 0, 13, 0),
                           'VA' : 560.0},
                          3:
                          {'TS' : dt.datetime(2009, 1, 1, 0, 28, 0),
                           'VA' : 560.0},
                          4:
                          {'TS' : dt.datetime(2009, 1, 1, 0, 30, 0),
                           'VA' : 498.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_corrupt_msg(self):
        """
        test conversion of message listed as corrupted
        """
        input_str = '2006:10:13:15:13:26:GMT: subject=BMRA.BM.T_DIDCB6.BOAL, \
        message={NK=46010,TA=2006:10:13:02:12:00:GMT,AD=F,NP=3,\
        TS=2006:10:13:02:19:00:GMT,VA=480.0,\
        TS=2006:10:13:02:49:00:GMT,VA=480.0,\
        TS=2006:10:13:02:51:00:GMT,VA=450.0,SD=2006:10:13:00:00:00:GMT,SP=29,VD=6621.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=6518.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=6579.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=6602.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=6561.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=6654.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=6727.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=6758.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=6906.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=7109.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=7000.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=6756.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=6563.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=6365.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=6161.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=5901.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=5637.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=5330.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=4899.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=4825.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=4837.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=4713.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=4861.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=4861.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=4762.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=4696.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=4588.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=4518.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=4457.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=4420.0,SD=2006:10:13:00:00:00:GMT,SP=29,VD=9232.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=9080.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=9007.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=9041.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=9145.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=9318.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=9461.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=9507.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=9725.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=10022.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=9863.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=9504.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=9221.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=8930.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=8629.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=8248.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=7860.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=7529.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=7122.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=6739.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=6415.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=6156.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=6157.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=6156.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=6012.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=5914.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=5755.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=5653.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=5564.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=5508.0,SD=2006:10:13:00:00:00:GMT,SP=29,VD=6240.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=6138.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=6088.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=6111.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=6181.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=6299.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=6395.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=6426.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=6573.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=6774.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=6666.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=6424.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=6233.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=6036.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=5833.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=5575.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=5313.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=5142.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=5877.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=5615.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=5416.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=5238.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=5234.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=5245.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=5152.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=5101.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=4990.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=4913.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=4849.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=4807.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VD=20985.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=20641.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=20475.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=20551.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=20788.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=21182.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=21506.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=21610.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=22105.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=22782.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=22419.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=21605.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=20961.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=20298.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=19615.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=18749.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=17867.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=17114.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=16189.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=15319.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=14583.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=13994.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=13995.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=13994.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=13666.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=13443.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=13082.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=12850.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=12647.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=12521.0,SD=2006:10:13:00:00:00:GMT,SP=29,VD=8462.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=8324.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=8257.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=8287.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=8383.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=8542.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=8672.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=8715.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=8914.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=9187.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=9041.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=8712.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=8453.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=8186.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=7976.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=7627.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=7205.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=6901.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=6528.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=6178.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=5881.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=5643.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=5644.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=5643.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=5511.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=5421.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=5275.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=5182.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=5100.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=5049.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VD=43077.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=42377.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=42149.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=42304.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=42675.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=43453.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=44088.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=44301.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=45309.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=46688.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=45948.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=44290.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=42978.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=41629.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=40237.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=38473.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=36678.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=35114.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=34087.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=32498.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=31251.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=30100.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=30247.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=30255.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=29592.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=29153.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=28414.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=27934.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=27516.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=27255.0,SD=2006:10:13:00:00:00:GMT,SP=29,VG=7604.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VG=7411.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VG=7388.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VG=7434.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VG=7460.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VG=7632.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VG=7937.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VG=8046.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VG=8303.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VG=8352.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VG=8250.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VG=8171.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VG=7855.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VG=7438.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VG=7263.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VG=7112.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VG=6740.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VG=6382.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VG=6264.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VG=6165.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VG=5713.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VG=5612.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VG=5555.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VG=5553.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VG=5553.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VG=5554.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VG=5555.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VG=5553.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VG=5553.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VG=5555.0,SD=2006:10:13:00:00:00:GMT,SP=29,VG=16245.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VG=16256.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VG=16311.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VG=16313.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VG=16347.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VG=16411.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VG=16500.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VG=16624.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VG=16839.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VG=16842.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VG=16881.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VG=16699.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VG=16057.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VG=15297.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VG=14712.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VG=14368.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VG=13311.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VG=12259.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VG=11155.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VG=9992.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VG=9698.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VG=9596.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VG=9664.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VG=9626.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VG=9582.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VG=9440.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VG=9346.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VG=9684.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VG=9658.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VG=9601.0,SD=2006:10:13:00:00:00:GMT,SP=29,VG=7267.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VG=7063.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VG=6831.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VG=6831.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VG=6824.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VG=6873.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VG=6875.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VG=6884.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VG=6886.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VG=6881.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VG=6735.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VG=6631.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VG=6570.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VG=6434.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VG=6330.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VG=6293.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VG=6127.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VG=5749.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VG=5001.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VG=4627.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VG=4555.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VG=4555.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VG=4555.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VG=4555.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VG=4555.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VG=4555.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VG=4548.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VG=4517.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VG=4517.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VG=4517.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VG=14862.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VG=14867.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VG=15425.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VG=15426.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VG=15423.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VG=15474.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VG=15757.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VG=15778.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VG=15795.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VG=15797.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VG=16077.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VG=15970.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VG=15745.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VG=15741.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VG=15134.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VG=14628.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VG=14599.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VG=14597.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VG=13356.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VG=12379.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VG=11100.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VG=10743.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VG=10745.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VG=10746.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VG=10762.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VG=10785.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VG=10698.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VG=10177.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VG=10045.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VG=9958.0,SD=2006:10:13:00:00:00:GMT,SP=29,VG=5678.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VG=5682.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VG=6169.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VG=6169.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VG=6166.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VG=6195.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VG=6429.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VG=6425.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VG=6429.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VG=6427.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VG=6089.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VG=6116.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VG=6122.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VG=6122.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VG=5791.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VG=5764.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VG=5767.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VG=5766.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VG=5396.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VG=4639.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VG=3662.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VG=3443.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VG=3444.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VG=3445.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VG=3447.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VG=3449.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VG=3449.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VG=3450.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VG=3450.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VG=3451.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VG=46444.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VG=46061.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VG=46420.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VG=46469.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VG=46519.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VG=46854.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VG=47534.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VG=47797.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VG=48293.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VG=48342.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VG=48413.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VG=47941.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VG=46697.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VG=45380.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VG=43909.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VG=42871.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VG=41247.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VG=39458.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VG=36250.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VG=33637.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VG=31541.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VG=30981.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VG=30994.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VG=30954.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VG=30926.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VG=30809.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VG=30621.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VG=30405.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VG=30248.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VG=30106.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VD=-5270.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=-5168.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=-5273.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=-5310.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=-5308.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=-5380.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=-5387.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=-5415.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=-5510.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=-5653.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=-5638.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=-5585.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=-5380.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=-5234.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=-5042.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=-4836.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=-4664.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=-4424.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=-4056.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=-4083.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=-4142.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=-4052.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=-4211.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=-4147.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=-4057.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=-4025.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=-3970.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=-3985.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=-3921.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=-3895.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VD=-7480.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=-7418.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=-7368.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=-7376.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=-7434.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=-7518.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=-7677.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=-7712.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=-7850.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=-8168.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=-8101.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=-7882.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=-7778.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=-7533.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=-7170.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=-6848.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=-6463.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=-6092.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=-5679.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=-5345.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=-5110.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=-4932.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=-5083.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=-5278.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=-5185.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=-5072.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=-4964.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=-4851.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=-4758.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=-4688.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VD=-5638.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=-5601.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=-5572.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=-5623.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=-5743.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=-5839.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=-5923.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=-5967.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=-6082.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=-6254.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=-6254.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=-6116.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=-5931.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=-5761.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=-5574.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=-5346.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=-5150.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=-5131.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=-5861.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=-5617.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=-5381.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=-5093.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=-5048.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=-5121.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=-5104.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=-5204.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=-5115.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=-5051.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=-4981.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=-4911.0,SP=28,VD=-16735.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VD=-16602.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=-16427.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=-16414.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=-16512.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=-16719.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=-16986.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=-17156.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=-17327.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=-17878.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=-18375.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=-18282.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=-17682.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=-17065.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=-16519.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=-15817.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=-15124.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=-14330.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=-13531.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=-12674.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=-11945.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=-11222.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=-10999.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=-11110.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=-11097.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=-10813.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=-10534.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=-10291.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=-10180.0,SD=2006:10:14:00:00:00:GMT,SP=9,VD=-10018.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=-9953.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VD=-6337.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=-6256.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=-6313.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=-6325.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=-6411.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=-6469.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=-6446.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=-6480.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=-6619.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=-6815.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=-6792.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=-6611.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=-6392.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=-6193.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=-5973.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=-5717.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=-5382.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=-5122.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=-4873.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=-4610.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=-4411.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=-4419.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=-4475.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=-4487.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=-4401.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=-4283.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=-4186.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=-4119.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=9,VD=-4051.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=-4009.0,SP=28,VD=-35333.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=29,VD=-35057.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=30,VD=-34680.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=31,VD=-34693.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=32,VD=-34887.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=33,VD=-35270.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=34,VD=-35788.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=35,VD=-36209.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=36,VD=-36488.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=37,VD=-37386.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=38,VD=-38517.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=39,VD=-38340.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=40,VD=-37331.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=41,VD=-36220.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=42,VD=-35112.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=43,VD=-33669.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=44,VD=-32220.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=45,VD=-30672.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=46,VD=-29244.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=47,VD=-28336.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:13:00:00:00:GMT,SP=48,VD=-27056.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=1,VD=-25921.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=2,VD=-25142.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=3,VD=-25518.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=4,VD=-25710.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=5,VD=-25226.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=6,VD=-24901.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=7,VD=-24407.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=8,VD=-24133.0,SD=2006:10:14:00:00:00:GMT,SP=9,VD=-23744.0,\
        TP=2006:10:13:02:16:00:GMT,SD=2006:10:14:00:00:00:GMT,SP=10,VD=-23512.0}'

        expected_dict = None

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

    def test_bsad_to_dict(self):
        """
        test conversion of BSAD raw data string to dictionary
        """
        input_str = '2003:01:01:00:08:12:GMT: subject=BMRA.SYSTEM.BSAD, \
        message={SD=2003:01:01:00:00:00:GMT,SP=3,A1=-5248.75,A2=-417.5,\
        A3=0.0,A4=0.0,A5=0.0,A6=3.11}'

        expected_dict = {'received_time' : dt.datetime(2003, 1, 1, 0, 8, 12),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'BSAD',
                         'SD' : dt.datetime(2003, 1, 1),
                         'SP' : 3,
                         'A1' : -5248.75,
                         'A2' : -417.5,
                         'A3' : 0.0,
                         'A4' : 0.0,
                         'A5' : 0.0,
                         'A6' : 3.11
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

    def test_netebsp_to_dict(self):
        """
        test conversion of NETEBSP raw data string to dictionary
        """
        input_str = '2009:01:01:00:20:48:GMT: subject=BMRA.SYSTEM.NETEBSP, \
        message={SD=2008:12:31:00:00:00:GMT,SP=48,PB=59.18782,PS=47.9,\
        PD=A,AO=422.9223,AB=-325.8473,AP=0.0,AC=-8.25,PP=96.8589,\
        PC=-0.0,NI=96.8589,BD=F,A7=0.0,A8=0.0,A11=0.0,A3=0.0,A9=0.0,\
        A10=0.0,A12=0.0,A6=0.0}'

        expected_dict = {'received_time' : dt.datetime(2009, 1, 1, 0, 20, 48),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'NETEBSP',
                         'SD' : dt.datetime(2008, 12, 31),
                         'SP' : 48,
                         'PB' : 59.18782,
                         'PS' : 47.9,
                         'PD' : 'A',
                         'AO' : 422.9223,
                         'AB' : -325.8473,
                         'AP' : 0.0,
                         'AC' : -8.25,
                         'PP' : 96.8589,
                         'PC' : -0.0,
                         'NI' : 96.8589,
                         'BD' : False,
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

    def test_ebsp_to_dict(self):
        """
        test conversion of EBSP raw data string to dictionary
        """
        input_str = '2003:01:01:00:20:32:GMT: subject=BMRA.SYSTEM.EBSP, \
        message={SD=2002:12:31:00:00:00:GMT,SP=48,PB=15.13,PS=11.10644,\
        AO=307.2657,AB=-686.525,AP=36.6594,AC=0.0,PP=5.0,PC=-420.9187,\
        BD=F,A1=-5248.75,A2=-417.5,A3=0.0,A4=0.0,A5=0.0,A6=0.0}'

        expected_dict = {'received_time' : dt.datetime(2003, 1, 1, 0, 20, 32),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'EBSP',
                         'SD' : dt.datetime(2002, 12, 31),
                         'SP' : 48,
                         'PB' : 15.13,
                         'PS' : 11.10644,
                         'AO' : 307.2657,
                         'AB' : -686.525,
                         'AP' : 36.6594,
                         'AC' : 0.0,
                         'PP' : 5.0,
                         'PC' : -420.9187,
                         'BD' : False,
                         'A1' : -5248.75,
                         'A2' : -417.5,
                         'A3' : 0.0,
                         'A4' : 0.0,
                         'A5' : 0.0,
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

    def test_dcontrol_to_dict(self):
        """
        test conversion of DCONTROL raw data string to dictionary
        """
        input_str = '2015:11:30:11:35:59:GMT: subject=BMRA.SYSTEM.DCONTROL, \
        message={TP=2015:11:30:11:32:32:GMT,NR=1,DS=ETCL,ID=00002,SQ=1,EV=I,\
        TF=2015:11:30:00:00:00:GMT,TI=2015:12:02:00:00:00:GMT,VO=34.0,SO=T,AM=ORI}'

        expected_dict = {'received_time' : dt.datetime(2015, 11, 30, 11, 35, 59),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'DCONTROL',
                         'TP' : dt.datetime(2015, 11, 30, 11, 32, 32),
                         'data_points' : {
                             1 : {
                                 'DS' : 'ETCL',
                                 'ID' : 2,
                                 'SQ' : 1,
                                 'EV' : 'I',
                                 'TF' : dt.datetime(2015, 11, 30),
                                 'TI' : dt.datetime(2015, 12, 2),
                                 'VO' : 34.0,
                                 'SO' : True,
                                 'AM' : 'ORI'
                                 }
                             }
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
        test conversion of NDF raw data string to dictionary
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

    def test_df_to_dict(self):
        """
        test conversion of DF raw data string to dictionary
        """
        input_str = '2009:01:01:00:16:52:GMT: subject=BMRA.SYSTEM.DF.A, message={ZI=A,NR=58,TP=2008:12:31:23:47:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=1,VD=6177.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=2,VD=6210.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=3,VD=6305.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=4,VD=6318.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=5,VD=6326.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=6,VD=6234.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=7,VD=6007.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=8,VD=5819.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=9,VD=5639.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=10,VD=5520.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=11,VD=5448.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=12,VD=5439.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=13,VD=5310.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=14,VD=5304.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=15,VD=5264.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=16,VD=5132.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=17,VD=4764.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=18,VD=4878.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=19,VD=4974.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=20,VD=5072.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=21,VD=5340.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=22,VD=5643.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=23,VD=5930.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=24,VD=6110.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=25,VD=6366.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=26,VD=6360.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=27,VD=6280.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=28,VD=6243.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=29,VD=6251.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=30,VD=6231.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=31,VD=6216.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=32,VD=6388.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=33,VD=6675.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=34,VD=6971.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=35,VD=7107.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=36,VD=7126.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=37,VD=7043.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=38,VD=6909.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=39,VD=6925.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=40,VD=6800.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=41,VD=6685.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=42,VD=6556.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=43,VD=6410.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=44,VD=6153.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=45,VD=5999.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=46,VD=5765.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=47,VD=5612.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:01:00:00:00:GMT,SP=48,VD=5623.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=1,VD=5767.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=2,VD=5855.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=3,VD=5866.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=4,VD=5678.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=5,VD=5702.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=6,VD=5897.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=7,VD=5916.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=8,VD=5825.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=9,VD=5737.0,TP=2009:01:01:00:16:00:GMT,SD=2009:01:02:00:00:00:GMT,SP=10,VD=5729.0}'

        expected_dict = {'received_time' : dt.datetime(2009, 1, 1, 0, 16, 52),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'DF',
                         'ZI': 'A',
                         'data_points': {
                 1: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 1,
                     'TP': dt.datetime(2008, 12, 31, 23, 47),
                     'VD': 6177.0},
                 2: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 2,
                     'TP': dt.datetime(2009, 1, 1, 0, 16),
                     'VD': 6210.0},
                 3: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 3,
                     'TP': dt.datetime(2009, 1, 1, 0, 16),
                     'VD': 6305.0},
                 4: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 4,
                     'TP': dt.datetime(2009, 1, 1, 0, 16),
                     'VD': 6318.0},
                 5: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 5,
                     'TP': dt.datetime(2009, 1, 1, 0, 16),
                     'VD': 6326.0},
                 6: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 6,
                     'TP': dt.datetime(2009, 1, 1, 0, 16),
                     'VD': 6234.0},
                 7: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 7,
                     'TP': dt.datetime(2009, 1, 1, 0, 16),
                     'VD': 6007.0},
                 8: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 8,
                     'TP': dt.datetime(2009, 1, 1, 0, 16),
                     'VD': 5819.0},
                 9: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                     'SP': 9,
                     'TP': dt.datetime(2009, 1, 1, 0, 16),
                     'VD': 5639.0},
                 10: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 10,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5520.0},
                 11: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 11,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5448.0},
                 12: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 12,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5439.0},
                 13: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 13,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5310.0},
                 14: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 14,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5304.0},
                 15: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 15,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5264.0},
                 16: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 16,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5132.0},
                 17: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 17,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 4764.0},
                 18: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 18,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 4878.0},
                 19: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 19,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 4974.0},
                 20: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 20,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5072.0},
                 21: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 21,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5340.0},
                 22: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 22,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5643.0},
                 23: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 23,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5930.0},
                 24: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 24,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6110.0},
                 25: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 25,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6366.0},
                 26: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 26,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6360.0},
                 27: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 27,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6280.0},
                 28: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 28,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6243.0},
                 29: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 29,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6251.0},
                 30: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 30,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6231.0},
                 31: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 31,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6216.0},
                 32: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 32,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6388.0},
                 33: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 33,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6675.0},
                 34: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 34,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6971.0},
                 35: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 35,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 7107.0},
                 36: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 36,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 7126.0},
                 37: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 37,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 7043.0},
                 38: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 38,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6909.0},
                 39: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 39,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6925.0},
                 40: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 40,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6800.0},
                 41: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 41,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6685.0},
                 42: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 42,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6556.0},
                 43: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 43,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6410.0},
                 44: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 44,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 6153.0},
                 45: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 45,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5999.0},
                 46: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 46,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5765.0},
                 47: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 47,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5612.0},
                 48: {'SD': dt.datetime(2009, 1, 1, 0, 0),
                      'SP': 48,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5623.0},
                 49: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 1,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5767.0},
                 50: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 2,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5855.0},
                 51: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 3,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5866.0},
                 52: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 4,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5678.0},
                 53: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 5,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5702.0},
                 54: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 6,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5897.0},
                 55: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 7,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5916.0},
                 56: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 8,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5825.0},
                 57: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 9,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5737.0},
                 58: {'SD': dt.datetime(2009, 1, 2, 0, 0),
                      'SP': 10,
                      'TP': dt.datetime(2009, 1, 1, 0, 16),
                      'VD': 5729.0}}
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ndfd_to_dict(self):
        """
        test conversion of NDFD raw data string to dictionary
        """
        input_str = '2017:04:21:13:45:37:GMT: subject=BMRA.SYSTEM.NDFD, \
        message={TP=2017:04:21:13:45:00:GMT,NR=13,\
        SD=2017:04:23:00:00:00:GMT,SP=3,VD=30950.0,\
        SD=2017:04:24:00:00:00:GMT,SP=3,VD=34400.0,\
        SD=2017:04:25:00:00:00:GMT,SP=3,VD=34700.0,\
        SD=2017:04:26:00:00:00:GMT,SP=3,VD=35690.0,\
        SD=2017:04:27:00:00:00:GMT,SP=3,VD=35700.0,\
        SD=2017:04:28:00:00:00:GMT,SP=3,VD=35330.0,\
        SD=2017:04:29:00:00:00:GMT,SP=3,VD=30090.0,\
        SD=2017:04:30:00:00:00:GMT,SP=3,VD=29400.0,\
        SD=2017:05:01:00:00:00:GMT,SP=3,VD=31410.0,\
        SD=2017:05:02:00:00:00:GMT,SP=3,VD=33770.0,\
        SD=2017:05:03:00:00:00:GMT,SP=3,VD=33500.0,\
        SD=2017:05:04:00:00:00:GMT,SP=3,VD=32710.0,\
        SD=2017:05:05:00:00:00:GMT,SP=3,VD=32360.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 13, 45, 37),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'NDFD',
                         'TP': dt.datetime(2017,4,21,13,45),
                         'data_points': {
                  1: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 3,
                      'VD': 30950.0},
                  2: {'SD': dt.datetime(2017, 4, 24, 0, 0),
                      'SP': 3,
                      'VD': 34400.0},
                  3: {'SD': dt.datetime(2017, 4, 25, 0, 0),
                      'SP': 3,
                      'VD': 34700.0},
                  4: {'SD': dt.datetime(2017, 4, 26, 0, 0),
                      'SP': 3,
                      'VD': 35690.0},
                  5: {'SD': dt.datetime(2017, 4, 27, 0, 0),
                      'SP': 3,
                      'VD': 35700.0},
                  6: {'SD': dt.datetime(2017, 4, 28, 0, 0),
                      'SP': 3,
                      'VD': 35330.0},
                  7: {'SD': dt.datetime(2017, 4, 29, 0, 0),
                      'SP': 3,
                      'VD': 30090.0},
                  8: {'SD': dt.datetime(2017, 4, 30, 0, 0),
                      'SP': 3,
                      'VD': 29400.0},
                  9: {'SD': dt.datetime(2017, 5, 1, 0, 0),
                      'SP': 3,
                      'VD': 31410.0},
                  10: {'SD': dt.datetime(2017, 5, 2, 0, 0),
                       'SP': 3,
                       'VD': 33770.0},
                  11: {'SD': dt.datetime(2017, 5, 3, 0, 0),
                       'SP': 3,
                       'VD': 33500.0},
                  12: {'SD': dt.datetime(2017, 5, 4, 0, 0),
                       'SP': 3,
                       'VD': 32710.0},
                  13: {'SD': dt.datetime(2017, 5, 5, 0, 0),
                       'SP': 3,
                       'VD': 32360.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_tsdfd_to_dict(self):
        """
        test conversion of TSDFD raw data string to dictionary
        """
        input_str = '2017:04:21:13:45:53:GMT: subject=BMRA.SYSTEM.TSDFD, \
        message={TP=2017:04:21:13:45:00:GMT,NR=13,\
        SD=2017:04:23:00:00:00:GMT,SP=3,VD=31450.0,\
        SD=2017:04:24:00:00:00:GMT,SP=3,VD=34900.0,\
        SD=2017:04:25:00:00:00:GMT,SP=3,VD=35200.0,\
        SD=2017:04:26:00:00:00:GMT,SP=3,VD=36190.0,\
        SD=2017:04:27:00:00:00:GMT,SP=3,VD=36200.0,\
        SD=2017:04:28:00:00:00:GMT,SP=3,VD=35830.0,\
        SD=2017:04:29:00:00:00:GMT,SP=3,VD=30590.0,\
        SD=2017:04:30:00:00:00:GMT,SP=3,VD=29900.0,\
        SD=2017:05:01:00:00:00:GMT,SP=3,VD=31910.0,\
        SD=2017:05:02:00:00:00:GMT,SP=3,VD=34270.0,\
        SD=2017:05:03:00:00:00:GMT,SP=3,VD=34000.0,\
        SD=2017:05:04:00:00:00:GMT,SP=3,VD=33210.0,\
        SD=2017:05:05:00:00:00:GMT,SP=3,VD=32860.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 13, 45, 53),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'TSDFD',
                         'TP': dt.datetime(2017,4,21,13,45),
                         'data_points': {
                 1: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                     'SP': 3,
                     'VD': 31450.0},
                 2: {'SD': dt.datetime(2017, 4, 24, 0, 0),
                     'SP': 3,
                     'VD': 34900.0},
                 3: {'SD': dt.datetime(2017, 4, 25, 0, 0),
                     'SP': 3,
                     'VD': 35200.0},
                 4: {'SD': dt.datetime(2017, 4, 26, 0, 0),
                     'SP': 3,
                     'VD': 36190.0},
                 5: {'SD': dt.datetime(2017, 4, 27, 0, 0),
                     'SP': 3,
                     'VD': 36200.0},
                 6: {'SD': dt.datetime(2017, 4, 28, 0, 0),
                     'SP': 3,
                     'VD': 35830.0},
                 7: {'SD': dt.datetime(2017, 4, 29, 0, 0),
                     'SP': 3,
                     'VD': 30590.0},
                 8: {'SD': dt.datetime(2017, 4, 30, 0, 0),
                     'SP': 3,
                     'VD': 29900.0},
                 9: {'SD': dt.datetime(2017, 5, 1, 0, 0),
                     'SP': 3,
                     'VD': 31910.0},
                 10: {'SD': dt.datetime(2017, 5, 2, 0, 0),
                      'SP': 3,
                      'VD': 34270.0},
                 11: {'SD': dt.datetime(2017, 5, 3, 0, 0),
                      'SP': 3,
                      'VD': 34000.0},
                 12: {'SD': dt.datetime(2017, 5, 4, 0, 0),
                      'SP': 3,
                      'VD': 33210.0},
                 13: {'SD': dt.datetime(2017, 5, 5, 0, 0),
                      'SP': 3,
                      'VD': 32860.0}}
                         }
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

    def test_indgen_to_dict(self):
        """
        test conversion of INDGEN raw data string to dictionary
        """
        input_str = '2017:04:21:00:17:42:GMT: subject=BMRA.SYSTEM.INDGEN.B14, \
        message={ZI=B14,NR=58,\
        TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VG=255.0,\
        TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VG=255.0,\
        TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VG=255.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VG=353.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VG=375.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VG=357.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VG=255.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VG=255.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VG=255.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VG=255.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VG=390.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VG=430.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VG=431.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VG=432.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VG=434.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VG=435.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VG=435.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VG=435.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VG=434.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VG=432.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VG=430.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VG=429.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VG=430.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VG=426.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VG=426.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VG=427.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VG=428.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VG=428.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 17, 42),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'INDGEN',
                         'ZI': 'B14',
                         'data_points': {
                              1: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 1,
                                  'TP': dt.datetime(2017, 4, 20, 22, 45),
                                  'VG': 255.0},
                              2: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 2,
                                  'TP': dt.datetime(2017, 4, 20, 23, 15),
                                  'VG': 255.0},
                              3: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 3,
                                  'TP': dt.datetime(2017, 4, 20, 23, 45),
                                  'VG': 255.0},
                              4: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 4,
                                  'TP': dt.datetime(2017, 4, 21, 0, 15),
                                  'VG': 353.0},
                              5: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 5,
                                  'TP': dt.datetime(2017, 4, 21, 0, 15),
                                  'VG': 375.0},
                              6: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 6,
                                  'TP': dt.datetime(2017, 4, 21, 0, 15),
                                  'VG': 357.0},
                              7: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 7,
                                  'TP': dt.datetime(2017, 4, 21, 0, 15),
                                  'VG': 255.0},
                              8: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 8,
                                  'TP': dt.datetime(2017, 4, 21, 0, 15),
                                  'VG': 255.0},
                              9: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                  'SP': 9,
                                  'TP': dt.datetime(2017, 4, 21, 0, 15),
                                  'VG': 255.0},
                              10: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 10,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 255.0},
                              11: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 11,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 390.0},
                              12: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 12,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              13: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 13,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              14: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 14,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              15: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 15,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 430.0},
                              16: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 16,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              17: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 17,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              18: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 18,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              19: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 19,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              20: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 20,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              21: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 21,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              22: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 22,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              23: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 23,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 431.0},
                              24: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 24,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 432.0},
                              25: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 25,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 434.0},
                              26: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 26,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 435.0},
                              27: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 27,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 435.0},
                              28: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 28,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 435.0},
                              29: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 29,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 434.0},
                              30: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 30,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 432.0},
                              31: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 31,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 430.0},
                              32: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 32,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              33: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 33,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              34: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 34,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              35: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 35,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              36: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 36,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 429.0},
                              37: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 37,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 430.0},
                              38: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 38,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              39: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 39,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              40: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 40,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 426.0},
                              41: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 41,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 426.0},
                              42: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 42,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              43: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 43,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              44: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 44,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              45: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 45,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              46: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 46,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              47: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 47,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              48: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                                   'SP': 48,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              49: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 1,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 427.0},
                              50: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 2,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              51: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 3,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              52: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 4,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              53: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 5,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              54: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 6,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              55: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 7,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              56: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 8,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              57: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 9,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0},
                              58: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                                   'SP': 10,
                                   'TP': dt.datetime(2017, 4, 21, 0, 15),
                                   'VG': 428.0}
                                    }}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_melngc_to_dict(self):
        """
        test conversion of MELNGC raw data string to dictionary
        """
        input_str = '2017:04:21:00:19:12:GMT: subject=BMRA.SYSTEM.MELNGC.B1, \
        message={ZI=B1,NR=58,\
        TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VM=-895.0,\
        TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VM=-910.0,\
        TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VM=-881.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VM=-896.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VM=-908.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VM=-922.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VM=-933.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VM=-941.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VM=-944.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VM=-939.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VM=-923.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VM=-900.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VM=-872.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VM=-841.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VM=-812.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VM=-796.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VM=-781.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VM=-780.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VM=-784.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VM=-793.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VM=-810.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VM=-826.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VM=-848.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VM=-867.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VM=-885.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VM=-904.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VM=-918.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VM=-921.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VM=-921.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VM=-923.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VM=-923.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VM=-915.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VM=-902.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VM=-883.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VM=-866.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VM=-850.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VM=-831.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VM=-809.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VM=-783.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VM=-745.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VM=-707.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VM=-670.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VM=-647.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VM=-632.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VM=-626.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VM=-624.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VM=-623.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VM=-623.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VM=-618.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VM=-617.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VM=-607.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VM=-601.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VM=-599.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VM=-595.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VM=-591.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VM=-589.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VM=-587.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VM=-580.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 19, 12),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'MELNGC',
                         'ZI': 'B1',
                         'data_points': {
                 1: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 1,
                     'TP': dt.datetime(2017, 4, 20, 22, 45),
                     'VM': -895.0},
                 2: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 2,
                     'TP': dt.datetime(2017, 4, 20, 23, 15),
                     'VM': -910.0},
                 3: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 3,
                     'TP': dt.datetime(2017, 4, 20, 23, 45),
                     'VM': -881.0},
                 4: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 4,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VM': -896.0},
                 5: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 5,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VM': -908.0},
                 6: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 6,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VM': -922.0},
                 7: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 7,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VM': -933.0},
                 8: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 8,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VM': -941.0},
                 9: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 9,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VM': -944.0},
                 10: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 10,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -939.0},
                 11: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 11,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -923.0},
                 12: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 12,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -900.0},
                 13: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 13,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -872.0},
                 14: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 14,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -841.0},
                 15: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 15,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -812.0},
                 16: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 16,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -796.0},
                 17: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 17,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -781.0},
                 18: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 18,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -780.0},
                 19: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 19,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -784.0},
                 20: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 20,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -793.0},
                 21: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 21,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -810.0},
                 22: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 22,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -826.0},
                 23: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 23,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -848.0},
                 24: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 24,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -867.0},
                 25: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 25,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -885.0},
                 26: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 26,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -904.0},
                 27: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 27,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -918.0},
                 28: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 28,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -921.0},
                 29: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 29,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -921.0},
                 30: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 30,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -923.0},
                 31: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 31,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -923.0},
                 32: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 32,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -915.0},
                 33: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 33,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -902.0},
                 34: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 34,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -883.0},
                 35: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 35,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -866.0},
                 36: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 36,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -850.0},
                 37: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 37,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -831.0},
                 38: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 38,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -809.0},
                 39: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 39,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -783.0},
                 40: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 40,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -745.0},
                 41: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 41,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -707.0},
                 42: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 42,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -670.0},
                 43: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 43,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -647.0},
                 44: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 44,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -632.0},
                 45: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 45,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -626.0},
                 46: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 46,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -624.0},
                 47: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 47,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -623.0},
                 48: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 48,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -623.0},
                 49: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 1,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -618.0},
                 50: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 2,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -617.0},
                 51: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 3,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -607.0},
                 52: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 4,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -601.0},
                 53: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 5,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -599.0},
                 54: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 6,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -595.0},
                 55: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 7,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -591.0},
                 56: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 8,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -589.0},
                 57: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 9,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VM': -587.0},
                 58: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 10,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                       'VM': -580.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_inddem_to_dict(self):
        """
        test conversion of INDDEM raw data string to dictionary
        """
        input_str = '2017:04:21:00:20:44:GMT: subject=BMRA.SYSTEM.INDDEM.B1, \
        message={ZI=B1,NR=58,\
        TP=2017:04:20:22:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VD=-99.0,\
        TP=2017:04:20:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=2,VD=-98.0,\
        TP=2017:04:20:23:45:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VD=-100.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=4,VD=-100.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VD=-98.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=6,VD=-101.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VD=-105.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=8,VD=-103.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VD=-94.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=10,VD=-93.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VD=-94.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=12,VD=-97.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VD=-101.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=14,VD=-109.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VD=-121.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=16,VD=-131.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VD=-144.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=18,VD=-149.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VD=-150.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=20,VD=-149.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VD=-150.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=22,VD=-150.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VD=-151.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=24,VD=-152.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VD=-151.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=26,VD=-147.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VD=-145.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=28,VD=-140.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VD=-133.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=30,VD=-131.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VD=-131.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=32,VD=-128.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VD=-129.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=34,VD=-132.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VD=-135.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=36,VD=-130.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VD=-127.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=38,VD=-125.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VD=-125.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=40,VD=-125.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VD=-134.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=42,VD=-131.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VD=-129.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=44,VD=-121.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VD=-120.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=46,VD=-115.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VD=-110.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=48,VD=-107.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VD=-99.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=2,VD=-99.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VD=-100.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=4,VD=-101.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VD=-98.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=6,VD=-99.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VD=-104.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=8,VD=-101.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VD=-94.0,\
        TP=2017:04:21:00:15:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=10,VD=-92.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 0, 20, 44),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'INDDEM',
                         'ZI': 'B1',
                         'data_points': {1: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 1,
                     'TP': dt.datetime(2017, 4, 20, 22, 45),
                     'VD': -99.0},
                 2: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 2,
                     'TP': dt.datetime(2017, 4, 20, 23, 15),
                     'VD': -98.0},
                 3: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 3,
                     'TP': dt.datetime(2017, 4, 20, 23, 45),
                     'VD': -100.0},
                 4: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 4,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VD': -100.0},
                 5: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 5,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VD': -98.0},
                 6: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 6,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VD': -101.0},
                 7: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 7,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VD': -105.0},
                 8: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 8,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VD': -103.0},
                 9: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 9,
                     'TP': dt.datetime(2017, 4, 21, 0, 15),
                     'VD': -94.0},
                 10: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 10,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -93.0},
                 11: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 11,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -94.0},
                 12: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 12,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -97.0},
                 13: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 13,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -101.0},
                 14: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 14,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -109.0},
                 15: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 15,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -121.0},
                 16: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 16,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -131.0},
                 17: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 17,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -144.0},
                 18: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 18,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -149.0},
                 19: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 19,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -150.0},
                 20: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 20,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -149.0},
                 21: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 21,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -150.0},
                 22: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 22,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -150.0},
                 23: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 23,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -151.0},
                 24: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 24,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -152.0},
                 25: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 25,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -151.0},
                 26: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 26,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -147.0},
                 27: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 27,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -145.0},
                 28: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 28,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -140.0},
                 29: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 29,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -133.0},
                 30: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 30,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -131.0},
                 31: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 31,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -131.0},
                 32: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 32,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -128.0},
                 33: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 33,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -129.0},
                 34: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 34,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -132.0},
                 35: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 35,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -135.0},
                 36: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 36,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -130.0},
                 37: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 37,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -127.0},
                 38: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 38,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -125.0},
                 39: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 39,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -125.0},
                 40: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 40,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -125.0},
                 41: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 41,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -134.0},
                 42: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 42,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -131.0},
                 43: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 43,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -129.0},
                 44: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 44,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -121.0},
                 45: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 45,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -120.0},
                 46: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 46,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -115.0},
                 47: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 47,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -110.0},
                 48: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 48,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -107.0},
                 49: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 1,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -99.0},
                 50: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 2,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -99.0},
                 51: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 3,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -100.0},
                 52: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 4,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -101.0},
                 53: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 5,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -98.0},
                 54: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 6,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -99.0},
                 55: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 7,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -104.0},
                 56: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 8,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -101.0},
                 57: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 9,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -94.0},
                 58: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 10,
                      'TP': dt.datetime(2017, 4, 21, 0, 15),
                      'VD': -92.0}
                         }}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_windfor_to_dict(self):
        """
        test conversion of WINDFOR raw data string to dictionary
        """
        input_str = '2017:04:21:04:31:00:GMT: subject=BMRA.SYSTEM.WINDFOR, message={NR=70,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=1,VG=2781.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=3,VG=2937.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=5,VG=3169.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=7,VG=3433.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=9,VG=3662.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=11,VG=3854.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=13,VG=4045.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=15,VG=4148.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=17,VG=4260.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=19,VG=4334.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=21,VG=4408.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=23,VG=4448.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=25,VG=4505.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=27,VG=4266.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=29,VG=4278.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=31,VG=4224.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=33,VG=4503.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=35,VG=4295.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=37,VG=3983.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=39,VG=3598.0,TR=9910,\
        TP=2017:04:20:22:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=41,VG=3191.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=43,VG=2773.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=45,VG=2498.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:21:00:00:00:GMT,SP=47,VG=2368.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=1,VG=2296.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=3,VG=2204.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=5,VG=2149.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=7,VG=2108.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=9,VG=2012.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=11,VG=1868.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=13,VG=1708.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=15,VG=1534.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=17,VG=1426.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=19,VG=1412.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=21,VG=1404.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=23,VG=1495.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=25,VG=1554.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=27,VG=1615.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=29,VG=1765.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=31,VG=1895.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=33,VG=2001.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=35,VG=2104.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=37,VG=2044.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=39,VG=2004.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=41,VG=1707.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=43,VG=1466.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=45,VG=1272.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:22:00:00:00:GMT,SP=47,VG=1060.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=1,VG=902.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=3,VG=779.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=5,VG=756.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=7,VG=745.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=9,VG=748.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=11,VG=777.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=13,VG=808.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=15,VG=840.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=17,VG=903.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=19,VG=984.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=21,VG=1107.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=23,VG=1252.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=25,VG=1431.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=27,VG=1640.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=29,VG=1861.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=31,VG=2097.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=33,VG=2343.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=35,VG=2466.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=37,VG=2597.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=39,VG=2740.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=41,VG=2896.0,TR=9910,\
        TP=2017:04:21:04:30:00:GMT,SD=2017:04:23:00:00:00:GMT,SP=43,VG=3087.0,TR=9910}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 4, 31),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'WINDFOR',
                         'data_points': {
                 1: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 1,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 2781.0},
                 2: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 3,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 2937.0},
                 3: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 5,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 3169.0},
                 4: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 7,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 3433.0},
                 5: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 9,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 3662.0},
                 6: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 11,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 3854.0},
                 7: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 13,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 4045.0},
                 8: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 15,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 4148.0},
                 9: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                     'SP': 17,
                     'TP': dt.datetime(2017, 4, 20, 22, 30),
                     'TR': 9910,
                     'VG': 4260.0},
                 10: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 19,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4334.0},
                 11: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 21,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4408.0},
                 12: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 23,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4448.0},
                 13: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 25,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4505.0},
                 14: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 27,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4266.0},
                 15: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 29,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4278.0},
                 16: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 31,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4224.0},
                 17: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 33,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4503.0},
                 18: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 35,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 4295.0},
                 19: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 37,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 3983.0},
                 20: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 39,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 3598.0},
                 21: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 41,
                      'TP': dt.datetime(2017, 4, 20, 22, 30),
                      'TR': 9910,
                      'VG': 3191.0},
                 22: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 43,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2773.0},
                 23: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 45,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2498.0},
                 24: {'SD': dt.datetime(2017, 4, 21, 0, 0),
                      'SP': 47,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2368.0},
                 25: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 1,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2296.0},
                 26: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 3,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2204.0},
                 27: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 5,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2149.0},
                 28: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 7,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2108.0},
                 29: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 9,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2012.0},
                 30: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 11,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1868.0},
                 31: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 13,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1708.0},
                 32: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 15,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1534.0},
                 33: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 17,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1426.0},
                 34: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 19,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1412.0},
                 35: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 21,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1404.0},
                 36: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 23,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1495.0},
                 37: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 25,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1554.0},
                 38: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 27,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1615.0},
                 39: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 29,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1765.0},
                 40: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 31,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1895.0},
                 41: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 33,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2001.0},
                 42: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 35,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2104.0},
                 43: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 37,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2044.0},
                 44: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 39,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2004.0},
                 45: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 41,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1707.0},
                 46: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 43,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1466.0},
                 47: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 45,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1272.0},
                 48: {'SD': dt.datetime(2017, 4, 22, 0, 0),
                      'SP': 47,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1060.0},
                 49: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 1,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 902.0},
                 50: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 3,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 779.0},
                 51: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 5,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 756.0},
                 52: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 7,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 745.0},
                 53: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 9,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 748.0},
                 54: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 11,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 777.0},
                 55: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 13,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 808.0},
                 56: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 15,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 840.0},
                 57: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 17,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 903.0},
                 58: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 19,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 984.0},
                 59: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 21,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1107.0},
                 60: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 23,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1252.0},
                 61: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 25,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1431.0},
                 62: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 27,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1640.0},
                 63: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 29,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 1861.0},
                 64: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 31,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2097.0},
                 65: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 33,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2343.0},
                 66: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 35,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2466.0},
                 67: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 37,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2597.0},
                 68: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 39,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2740.0},
                 69: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 41,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 2896.0},
                 70: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                      'SP': 43,
                      'TP': dt.datetime(2017, 4, 21, 4, 30),
                      'TR': 9910,
                      'VG': 3087.0}
                      }}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ocnmfd_to_dict(self):
        """
        test conversion of OCNMFD raw data string to dictionary
        """
        input_str = '2017:04:21:12:38:37:GMT: subject=BMRA.SYSTEM.OCNMFD, \
        message={TP=2017:04:21:12:37:00:GMT,NR=13,\
        SD=2017:04:23:00:00:00:GMT,SP=3,VM=10910.0,\
        SD=2017:04:24:00:00:00:GMT,SP=3,VM=11422.0,\
        SD=2017:04:25:00:00:00:GMT,SP=3,VM=10520.0,\
        SD=2017:04:26:00:00:00:GMT,SP=3,VM=7643.0,\
        SD=2017:04:27:00:00:00:GMT,SP=3,VM=7239.0,\
        SD=2017:04:28:00:00:00:GMT,SP=3,VM=6933.0,\
        SD=2017:04:29:00:00:00:GMT,SP=3,VM=10730.0,\
        SD=2017:04:30:00:00:00:GMT,SP=3,VM=11714.0,\
        SD=2017:05:01:00:00:00:GMT,SP=3,VM=11903.0,\
        SD=2017:05:02:00:00:00:GMT,SP=3,VM=9834.0,\
        SD=2017:05:03:00:00:00:GMT,SP=3,VM=10329.0,\
        SD=2017:05:04:00:00:00:GMT,SP=3,VM=10910.0,\
        SD=2017:05:05:00:00:00:GMT,SP=3,VM=11699.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 12, 38, 37),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'OCNMFD',
                         'TP' : dt.datetime(2017, 4, 21, 12, 37),
                         'data_points': {
                 1: {'SD': dt.datetime(2017, 4, 23, 0, 0),
                     'SP': 3,
                     'VM': 10910.0},
                 2: {'SD': dt.datetime(2017, 4, 24, 0, 0),
                     'SP': 3,
                     'VM': 11422.0},
                 3: {'SD': dt.datetime(2017, 4, 25, 0, 0),
                     'SP': 3,
                     'VM': 10520.0},
                 4: {'SD': dt.datetime(2017, 4, 26, 0, 0),
                     'SP': 3,
                     'VM': 7643.0},
                 5: {'SD': dt.datetime(2017, 4, 27, 0, 0),
                     'SP': 3,
                     'VM': 7239.0},
                 6: {'SD': dt.datetime(2017, 4, 28, 0, 0),
                     'SP': 3,
                     'VM': 6933.0},
                 7: {'SD': dt.datetime(2017, 4, 29, 0, 0),
                     'SP': 3,
                     'VM': 10730.0},
                 8: {'SD': dt.datetime(2017, 4, 30, 0, 0),
                     'SP': 3,
                     'VM': 11714.0},
                 9: {'SD': dt.datetime(2017, 5, 1, 0, 0),
                     'SP': 3,
                     'VM': 11903.0},
                 10: {'SD': dt.datetime(2017, 5, 2, 0, 0),
                      'SP': 3,
                      'VM': 9834.0},
                 11: {'SD': dt.datetime(2017, 5, 3, 0, 0),
                      'SP': 3,
                      'VM': 10329.0},
                 12: {'SD': dt.datetime(2017, 5, 4, 0, 0),
                      'SP': 3,
                      'VM': 10910.0},
                 13: {'SD': dt.datetime(2017, 5, 5, 0, 0),
                      'SP': 3,
                      'VM': 11699.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_ocnmfd2_to_dict(self):
        """
        test conversion of OCNMFD2 raw data string to dictionary
        """
        input_str = '2017:04:21:12:39:24:GMT: subject=BMRA.SYSTEM.OCNMFD2, \
        message={TP=2017:04:21:12:38:00:GMT,NR=13,\
        SD=2017:04:23:00:00:00:GMT,DM=15686.0,\
        SD=2017:04:24:00:00:00:GMT,DM=16196.0,\
        SD=2017:04:25:00:00:00:GMT,DM=15291.0,\
        SD=2017:04:26:00:00:00:GMT,DM=11728.0,\
        SD=2017:04:27:00:00:00:GMT,DM=11324.0,\
        SD=2017:04:28:00:00:00:GMT,DM=11028.0,\
        SD=2017:04:29:00:00:00:GMT,DM=14965.0,\
        SD=2017:04:30:00:00:00:GMT,DM=15967.0,\
        SD=2017:05:01:00:00:00:GMT,DM=16103.0,\
        SD=2017:05:02:00:00:00:GMT,DM=13971.0,\
        SD=2017:05:03:00:00:00:GMT,DM=14473.0,\
        SD=2017:05:04:00:00:00:GMT,DM=15075.0,\
        SD=2017:05:05:00:00:00:GMT,DM=15873.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 12, 39, 24),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'OCNMFD2',
                         'TP' : dt.datetime(2017, 4, 21, 12, 38),
                         'data_points': {
                  1: {'DM': 15686.0, 'SD': dt.datetime(2017, 4, 23, 0, 0)},
                  2: {'DM': 16196.0, 'SD': dt.datetime(2017, 4, 24, 0, 0)},
                  3: {'DM': 15291.0, 'SD': dt.datetime(2017, 4, 25, 0, 0)},
                  4: {'DM': 11728.0, 'SD': dt.datetime(2017, 4, 26, 0, 0)},
                  5: {'DM': 11324.0, 'SD': dt.datetime(2017, 4, 27, 0, 0)},
                  6: {'DM': 11028.0, 'SD': dt.datetime(2017, 4, 28, 0, 0)},
                  7: {'DM': 14965.0, 'SD': dt.datetime(2017, 4, 29, 0, 0)},
                  8: {'DM': 15967.0, 'SD': dt.datetime(2017, 4, 30, 0, 0)},
                  9: {'DM': 16103.0, 'SD': dt.datetime(2017, 5, 1, 0, 0)},
                  10: {'DM': 13971.0, 'SD': dt.datetime(2017, 5, 2, 0, 0)},
                  11: {'DM': 14473.0, 'SD': dt.datetime(2017, 5, 3, 0, 0)},
                  12: {'DM': 15075.0, 'SD': dt.datetime(2017, 5, 4, 0, 0)},
                  13: {'DM': 15873.0, 'SD': dt.datetime(2017, 5, 5, 0, 0)}
                         }}
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_fou2t14d_to_dict(self):
        """
        test conversion of FOU2T14D raw data string to dictionary
        """
        input_str = '2017:04:21:12:39:09:GMT: subject=BMRA.SYSTEM.FOU2T14D, \
        message={TP=2017:04:21:12:38:00:GMT,NR=169,\
        SD=2017:04:23:00:00:00:GMT,FT=WIND,OU=4084.0,\
        SD=2017:04:23:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:04:23:00:00:00:GMT,FT=OTHER,OU=2065.0,\
        SD=2017:04:23:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:04:23:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:04:23:00:00:00:GMT,FT=NUCLEAR,OU=6898.0,\
        SD=2017:04:23:00:00:00:GMT,FT=NPSHYD,OU=1030.0,\
        SD=2017:04:23:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:04:23:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:04:23:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:04:23:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:04:23:00:00:00:GMT,FT=COAL,OU=6831.0,\
        SD=2017:04:23:00:00:00:GMT,FT=CCGT,OU=23092.0,\
        SD=2017:04:24:00:00:00:GMT,FT=WIND,OU=6357.0,\
        SD=2017:04:24:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:04:24:00:00:00:GMT,FT=OTHER,OU=2065.0,\
        SD=2017:04:24:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:04:24:00:00:00:GMT,FT=OCGT,OU=700.0,\
        SD=2017:04:24:00:00:00:GMT,FT=NUCLEAR,OU=6898.0,\
        SD=2017:04:24:00:00:00:GMT,FT=NPSHYD,OU=1030.0,\
        SD=2017:04:24:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:04:24:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:04:24:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:04:24:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:04:24:00:00:00:GMT,FT=COAL,OU=8121.0,\
        SD=2017:04:24:00:00:00:GMT,FT=CCGT,OU=23517.0,\
        SD=2017:04:25:00:00:00:GMT,FT=WIND,OU=6440.0,\
        SD=2017:04:25:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:04:25:00:00:00:GMT,FT=OTHER,OU=2065.0,\
        SD=2017:04:25:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:04:25:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:04:25:00:00:00:GMT,FT=NUCLEAR,OU=6658.0,\
        SD=2017:04:25:00:00:00:GMT,FT=NPSHYD,OU=1030.0,\
        SD=2017:04:25:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:04:25:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:04:25:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:04:25:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:04:25:00:00:00:GMT,FT=COAL,OU=7621.0,\
        SD=2017:04:25:00:00:00:GMT,FT=CCGT,OU=23541.0,\
        SD=2017:04:26:00:00:00:GMT,FT=WIND,OU=3799.0,\
        SD=2017:04:26:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:04:26:00:00:00:GMT,FT=OTHER,OU=2065.0,\
        SD=2017:04:26:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:04:26:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:04:26:00:00:00:GMT,FT=NUCLEAR,OU=6750.0,\
        SD=2017:04:26:00:00:00:GMT,FT=NPSHYD,OU=1030.0,\
        SD=2017:04:26:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:04:26:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:04:26:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:04:26:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:04:26:00:00:00:GMT,FT=COAL,OU=7129.0,\
        SD=2017:04:26:00:00:00:GMT,FT=CCGT,OU=24009.0,\
        SD=2017:04:27:00:00:00:GMT,FT=WIND,OU=2352.0,\
        SD=2017:04:27:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:04:27:00:00:00:GMT,FT=OTHER,OU=2063.0,\
        SD=2017:04:27:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:04:27:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:04:27:00:00:00:GMT,FT=NUCLEAR,OU=6809.0,\
        SD=2017:04:27:00:00:00:GMT,FT=NPSHYD,OU=1030.0,\
        SD=2017:04:27:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:04:27:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:04:27:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:04:27:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:04:27:00:00:00:GMT,FT=COAL,OU=8121.0,\
        SD=2017:04:27:00:00:00:GMT,FT=CCGT,OU=24013.0,\
        SD=2017:04:28:00:00:00:GMT,FT=WIND,OU=2534.0,\
        SD=2017:04:28:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:04:28:00:00:00:GMT,FT=OTHER,OU=2115.0,\
        SD=2017:04:28:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:04:28:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:04:28:00:00:00:GMT,FT=NUCLEAR,OU=6781.0,\
        SD=2017:04:28:00:00:00:GMT,FT=NPSHYD,OU=1016.0,\
        SD=2017:04:28:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:04:28:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:04:28:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:04:28:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:04:28:00:00:00:GMT,FT=COAL,OU=7716.0,\
        SD=2017:04:28:00:00:00:GMT,FT=CCGT,OU=23560.0,\
        SD=2017:04:29:00:00:00:GMT,FT=WIND,OU=2748.0,\
        SD=2017:04:29:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:04:29:00:00:00:GMT,FT=OTHER,OU=2115.0,\
        SD=2017:04:29:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:04:29:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:04:29:00:00:00:GMT,FT=NUCLEAR,OU=6624.0,\
        SD=2017:04:29:00:00:00:GMT,FT=NPSHYD,OU=1016.0,\
        SD=2017:04:29:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:04:29:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:04:29:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:04:29:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:04:29:00:00:00:GMT,FT=COAL,OU=7216.0,\
        SD=2017:04:29:00:00:00:GMT,FT=CCGT,OU=22700.0,\
        SD=2017:04:30:00:00:00:GMT,FT=WIND,OU=2867.0,\
        SD=2017:04:30:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:04:30:00:00:00:GMT,FT=OTHER,OU=2115.0,\
        SD=2017:04:30:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:04:30:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:04:30:00:00:00:GMT,FT=NUCLEAR,OU=6914.0,\
        SD=2017:04:30:00:00:00:GMT,FT=NPSHYD,OU=1016.0,\
        SD=2017:04:30:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:04:30:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:04:30:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:04:30:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:04:30:00:00:00:GMT,FT=COAL,OU=7216.0,\
        SD=2017:04:30:00:00:00:GMT,FT=CCGT,OU=22603.0,\
        SD=2017:05:01:00:00:00:GMT,FT=WIND,OU=3063.0,\
        SD=2017:05:01:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:05:01:00:00:00:GMT,FT=OTHER,OU=2115.0,\
        SD=2017:05:01:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:05:01:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:05:01:00:00:00:GMT,FT=NUCLEAR,OU=7179.0,\
        SD=2017:05:01:00:00:00:GMT,FT=NPSHYD,OU=951.0,\
        SD=2017:05:01:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:05:01:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:05:01:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:05:01:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:05:01:00:00:00:GMT,FT=COAL,OU=7716.0,\
        SD=2017:05:01:00:00:00:GMT,FT=CCGT,OU=23853.0,\
        SD=2017:05:02:00:00:00:GMT,FT=WIND,OU=2773.0,\
        SD=2017:05:02:00:00:00:GMT,FT=PS,OU=2408.0,\
        SD=2017:05:02:00:00:00:GMT,FT=OTHER,OU=2115.0,\
        SD=2017:05:02:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:05:02:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:05:02:00:00:00:GMT,FT=NUCLEAR,OU=7288.0,\
        SD=2017:05:02:00:00:00:GMT,FT=NPSHYD,OU=965.0,\
        SD=2017:05:02:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:05:02:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:05:02:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:05:02:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:05:02:00:00:00:GMT,FT=COAL,OU=7716.0,\
        SD=2017:05:02:00:00:00:GMT,FT=CCGT,OU=24248.0,\
        SD=2017:05:03:00:00:00:GMT,FT=WIND,OU=2857.0,\
        SD=2017:05:03:00:00:00:GMT,FT=PS,OU=2648.0,\
        SD=2017:05:03:00:00:00:GMT,FT=OTHER,OU=2115.0,\
        SD=2017:05:03:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:05:03:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:05:03:00:00:00:GMT,FT=NUCLEAR,OU=7361.0,\
        SD=2017:05:03:00:00:00:GMT,FT=NPSHYD,OU=965.0,\
        SD=2017:05:03:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:05:03:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:05:03:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:05:03:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:05:03:00:00:00:GMT,FT=COAL,OU=7716.0,\
        SD=2017:05:03:00:00:00:GMT,FT=CCGT,OU=24083.0,\
        SD=2017:05:04:00:00:00:GMT,FT=WIND,OU=2889.0,\
        SD=2017:05:04:00:00:00:GMT,FT=PS,OU=2648.0,\
        SD=2017:05:04:00:00:00:GMT,FT=OTHER,OU=2115.0,\
        SD=2017:05:04:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:05:04:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:05:04:00:00:00:GMT,FT=NUCLEAR,OU=7361.0,\
        SD=2017:05:04:00:00:00:GMT,FT=NPSHYD,OU=965.0,\
        SD=2017:05:04:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:05:04:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:05:04:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:05:04:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:05:04:00:00:00:GMT,FT=COAL,OU=7716.0,\
        SD=2017:05:04:00:00:00:GMT,FT=CCGT,OU=23863.0,\
        SD=2017:05:05:00:00:00:GMT,FT=WIND,OU=4033.0,\
        SD=2017:05:05:00:00:00:GMT,FT=PS,OU=2648.0,\
        SD=2017:05:05:00:00:00:GMT,FT=OTHER,OU=2115.0,\
        SD=2017:05:05:00:00:00:GMT,FT=OIL,OU=0.0,\
        SD=2017:05:05:00:00:00:GMT,FT=OCGT,OU=728.0,\
        SD=2017:05:05:00:00:00:GMT,FT=NUCLEAR,OU=7361.0,\
        SD=2017:05:05:00:00:00:GMT,FT=NPSHYD,OU=965.0,\
        SD=2017:05:05:00:00:00:GMT,FT=INTNED,OU=1000.0,\
        SD=2017:05:05:00:00:00:GMT,FT=INTIRL,OU=250.0,\
        SD=2017:05:05:00:00:00:GMT,FT=INTFR,OU=2000.0,\
        SD=2017:05:05:00:00:00:GMT,FT=INTEW,OU=0.0,\
        SD=2017:05:05:00:00:00:GMT,FT=COAL,OU=7716.0,\
        SD=2017:05:05:00:00:00:GMT,FT=CCGT,OU=23167.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 12, 39, 9),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'FOU2T14D',
                         'TP' : dt.datetime(2017, 4, 21, 12, 38),
                         'data_points': {
                 1: {'FT': 'WIND',
                     'OU': 4084.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 2: {'FT': 'PS',
                     'OU': 2408.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 3: {'FT': 'OTHER',
                     'OU': 2065.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 4: {'FT': 'OIL',
                     'OU': 0.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 5: {'FT': 'OCGT',
                     'OU': 728.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 6: {'FT': 'NUCLEAR',
                     'OU': 6898.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 7: {'FT': 'NPSHYD',
                     'OU': 1030.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 8: {'FT': 'INTNED',
                     'OU': 1000.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 9: {'FT': 'INTIRL',
                     'OU': 250.0,
                     'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 10: {'FT': 'INTFR',
                      'OU': 2000.0,
                      'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 11: {'FT': 'INTEW',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 12: {'FT': 'COAL',
                      'OU': 6831.0,
                      'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 13: {'FT': 'CCGT',
                      'OU': 23092.0,
                      'SD': dt.datetime(2017, 4, 23, 0, 0)},
                 14: {'FT': 'WIND',
                      'OU': 6357.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 15: {'FT': 'PS',
                      'OU': 2408.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 16: {'FT': 'OTHER',
                      'OU': 2065.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 17: {'FT': 'OIL',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 18: {'FT': 'OCGT',
                      'OU': 700.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 19: {'FT': 'NUCLEAR',
                      'OU': 6898.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 20: {'FT': 'NPSHYD',
                      'OU': 1030.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 21: {'FT': 'INTNED',
                      'OU': 1000.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 22: {'FT': 'INTIRL',
                      'OU': 250.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 23: {'FT': 'INTFR',
                      'OU': 2000.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 24: {'FT': 'INTEW',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 25: {'FT': 'COAL',
                      'OU': 8121.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 26: {'FT': 'CCGT',
                      'OU': 23517.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                 27: {'FT': 'WIND',
                      'OU': 6440.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 28: {'FT': 'PS',
                      'OU': 2408.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 29: {'FT': 'OTHER',
                      'OU': 2065.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 30: {'FT': 'OIL',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 31: {'FT': 'OCGT',
                      'OU': 728.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 32: {'FT': 'NUCLEAR',
                      'OU': 6658.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 33: {'FT': 'NPSHYD',
                      'OU': 1030.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 34: {'FT': 'INTNED',
                      'OU': 1000.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 35: {'FT': 'INTIRL',
                      'OU': 250.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 36: {'FT': 'INTFR',
                      'OU': 2000.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 37: {'FT': 'INTEW',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 38: {'FT': 'COAL',
                      'OU': 7621.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 39: {'FT': 'CCGT',
                      'OU': 23541.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                 40: {'FT': 'WIND',
                      'OU': 3799.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 41: {'FT': 'PS',
                      'OU': 2408.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 42: {'FT': 'OTHER',
                      'OU': 2065.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 43: {'FT': 'OIL',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 44: {'FT': 'OCGT',
                      'OU': 728.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 45: {'FT': 'NUCLEAR',
                      'OU': 6750.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 46: {'FT': 'NPSHYD',
                      'OU': 1030.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 47: {'FT': 'INTNED',
                      'OU': 1000.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 48: {'FT': 'INTIRL',
                      'OU': 250.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 49: {'FT': 'INTFR',
                      'OU': 2000.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 50: {'FT': 'INTEW',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 51: {'FT': 'COAL',
                      'OU': 7129.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 52: {'FT': 'CCGT',
                      'OU': 24009.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                 53: {'FT': 'WIND',
                      'OU': 2352.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 54: {'FT': 'PS',
                      'OU': 2408.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 55: {'FT': 'OTHER',
                      'OU': 2063.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 56: {'FT': 'OIL',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 57: {'FT': 'OCGT',
                      'OU': 728.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 58: {'FT': 'NUCLEAR',
                      'OU': 6809.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 59: {'FT': 'NPSHYD',
                      'OU': 1030.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 60: {'FT': 'INTNED',
                      'OU': 1000.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 61: {'FT': 'INTIRL',
                      'OU': 250.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 62: {'FT': 'INTFR',
                      'OU': 2000.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 63: {'FT': 'INTEW',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 64: {'FT': 'COAL',
                      'OU': 8121.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 65: {'FT': 'CCGT',
                      'OU': 24013.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                 66: {'FT': 'WIND',
                      'OU': 2534.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 67: {'FT': 'PS',
                      'OU': 2408.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 68: {'FT': 'OTHER',
                      'OU': 2115.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 69: {'FT': 'OIL',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 70: {'FT': 'OCGT',
                      'OU': 728.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 71: {'FT': 'NUCLEAR',
                      'OU': 6781.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 72: {'FT': 'NPSHYD',
                      'OU': 1016.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 73: {'FT': 'INTNED',
                      'OU': 1000.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 74: {'FT': 'INTIRL',
                      'OU': 250.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 75: {'FT': 'INTFR',
                      'OU': 2000.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 76: {'FT': 'INTEW',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 77: {'FT': 'COAL',
                      'OU': 7716.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 78: {'FT': 'CCGT',
                      'OU': 23560.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                 79: {'FT': 'WIND',
                      'OU': 2748.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 80: {'FT': 'PS',
                      'OU': 2408.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 81: {'FT': 'OTHER',
                      'OU': 2115.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 82: {'FT': 'OIL',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 83: {'FT': 'OCGT',
                      'OU': 728.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 84: {'FT': 'NUCLEAR',
                      'OU': 6624.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 85: {'FT': 'NPSHYD',
                      'OU': 1016.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 86: {'FT': 'INTNED',
                      'OU': 1000.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 87: {'FT': 'INTIRL',
                      'OU': 250.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 88: {'FT': 'INTFR',
                      'OU': 2000.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 89: {'FT': 'INTEW',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 90: {'FT': 'COAL',
                      'OU': 7216.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 91: {'FT': 'CCGT',
                      'OU': 22700.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                 92: {'FT': 'WIND',
                      'OU': 2867.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 93: {'FT': 'PS',
                      'OU': 2408.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 94: {'FT': 'OTHER',
                      'OU': 2115.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 95: {'FT': 'OIL',
                      'OU': 0.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 96: {'FT': 'OCGT',
                      'OU': 728.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 97: {'FT': 'NUCLEAR',
                      'OU': 6914.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 98: {'FT': 'NPSHYD',
                      'OU': 1016.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 99: {'FT': 'INTNED',
                      'OU': 1000.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 100: {'FT': 'INTIRL',
                       'OU': 250.0,
                       'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 101: {'FT': 'INTFR',
                       'OU': 2000.0,
                       'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 102: {'FT': 'INTEW',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 103: {'FT': 'COAL',
                       'OU': 7216.0,
                       'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 104: {'FT': 'CCGT',
                       'OU': 22603.0,
                       'SD': dt.datetime(2017, 4, 30, 0, 0)},
                 105: {'FT': 'WIND',
                       'OU': 3063.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 106: {'FT': 'PS',
                       'OU': 2408.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 107: {'FT': 'OTHER',
                       'OU': 2115.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 108: {'FT': 'OIL',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 109: {'FT': 'OCGT',
                       'OU': 728.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 110: {'FT': 'NUCLEAR',
                       'OU': 7179.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 111: {'FT': 'NPSHYD',
                       'OU': 951.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 112: {'FT': 'INTNED',
                       'OU': 1000.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 113: {'FT': 'INTIRL',
                       'OU': 250.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 114: {'FT': 'INTFR',
                       'OU': 2000.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 115: {'FT': 'INTEW',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 116: {'FT': 'COAL',
                       'OU': 7716.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 117: {'FT': 'CCGT',
                       'OU': 23853.0,
                       'SD': dt.datetime(2017, 5, 1, 0, 0)},
                 118: {'FT': 'WIND',
                       'OU': 2773.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 119: {'FT': 'PS',
                       'OU': 2408.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 120: {'FT': 'OTHER',
                       'OU': 2115.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 121: {'FT': 'OIL',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 122: {'FT': 'OCGT',
                       'OU': 728.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 123: {'FT': 'NUCLEAR',
                       'OU': 7288.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 124: {'FT': 'NPSHYD',
                       'OU': 965.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 125: {'FT': 'INTNED',
                       'OU': 1000.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 126: {'FT': 'INTIRL',
                       'OU': 250.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 127: {'FT': 'INTFR',
                       'OU': 2000.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 128: {'FT': 'INTEW',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 129: {'FT': 'COAL',
                       'OU': 7716.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 130: {'FT': 'CCGT',
                       'OU': 24248.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                 131: {'FT': 'WIND',
                       'OU': 2857.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 132: {'FT': 'PS',
                       'OU': 2648.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 133: {'FT': 'OTHER',
                       'OU': 2115.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 134: {'FT': 'OIL',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 135: {'FT': 'OCGT',
                       'OU': 728.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 136: {'FT': 'NUCLEAR',
                       'OU': 7361.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 137: {'FT': 'NPSHYD',
                       'OU': 965.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 138: {'FT': 'INTNED',
                       'OU': 1000.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 139: {'FT': 'INTIRL',
                       'OU': 250.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 140: {'FT': 'INTFR',
                       'OU': 2000.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 141: {'FT': 'INTEW',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 142: {'FT': 'COAL',
                       'OU': 7716.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 143: {'FT': 'CCGT',
                       'OU': 24083.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                 144: {'FT': 'WIND',
                       'OU': 2889.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 145: {'FT': 'PS',
                       'OU': 2648.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 146: {'FT': 'OTHER',
                       'OU': 2115.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 147: {'FT': 'OIL',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 148: {'FT': 'OCGT',
                       'OU': 728.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 149: {'FT': 'NUCLEAR',
                       'OU': 7361.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 150: {'FT': 'NPSHYD',
                       'OU': 965.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 151: {'FT': 'INTNED',
                       'OU': 1000.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 152: {'FT': 'INTIRL',
                       'OU': 250.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 153: {'FT': 'INTFR',
                       'OU': 2000.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 154: {'FT': 'INTEW',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 155: {'FT': 'COAL',
                       'OU': 7716.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 156: {'FT': 'CCGT',
                       'OU': 23863.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                 157: {'FT': 'WIND',
                       'OU': 4033.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 158: {'FT': 'PS',
                       'OU': 2648.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 159: {'FT': 'OTHER',
                       'OU': 2115.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 160: {'FT': 'OIL',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 161: {'FT': 'OCGT',
                       'OU': 728.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 162: {'FT': 'NUCLEAR',
                       'OU': 7361.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 163: {'FT': 'NPSHYD',
                       'OU': 965.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 164: {'FT': 'INTNED',
                       'OU': 1000.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 165: {'FT': 'INTIRL',
                       'OU': 250.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 166: {'FT': 'INTFR',
                       'OU': 2000.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 167: {'FT': 'INTEW',
                       'OU': 0.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 168: {'FT': 'COAL',
                       'OU': 7716.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)},
                 169: {'FT': 'CCGT',
                       'OU': 23167.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)}}
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_uou2t14d_to_dict(self):
        """
        test conversion of UOU2T14D raw data string to dictionary
        """
        input_str = '2017:04:21:12:40:35:GMT: subject=BMRA.SYSTEM.2__PPGEN001.UOU2T14D, \
        message={TP=2017:04:21:12:38:00:GMT,NR=13,\
        SD=2017:04:23:00:00:00:GMT,FT=WIND,OU=12.0,\
        SD=2017:04:24:00:00:00:GMT,FT=WIND,OU=26.0,\
        SD=2017:04:25:00:00:00:GMT,FT=WIND,OU=30.0,\
        SD=2017:04:26:00:00:00:GMT,FT=WIND,OU=8.0,\
        SD=2017:04:27:00:00:00:GMT,FT=WIND,OU=3.0,\
        SD=2017:04:28:00:00:00:GMT,FT=WIND,OU=4.0,\
        SD=2017:04:29:00:00:00:GMT,FT=WIND,OU=5.0,\
        SD=2017:04:30:00:00:00:GMT,FT=WIND,OU=4.0,\
        SD=2017:05:01:00:00:00:GMT,FT=WIND,OU=4.0,\
        SD=2017:05:02:00:00:00:GMT,FT=WIND,OU=5.0,\
        SD=2017:05:03:00:00:00:GMT,FT=WIND,OU=4.0,\
        SD=2017:05:04:00:00:00:GMT,FT=WIND,OU=4.0,\
        SD=2017:05:05:00:00:00:GMT,FT=WIND,OU=18.0}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 12, 40, 35),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'UOU2T14D',
                         'bmu_id' : '2__PPGEN001',
                         'TP' : dt.datetime(2017, 4, 21, 12, 38),
                         'data_points': {
                  1: {'FT': 'WIND',
                      'OU': 12.0,
                      'SD': dt.datetime(2017, 4, 23, 0, 0)},
                  2: {'FT': 'WIND',
                      'OU': 26.0,
                      'SD': dt.datetime(2017, 4, 24, 0, 0)},
                  3: {'FT': 'WIND',
                      'OU': 30.0,
                      'SD': dt.datetime(2017, 4, 25, 0, 0)},
                  4: {'FT': 'WIND',
                      'OU': 8.0,
                      'SD': dt.datetime(2017, 4, 26, 0, 0)},
                  5: {'FT': 'WIND',
                      'OU': 3.0,
                      'SD': dt.datetime(2017, 4, 27, 0, 0)},
                  6: {'FT': 'WIND',
                      'OU': 4.0,
                      'SD': dt.datetime(2017, 4, 28, 0, 0)},
                  7: {'FT': 'WIND',
                      'OU': 5.0,
                      'SD': dt.datetime(2017, 4, 29, 0, 0)},
                  8: {'FT': 'WIND',
                      'OU': 4.0,
                      'SD': dt.datetime(2017, 4, 30, 0, 0)},
                  9: {'FT': 'WIND',
                      'OU': 4.0,
                      'SD': dt.datetime(2017, 5, 1, 0, 0)},
                  10: {'FT': 'WIND',
                       'OU': 5.0,
                       'SD': dt.datetime(2017, 5, 2, 0, 0)},
                  11: {'FT': 'WIND',
                       'OU': 4.0,
                       'SD': dt.datetime(2017, 5, 3, 0, 0)},
                  12: {'FT': 'WIND',
                       'OU': 4.0,
                       'SD': dt.datetime(2017, 5, 4, 0, 0)},
                  13: {'FT': 'WIND',
                       'OU': 18.0,
                       'SD': dt.datetime(2017, 5, 5, 0, 0)}}
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_uou2t52w_to_dict(self):
        """
        test conversion of UOU2T52W raw data string to dictionary
        """
        input_str = '2018:01:04:13:41:23:GMT: subject=BMRA.SYSTEM.2__PPGEN001.UOU2T52W, message={TP=2018:01:04:13:31:00:GMT,NR=51,WN=3,CY=2018,FT=WIND,OU=28.0,WN=4,CY=2018,FT=WIND,OU=28.0,WN=5,CY=2018,FT=WIND,OU=28.0,WN=6,CY=2018,FT=WIND,OU=26.0,WN=7,CY=2018,FT=WIND,OU=26.0,WN=8,CY=2018,FT=WIND,OU=26.0,WN=9,CY=2018,FT=WIND,OU=26.0,WN=10,CY=2018,FT=WIND,OU=20.0,WN=11,CY=2018,FT=WIND,OU=20.0,WN=12,CY=2018,FT=WIND,OU=20.0,WN=13,CY=2018,FT=WIND,OU=20.0,WN=14,CY=2018,FT=WIND,OU=15.0,WN=15,CY=2018,FT=WIND,OU=15.0,WN=16,CY=2018,FT=WIND,OU=15.0,WN=17,CY=2018,FT=WIND,OU=15.0,WN=18,CY=2018,FT=WIND,OU=15.0,WN=19,CY=2018,FT=WIND,OU=18.0,WN=20,CY=2018,FT=WIND,OU=18.0,WN=21,CY=2018,FT=WIND,OU=18.0,WN=22,CY=2018,FT=WIND,OU=18.0,WN=23,CY=2018,FT=WIND,OU=10.0,WN=24,CY=2018,FT=WIND,OU=10.0,WN=25,CY=2018,FT=WIND,OU=10.0,WN=26,CY=2018,FT=WIND,OU=10.0,WN=27,CY=2018,FT=WIND,OU=10.0,WN=28,CY=2018,FT=WIND,OU=10.0,WN=29,CY=2018,FT=WIND,OU=10.0,WN=30,CY=2018,FT=WIND,OU=10.0,WN=31,CY=2018,FT=WIND,OU=10.0,WN=32,CY=2018,FT=WIND,OU=13.0,WN=33,CY=2018,FT=WIND,OU=13.0,WN=34,CY=2018,FT=WIND,OU=13.0,WN=35,CY=2018,FT=WIND,OU=13.0,WN=36,CY=2018,FT=WIND,OU=15.0,WN=37,CY=2018,FT=WIND,OU=15.0,WN=38,CY=2018,FT=WIND,OU=15.0,WN=39,CY=2018,FT=WIND,OU=15.0,WN=40,CY=2018,FT=WIND,OU=20.0,WN=41,CY=2018,FT=WIND,OU=20.0,WN=42,CY=2018,FT=WIND,OU=20.0,WN=43,CY=2018,FT=WIND,OU=20.0,WN=44,CY=2018,FT=WIND,OU=20.0,WN=45,CY=2018,FT=WIND,OU=23.0,WN=46,CY=2018,FT=WIND,OU=23.0,WN=47,CY=2018,FT=WIND,OU=23.0,WN=48,CY=2018,FT=WIND,OU=23.0,WN=49,CY=2018,FT=WIND,OU=28.0,WN=50,CY=2018,FT=WIND,OU=28.0,WN=51,CY=2018,FT=WIND,OU=28.0,WN=52,CY=2018,FT=WIND,OU=28.0,WN=1,CY=2019,FT=WIND,OU=28.0}'

        expected_dict = {'received_time' : dt.datetime(2018, 1, 4, 13, 41, 23),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'UOU2T52W',
                         'bmu_id' : '2__PPGEN001',
                         'TP' : dt.datetime(2018, 1, 4, 13, 31),
                         'data_points': {
                 1: {'CY': 2018, 'FT': 'WIND', 'OU': 28.0, 'WN': 3},
                 2: {'CY': 2018, 'FT': 'WIND', 'OU': 28.0, 'WN': 4},
                 3: {'CY': 2018, 'FT': 'WIND', 'OU': 28.0, 'WN': 5},
                 4: {'CY': 2018, 'FT': 'WIND', 'OU': 26.0, 'WN': 6},
                 5: {'CY': 2018, 'FT': 'WIND', 'OU': 26.0, 'WN': 7},
                 6: {'CY': 2018, 'FT': 'WIND', 'OU': 26.0, 'WN': 8},
                 7: {'CY': 2018, 'FT': 'WIND', 'OU': 26.0, 'WN': 9},
                 8: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 10},
                 9: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 11},
                 10: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 12},
                 11: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 13},
                 12: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 14},
                 13: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 15},
                 14: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 16},
                 15: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 17},
                 16: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 18},
                 17: {'CY': 2018, 'FT': 'WIND', 'OU': 18.0, 'WN': 19},
                 18: {'CY': 2018, 'FT': 'WIND', 'OU': 18.0, 'WN': 20},
                 19: {'CY': 2018, 'FT': 'WIND', 'OU': 18.0, 'WN': 21},
                 20: {'CY': 2018, 'FT': 'WIND', 'OU': 18.0, 'WN': 22},
                 21: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 23},
                 22: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 24},
                 23: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 25},
                 24: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 26},
                 25: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 27},
                 26: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 28},
                 27: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 29},
                 28: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 30},
                 29: {'CY': 2018, 'FT': 'WIND', 'OU': 10.0, 'WN': 31},
                 30: {'CY': 2018, 'FT': 'WIND', 'OU': 13.0, 'WN': 32},
                 31: {'CY': 2018, 'FT': 'WIND', 'OU': 13.0, 'WN': 33},
                 32: {'CY': 2018, 'FT': 'WIND', 'OU': 13.0, 'WN': 34},
                 33: {'CY': 2018, 'FT': 'WIND', 'OU': 13.0, 'WN': 35},
                 34: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 36},
                 35: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 37},
                 36: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 38},
                 37: {'CY': 2018, 'FT': 'WIND', 'OU': 15.0, 'WN': 39},
                 38: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 40},
                 39: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 41},
                 40: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 42},
                 41: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 43},
                 42: {'CY': 2018, 'FT': 'WIND', 'OU': 20.0, 'WN': 44},
                 43: {'CY': 2018, 'FT': 'WIND', 'OU': 23.0, 'WN': 45},
                 44: {'CY': 2018, 'FT': 'WIND', 'OU': 23.0, 'WN': 46},
                 45: {'CY': 2018, 'FT': 'WIND', 'OU': 23.0, 'WN': 47},
                 46: {'CY': 2018, 'FT': 'WIND', 'OU': 23.0, 'WN': 48},
                 47: {'CY': 2018, 'FT': 'WIND', 'OU': 28.0, 'WN': 49},
                 48: {'CY': 2018, 'FT': 'WIND', 'OU': 28.0, 'WN': 50},
                 49: {'CY': 2018, 'FT': 'WIND', 'OU': 28.0, 'WN': 51},
                 50: {'CY': 2018, 'FT': 'WIND', 'OU': 28.0, 'WN': 52},
                 51: {'CY': 2019, 'FT': 'WIND', 'OU': 28.0, 'WN': 1}}
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_syswarn_to_dict(self):
        """
        test conversion of SYSWARN raw data string to dictionary
        """
        input_str = '2017:04:21:14:28:15:GMT: subject=BMRA.SYSTEM.SYSWARN, message={TP=2017:04:21:14:28:09:GMT,SW=NATIONAL GRID NOTIFICATION of excess energy prices used for settlement outside of BALIT for SO to SO Transactions over the National Grid/RTE  Interconnector.  Prices cover 23:00Hrs Today to 05:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 98.69; Bid 1.03 From NGC: Offer 247.38; Bid 0.00  Prices cover 05:00Hrs Tomorrow to 19:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 89.05; Bid 0.00 From NGC: Offer 329.84; Bid 17.67  Prices cover 19:00Hrs Tomorrow to 23:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 98.69; Bid 1.03 From NGC: Offer 353.40; Bid 23.56}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 14, 28, 15),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'SYSWARN',
                         'TP' : dt.datetime(2017, 4, 21, 14, 28, 9),
                         'SW' : 'NATIONAL GRID NOTIFICATION of excess energy prices used for settlement outside of BALIT for SO to SO Transactions over the National Grid/RTE  Interconnector.  Prices cover 23:00Hrs Today to 05:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 98.69; Bid 1.03 From NGC: Offer 247.38; Bid 0.00  Prices cover 05:00Hrs Tomorrow to 19:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 89.05; Bid 0.00 From NGC: Offer 329.84; Bid 17.67  Prices cover 19:00Hrs Tomorrow to 23:00Hrs Tomorrow (UK local time) and are in Euro/MWh. From RTE: Offer 98.69; Bid 1.03 From NGC: Offer 353.40; Bid 23.56'
                         }

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_sysmsg_to_dict(self):
        """
        test conversion of SYSMSG raw data string to dictionary
        """
        input_str = '2018:01:02:17:52:56:GMT: subject=BMRA.SYSTEM.SYSMSG, message={MT=MIDNP,TP=2018:01:02:17:51:46:GMT,SM=Market Index Data for Settlement Day 20180102 period 35 from Automated Power Exchange (UK) (APXMIDP) was not received. Price and volume defaulted to 0.}'

        expected_dict = {'received_time' : dt.datetime(2018, 1, 2, 17, 52, 56),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'SYSMSG',
                         'TP' : dt.datetime(2018, 1, 2, 17, 51, 46),
                         'MT' : 'MIDNP',
                         'SM' : 'Market Index Data for Settlement Day 20180102 period 35 from Automated Power Exchange (UK) (APXMIDP) was not received. Price and volume defaulted to 0.'
                         }

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_temp_to_dict(self):
        """
        test conversion of TEMP raw data string to dictionary
        """
        input_str = '2017:04:21:15:45:35:GMT: subject=BMRA.SYSTEM.TEMP, \
        message={TP=2017:04:21:15:45:00:GMT,TS=2017:04:21:11:00:00:GMT,\
        TO=11.2,TN=9.9,TL=7.0,TH=12.5}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 15, 45, 35),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'TEMP',
                         'TP' : dt.datetime(2017, 4, 21, 15, 45),
                         'TS' : dt.datetime(2017, 4, 21, 11),
                         'TO' : 11.2,
                         'TN' : 9.9,
                         'TL' : 7.0,
                         'TH' : 12.5}

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_cdn_to_dict(self):
        """
        test conversion of CDN raw data string to dictionary
        """
        input_str = '2017:04:21:23:13:54:GMT: subject=BMRA.BP.GALENA.CDN, \
        message={DL=2,ED=2017:04:22:00:00:00:GMT,EP=3}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 23, 13, 54),
                         'message_type' : 'BP',
                         'message_subtype' : 'CDN',
                         'bmu_id' : 'GALENA',
                         'DL' : 2,
                         'ED' : dt.datetime(2017, 4, 22),
                         'EP' : 3}

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_indod_to_dict(self):
        """
        test conversion of INDOD raw data string to dictionary
        """
        input_str = '2017:04:21:23:15:37:GMT: subject=BMRA.SYSTEM.INDOD, \
        message={TP=2017:04:21:23:15:00:GMT,SD=2017:04:21:00:00:00:GMT,\
        EO=716234,EL=657654,EH=808531,EN=757111}'
        expected_dict = {'received_time' : dt.datetime(2017, 4, 21, 23, 15, 37),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'INDOD',
                         'TP' : dt.datetime(2017, 4, 21, 23, 15),
                         'SD' : dt.datetime(2017, 4, 21),
                         'EO' : 716234,
                         'EL' : 657654,
                         'EH' : 808531,
                         'EN' : 757111}

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_TSDFW_to_dict(self):
        """
        test conversion of TSDFW raw data string to dictionary
        """
        input_str = '2017:04:27:13:45:44:GMT: subject=BMRA.SYSTEM.TSDFW, \
        message={TP=2017:04:27:13:45:00:GMT,NR=51,\
        WN=19,WD=2017:05:08:00:00:00:GMT,VD=33970.0,\
        WN=20,WD=2017:05:15:00:00:00:GMT,VD=33040.0,\
        WN=21,WD=2017:05:22:00:00:00:GMT,VD=32410.0,\
        WN=22,WD=2017:05:29:00:00:00:GMT,VD=32010.0,\
        WN=23,WD=2017:06:05:00:00:00:GMT,VD=31950.0,\
        WN=24,WD=2017:06:12:00:00:00:GMT,VD=31660.0,\
        WN=25,WD=2017:06:19:00:00:00:GMT,VD=31240.0,\
        WN=26,WD=2017:06:26:00:00:00:GMT,VD=31160.0,\
        WN=27,WD=2017:07:03:00:00:00:GMT,VD=31140.0,\
        WN=28,WD=2017:07:10:00:00:00:GMT,VD=31030.0,\
        WN=29,WD=2017:07:17:00:00:00:GMT,VD=32030.0,\
        WN=30,WD=2017:07:24:00:00:00:GMT,VD=31508.0,\
        WN=31,WD=2017:07:31:00:00:00:GMT,VD=31696.0,\
        WN=32,WD=2017:08:07:00:00:00:GMT,VD=32410.0,\
        WN=33,WD=2017:08:14:00:00:00:GMT,VD=33260.0,\
        WN=34,WD=2017:08:21:00:00:00:GMT,VD=33978.0,\
        WN=35,WD=2017:08:28:00:00:00:GMT,VD=34904.0,\
        WN=36,WD=2017:09:04:00:00:00:GMT,VD=36027.0,\
        WN=37,WD=2017:09:11:00:00:00:GMT,VD=36613.0,\
        WN=38,WD=2017:09:18:00:00:00:GMT,VD=37876.0,\
        WN=39,WD=2017:09:25:00:00:00:GMT,VD=38874.0,\
        WN=40,WD=2017:10:02:00:00:00:GMT,VD=39947.0,\
        WN=41,WD=2017:10:09:00:00:00:GMT,VD=41029.0,\
        WN=42,WD=2017:10:16:00:00:00:GMT,VD=42368.0,\
        WN=43,WD=2017:10:23:00:00:00:GMT,VD=42847.0,\
        WN=44,WD=2017:10:30:00:00:00:GMT,VD=45510.0,\
        WN=45,WD=2017:11:06:00:00:00:GMT,VD=46671.0,\
        WN=46,WD=2017:11:13:00:00:00:GMT,VD=47267.0,\
        WN=47,WD=2017:11:20:00:00:00:GMT,VD=48044.0,\
        WN=48,WD=2017:11:27:00:00:00:GMT,VD=48265.0,\
        WN=49,WD=2017:12:04:00:00:00:GMT,VD=49303.0,\
        WN=50,WD=2017:12:11:00:00:00:GMT,VD=49889.0,\
        WN=51,WD=2017:12:18:00:00:00:GMT,VD=49428.0,\
        WN=52,WD=2017:12:25:00:00:00:GMT,VD=44450.0,\
        WN=1,WD=2018:01:01:00:00:00:GMT,VD=48753.0,\
        WN=2,WD=2018:01:08:00:00:00:GMT,VD=49280.0,\
        WN=3,WD=2018:01:15:00:00:00:GMT,VD=48915.0,\
        WN=4,WD=2018:01:22:00:00:00:GMT,VD=49060.0,\
        WN=5,WD=2018:01:29:00:00:00:GMT,VD=48683.0,\
        WN=6,WD=2018:02:05:00:00:00:GMT,VD=48139.0,\
        WN=7,WD=2018:02:12:00:00:00:GMT,VD=47201.0,\
        WN=8,WD=2018:02:19:00:00:00:GMT,VD=46668.0,\
        WN=9,WD=2018:02:26:00:00:00:GMT,VD=45996.0,\
        WN=10,WD=2018:03:05:00:00:00:GMT,VD=45172.0,\
        WN=11,WD=2018:03:12:00:00:00:GMT,VD=44460.0,\
        WN=12,WD=2018:03:19:00:00:00:GMT,VD=42797.0,\
        WN=13,WD=2018:03:26:00:00:00:GMT,VD=40651.0,\
        WN=14,WD=2018:04:02:00:00:00:GMT,VD=39598.0,\
        WN=15,WD=2018:04:09:00:00:00:GMT,VD=38254.0,\
        WN=16,WD=2018:04:16:00:00:00:GMT,VD=37149.0,\
        WN=17,WD=2018:04:23:00:00:00:GMT,VD=36207.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 27, 13, 45, 44),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'TSDFW',
                         'TP' : dt.datetime(2017, 4, 27, 13, 45),
                         'data_points' : {
                 1: {'VD': 33970.0,
                     'WD': dt.datetime(2017, 5, 8, 0, 0),
                     'WN': 19},
                 2: {'VD': 33040.0,
                     'WD': dt.datetime(2017, 5, 15, 0, 0),
                     'WN': 20},
                 3: {'VD': 32410.0,
                     'WD': dt.datetime(2017, 5, 22, 0, 0),
                     'WN': 21},
                 4: {'VD': 32010.0,
                     'WD': dt.datetime(2017, 5, 29, 0, 0),
                     'WN': 22},
                 5: {'VD': 31950.0,
                     'WD': dt.datetime(2017, 6, 5, 0, 0),
                     'WN': 23},
                 6: {'VD': 31660.0,
                     'WD': dt.datetime(2017, 6, 12, 0, 0),
                     'WN': 24},
                 7: {'VD': 31240.0,
                     'WD': dt.datetime(2017, 6, 19, 0, 0),
                     'WN': 25},
                 8: {'VD': 31160.0,
                     'WD': dt.datetime(2017, 6, 26, 0, 0),
                     'WN': 26},
                 9: {'VD': 31140.0,
                     'WD': dt.datetime(2017, 7, 3, 0, 0),
                     'WN': 27},
                 10: {'VD': 31030.0,
                      'WD': dt.datetime(2017, 7, 10, 0, 0),
                      'WN': 28},
                 11: {'VD': 32030.0,
                      'WD': dt.datetime(2017, 7, 17, 0, 0),
                      'WN': 29},
                 12: {'VD': 31508.0,
                      'WD': dt.datetime(2017, 7, 24, 0, 0),
                      'WN': 30},
                 13: {'VD': 31696.0,
                      'WD': dt.datetime(2017, 7, 31, 0, 0),
                      'WN': 31},
                 14: {'VD': 32410.0,
                      'WD': dt.datetime(2017, 8, 7, 0, 0),
                      'WN': 32},
                 15: {'VD': 33260.0,
                      'WD': dt.datetime(2017, 8, 14, 0, 0),
                      'WN': 33},
                 16: {'VD': 33978.0,
                      'WD': dt.datetime(2017, 8, 21, 0, 0),
                      'WN': 34},
                 17: {'VD': 34904.0,
                      'WD': dt.datetime(2017, 8, 28, 0, 0),
                      'WN': 35},
                 18: {'VD': 36027.0,
                      'WD': dt.datetime(2017, 9, 4, 0, 0),
                      'WN': 36},
                 19: {'VD': 36613.0,
                      'WD': dt.datetime(2017, 9, 11, 0, 0),
                      'WN': 37},
                 20: {'VD': 37876.0,
                      'WD': dt.datetime(2017, 9, 18, 0, 0),
                      'WN': 38},
                 21: {'VD': 38874.0,
                      'WD': dt.datetime(2017, 9, 25, 0, 0),
                      'WN': 39},
                 22: {'VD': 39947.0,
                      'WD': dt.datetime(2017, 10, 2, 0, 0),
                      'WN': 40},
                 23: {'VD': 41029.0,
                      'WD': dt.datetime(2017, 10, 9, 0, 0),
                      'WN': 41},
                 24: {'VD': 42368.0,
                      'WD': dt.datetime(2017, 10, 16, 0, 0),
                      'WN': 42},
                 25: {'VD': 42847.0,
                      'WD': dt.datetime(2017, 10, 23, 0, 0),
                      'WN': 43},
                 26: {'VD': 45510.0,
                      'WD': dt.datetime(2017, 10, 30, 0, 0),
                      'WN': 44},
                 27: {'VD': 46671.0,
                      'WD': dt.datetime(2017, 11, 6, 0, 0),
                      'WN': 45},
                 28: {'VD': 47267.0,
                      'WD': dt.datetime(2017, 11, 13, 0, 0),
                      'WN': 46},
                 29: {'VD': 48044.0,
                      'WD': dt.datetime(2017, 11, 20, 0, 0),
                      'WN': 47},
                 30: {'VD': 48265.0,
                      'WD': dt.datetime(2017, 11, 27, 0, 0),
                      'WN': 48},
                 31: {'VD': 49303.0,
                      'WD': dt.datetime(2017, 12, 4, 0, 0),
                      'WN': 49},
                 32: {'VD': 49889.0,
                      'WD': dt.datetime(2017, 12, 11, 0, 0),
                      'WN': 50},
                 33: {'VD': 49428.0,
                      'WD': dt.datetime(2017, 12, 18, 0, 0),
                      'WN': 51},
                 34: {'VD': 44450.0,
                      'WD': dt.datetime(2017, 12, 25, 0, 0),
                      'WN': 52},
                 35: {'VD': 48753.0,
                      'WD': dt.datetime(2018, 1, 1, 0, 0),
                      'WN': 1},
                 36: {'VD': 49280.0,
                      'WD': dt.datetime(2018, 1, 8, 0, 0),
                      'WN': 2},
                 37: {'VD': 48915.0,
                      'WD': dt.datetime(2018, 1, 15, 0, 0),
                      'WN': 3},
                 38: {'VD': 49060.0,
                      'WD': dt.datetime(2018, 1, 22, 0, 0),
                      'WN': 4},
                 39: {'VD': 48683.0,
                      'WD': dt.datetime(2018, 1, 29, 0, 0),
                      'WN': 5},
                 40: {'VD': 48139.0,
                      'WD': dt.datetime(2018, 2, 5, 0, 0),
                      'WN': 6},
                 41: {'VD': 47201.0,
                      'WD': dt.datetime(2018, 2, 12, 0, 0),
                      'WN': 7},
                 42: {'VD': 46668.0,
                      'WD': dt.datetime(2018, 2, 19, 0, 0),
                      'WN': 8},
                 43: {'VD': 45996.0,
                      'WD': dt.datetime(2018, 2, 26, 0, 0),
                      'WN': 9},
                 44: {'VD': 45172.0,
                      'WD': dt.datetime(2018, 3, 5, 0, 0),
                      'WN': 10},
                 45: {'VD': 44460.0,
                      'WD': dt.datetime(2018, 3, 12, 0, 0),
                      'WN': 11},
                 46: {'VD': 42797.0,
                      'WD': dt.datetime(2018, 3, 19, 0, 0),
                      'WN': 12},
                 47: {'VD': 40651.0,
                      'WD': dt.datetime(2018, 3, 26, 0, 0),
                      'WN': 13},
                 48: {'VD': 39598.0,
                      'WD': dt.datetime(2018, 4, 2, 0, 0),
                      'WN': 14},
                 49: {'VD': 38254.0,
                      'WD': dt.datetime(2018, 4, 9, 0, 0),
                      'WN': 15},
                 50: {'VD': 37149.0,
                      'WD': dt.datetime(2018, 4, 16, 0, 0),
                      'WN': 16},
                 51: {'VD': 36207.0,
                      'WD': dt.datetime(2018, 4, 23, 0, 0),
                      'WN': 17}}
                         }

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_NDFW_to_dict(self):
        """
        test conversion of NDFW raw data string to dictionary
        """
        input_str = '2017:04:27:13:46:00:GMT: subject=BMRA.SYSTEM.NDFW, \
        message={TP=2017:04:27:13:45:00:GMT,NR=51,\
        WN=19,WD=2017:05:08:00:00:00:GMT,VD=33470.0,\
        WN=20,WD=2017:05:15:00:00:00:GMT,VD=32540.0,\
        WN=21,WD=2017:05:22:00:00:00:GMT,VD=31910.0,\
        WN=22,WD=2017:05:29:00:00:00:GMT,VD=31510.0,\
        WN=23,WD=2017:06:05:00:00:00:GMT,VD=31450.0,\
        WN=24,WD=2017:06:12:00:00:00:GMT,VD=31160.0,\
        WN=25,WD=2017:06:19:00:00:00:GMT,VD=30740.0,\
        WN=26,WD=2017:06:26:00:00:00:GMT,VD=30660.0,\
        WN=27,WD=2017:07:03:00:00:00:GMT,VD=30640.0,\
        WN=28,WD=2017:07:10:00:00:00:GMT,VD=30530.0,\
        WN=29,WD=2017:07:17:00:00:00:GMT,VD=31530.0,\
        WN=30,WD=2017:07:24:00:00:00:GMT,VD=31008.0,\
        WN=31,WD=2017:07:31:00:00:00:GMT,VD=31196.0,\
        WN=32,WD=2017:08:07:00:00:00:GMT,VD=31910.0,\
        WN=33,WD=2017:08:14:00:00:00:GMT,VD=32760.0,\
        WN=34,WD=2017:08:21:00:00:00:GMT,VD=33478.0,\
        WN=35,WD=2017:08:28:00:00:00:GMT,VD=34404.0,\
        WN=36,WD=2017:09:04:00:00:00:GMT,VD=35527.0,\
        WN=37,WD=2017:09:11:00:00:00:GMT,VD=36113.0,\
        WN=38,WD=2017:09:18:00:00:00:GMT,VD=37376.0,\
        WN=39,WD=2017:09:25:00:00:00:GMT,VD=38374.0,\
        WN=40,WD=2017:10:02:00:00:00:GMT,VD=39447.0,\
        WN=41,WD=2017:10:09:00:00:00:GMT,VD=40529.0,\
        WN=42,WD=2017:10:16:00:00:00:GMT,VD=41868.0,\
        WN=43,WD=2017:10:23:00:00:00:GMT,VD=42347.0,\
        WN=44,WD=2017:10:30:00:00:00:GMT,VD=45010.0,\
        WN=45,WD=2017:11:06:00:00:00:GMT,VD=46171.0,\
        WN=46,WD=2017:11:13:00:00:00:GMT,VD=46767.0,\
        WN=47,WD=2017:11:20:00:00:00:GMT,VD=47544.0,\
        WN=48,WD=2017:11:27:00:00:00:GMT,VD=47765.0,\
        WN=49,WD=2017:12:04:00:00:00:GMT,VD=48803.0,\
        WN=50,WD=2017:12:11:00:00:00:GMT,VD=49389.0,\
        WN=51,WD=2017:12:18:00:00:00:GMT,VD=48928.0,\
        WN=52,WD=2017:12:25:00:00:00:GMT,VD=43950.0,\
        WN=1,WD=2018:01:01:00:00:00:GMT,VD=48253.0,\
        WN=2,WD=2018:01:08:00:00:00:GMT,VD=48780.0,\
        WN=3,WD=2018:01:15:00:00:00:GMT,VD=48415.0,\
        WN=4,WD=2018:01:22:00:00:00:GMT,VD=48560.0,\
        WN=5,WD=2018:01:29:00:00:00:GMT,VD=48183.0,\
        WN=6,WD=2018:02:05:00:00:00:GMT,VD=47639.0,\
        WN=7,WD=2018:02:12:00:00:00:GMT,VD=46701.0,\
        WN=8,WD=2018:02:19:00:00:00:GMT,VD=46168.0,\
        WN=9,WD=2018:02:26:00:00:00:GMT,VD=45496.0,\
        WN=10,WD=2018:03:05:00:00:00:GMT,VD=44672.0,\
        WN=11,WD=2018:03:12:00:00:00:GMT,VD=43960.0,\
        WN=12,WD=2018:03:19:00:00:00:GMT,VD=42297.0,\
        WN=13,WD=2018:03:26:00:00:00:GMT,VD=40151.0,\
        WN=14,WD=2018:04:02:00:00:00:GMT,VD=39098.0,\
        WN=15,WD=2018:04:09:00:00:00:GMT,VD=37754.0,\
        WN=16,WD=2018:04:16:00:00:00:GMT,VD=36649.0,\
        WN=17,WD=2018:04:23:00:00:00:GMT,VD=35707.0}'

        expected_dict = {'received_time' : dt.datetime(2017, 4, 27, 13, 46, 0),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'NDFW',
                         'TP' : dt.datetime(2017, 4, 27, 13, 45),
                         'data_points' : {1: {'VD': 33470.0,
                     'WD': dt.datetime(2017, 5, 8, 0, 0),
                     'WN': 19},
                 2: {'VD': 32540.0,
                     'WD': dt.datetime(2017, 5, 15, 0, 0),
                     'WN': 20},
                 3: {'VD': 31910.0,
                     'WD': dt.datetime(2017, 5, 22, 0, 0),
                     'WN': 21},
                 4: {'VD': 31510.0,
                     'WD': dt.datetime(2017, 5, 29, 0, 0),
                     'WN': 22},
                 5: {'VD': 31450.0,
                     'WD': dt.datetime(2017, 6, 5, 0, 0),
                     'WN': 23},
                 6: {'VD': 31160.0,
                     'WD': dt.datetime(2017, 6, 12, 0, 0),
                     'WN': 24},
                 7: {'VD': 30740.0,
                     'WD': dt.datetime(2017, 6, 19, 0, 0),
                     'WN': 25},
                 8: {'VD': 30660.0,
                     'WD': dt.datetime(2017, 6, 26, 0, 0),
                     'WN': 26},
                 9: {'VD': 30640.0,
                     'WD': dt.datetime(2017, 7, 3, 0, 0),
                     'WN': 27},
                 10: {'VD': 30530.0,
                      'WD': dt.datetime(2017, 7, 10, 0, 0),
                      'WN': 28},
                 11: {'VD': 31530.0,
                      'WD': dt.datetime(2017, 7, 17, 0, 0),
                      'WN': 29},
                 12: {'VD': 31008.0,
                      'WD': dt.datetime(2017, 7, 24, 0, 0),
                      'WN': 30},
                 13: {'VD': 31196.0,
                      'WD': dt.datetime(2017, 7, 31, 0, 0),
                      'WN': 31},
                 14: {'VD': 31910.0,
                      'WD': dt.datetime(2017, 8, 7, 0, 0),
                      'WN': 32},
                 15: {'VD': 32760.0,
                      'WD': dt.datetime(2017, 8, 14, 0, 0),
                      'WN': 33},
                 16: {'VD': 33478.0,
                      'WD': dt.datetime(2017, 8, 21, 0, 0),
                      'WN': 34},
                 17: {'VD': 34404.0,
                      'WD': dt.datetime(2017, 8, 28, 0, 0),
                      'WN': 35},
                 18: {'VD': 35527.0,
                      'WD': dt.datetime(2017, 9, 4, 0, 0),
                      'WN': 36},
                 19: {'VD': 36113.0,
                      'WD': dt.datetime(2017, 9, 11, 0, 0),
                      'WN': 37},
                 20: {'VD': 37376.0,
                      'WD': dt.datetime(2017, 9, 18, 0, 0),
                      'WN': 38},
                 21: {'VD': 38374.0,
                      'WD': dt.datetime(2017, 9, 25, 0, 0),
                      'WN': 39},
                 22: {'VD': 39447.0,
                      'WD': dt.datetime(2017, 10, 2, 0, 0),
                      'WN': 40},
                 23: {'VD': 40529.0,
                      'WD': dt.datetime(2017, 10, 9, 0, 0),
                      'WN': 41},
                 24: {'VD': 41868.0,
                      'WD': dt.datetime(2017, 10, 16, 0, 0),
                      'WN': 42},
                 25: {'VD': 42347.0,
                      'WD': dt.datetime(2017, 10, 23, 0, 0),
                      'WN': 43},
                 26: {'VD': 45010.0,
                      'WD': dt.datetime(2017, 10, 30, 0, 0),
                      'WN': 44},
                 27: {'VD': 46171.0,
                      'WD': dt.datetime(2017, 11, 6, 0, 0),
                      'WN': 45},
                 28: {'VD': 46767.0,
                      'WD': dt.datetime(2017, 11, 13, 0, 0),
                      'WN': 46},
                 29: {'VD': 47544.0,
                      'WD': dt.datetime(2017, 11, 20, 0, 0),
                      'WN': 47},
                 30: {'VD': 47765.0,
                      'WD': dt.datetime(2017, 11, 27, 0, 0),
                      'WN': 48},
                 31: {'VD': 48803.0,
                      'WD': dt.datetime(2017, 12, 4, 0, 0),
                      'WN': 49},
                 32: {'VD': 49389.0,
                      'WD': dt.datetime(2017, 12, 11, 0, 0),
                      'WN': 50},
                 33: {'VD': 48928.0,
                      'WD': dt.datetime(2017, 12, 18, 0, 0),
                      'WN': 51},
                 34: {'VD': 43950.0,
                      'WD': dt.datetime(2017, 12, 25, 0, 0),
                      'WN': 52},
                 35: {'VD': 48253.0,
                      'WD': dt.datetime(2018, 1, 1, 0, 0),
                      'WN': 1},
                 36: {'VD': 48780.0,
                      'WD': dt.datetime(2018, 1, 8, 0, 0),
                      'WN': 2},
                 37: {'VD': 48415.0,
                      'WD': dt.datetime(2018, 1, 15, 0, 0),
                      'WN': 3},
                 38: {'VD': 48560.0,
                      'WD': dt.datetime(2018, 1, 22, 0, 0),
                      'WN': 4},
                 39: {'VD': 48183.0,
                      'WD': dt.datetime(2018, 1, 29, 0, 0),
                      'WN': 5},
                 40: {'VD': 47639.0,
                      'WD': dt.datetime(2018, 2, 5, 0, 0),
                      'WN': 6},
                 41: {'VD': 46701.0,
                      'WD': dt.datetime(2018, 2, 12, 0, 0),
                      'WN': 7},
                 42: {'VD': 46168.0,
                      'WD': dt.datetime(2018, 2, 19, 0, 0),
                      'WN': 8},
                 43: {'VD': 45496.0,
                      'WD': dt.datetime(2018, 2, 26, 0, 0),
                      'WN': 9},
                 44: {'VD': 44672.0,
                      'WD': dt.datetime(2018, 3, 5, 0, 0),
                      'WN': 10},
                 45: {'VD': 43960.0,
                      'WD': dt.datetime(2018, 3, 12, 0, 0),
                      'WN': 11},
                 46: {'VD': 42297.0,
                      'WD': dt.datetime(2018, 3, 19, 0, 0),
                      'WN': 12},
                 47: {'VD': 40151.0,
                      'WD': dt.datetime(2018, 3, 26, 0, 0),
                      'WN': 13},
                 48: {'VD': 39098.0,
                      'WD': dt.datetime(2018, 4, 2, 0, 0),
                      'WN': 14},
                 49: {'VD': 37754.0,
                      'WD': dt.datetime(2018, 4, 9, 0, 0),
                      'WN': 15},
                 50: {'VD': 36649.0,
                      'WD': dt.datetime(2018, 4, 16, 0, 0),
                      'WN': 16},
                 51: {'VD': 35707.0,
                      'WD': dt.datetime(2018, 4, 23, 0, 0),
                      'WN': 17}}
                         }

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_OCNMFW_to_dict(self):
        """
        test conversion of OCNMFW raw data string to dictionary
        """
        input_str = '2018:01:04:13:35:52:GMT: subject=BMRA.SYSTEM.OCNMFW, \
        message={TP=2018:01:04:13:31:00:GMT,NR=51,\
        WN=3,WD=2018:01:15:00:00:00:GMT,VM=10087.0,\
        WN=4,WD=2018:01:22:00:00:00:GMT,VM=9690.0,\
        WN=5,WD=2018:01:29:00:00:00:GMT,VM=9386.0,\
        WN=6,WD=2018:02:05:00:00:00:GMT,VM=10928.0,\
        WN=7,WD=2018:02:12:00:00:00:GMT,VM=12311.0,\
        WN=8,WD=2018:02:19:00:00:00:GMT,VM=14367.0,\
        WN=9,WD=2018:02:26:00:00:00:GMT,VM=13735.0,\
        WN=10,WD=2018:03:05:00:00:00:GMT,VM=12289.0,\
        WN=11,WD=2018:03:12:00:00:00:GMT,VM=13818.0,\
        WN=12,WD=2018:03:19:00:00:00:GMT,VM=15448.0,\
        WN=13,WD=2018:03:26:00:00:00:GMT,VM=16102.0,\
        WN=14,WD=2018:04:02:00:00:00:GMT,VM=11437.0,\
        WN=15,WD=2018:04:09:00:00:00:GMT,VM=12125.0,\
        WN=16,WD=2018:04:16:00:00:00:GMT,VM=12122.0,\
        WN=17,WD=2018:04:23:00:00:00:GMT,VM=13588.0,\
        WN=18,WD=2018:04:30:00:00:00:GMT,VM=13438.0,\
        WN=19,WD=2018:05:07:00:00:00:GMT,VM=12305.0,\
        WN=20,WD=2018:05:14:00:00:00:GMT,VM=14366.0,\
        WN=21,WD=2018:05:21:00:00:00:GMT,VM=14562.0,\
        WN=22,WD=2018:05:28:00:00:00:GMT,VM=17926.0,\
        WN=23,WD=2018:06:04:00:00:00:GMT,VM=13759.0,\
        WN=24,WD=2018:06:11:00:00:00:GMT,VM=13488.0,\
        WN=25,WD=2018:06:18:00:00:00:GMT,VM=13715.0,\
        WN=26,WD=2018:06:25:00:00:00:GMT,VM=12919.0,\
        WN=27,WD=2018:07:02:00:00:00:GMT,VM=11096.0,\
        WN=28,WD=2018:07:09:00:00:00:GMT,VM=9618.0,\
        WN=29,WD=2018:07:16:00:00:00:GMT,VM=12856.0,\
        WN=30,WD=2018:07:23:00:00:00:GMT,VM=14795.0,\
        WN=31,WD=2018:07:30:00:00:00:GMT,VM=15440.0,\
        WN=32,WD=2018:08:06:00:00:00:GMT,VM=15990.0,\
        WN=33,WD=2018:08:13:00:00:00:GMT,VM=15907.0,\
        WN=34,WD=2018:08:20:00:00:00:GMT,VM=15868.0,\
        WN=35,WD=2018:08:27:00:00:00:GMT,VM=16813.0,\
        WN=36,WD=2018:09:03:00:00:00:GMT,VM=15632.0,\
        WN=37,WD=2018:09:10:00:00:00:GMT,VM=12593.0,\
        WN=38,WD=2018:09:17:00:00:00:GMT,VM=12833.0,\
        WN=39,WD=2018:09:24:00:00:00:GMT,VM=13727.0,\
        WN=40,WD=2018:10:01:00:00:00:GMT,VM=12985.0,\
        WN=41,WD=2018:10:08:00:00:00:GMT,VM=11670.0,\
        WN=42,WD=2018:10:15:00:00:00:GMT,VM=10954.0,\
        WN=43,WD=2018:10:22:00:00:00:GMT,VM=10741.0,\
        WN=44,WD=2018:10:29:00:00:00:GMT,VM=9306.0,\
        WN=45,WD=2018:11:05:00:00:00:GMT,VM=8613.0,\
        WN=46,WD=2018:11:12:00:00:00:GMT,VM=8440.0,\
        WN=47,WD=2018:11:19:00:00:00:GMT,VM=7211.0,\
        WN=48,WD=2018:11:26:00:00:00:GMT,VM=7408.0,\
        WN=49,WD=2018:12:03:00:00:00:GMT,VM=6461.0,\
        WN=50,WD=2018:12:10:00:00:00:GMT,VM=6399.0,\
        WN=51,WD=2018:12:17:00:00:00:GMT,VM=5329.0,\
        WN=52,WD=2018:12:24:00:00:00:GMT,VM=11976.0,\
        WN=1,WD=2018:12:31:00:00:00:GMT,VM=7743.0}'

        expected_dict = {'received_time' : dt.datetime(2018, 1, 4, 13, 35, 52),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'OCNMFW',
                         'TP' : dt.datetime(2018, 1, 4, 13, 31),
                         'data_points' : {1: {'VM': 10087.0,
                     'WD': dt.datetime(2018, 1, 15, 0, 0),
                     'WN': 3},
                 2: {'VM': 9690.0,
                     'WD': dt.datetime(2018, 1, 22, 0, 0),
                     'WN': 4},
                 3: {'VM': 9386.0,
                     'WD': dt.datetime(2018, 1, 29, 0, 0),
                     'WN': 5},
                 4: {'VM': 10928.0,
                     'WD': dt.datetime(2018, 2, 5, 0, 0),
                     'WN': 6},
                 5: {'VM': 12311.0,
                     'WD': dt.datetime(2018, 2, 12, 0, 0),
                     'WN': 7},
                 6: {'VM': 14367.0,
                     'WD': dt.datetime(2018, 2, 19, 0, 0),
                     'WN': 8},
                 7: {'VM': 13735.0,
                     'WD': dt.datetime(2018, 2, 26, 0, 0),
                     'WN': 9},
                 8: {'VM': 12289.0,
                     'WD': dt.datetime(2018, 3, 5, 0, 0),
                     'WN': 10},
                 9: {'VM': 13818.0,
                     'WD': dt.datetime(2018, 3, 12, 0, 0),
                     'WN': 11},
                 10: {'VM': 15448.0,
                      'WD': dt.datetime(2018, 3, 19, 0, 0),
                      'WN': 12},
                 11: {'VM': 16102.0,
                      'WD': dt.datetime(2018, 3, 26, 0, 0),
                      'WN': 13},
                 12: {'VM': 11437.0,
                      'WD': dt.datetime(2018, 4, 2, 0, 0),
                      'WN': 14},
                 13: {'VM': 12125.0,
                      'WD': dt.datetime(2018, 4, 9, 0, 0),
                      'WN': 15},
                 14: {'VM': 12122.0,
                      'WD': dt.datetime(2018, 4, 16, 0, 0),
                      'WN': 16},
                 15: {'VM': 13588.0,
                      'WD': dt.datetime(2018, 4, 23, 0, 0),
                      'WN': 17},
                 16: {'VM': 13438.0,
                      'WD': dt.datetime(2018, 4, 30, 0, 0),
                      'WN': 18},
                 17: {'VM': 12305.0,
                      'WD': dt.datetime(2018, 5, 7, 0, 0),
                      'WN': 19},
                 18: {'VM': 14366.0,
                      'WD': dt.datetime(2018, 5, 14, 0, 0),
                      'WN': 20},
                 19: {'VM': 14562.0,
                      'WD': dt.datetime(2018, 5, 21, 0, 0),
                      'WN': 21},
                 20: {'VM': 17926.0,
                      'WD': dt.datetime(2018, 5, 28, 0, 0),
                      'WN': 22},
                 21: {'VM': 13759.0,
                      'WD': dt.datetime(2018, 6, 4, 0, 0),
                      'WN': 23},
                 22: {'VM': 13488.0,
                      'WD': dt.datetime(2018, 6, 11, 0, 0),
                      'WN': 24},
                 23: {'VM': 13715.0,
                      'WD': dt.datetime(2018, 6, 18, 0, 0),
                      'WN': 25},
                 24: {'VM': 12919.0,
                      'WD': dt.datetime(2018, 6, 25, 0, 0),
                      'WN': 26},
                 25: {'VM': 11096.0,
                      'WD': dt.datetime(2018, 7, 2, 0, 0),
                      'WN': 27},
                 26: {'VM': 9618.0,
                      'WD': dt.datetime(2018, 7, 9, 0, 0),
                      'WN': 28},
                 27: {'VM': 12856.0,
                      'WD': dt.datetime(2018, 7, 16, 0, 0),
                      'WN': 29},
                 28: {'VM': 14795.0,
                      'WD': dt.datetime(2018, 7, 23, 0, 0),
                      'WN': 30},
                 29: {'VM': 15440.0,
                      'WD': dt.datetime(2018, 7, 30, 0, 0),
                      'WN': 31},
                 30: {'VM': 15990.0,
                      'WD': dt.datetime(2018, 8, 6, 0, 0),
                      'WN': 32},
                 31: {'VM': 15907.0,
                      'WD': dt.datetime(2018, 8, 13, 0, 0),
                      'WN': 33},
                 32: {'VM': 15868.0,
                      'WD': dt.datetime(2018, 8, 20, 0, 0),
                      'WN': 34},
                 33: {'VM': 16813.0,
                      'WD': dt.datetime(2018, 8, 27, 0, 0),
                      'WN': 35},
                 34: {'VM': 15632.0,
                      'WD': dt.datetime(2018, 9, 3, 0, 0),
                      'WN': 36},
                 35: {'VM': 12593.0,
                      'WD': dt.datetime(2018, 9, 10, 0, 0),
                      'WN': 37},
                 36: {'VM': 12833.0,
                      'WD': dt.datetime(2018, 9, 17, 0, 0),
                      'WN': 38},
                 37: {'VM': 13727.0,
                      'WD': dt.datetime(2018, 9, 24, 0, 0),
                      'WN': 39},
                 38: {'VM': 12985.0,
                      'WD': dt.datetime(2018, 10, 1, 0, 0),
                      'WN': 40},
                 39: {'VM': 11670.0,
                      'WD': dt.datetime(2018, 10, 8, 0, 0),
                      'WN': 41},
                 40: {'VM': 10954.0,
                      'WD': dt.datetime(2018, 10, 15, 0, 0),
                      'WN': 42},
                 41: {'VM': 10741.0,
                      'WD': dt.datetime(2018, 10, 22, 0, 0),
                      'WN': 43},
                 42: {'VM': 9306.0,
                      'WD': dt.datetime(2018, 10, 29, 0, 0),
                      'WN': 44},
                 43: {'VM': 8613.0,
                      'WD': dt.datetime(2018, 11, 5, 0, 0),
                      'WN': 45},
                 44: {'VM': 8440.0,
                      'WD': dt.datetime(2018, 11, 12, 0, 0),
                      'WN': 46},
                 45: {'VM': 7211.0,
                      'WD': dt.datetime(2018, 11, 19, 0, 0),
                      'WN': 47},
                 46: {'VM': 7408.0,
                      'WD': dt.datetime(2018, 11, 26, 0, 0),
                      'WN': 48},
                 47: {'VM': 6461.0,
                      'WD': dt.datetime(2018, 12, 3, 0, 0),
                      'WN': 49},
                 48: {'VM': 6399.0,
                      'WD': dt.datetime(2018, 12, 10, 0, 0),
                      'WN': 50},
                 49: {'VM': 5329.0,
                      'WD': dt.datetime(2018, 12, 17, 0, 0),
                      'WN': 51},
                 50: {'VM': 11976.0,
                      'WD': dt.datetime(2018, 12, 24, 0, 0),
                      'WN': 52},
                 51: {'VM': 7743.0,
                      'WD': dt.datetime(2018, 12, 31, 0, 0),
                      'WN': 1}}
                         }

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_OCNMFW2_to_dict(self):
        """
        test conversion of OCNMFW2 raw data string to dictionary
        """
        input_str = '2018:01:04:13:37:17:GMT: subject=BMRA.SYSTEM.OCNMFW2, \
        message={TP=2018:01:04:13:35:00:GMT,NR=51,\
        WN=3,CY=2018,DM=13753.0,WN=4,CY=2018,DM=13351.0,\
        WN=5,CY=2018,DM=13068.0,WN=6,CY=2018,DM=14611.0,\
        WN=7,CY=2018,DM=16020.0,WN=8,CY=2018,DM=18103.0,\
        WN=9,CY=2018,DM=17484.0,WN=10,CY=2018,DM=16061.0,\
        WN=11,CY=2018,DM=17612.0,WN=12,CY=2018,DM=19269.0,\
        WN=13,CY=2018,DM=19904.0,WN=14,CY=2018,DM=15268.0,\
        WN=15,CY=2018,DM=15988.0,WN=16,CY=2018,DM=16792.0,\
        WN=17,CY=2018,DM=18282.0,WN=18,CY=2018,DM=17764.0,\
        WN=19,CY=2018,DM=16634.0,WN=20,CY=2018,DM=18714.0,\
        WN=21,CY=2018,DM=18944.0,WN=22,CY=2018,DM=22335.0,\
        WN=23,CY=2018,DM=18571.0,WN=24,CY=2018,DM=18305.0,\
        WN=25,CY=2018,DM=18540.0,WN=26,CY=2018,DM=17339.0,\
        WN=27,CY=2018,DM=15684.0,WN=28,CY=2018,DM=14211.0,\
        WN=29,CY=2018,DM=17441.0,WN=30,CY=2018,DM=19378.0,\
        WN=31,CY=2018,DM=20504.0,WN=32,CY=2018,DM=21038.0,\
        WN=33,CY=2018,DM=20934.0,WN=34,CY=2018,DM=20876.0,\
        WN=35,CY=2018,DM=21033.0,WN=36,CY=2018,DM=19809.0,\
        WN=37,CY=2018,DM=17131.0,WN=38,CY=2018,DM=17342.0,\
        WN=39,CY=2018,DM=18612.0,WN=40,CY=2018,DM=17835.0,\
        WN=41,CY=2018,DM=16493.0,WN=42,CY=2018,DM=15740.0,\
        WN=43,CY=2018,DM=15508.0,WN=44,CY=2018,DM=14023.0,\
        WN=45,CY=2018,DM=13305.0,WN=46,CY=2018,DM=13106.0,\
        WN=47,CY=2018,DM=11863.0,WN=48,CY=2018,DM=12052.0,\
        WN=49,CY=2018,DM=11081.0,WN=50,CY=2018,DM=10995.0,\
        WN=51,CY=2018,DM=11229.0,WN=52,CY=2018,DM=18039.0,\
        WN=1,CY=2019,DM=13693.0}'

        expected_dict = {'received_time' : dt.datetime(2018, 1, 4, 13, 37, 17),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'OCNMFW2',
                         'TP' : dt.datetime(2018, 1, 4, 13, 35),
                         'data_points' : {
                 1: {'CY': 2018, 'DM': 13753.0, 'WN': 3},
                 2: {'CY': 2018, 'DM': 13351.0, 'WN': 4},
                 3: {'CY': 2018, 'DM': 13068.0, 'WN': 5},
                 4: {'CY': 2018, 'DM': 14611.0, 'WN': 6},
                 5: {'CY': 2018, 'DM': 16020.0, 'WN': 7},
                 6: {'CY': 2018, 'DM': 18103.0, 'WN': 8},
                 7: {'CY': 2018, 'DM': 17484.0, 'WN': 9},
                 8: {'CY': 2018, 'DM': 16061.0, 'WN': 10},
                 9: {'CY': 2018, 'DM': 17612.0, 'WN': 11},
                 10: {'CY': 2018, 'DM': 19269.0, 'WN': 12},
                 11: {'CY': 2018, 'DM': 19904.0, 'WN': 13},
                 12: {'CY': 2018, 'DM': 15268.0, 'WN': 14},
                 13: {'CY': 2018, 'DM': 15988.0, 'WN': 15},
                 14: {'CY': 2018, 'DM': 16792.0, 'WN': 16},
                 15: {'CY': 2018, 'DM': 18282.0, 'WN': 17},
                 16: {'CY': 2018, 'DM': 17764.0, 'WN': 18},
                 17: {'CY': 2018, 'DM': 16634.0, 'WN': 19},
                 18: {'CY': 2018, 'DM': 18714.0, 'WN': 20},
                 19: {'CY': 2018, 'DM': 18944.0, 'WN': 21},
                 20: {'CY': 2018, 'DM': 22335.0, 'WN': 22},
                 21: {'CY': 2018, 'DM': 18571.0, 'WN': 23},
                 22: {'CY': 2018, 'DM': 18305.0, 'WN': 24},
                 23: {'CY': 2018, 'DM': 18540.0, 'WN': 25},
                 24: {'CY': 2018, 'DM': 17339.0, 'WN': 26},
                 25: {'CY': 2018, 'DM': 15684.0, 'WN': 27},
                 26: {'CY': 2018, 'DM': 14211.0, 'WN': 28},
                 27: {'CY': 2018, 'DM': 17441.0, 'WN': 29},
                 28: {'CY': 2018, 'DM': 19378.0, 'WN': 30},
                 29: {'CY': 2018, 'DM': 20504.0, 'WN': 31},
                 30: {'CY': 2018, 'DM': 21038.0, 'WN': 32},
                 31: {'CY': 2018, 'DM': 20934.0, 'WN': 33},
                 32: {'CY': 2018, 'DM': 20876.0, 'WN': 34},
                 33: {'CY': 2018, 'DM': 21033.0, 'WN': 35},
                 34: {'CY': 2018, 'DM': 19809.0, 'WN': 36},
                 35: {'CY': 2018, 'DM': 17131.0, 'WN': 37},
                 36: {'CY': 2018, 'DM': 17342.0, 'WN': 38},
                 37: {'CY': 2018, 'DM': 18612.0, 'WN': 39},
                 38: {'CY': 2018, 'DM': 17835.0, 'WN': 40},
                 39: {'CY': 2018, 'DM': 16493.0, 'WN': 41},
                 40: {'CY': 2018, 'DM': 15740.0, 'WN': 42},
                 41: {'CY': 2018, 'DM': 15508.0, 'WN': 43},
                 42: {'CY': 2018, 'DM': 14023.0, 'WN': 44},
                 43: {'CY': 2018, 'DM': 13305.0, 'WN': 45},
                 44: {'CY': 2018, 'DM': 13106.0, 'WN': 46},
                 45: {'CY': 2018, 'DM': 11863.0, 'WN': 47},
                 46: {'CY': 2018, 'DM': 12052.0, 'WN': 48},
                 47: {'CY': 2018, 'DM': 11081.0, 'WN': 49},
                 48: {'CY': 2018, 'DM': 10995.0, 'WN': 50},
                 49: {'CY': 2018, 'DM': 11229.0, 'WN': 51},
                 50: {'CY': 2018, 'DM': 18039.0, 'WN': 52},
                 51: {'CY': 2019, 'DM': 13693.0, 'WN': 1}}
                }

        self.assertEqual(message_to_dict(input_str), expected_dict)

    def test_fou2t52w_to_dict(self):
        """
        test conversion of FOU2T52W raw data string to dictionary
        """
        input_str = '2018:01:04:13:37:11:GMT: subject=BMRA.SYSTEM.FOU2T52W, message={TP=2018:01:04:13:31:00:GMT,NR=679,WN=3,CY=2018,FT=WIND,OU=6447.0,WN=3,CY=2018,FT=PS,OU=2828.0,WN=3,CY=2018,FT=OTHER,OU=6.0,WN=3,CY=2018,FT=OIL,OU=0.0,WN=3,CY=2018,FT=OCGT,OU=837.0,WN=3,CY=2018,FT=NUCLEAR,OU=6990.0,WN=3,CY=2018,FT=NPSHYD,OU=1051.0,WN=3,CY=2018,FT=INTNED,OU=1000.0,WN=3,CY=2018,FT=INTIRL,OU=500.0,WN=3,CY=2018,FT=INTFR,OU=2000.0,WN=3,CY=2018,FT=INTEW,OU=500.0,WN=3,CY=2018,FT=COAL,OU=12786.0,WN=3,CY=2018,FT=CCGT,OU=29578.0,WN=3,CY=2018,FT=BIOMASS,OU=2130.0,WN=4,CY=2018,FT=WIND,OU=6467.0,WN=4,CY=2018,FT=PS,OU=2828.0,WN=4,CY=2018,FT=OTHER,OU=6.0,WN=4,CY=2018,FT=OIL,OU=0.0,WN=4,CY=2018,FT=OCGT,OU=837.0,WN=4,CY=2018,FT=NUCLEAR,OU=6728.0,WN=4,CY=2018,FT=NPSHYD,OU=1051.0,WN=4,CY=2018,FT=INTNED,OU=1000.0,WN=4,CY=2018,FT=INTIRL,OU=500.0,WN=4,CY=2018,FT=INTFR,OU=2000.0,WN=4,CY=2018,FT=INTEW,OU=500.0,WN=4,CY=2018,FT=COAL,OU=12786.0,WN=4,CY=2018,FT=CCGT,OU=29583.0,WN=4,CY=2018,FT=BIOMASS,OU=2165.0,WN=5,CY=2018,FT=WIND,OU=6474.0,WN=5,CY=2018,FT=PS,OU=2828.0,WN=5,CY=2018,FT=OTHER,OU=6.0,WN=5,CY=2018,FT=OIL,OU=0.0,WN=5,CY=2018,FT=OCGT,OU=837.0,WN=5,CY=2018,FT=NUCLEAR,OU=6108.0,WN=5,CY=2018,FT=NPSHYD,OU=1051.0,WN=5,CY=2018,FT=INTNED,OU=1000.0,WN=5,CY=2018,FT=INTIRL,OU=500.0,WN=5,CY=2018,FT=INTFR,OU=2000.0,WN=5,CY=2018,FT=INTEW,OU=500.0,WN=5,CY=2018,FT=COAL,OU=12786.0,WN=5,CY=2018,FT=CCGT,OU=29143.0,WN=5,CY=2018,FT=BIOMASS,OU=2165.0,WN=6,CY=2018,FT=WIND,OU=5923.0,WN=6,CY=2018,FT=PS,OU=2828.0,WN=6,CY=2018,FT=OTHER,OU=6.0,WN=6,CY=2018,FT=OIL,OU=0.0,WN=6,CY=2018,FT=OCGT,OU=837.0,WN=6,CY=2018,FT=NUCLEAR,OU=7271.0,WN=6,CY=2018,FT=NPSHYD,OU=1051.0,WN=6,CY=2018,FT=INTNED,OU=1000.0,WN=6,CY=2018,FT=INTIRL,OU=500.0,WN=6,CY=2018,FT=INTFR,OU=2000.0,WN=6,CY=2018,FT=INTEW,OU=500.0,WN=6,CY=2018,FT=COAL,OU=12786.0,WN=6,CY=2018,FT=CCGT,OU=29912.0,WN=6,CY=2018,FT=BIOMASS,OU=2297.0,WN=7,CY=2018,FT=WIND,OU=5939.0,WN=7,CY=2018,FT=PS,OU=2828.0,WN=7,CY=2018,FT=OTHER,OU=6.0,WN=7,CY=2018,FT=OIL,OU=0.0,WN=7,CY=2018,FT=OCGT,OU=837.0,WN=7,CY=2018,FT=NUCLEAR,OU=7418.0,WN=7,CY=2018,FT=NPSHYD,OU=1051.0,WN=7,CY=2018,FT=INTNED,OU=1000.0,WN=7,CY=2018,FT=INTIRL,OU=500.0,WN=7,CY=2018,FT=INTFR,OU=2000.0,WN=7,CY=2018,FT=INTEW,OU=500.0,WN=7,CY=2018,FT=COAL,OU=12786.0,WN=7,CY=2018,FT=CCGT,OU=30158.0,WN=7,CY=2018,FT=BIOMASS,OU=2297.0,WN=8,CY=2018,FT=WIND,OU=5939.0,WN=8,CY=2018,FT=PS,OU=2828.0,WN=8,CY=2018,FT=OTHER,OU=6.0,WN=8,CY=2018,FT=OIL,OU=0.0,WN=8,CY=2018,FT=OCGT,OU=837.0,WN=8,CY=2018,FT=NUCLEAR,OU=7751.0,WN=8,CY=2018,FT=NPSHYD,OU=1051.0,WN=8,CY=2018,FT=INTNED,OU=1000.0,WN=8,CY=2018,FT=INTIRL,OU=500.0,WN=8,CY=2018,FT=INTFR,OU=2000.0,WN=8,CY=2018,FT=INTEW,OU=500.0,WN=8,CY=2018,FT=COAL,OU=13266.0,WN=8,CY=2018,FT=CCGT,OU=30351.0,WN=8,CY=2018,FT=BIOMASS,OU=2374.0,WN=9,CY=2018,FT=WIND,OU=5955.0,WN=9,CY=2018,FT=PS,OU=2828.0,WN=9,CY=2018,FT=OTHER,OU=6.0,WN=9,CY=2018,FT=OIL,OU=0.0,WN=9,CY=2018,FT=OCGT,OU=837.0,WN=9,CY=2018,FT=NUCLEAR,OU=7708.0,WN=9,CY=2018,FT=NPSHYD,OU=1051.0,WN=9,CY=2018,FT=INTNED,OU=1000.0,WN=9,CY=2018,FT=INTIRL,OU=500.0,WN=9,CY=2018,FT=INTFR,OU=2000.0,WN=9,CY=2018,FT=INTEW,OU=500.0,WN=9,CY=2018,FT=COAL,OU=13266.0,WN=9,CY=2018,FT=CCGT,OU=29204.0,WN=9,CY=2018,FT=BIOMASS,OU=2429.0,WN=10,CY=2018,FT=WIND,OU=4761.0,WN=10,CY=2018,FT=PS,OU=2828.0,WN=10,CY=2018,FT=OTHER,OU=6.0,WN=10,CY=2018,FT=OIL,OU=0.0,WN=10,CY=2018,FT=OCGT,OU=837.0,WN=10,CY=2018,FT=NUCLEAR,OU=7461.0,WN=10,CY=2018,FT=NPSHYD,OU=1051.0,WN=10,CY=2018,FT=INTNED,OU=1000.0,WN=10,CY=2018,FT=INTIRL,OU=500.0,WN=10,CY=2018,FT=INTFR,OU=2000.0,WN=10,CY=2018,FT=INTEW,OU=500.0,WN=10,CY=2018,FT=COAL,OU=13266.0,WN=10,CY=2018,FT=CCGT,OU=28372.0,WN=10,CY=2018,FT=BIOMASS,OU=2429.0,WN=11,CY=2018,FT=WIND,OU=4761.0,WN=11,CY=2018,FT=PS,OU=2628.0,WN=11,CY=2018,FT=OTHER,OU=6.0,WN=11,CY=2018,FT=OIL,OU=0.0,WN=11,CY=2018,FT=OCGT,OU=837.0,WN=11,CY=2018,FT=NUCLEAR,OU=7640.0,WN=11,CY=2018,FT=NPSHYD,OU=1051.0,WN=11,CY=2018,FT=INTNED,OU=1000.0,WN=11,CY=2018,FT=INTIRL,OU=500.0,WN=11,CY=2018,FT=INTFR,OU=2000.0,WN=11,CY=2018,FT=INTEW,OU=500.0,WN=11,CY=2018,FT=COAL,OU=13266.0,WN=11,CY=2018,FT=CCGT,OU=29067.0,WN=11,CY=2018,FT=BIOMASS,OU=2496.0,WN=12,CY=2018,FT=WIND,OU=4761.0,WN=12,CY=2018,FT=PS,OU=2628.0,WN=12,CY=2018,FT=OTHER,OU=6.0,WN=12,CY=2018,FT=OIL,OU=0.0,WN=12,CY=2018,FT=OCGT,OU=837.0,WN=12,CY=2018,FT=NUCLEAR,OU=7462.0,WN=12,CY=2018,FT=NPSHYD,OU=1011.0,WN=12,CY=2018,FT=INTNED,OU=1000.0,WN=12,CY=2018,FT=INTIRL,OU=500.0,WN=12,CY=2018,FT=INTFR,OU=2000.0,WN=12,CY=2018,FT=INTEW,OU=500.0,WN=12,CY=2018,FT=COAL,OU=13266.0,WN=12,CY=2018,FT=CCGT,OU=29942.0,WN=12,CY=2018,FT=BIOMASS,OU=2496.0,WN=13,CY=2018,FT=WIND,OU=4703.0,WN=13,CY=2018,FT=PS,OU=2340.0,WN=13,CY=2018,FT=OTHER,OU=6.0,WN=13,CY=2018,FT=OIL,OU=0.0,WN=13,CY=2018,FT=OCGT,OU=837.0,WN=13,CY=2018,FT=NUCLEAR,OU=7757.0,WN=13,CY=2018,FT=NPSHYD,OU=1011.0,WN=13,CY=2018,FT=INTNED,OU=1000.0,WN=13,CY=2018,FT=INTIRL,OU=500.0,WN=13,CY=2018,FT=INTFR,OU=2000.0,WN=13,CY=2018,FT=INTEW,OU=500.0,WN=13,CY=2018,FT=COAL,OU=13266.0,WN=13,CY=2018,FT=CCGT,OU=28188.0,WN=13,CY=2018,FT=BIOMASS,OU=2496.0,WN=14,CY=2018,FT=WIND,OU=3636.0,WN=14,CY=2018,FT=PS,OU=2052.0,WN=14,CY=2018,FT=OTHER,OU=6.0,WN=14,CY=2018,FT=OIL,OU=0.0,WN=14,CY=2018,FT=OCGT,OU=697.0,WN=14,CY=2018,FT=NUCLEAR,OU=8089.0,WN=14,CY=2018,FT=NPSHYD,OU=891.0,WN=14,CY=2018,FT=INTNED,OU=1000.0,WN=14,CY=2018,FT=INTIRL,OU=500.0,WN=14,CY=2018,FT=INTFR,OU=2000.0,WN=14,CY=2018,FT=INTEW,OU=500.0,WN=14,CY=2018,FT=COAL,OU=11096.0,WN=14,CY=2018,FT=CCGT,OU=25905.0,WN=14,CY=2018,FT=BIOMASS,OU=2496.0,WN=15,CY=2018,FT=WIND,OU=3635.0,WN=15,CY=2018,FT=PS,OU=2052.0,WN=15,CY=2018,FT=OTHER,OU=6.0,WN=15,CY=2018,FT=OIL,OU=0.0,WN=15,CY=2018,FT=OCGT,OU=697.0,WN=15,CY=2018,FT=NUCLEAR,OU=7752.0,WN=15,CY=2018,FT=NPSHYD,OU=899.0,WN=15,CY=2018,FT=INTNED,OU=1000.0,WN=15,CY=2018,FT=INTIRL,OU=500.0,WN=15,CY=2018,FT=INTFR,OU=2000.0,WN=15,CY=2018,FT=INTEW,OU=500.0,WN=15,CY=2018,FT=COAL,OU=10111.0,WN=15,CY=2018,FT=CCGT,OU=26740.0,WN=15,CY=2018,FT=BIOMASS,OU=2496.0,WN=16,CY=2018,FT=WIND,OU=3634.0,WN=16,CY=2018,FT=PS,OU=2052.0,WN=16,CY=2018,FT=OTHER,OU=6.0,WN=16,CY=2018,FT=OIL,OU=0.0,WN=16,CY=2018,FT=OCGT,OU=777.0,WN=16,CY=2018,FT=NUCLEAR,OU=7851.0,WN=16,CY=2018,FT=NPSHYD,OU=899.0,WN=16,CY=2018,FT=INTNED,OU=1000.0,WN=16,CY=2018,FT=INTIRL,OU=500.0,WN=16,CY=2018,FT=INTFR,OU=2000.0,WN=16,CY=2018,FT=INTEW,OU=500.0,WN=16,CY=2018,FT=COAL,OU=10111.0,WN=16,CY=2018,FT=CCGT,OU=26366.0,WN=16,CY=2018,FT=BIOMASS,OU=2496.0,WN=17,CY=2018,FT=WIND,OU=3555.0,WN=17,CY=2018,FT=PS,OU=2152.0,WN=17,CY=2018,FT=OTHER,OU=6.0,WN=17,CY=2018,FT=OIL,OU=0.0,WN=17,CY=2018,FT=OCGT,OU=777.0,WN=17,CY=2018,FT=NUCLEAR,OU=8506.0,WN=17,CY=2018,FT=NPSHYD,OU=921.0,WN=17,CY=2018,FT=INTNED,OU=1000.0,WN=17,CY=2018,FT=INTIRL,OU=500.0,WN=17,CY=2018,FT=INTFR,OU=2000.0,WN=17,CY=2018,FT=INTEW,OU=500.0,WN=17,CY=2018,FT=COAL,OU=10111.0,WN=17,CY=2018,FT=CCGT,OU=26258.0,WN=17,CY=2018,FT=BIOMASS,OU=2496.0,WN=18,CY=2018,FT=WIND,OU=3615.0,WN=18,CY=2018,FT=PS,OU=2002.0,WN=18,CY=2018,FT=OTHER,OU=6.0,WN=18,CY=2018,FT=OIL,OU=0.0,WN=18,CY=2018,FT=OCGT,OU=777.0,WN=18,CY=2018,FT=NUCLEAR,OU=7978.0,WN=18,CY=2018,FT=NPSHYD,OU=921.0,WN=18,CY=2018,FT=INTNED,OU=1000.0,WN=18,CY=2018,FT=INTIRL,OU=500.0,WN=18,CY=2018,FT=INTFR,OU=2000.0,WN=18,CY=2018,FT=INTEW,OU=0.0,WN=18,CY=2018,FT=COAL,OU=9114.0,WN=18,CY=2018,FT=CCGT,OU=26155.0,WN=18,CY=2018,FT=BIOMASS,OU=2496.0,WN=19,CY=2018,FT=WIND,OU=4224.0,WN=19,CY=2018,FT=PS,OU=2002.0,WN=19,CY=2018,FT=OTHER,OU=6.0,WN=19,CY=2018,FT=OCGT,OU=837.0,WN=19,CY=2018,FT=NUCLEAR,OU=6970.0,WN=19,CY=2018,FT=NPSHYD,OU=903.0,WN=19,CY=2018,FT=INTNED,OU=1000.0,WN=19,CY=2018,FT=INTIRL,OU=500.0,WN=19,CY=2018,FT=INTFR,OU=2000.0,WN=19,CY=2018,FT=INTEW,OU=0.0,WN=19,CY=2018,FT=COAL,OU=8634.0,WN=19,CY=2018,FT=CCGT,OU=25762.0,WN=19,CY=2018,FT=BIOMASS,OU=2496.0,WN=20,CY=2018,FT=WIND,OU=4222.0,WN=20,CY=2018,FT=PS,OU=1732.0,WN=20,CY=2018,FT=OTHER,OU=6.0,WN=20,CY=2018,FT=OCGT,OU=837.0,WN=20,CY=2018,FT=NUCLEAR,OU=7248.0,WN=20,CY=2018,FT=NPSHYD,OU=864.0,WN=20,CY=2018,FT=INTNED,OU=0.0,WN=20,CY=2018,FT=INTIRL,OU=500.0,WN=20,CY=2018,FT=INTFR,OU=2000.0,WN=20,CY=2018,FT=INTEW,OU=500.0,WN=20,CY=2018,FT=COAL,OU=8634.0,WN=20,CY=2018,FT=CCGT,OU=27175.0,WN=20,CY=2018,FT=BIOMASS,OU=2496.0,WN=21,CY=2018,FT=WIND,OU=4219.0,WN=21,CY=2018,FT=PS,OU=1732.0,WN=21,CY=2018,FT=OTHER,OU=6.0,WN=21,CY=2018,FT=OCGT,OU=837.0,WN=21,CY=2018,FT=NUCLEAR,OU=7517.0,WN=21,CY=2018,FT=NPSHYD,OU=904.0,WN=21,CY=2018,FT=INTNED,OU=1000.0,WN=21,CY=2018,FT=INTIRL,OU=500.0,WN=21,CY=2018,FT=INTFR,OU=2000.0,WN=21,CY=2018,FT=INTEW,OU=500.0,WN=21,CY=2018,FT=COAL,OU=7627.0,WN=21,CY=2018,FT=CCGT,OU=26806.0,WN=21,CY=2018,FT=BIOMASS,OU=2496.0,WN=22,CY=2018,FT=WIND,OU=4222.0,WN=22,CY=2018,FT=PS,OU=2002.0,WN=22,CY=2018,FT=OTHER,OU=6.0,WN=22,CY=2018,FT=OCGT,OU=837.0,WN=22,CY=2018,FT=NUCLEAR,OU=8024.0,WN=22,CY=2018,FT=NPSHYD,OU=975.0,WN=22,CY=2018,FT=INTNED,OU=1000.0,WN=22,CY=2018,FT=INTIRL,OU=500.0,WN=22,CY=2018,FT=INTFR,OU=2000.0,WN=22,CY=2018,FT=INTEW,OU=500.0,WN=22,CY=2018,FT=COAL,OU=8124.0,WN=22,CY=2018,FT=CCGT,OU=27849.0,WN=22,CY=2018,FT=BIOMASS,OU=2496.0,WN=23,CY=2018,FT=WIND,OU=2355.0,WN=23,CY=2018,FT=PS,OU=2190.0,WN=23,CY=2018,FT=OTHER,OU=6.0,WN=23,CY=2018,FT=OCGT,OU=837.0,WN=23,CY=2018,FT=NUCLEAR,OU=7887.0,WN=23,CY=2018,FT=NPSHYD,OU=950.0,WN=23,CY=2018,FT=INTNED,OU=1000.0,WN=23,CY=2018,FT=INTIRL,OU=500.0,WN=23,CY=2018,FT=INTFR,OU=2000.0,WN=23,CY=2018,FT=INTEW,OU=500.0,WN=23,CY=2018,FT=COAL,OU=8277.0,WN=23,CY=2018,FT=CCGT,OU=26318.0,WN=23,CY=2018,FT=BIOMASS,OU=1851.0,WN=24,CY=2018,FT=WIND,OU=2381.0,WN=24,CY=2018,FT=PS,OU=2340.0,WN=24,CY=2018,FT=OTHER,OU=6.0,WN=24,CY=2018,FT=OCGT,OU=837.0,WN=24,CY=2018,FT=NUCLEAR,OU=7932.0,WN=24,CY=2018,FT=NPSHYD,OU=947.0,WN=24,CY=2018,FT=INTNED,OU=1000.0,WN=24,CY=2018,FT=INTIRL,OU=500.0,WN=24,CY=2018,FT=INTFR,OU=2000.0,WN=24,CY=2018,FT=INTEW,OU=500.0,WN=24,CY=2018,FT=COAL,OU=8604.0,WN=24,CY=2018,FT=CCGT,OU=25317.0,WN=24,CY=2018,FT=BIOMASS,OU=1841.0,WN=25,CY=2018,FT=WIND,OU=2390.0,WN=25,CY=2018,FT=PS,OU=2320.0,WN=25,CY=2018,FT=OTHER,OU=6.0,WN=25,CY=2018,FT=OCGT,OU=837.0,WN=25,CY=2018,FT=NUCLEAR,OU=7827.0,WN=25,CY=2018,FT=NPSHYD,OU=806.0,WN=25,CY=2018,FT=INTNED,OU=1000.0,WN=25,CY=2018,FT=INTIRL,OU=500.0,WN=25,CY=2018,FT=INTFR,OU=1000.0,WN=25,CY=2018,FT=INTEW,OU=500.0,WN=25,CY=2018,FT=COAL,OU=9124.0,WN=25,CY=2018,FT=CCGT,OU=24989.0,WN=25,CY=2018,FT=BIOMASS,OU=1841.0,WN=26,CY=2018,FT=WIND,OU=2393.0,WN=26,CY=2018,FT=PS,OU=2320.0,WN=26,CY=2018,FT=OTHER,OU=6.0,WN=26,CY=2018,FT=OCGT,OU=837.0,WN=26,CY=2018,FT=NUCLEAR,OU=7578.0,WN=26,CY=2018,FT=NPSHYD,OU=780.0,WN=26,CY=2018,FT=INTNED,OU=1000.0,WN=26,CY=2018,FT=INTIRL,OU=500.0,WN=26,CY=2018,FT=INTFR,OU=1000.0,WN=26,CY=2018,FT=INTEW,OU=500.0,WN=26,CY=2018,FT=COAL,OU=8624.0,WN=26,CY=2018,FT=CCGT,OU=24760.0,WN=26,CY=2018,FT=BIOMASS,OU=1841.0,WN=27,CY=2018,FT=WIND,OU=2330.0,WN=27,CY=2018,FT=PS,OU=2440.0,WN=27,CY=2018,FT=OTHER,OU=6.0,WN=27,CY=2018,FT=OCGT,OU=798.0,WN=27,CY=2018,FT=NUCLEAR,OU=7221.0,WN=27,CY=2018,FT=NPSHYD,OU=810.0,WN=27,CY=2018,FT=INTNED,OU=1000.0,WN=27,CY=2018,FT=INTIRL,OU=500.0,WN=27,CY=2018,FT=INTFR,OU=2000.0,WN=27,CY=2018,FT=INTEW,OU=500.0,WN=27,CY=2018,FT=COAL,OU=8124.0,WN=27,CY=2018,FT=CCGT,OU=24014.0,WN=27,CY=2018,FT=BIOMASS,OU=1841.0,WN=28,CY=2018,FT=WIND,OU=2367.0,WN=28,CY=2018,FT=PS,OU=2440.0,WN=28,CY=2018,FT=OTHER,OU=6.0,WN=28,CY=2018,FT=OCGT,OU=798.0,WN=28,CY=2018,FT=NUCLEAR,OU=7311.0,WN=28,CY=2018,FT=NPSHYD,OU=763.0,WN=28,CY=2018,FT=INTNED,OU=1000.0,WN=28,CY=2018,FT=INTIRL,OU=500.0,WN=28,CY=2018,FT=INTFR,OU=2000.0,WN=28,CY=2018,FT=INTEW,OU=500.0,WN=28,CY=2018,FT=COAL,OU=7618.0,WN=28,CY=2018,FT=CCGT,OU=22767.0,WN=28,CY=2018,FT=BIOMASS,OU=1841.0,WN=29,CY=2018,FT=WIND,OU=2368.0,WN=29,CY=2018,FT=PS,OU=2440.0,WN=29,CY=2018,FT=OTHER,OU=6.0,WN=29,CY=2018,FT=OCGT,OU=798.0,WN=29,CY=2018,FT=NUCLEAR,OU=7240.0,WN=29,CY=2018,FT=NPSHYD,OU=763.0,WN=29,CY=2018,FT=INTNED,OU=1000.0,WN=29,CY=2018,FT=INTIRL,OU=500.0,WN=29,CY=2018,FT=INTFR,OU=2000.0,WN=29,CY=2018,FT=INTEW,OU=500.0,WN=29,CY=2018,FT=COAL,OU=8118.0,WN=29,CY=2018,FT=CCGT,OU=25222.0,WN=29,CY=2018,FT=BIOMASS,OU=2486.0,WN=30,CY=2018,FT=WIND,OU=2332.0,WN=30,CY=2018,FT=PS,OU=2440.0,WN=30,CY=2018,FT=OTHER,OU=6.0,WN=30,CY=2018,FT=OCGT,OU=837.0,WN=30,CY=2018,FT=NUCLEAR,OU=7477.0,WN=30,CY=2018,FT=NPSHYD,OU=763.0,WN=30,CY=2018,FT=INTNED,OU=1000.0,WN=30,CY=2018,FT=INTIRL,OU=500.0,WN=30,CY=2018,FT=INTFR,OU=2000.0,WN=30,CY=2018,FT=INTEW,OU=500.0,WN=30,CY=2018,FT=COAL,OU=9103.0,WN=30,CY=2018,FT=CCGT,OU=26044.0,WN=30,CY=2018,FT=BIOMASS,OU=2476.0,WN=31,CY=2018,FT=WIND,OU=2330.0,WN=31,CY=2018,FT=PS,OU=2728.0,WN=31,CY=2018,FT=OTHER,OU=6.0,WN=31,CY=2018,FT=OCGT,OU=837.0,WN=31,CY=2018,FT=NUCLEAR,OU=7919.0,WN=31,CY=2018,FT=NPSHYD,OU=868.0,WN=31,CY=2018,FT=INTNED,OU=1000.0,WN=31,CY=2018,FT=INTIRL,OU=500.0,WN=31,CY=2018,FT=INTFR,OU=2000.0,WN=31,CY=2018,FT=INTEW,OU=500.0,WN=31,CY=2018,FT=COAL,OU=10089.0,WN=31,CY=2018,FT=CCGT,OU=25451.0,WN=31,CY=2018,FT=BIOMASS,OU=2476.0,WN=32,CY=2018,FT=WIND,OU=2887.0,WN=32,CY=2018,FT=PS,OU=2728.0,WN=32,CY=2018,FT=OTHER,OU=6.0,WN=32,CY=2018,FT=OCGT,OU=837.0,WN=32,CY=2018,FT=NUCLEAR,OU=7111.0,WN=32,CY=2018,FT=NPSHYD,OU=931.0,WN=32,CY=2018,FT=INTNED,OU=1000.0,WN=32,CY=2018,FT=INTIRL,OU=500.0,WN=32,CY=2018,FT=INTFR,OU=2000.0,WN=32,CY=2018,FT=INTEW,OU=500.0,WN=32,CY=2018,FT=COAL,OU=10092.0,WN=32,CY=2018,FT=CCGT,OU=26770.0,WN=32,CY=2018,FT=BIOMASS,OU=2476.0,WN=33,CY=2018,FT=WIND,OU=2995.0,WN=33,CY=2018,FT=PS,OU=2728.0,WN=33,CY=2018,FT=OTHER,OU=6.0,WN=33,CY=2018,FT=OCGT,OU=837.0,WN=33,CY=2018,FT=NUCLEAR,OU=6852.0,WN=33,CY=2018,FT=NPSHYD,OU=938.0,WN=33,CY=2018,FT=INTNED,OU=1000.0,WN=33,CY=2018,FT=INTIRL,OU=500.0,WN=33,CY=2018,FT=INTFR,OU=2000.0,WN=33,CY=2018,FT=INTEW,OU=500.0,WN=33,CY=2018,FT=COAL,OU=10092.0,WN=33,CY=2018,FT=CCGT,OU=27610.0,WN=33,CY=2018,FT=BIOMASS,OU=2476.0,WN=34,CY=2018,FT=WIND,OU=2997.0,WN=34,CY=2018,FT=PS,OU=2728.0,WN=34,CY=2018,FT=OTHER,OU=6.0,WN=34,CY=2018,FT=OCGT,OU=837.0,WN=34,CY=2018,FT=NUCLEAR,OU=7157.0,WN=34,CY=2018,FT=NPSHYD,OU=938.0,WN=34,CY=2018,FT=INTNED,OU=1000.0,WN=34,CY=2018,FT=INTIRL,OU=500.0,WN=34,CY=2018,FT=INTFR,OU=2000.0,WN=34,CY=2018,FT=INTEW,OU=500.0,WN=34,CY=2018,FT=COAL,OU=9592.0,WN=34,CY=2018,FT=CCGT,OU=28445.0,WN=34,CY=2018,FT=BIOMASS,OU=2476.0,WN=35,CY=2018,FT=WIND,OU=2988.0,WN=35,CY=2018,FT=PS,OU=2728.0,WN=35,CY=2018,FT=OTHER,OU=6.0,WN=35,CY=2018,FT=OCGT,OU=837.0,WN=35,CY=2018,FT=NUCLEAR,OU=7060.0,WN=35,CY=2018,FT=NPSHYD,OU=938.0,WN=35,CY=2018,FT=INTNED,OU=1000.0,WN=35,CY=2018,FT=INTIRL,OU=500.0,WN=35,CY=2018,FT=INTFR,OU=2000.0,WN=35,CY=2018,FT=INTEW,OU=500.0,WN=35,CY=2018,FT=COAL,OU=11226.0,WN=35,CY=2018,FT=CCGT,OU=27374.0,WN=35,CY=2018,FT=BIOMASS,OU=2476.0,WN=36,CY=2018,FT=WIND,OU=3587.0,WN=36,CY=2018,FT=PS,OU=2728.0,WN=36,CY=2018,FT=OTHER,OU=6.0,WN=36,CY=2018,FT=OCGT,OU=837.0,WN=36,CY=2018,FT=NUCLEAR,OU=7763.0,WN=36,CY=2018,FT=NPSHYD,OU=975.0,WN=36,CY=2018,FT=INTNED,OU=1000.0,WN=36,CY=2018,FT=INTIRL,OU=500.0,WN=36,CY=2018,FT=INTFR,OU=1000.0,WN=36,CY=2018,FT=INTEW,OU=500.0,WN=36,CY=2018,FT=COAL,OU=11226.0,WN=36,CY=2018,FT=CCGT,OU=26411.0,WN=36,CY=2018,FT=BIOMASS,OU=2476.0,WN=37,CY=2018,FT=WIND,OU=3636.0,WN=37,CY=2018,FT=PS,OU=2368.0,WN=37,CY=2018,FT=OTHER,OU=6.0,WN=37,CY=2018,FT=OCGT,OU=837.0,WN=37,CY=2018,FT=NUCLEAR,OU=7144.0,WN=37,CY=2018,FT=NPSHYD,OU=1007.0,WN=37,CY=2018,FT=INTNED,OU=1000.0,WN=37,CY=2018,FT=INTIRL,OU=500.0,WN=37,CY=2018,FT=INTFR,OU=1000.0,WN=37,CY=2018,FT=INTEW,OU=500.0,WN=37,CY=2018,FT=COAL,OU=11726.0,WN=37,CY=2018,FT=CCGT,OU=24831.0,WN=37,CY=2018,FT=BIOMASS,OU=2476.0,WN=38,CY=2018,FT=WIND,OU=3637.0,WN=38,CY=2018,FT=PS,OU=2248.0,WN=38,CY=2018,FT=OTHER,OU=6.0,WN=38,CY=2018,FT=OCGT,OU=837.0,WN=38,CY=2018,FT=NUCLEAR,OU=7110.0,WN=38,CY=2018,FT=NPSHYD,OU=1007.0,WN=38,CY=2018,FT=INTNED,OU=0.0,WN=38,CY=2018,FT=INTIRL,OU=500.0,WN=38,CY=2018,FT=INTFR,OU=2000.0,WN=38,CY=2018,FT=INTEW,OU=500.0,WN=38,CY=2018,FT=COAL,OU=11726.0,WN=38,CY=2018,FT=CCGT,OU=26295.0,WN=38,CY=2018,FT=BIOMASS,OU=2476.0,WN=39,CY=2018,FT=WIND,OU=3626.0,WN=39,CY=2018,FT=PS,OU=2368.0,WN=39,CY=2018,FT=OTHER,OU=6.0,WN=39,CY=2018,FT=OCGT,OU=837.0,WN=39,CY=2018,FT=NUCLEAR,OU=7545.0,WN=39,CY=2018,FT=NPSHYD,OU=1049.0,WN=39,CY=2018,FT=INTNED,OU=1000.0,WN=39,CY=2018,FT=INTIRL,OU=500.0,WN=39,CY=2018,FT=INTFR,OU=2000.0,WN=39,CY=2018,FT=INTEW,OU=500.0,WN=39,CY=2018,FT=COAL,OU=11741.0,WN=39,CY=2018,FT=CCGT,OU=27864.0,WN=39,CY=2018,FT=BIOMASS,OU=2476.0,WN=40,CY=2018,FT=WIND,OU=4850.0,WN=40,CY=2018,FT=PS,OU=2448.0,WN=40,CY=2018,FT=OTHER,OU=6.0,WN=40,CY=2018,FT=OCGT,OU=837.0,WN=40,CY=2018,FT=NUCLEAR,OU=7501.0,WN=40,CY=2018,FT=NPSHYD,OU=1049.0,WN=40,CY=2018,FT=INTNED,OU=1000.0,WN=40,CY=2018,FT=INTIRL,OU=500.0,WN=40,CY=2018,FT=INTFR,OU=2000.0,WN=40,CY=2018,FT=INTEW,OU=500.0,WN=40,CY=2018,FT=COAL,OU=10874.0,WN=40,CY=2018,FT=CCGT,OU=27994.0,WN=40,CY=2018,FT=BIOMASS,OU=2476.0,WN=41,CY=2018,FT=WIND,OU=4858.0,WN=41,CY=2018,FT=PS,OU=2448.0,WN=41,CY=2018,FT=OTHER,OU=6.0,WN=41,CY=2018,FT=OCGT,OU=837.0,WN=41,CY=2018,FT=NUCLEAR,OU=7671.0,WN=41,CY=2018,FT=NPSHYD,OU=1049.0,WN=41,CY=2018,FT=INTNED,OU=1000.0,WN=41,CY=2018,FT=INTIRL,OU=500.0,WN=41,CY=2018,FT=INTFR,OU=2000.0,WN=41,CY=2018,FT=INTEW,OU=500.0,WN=41,CY=2018,FT=COAL,OU=10874.0,WN=41,CY=2018,FT=CCGT,OU=27474.0,WN=41,CY=2018,FT=BIOMASS,OU=2476.0,WN=42,CY=2018,FT=WIND,OU=4849.0,WN=42,CY=2018,FT=PS,OU=2448.0,WN=42,CY=2018,FT=OTHER,OU=6.0,WN=42,CY=2018,FT=OCGT,OU=837.0,WN=42,CY=2018,FT=NUCLEAR,OU=7582.0,WN=42,CY=2018,FT=NPSHYD,OU=1039.0,WN=42,CY=2018,FT=INTNED,OU=1000.0,WN=42,CY=2018,FT=INTIRL,OU=500.0,WN=42,CY=2018,FT=INTFR,OU=2000.0,WN=42,CY=2018,FT=INTEW,OU=500.0,WN=42,CY=2018,FT=COAL,OU=10874.0,WN=42,CY=2018,FT=CCGT,OU=28229.0,WN=42,CY=2018,FT=BIOMASS,OU=2476.0,WN=43,CY=2018,FT=WIND,OU=4827.0,WN=43,CY=2018,FT=PS,OU=2628.0,WN=43,CY=2018,FT=OTHER,OU=6.0,WN=43,CY=2018,FT=OCGT,OU=837.0,WN=43,CY=2018,FT=NUCLEAR,OU=7204.0,WN=43,CY=2018,FT=NPSHYD,OU=1019.0,WN=43,CY=2018,FT=INTNED,OU=1000.0,WN=43,CY=2018,FT=INTIRL,OU=500.0,WN=43,CY=2018,FT=INTFR,OU=2000.0,WN=43,CY=2018,FT=INTEW,OU=500.0,WN=43,CY=2018,FT=COAL,OU=10874.0,WN=43,CY=2018,FT=CCGT,OU=28937.0,WN=43,CY=2018,FT=BIOMASS,OU=2476.0,WN=44,CY=2018,FT=WIND,OU=4717.0,WN=44,CY=2018,FT=PS,OU=2628.0,WN=44,CY=2018,FT=OTHER,OU=6.0,WN=44,CY=2018,FT=OCGT,OU=837.0,WN=44,CY=2018,FT=NUCLEAR,OU=8456.0,WN=44,CY=2018,FT=NPSHYD,OU=1039.0,WN=44,CY=2018,FT=INTNED,OU=1000.0,WN=44,CY=2018,FT=INTIRL,OU=500.0,WN=44,CY=2018,FT=INTFR,OU=2000.0,WN=44,CY=2018,FT=INTEW,OU=500.0,WN=44,CY=2018,FT=COAL,OU=10874.0,WN=44,CY=2018,FT=CCGT,OU=28190.0,WN=44,CY=2018,FT=BIOMASS,OU=2476.0,WN=45,CY=2018,FT=WIND,OU=5317.0,WN=45,CY=2018,FT=PS,OU=2628.0,WN=45,CY=2018,FT=OTHER,OU=6.0,WN=45,CY=2018,FT=OCGT,OU=837.0,WN=45,CY=2018,FT=NUCLEAR,OU=8466.0,WN=45,CY=2018,FT=NPSHYD,OU=1039.0,WN=45,CY=2018,FT=INTNED,OU=1000.0,WN=45,CY=2018,FT=INTIRL,OU=500.0,WN=45,CY=2018,FT=INTFR,OU=2000.0,WN=45,CY=2018,FT=INTEW,OU=500.0,WN=45,CY=2018,FT=COAL,OU=10874.0,WN=45,CY=2018,FT=CCGT,OU=27762.0,WN=45,CY=2018,FT=BIOMASS,OU=2476.0,WN=46,CY=2018,FT=WIND,OU=5317.0,WN=46,CY=2018,FT=PS,OU=2728.0,WN=46,CY=2018,FT=OTHER,OU=6.0,WN=46,CY=2018,FT=OCGT,OU=836.0,WN=46,CY=2018,FT=NUCLEAR,OU=8429.0,WN=46,CY=2018,FT=NPSHYD,OU=1039.0,WN=46,CY=2018,FT=INTNED,OU=1000.0,WN=46,CY=2018,FT=INTIRL,OU=500.0,WN=46,CY=2018,FT=INTFR,OU=2000.0,WN=46,CY=2018,FT=INTEW,OU=500.0,WN=46,CY=2018,FT=COAL,OU=10389.0,WN=46,CY=2018,FT=CCGT,OU=28986.0,WN=46,CY=2018,FT=BIOMASS,OU=2476.0,WN=47,CY=2018,FT=WIND,OU=5317.0,WN=47,CY=2018,FT=PS,OU=2728.0,WN=47,CY=2018,FT=OTHER,OU=6.0,WN=47,CY=2018,FT=OCGT,OU=837.0,WN=47,CY=2018,FT=NUCLEAR,OU=7680.0,WN=47,CY=2018,FT=NPSHYD,OU=1039.0,WN=47,CY=2018,FT=INTNED,OU=1000.0,WN=47,CY=2018,FT=INTIRL,OU=500.0,WN=47,CY=2018,FT=INTFR,OU=2000.0,WN=47,CY=2018,FT=INTEW,OU=500.0,WN=47,CY=2018,FT=COAL,OU=10389.0,WN=47,CY=2018,FT=CCGT,OU=28991.0,WN=47,CY=2018,FT=BIOMASS,OU=2476.0,WN=48,CY=2018,FT=WIND,OU=5317.0,WN=48,CY=2018,FT=PS,OU=2728.0,WN=48,CY=2018,FT=OTHER,OU=6.0,WN=48,CY=2018,FT=OCGT,OU=837.0,WN=48,CY=2018,FT=NUCLEAR,OU=8157.0,WN=48,CY=2018,FT=NPSHYD,OU=1039.0,WN=48,CY=2018,FT=INTNED,OU=1000.0,WN=48,CY=2018,FT=INTIRL,OU=500.0,WN=48,CY=2018,FT=INTFR,OU=2000.0,WN=48,CY=2018,FT=INTEW,OU=500.0,WN=48,CY=2018,FT=COAL,OU=10389.0,WN=48,CY=2018,FT=CCGT,OU=29003.0,WN=48,CY=2018,FT=BIOMASS,OU=2476.0,WN=49,CY=2018,FT=WIND,OU=6483.0,WN=49,CY=2018,FT=PS,OU=2728.0,WN=49,CY=2018,FT=OTHER,OU=6.0,WN=49,CY=2018,FT=OCGT,OU=837.0,WN=49,CY=2018,FT=NUCLEAR,OU=8581.0,WN=49,CY=2018,FT=NPSHYD,OU=1039.0,WN=49,CY=2018,FT=INTNED,OU=1000.0,WN=49,CY=2018,FT=INTIRL,OU=500.0,WN=49,CY=2018,FT=INTFR,OU=2000.0,WN=49,CY=2018,FT=INTEW,OU=500.0,WN=49,CY=2018,FT=COAL,OU=8913.0,WN=49,CY=2018,FT=CCGT,OU=28808.0,WN=49,CY=2018,FT=BIOMASS,OU=2486.0,WN=50,CY=2018,FT=WIND,OU=6483.0,WN=50,CY=2018,FT=PS,OU=2728.0,WN=50,CY=2018,FT=OTHER,OU=6.0,WN=50,CY=2018,FT=OCGT,OU=837.0,WN=50,CY=2018,FT=NUCLEAR,OU=8555.0,WN=50,CY=2018,FT=NPSHYD,OU=1039.0,WN=50,CY=2018,FT=INTNED,OU=1000.0,WN=50,CY=2018,FT=INTIRL,OU=500.0,WN=50,CY=2018,FT=INTFR,OU=2000.0,WN=50,CY=2018,FT=INTEW,OU=500.0,WN=50,CY=2018,FT=COAL,OU=8913.0,WN=50,CY=2018,FT=CCGT,OU=29648.0,WN=50,CY=2018,FT=BIOMASS,OU=2486.0,WN=51,CY=2018,FT=WIND,OU=6483.0,WN=51,CY=2018,FT=PS,OU=2728.0,WN=51,CY=2018,FT=OTHER,OU=6.0,WN=51,CY=2018,FT=OCGT,OU=837.0,WN=51,CY=2018,FT=NUCLEAR,OU=8076.0,WN=51,CY=2018,FT=NPSHYD,OU=1049.0,WN=51,CY=2018,FT=INTNED,OU=1000.0,WN=51,CY=2018,FT=INTIRL,OU=500.0,WN=51,CY=2018,FT=INTFR,OU=2000.0,WN=51,CY=2018,FT=INTEW,OU=500.0,WN=51,CY=2018,FT=COAL,OU=8913.0,WN=51,CY=2018,FT=CCGT,OU=29851.0,WN=51,CY=2018,FT=BIOMASS,OU=2486.0,WN=52,CY=2018,FT=WIND,OU=6483.0,WN=52,CY=2018,FT=PS,OU=2548.0,WN=52,CY=2018,FT=OTHER,OU=6.0,WN=52,CY=2018,FT=OCGT,OU=837.0,WN=52,CY=2018,FT=NUCLEAR,OU=8966.0,WN=52,CY=2018,FT=NPSHYD,OU=1049.0,WN=52,CY=2018,FT=INTNED,OU=1000.0,WN=52,CY=2018,FT=INTIRL,OU=500.0,WN=52,CY=2018,FT=INTFR,OU=2000.0,WN=52,CY=2018,FT=INTEW,OU=500.0,WN=52,CY=2018,FT=COAL,OU=8913.0,WN=52,CY=2018,FT=CCGT,OU=29851.0,WN=52,CY=2018,FT=BIOMASS,OU=2486.0,WN=1,CY=2019,FT=WIND,OU=6458.0,WN=1,CY=2019,FT=PS,OU=2548.0,WN=1,CY=2019,FT=OTHER,OU=0.0,WN=1,CY=2019,FT=OCGT,OU=836.0,WN=1,CY=2019,FT=NUCLEAR,OU=8853.0,WN=1,CY=2019,FT=NPSHYD,OU=1048.0,WN=1,CY=2019,FT=INTNED,OU=1000.0,WN=1,CY=2019,FT=INTIRL,OU=500.0,WN=1,CY=2019,FT=INTFR,OU=2000.0,WN=1,CY=2019,FT=INTEW,OU=500.0,WN=1,CY=2019,FT=COAL,OU=8913.0,WN=1,CY=2019,FT=CCGT,OU=29851.0,WN=1,CY=2019,FT=BIOMASS,OU=2486.0}'

        expected_dict = {'received_time' : dt.datetime(2018, 1, 4, 13, 37, 11),
                         'message_type' : 'SYSTEM',
                         'message_subtype' : 'FOU2T52W',
                         'TP' : dt.datetime(2018, 1, 4, 13, 31),
                         'data_points' : {
                 1: {'CY': 2018, 'FT': 'WIND', 'OU': 6447.0, 'WN': 3},
                 2: {'CY': 2018, 'FT': 'PS', 'OU': 2828.0, 'WN': 3},
                 3: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 3},
                 4: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 3},
                 5: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 3},
                 6: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 6990.0, 'WN': 3},
                 7: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 3},
                 8: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 3},
                 9: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 3},
                 10: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 3},
                 11: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 3},
                 12: {'CY': 2018, 'FT': 'COAL', 'OU': 12786.0, 'WN': 3},
                 13: {'CY': 2018, 'FT': 'CCGT', 'OU': 29578.0, 'WN': 3},
                 14: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2130.0, 'WN': 3},
                 15: {'CY': 2018, 'FT': 'WIND', 'OU': 6467.0, 'WN': 4},
                 16: {'CY': 2018, 'FT': 'PS', 'OU': 2828.0, 'WN': 4},
                 17: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 4},
                 18: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 4},
                 19: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 4},
                 20: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 6728.0, 'WN': 4},
                 21: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 4},
                 22: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 4},
                 23: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 4},
                 24: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 4},
                 25: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 4},
                 26: {'CY': 2018, 'FT': 'COAL', 'OU': 12786.0, 'WN': 4},
                 27: {'CY': 2018, 'FT': 'CCGT', 'OU': 29583.0, 'WN': 4},
                 28: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2165.0, 'WN': 4},
                 29: {'CY': 2018, 'FT': 'WIND', 'OU': 6474.0, 'WN': 5},
                 30: {'CY': 2018, 'FT': 'PS', 'OU': 2828.0, 'WN': 5},
                 31: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 5},
                 32: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 5},
                 33: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 5},
                 34: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 6108.0, 'WN': 5},
                 35: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 5},
                 36: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 5},
                 37: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 5},
                 38: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 5},
                 39: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 5},
                 40: {'CY': 2018, 'FT': 'COAL', 'OU': 12786.0, 'WN': 5},
                 41: {'CY': 2018, 'FT': 'CCGT', 'OU': 29143.0, 'WN': 5},
                 42: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2165.0, 'WN': 5},
                 43: {'CY': 2018, 'FT': 'WIND', 'OU': 5923.0, 'WN': 6},
                 44: {'CY': 2018, 'FT': 'PS', 'OU': 2828.0, 'WN': 6},
                 45: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 6},
                 46: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 6},
                 47: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 6},
                 48: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7271.0, 'WN': 6},
                 49: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 6},
                 50: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 6},
                 51: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 6},
                 52: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 6},
                 53: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 6},
                 54: {'CY': 2018, 'FT': 'COAL', 'OU': 12786.0, 'WN': 6},
                 55: {'CY': 2018, 'FT': 'CCGT', 'OU': 29912.0, 'WN': 6},
                 56: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2297.0, 'WN': 6},
                 57: {'CY': 2018, 'FT': 'WIND', 'OU': 5939.0, 'WN': 7},
                 58: {'CY': 2018, 'FT': 'PS', 'OU': 2828.0, 'WN': 7},
                 59: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 7},
                 60: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 7},
                 61: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 7},
                 62: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7418.0, 'WN': 7},
                 63: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 7},
                 64: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 7},
                 65: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 7},
                 66: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 7},
                 67: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 7},
                 68: {'CY': 2018, 'FT': 'COAL', 'OU': 12786.0, 'WN': 7},
                 69: {'CY': 2018, 'FT': 'CCGT', 'OU': 30158.0, 'WN': 7},
                 70: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2297.0, 'WN': 7},
                 71: {'CY': 2018, 'FT': 'WIND', 'OU': 5939.0, 'WN': 8},
                 72: {'CY': 2018, 'FT': 'PS', 'OU': 2828.0, 'WN': 8},
                 73: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 8},
                 74: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 8},
                 75: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 8},
                 76: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7751.0, 'WN': 8},
                 77: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 8},
                 78: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 8},
                 79: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 8},
                 80: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 8},
                 81: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 8},
                 82: {'CY': 2018, 'FT': 'COAL', 'OU': 13266.0, 'WN': 8},
                 83: {'CY': 2018, 'FT': 'CCGT', 'OU': 30351.0, 'WN': 8},
                 84: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2374.0, 'WN': 8},
                 85: {'CY': 2018, 'FT': 'WIND', 'OU': 5955.0, 'WN': 9},
                 86: {'CY': 2018, 'FT': 'PS', 'OU': 2828.0, 'WN': 9},
                 87: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 9},
                 88: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 9},
                 89: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 9},
                 90: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7708.0, 'WN': 9},
                 91: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 9},
                 92: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 9},
                 93: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 9},
                 94: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 9},
                 95: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 9},
                 96: {'CY': 2018, 'FT': 'COAL', 'OU': 13266.0, 'WN': 9},
                 97: {'CY': 2018, 'FT': 'CCGT', 'OU': 29204.0, 'WN': 9},
                 98: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2429.0, 'WN': 9},
                 99: {'CY': 2018, 'FT': 'WIND', 'OU': 4761.0, 'WN': 10},
                 100: {'CY': 2018, 'FT': 'PS', 'OU': 2828.0, 'WN': 10},
                 101: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 10},
                 102: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 10},
                 103: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 10},
                 104: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7461.0, 'WN': 10},
                 105: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 10},
                 106: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 10},
                 107: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 10},
                 108: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 10},
                 109: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 10},
                 110: {'CY': 2018, 'FT': 'COAL', 'OU': 13266.0, 'WN': 10},
                 111: {'CY': 2018, 'FT': 'CCGT', 'OU': 28372.0, 'WN': 10},
                 112: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2429.0, 'WN': 10},
                 113: {'CY': 2018, 'FT': 'WIND', 'OU': 4761.0, 'WN': 11},
                 114: {'CY': 2018, 'FT': 'PS', 'OU': 2628.0, 'WN': 11},
                 115: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 11},
                 116: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 11},
                 117: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 11},
                 118: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7640.0, 'WN': 11},
                 119: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1051.0, 'WN': 11},
                 120: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 11},
                 121: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 11},
                 122: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 11},
                 123: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 11},
                 124: {'CY': 2018, 'FT': 'COAL', 'OU': 13266.0, 'WN': 11},
                 125: {'CY': 2018, 'FT': 'CCGT', 'OU': 29067.0, 'WN': 11},
                 126: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 11},
                 127: {'CY': 2018, 'FT': 'WIND', 'OU': 4761.0, 'WN': 12},
                 128: {'CY': 2018, 'FT': 'PS', 'OU': 2628.0, 'WN': 12},
                 129: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 12},
                 130: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 12},
                 131: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 12},
                 132: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7462.0, 'WN': 12},
                 133: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1011.0, 'WN': 12},
                 134: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 12},
                 135: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 12},
                 136: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 12},
                 137: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 12},
                 138: {'CY': 2018, 'FT': 'COAL', 'OU': 13266.0, 'WN': 12},
                 139: {'CY': 2018, 'FT': 'CCGT', 'OU': 29942.0, 'WN': 12},
                 140: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 12},
                 141: {'CY': 2018, 'FT': 'WIND', 'OU': 4703.0, 'WN': 13},
                 142: {'CY': 2018, 'FT': 'PS', 'OU': 2340.0, 'WN': 13},
                 143: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 13},
                 144: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 13},
                 145: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 13},
                 146: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7757.0, 'WN': 13},
                 147: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1011.0, 'WN': 13},
                 148: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 13},
                 149: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 13},
                 150: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 13},
                 151: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 13},
                 152: {'CY': 2018, 'FT': 'COAL', 'OU': 13266.0, 'WN': 13},
                 153: {'CY': 2018, 'FT': 'CCGT', 'OU': 28188.0, 'WN': 13},
                 154: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 13},
                 155: {'CY': 2018, 'FT': 'WIND', 'OU': 3636.0, 'WN': 14},
                 156: {'CY': 2018, 'FT': 'PS', 'OU': 2052.0, 'WN': 14},
                 157: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 14},
                 158: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 14},
                 159: {'CY': 2018, 'FT': 'OCGT', 'OU': 697.0, 'WN': 14},
                 160: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8089.0, 'WN': 14},
                 161: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 891.0, 'WN': 14},
                 162: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 14},
                 163: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 14},
                 164: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 14},
                 165: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 14},
                 166: {'CY': 2018, 'FT': 'COAL', 'OU': 11096.0, 'WN': 14},
                 167: {'CY': 2018, 'FT': 'CCGT', 'OU': 25905.0, 'WN': 14},
                 168: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 14},
                 169: {'CY': 2018, 'FT': 'WIND', 'OU': 3635.0, 'WN': 15},
                 170: {'CY': 2018, 'FT': 'PS', 'OU': 2052.0, 'WN': 15},
                 171: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 15},
                 172: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 15},
                 173: {'CY': 2018, 'FT': 'OCGT', 'OU': 697.0, 'WN': 15},
                 174: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7752.0, 'WN': 15},
                 175: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 899.0, 'WN': 15},
                 176: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 15},
                 177: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 15},
                 178: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 15},
                 179: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 15},
                 180: {'CY': 2018, 'FT': 'COAL', 'OU': 10111.0, 'WN': 15},
                 181: {'CY': 2018, 'FT': 'CCGT', 'OU': 26740.0, 'WN': 15},
                 182: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 15},
                 183: {'CY': 2018, 'FT': 'WIND', 'OU': 3634.0, 'WN': 16},
                 184: {'CY': 2018, 'FT': 'PS', 'OU': 2052.0, 'WN': 16},
                 185: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 16},
                 186: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 16},
                 187: {'CY': 2018, 'FT': 'OCGT', 'OU': 777.0, 'WN': 16},
                 188: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7851.0, 'WN': 16},
                 189: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 899.0, 'WN': 16},
                 190: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 16},
                 191: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 16},
                 192: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 16},
                 193: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 16},
                 194: {'CY': 2018, 'FT': 'COAL', 'OU': 10111.0, 'WN': 16},
                 195: {'CY': 2018, 'FT': 'CCGT', 'OU': 26366.0, 'WN': 16},
                 196: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 16},
                 197: {'CY': 2018, 'FT': 'WIND', 'OU': 3555.0, 'WN': 17},
                 198: {'CY': 2018, 'FT': 'PS', 'OU': 2152.0, 'WN': 17},
                 199: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 17},
                 200: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 17},
                 201: {'CY': 2018, 'FT': 'OCGT', 'OU': 777.0, 'WN': 17},
                 202: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8506.0, 'WN': 17},
                 203: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 921.0, 'WN': 17},
                 204: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 17},
                 205: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 17},
                 206: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 17},
                 207: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 17},
                 208: {'CY': 2018, 'FT': 'COAL', 'OU': 10111.0, 'WN': 17},
                 209: {'CY': 2018, 'FT': 'CCGT', 'OU': 26258.0, 'WN': 17},
                 210: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 17},
                 211: {'CY': 2018, 'FT': 'WIND', 'OU': 3615.0, 'WN': 18},
                 212: {'CY': 2018, 'FT': 'PS', 'OU': 2002.0, 'WN': 18},
                 213: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 18},
                 214: {'CY': 2018, 'FT': 'OIL', 'OU': 0.0, 'WN': 18},
                 215: {'CY': 2018, 'FT': 'OCGT', 'OU': 777.0, 'WN': 18},
                 216: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7978.0, 'WN': 18},
                 217: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 921.0, 'WN': 18},
                 218: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 18},
                 219: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 18},
                 220: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 18},
                 221: {'CY': 2018, 'FT': 'INTEW', 'OU': 0.0, 'WN': 18},
                 222: {'CY': 2018, 'FT': 'COAL', 'OU': 9114.0, 'WN': 18},
                 223: {'CY': 2018, 'FT': 'CCGT', 'OU': 26155.0, 'WN': 18},
                 224: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 18},
                 225: {'CY': 2018, 'FT': 'WIND', 'OU': 4224.0, 'WN': 19},
                 226: {'CY': 2018, 'FT': 'PS', 'OU': 2002.0, 'WN': 19},
                 227: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 19},
                 228: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 19},
                 229: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 6970.0, 'WN': 19},
                 230: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 903.0, 'WN': 19},
                 231: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 19},
                 232: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 19},
                 233: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 19},
                 234: {'CY': 2018, 'FT': 'INTEW', 'OU': 0.0, 'WN': 19},
                 235: {'CY': 2018, 'FT': 'COAL', 'OU': 8634.0, 'WN': 19},
                 236: {'CY': 2018, 'FT': 'CCGT', 'OU': 25762.0, 'WN': 19},
                 237: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 19},
                 238: {'CY': 2018, 'FT': 'WIND', 'OU': 4222.0, 'WN': 20},
                 239: {'CY': 2018, 'FT': 'PS', 'OU': 1732.0, 'WN': 20},
                 240: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 20},
                 241: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 20},
                 242: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7248.0, 'WN': 20},
                 243: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 864.0, 'WN': 20},
                 244: {'CY': 2018, 'FT': 'INTNED', 'OU': 0.0, 'WN': 20},
                 245: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 20},
                 246: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 20},
                 247: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 20},
                 248: {'CY': 2018, 'FT': 'COAL', 'OU': 8634.0, 'WN': 20},
                 249: {'CY': 2018, 'FT': 'CCGT', 'OU': 27175.0, 'WN': 20},
                 250: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 20},
                 251: {'CY': 2018, 'FT': 'WIND', 'OU': 4219.0, 'WN': 21},
                 252: {'CY': 2018, 'FT': 'PS', 'OU': 1732.0, 'WN': 21},
                 253: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 21},
                 254: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 21},
                 255: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7517.0, 'WN': 21},
                 256: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 904.0, 'WN': 21},
                 257: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 21},
                 258: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 21},
                 259: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 21},
                 260: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 21},
                 261: {'CY': 2018, 'FT': 'COAL', 'OU': 7627.0, 'WN': 21},
                 262: {'CY': 2018, 'FT': 'CCGT', 'OU': 26806.0, 'WN': 21},
                 263: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 21},
                 264: {'CY': 2018, 'FT': 'WIND', 'OU': 4222.0, 'WN': 22},
                 265: {'CY': 2018, 'FT': 'PS', 'OU': 2002.0, 'WN': 22},
                 266: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 22},
                 267: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 22},
                 268: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8024.0, 'WN': 22},
                 269: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 975.0, 'WN': 22},
                 270: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 22},
                 271: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 22},
                 272: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 22},
                 273: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 22},
                 274: {'CY': 2018, 'FT': 'COAL', 'OU': 8124.0, 'WN': 22},
                 275: {'CY': 2018, 'FT': 'CCGT', 'OU': 27849.0, 'WN': 22},
                 276: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2496.0, 'WN': 22},
                 277: {'CY': 2018, 'FT': 'WIND', 'OU': 2355.0, 'WN': 23},
                 278: {'CY': 2018, 'FT': 'PS', 'OU': 2190.0, 'WN': 23},
                 279: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 23},
                 280: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 23},
                 281: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7887.0, 'WN': 23},
                 282: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 950.0, 'WN': 23},
                 283: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 23},
                 284: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 23},
                 285: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 23},
                 286: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 23},
                 287: {'CY': 2018, 'FT': 'COAL', 'OU': 8277.0, 'WN': 23},
                 288: {'CY': 2018, 'FT': 'CCGT', 'OU': 26318.0, 'WN': 23},
                 289: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 1851.0, 'WN': 23},
                 290: {'CY': 2018, 'FT': 'WIND', 'OU': 2381.0, 'WN': 24},
                 291: {'CY': 2018, 'FT': 'PS', 'OU': 2340.0, 'WN': 24},
                 292: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 24},
                 293: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 24},
                 294: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7932.0, 'WN': 24},
                 295: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 947.0, 'WN': 24},
                 296: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 24},
                 297: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 24},
                 298: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 24},
                 299: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 24},
                 300: {'CY': 2018, 'FT': 'COAL', 'OU': 8604.0, 'WN': 24},
                 301: {'CY': 2018, 'FT': 'CCGT', 'OU': 25317.0, 'WN': 24},
                 302: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 1841.0, 'WN': 24},
                 303: {'CY': 2018, 'FT': 'WIND', 'OU': 2390.0, 'WN': 25},
                 304: {'CY': 2018, 'FT': 'PS', 'OU': 2320.0, 'WN': 25},
                 305: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 25},
                 306: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 25},
                 307: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7827.0, 'WN': 25},
                 308: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 806.0, 'WN': 25},
                 309: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 25},
                 310: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 25},
                 311: {'CY': 2018, 'FT': 'INTFR', 'OU': 1000.0, 'WN': 25},
                 312: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 25},
                 313: {'CY': 2018, 'FT': 'COAL', 'OU': 9124.0, 'WN': 25},
                 314: {'CY': 2018, 'FT': 'CCGT', 'OU': 24989.0, 'WN': 25},
                 315: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 1841.0, 'WN': 25},
                 316: {'CY': 2018, 'FT': 'WIND', 'OU': 2393.0, 'WN': 26},
                 317: {'CY': 2018, 'FT': 'PS', 'OU': 2320.0, 'WN': 26},
                 318: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 26},
                 319: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 26},
                 320: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7578.0, 'WN': 26},
                 321: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 780.0, 'WN': 26},
                 322: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 26},
                 323: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 26},
                 324: {'CY': 2018, 'FT': 'INTFR', 'OU': 1000.0, 'WN': 26},
                 325: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 26},
                 326: {'CY': 2018, 'FT': 'COAL', 'OU': 8624.0, 'WN': 26},
                 327: {'CY': 2018, 'FT': 'CCGT', 'OU': 24760.0, 'WN': 26},
                 328: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 1841.0, 'WN': 26},
                 329: {'CY': 2018, 'FT': 'WIND', 'OU': 2330.0, 'WN': 27},
                 330: {'CY': 2018, 'FT': 'PS', 'OU': 2440.0, 'WN': 27},
                 331: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 27},
                 332: {'CY': 2018, 'FT': 'OCGT', 'OU': 798.0, 'WN': 27},
                 333: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7221.0, 'WN': 27},
                 334: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 810.0, 'WN': 27},
                 335: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 27},
                 336: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 27},
                 337: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 27},
                 338: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 27},
                 339: {'CY': 2018, 'FT': 'COAL', 'OU': 8124.0, 'WN': 27},
                 340: {'CY': 2018, 'FT': 'CCGT', 'OU': 24014.0, 'WN': 27},
                 341: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 1841.0, 'WN': 27},
                 342: {'CY': 2018, 'FT': 'WIND', 'OU': 2367.0, 'WN': 28},
                 343: {'CY': 2018, 'FT': 'PS', 'OU': 2440.0, 'WN': 28},
                 344: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 28},
                 345: {'CY': 2018, 'FT': 'OCGT', 'OU': 798.0, 'WN': 28},
                 346: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7311.0, 'WN': 28},
                 347: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 763.0, 'WN': 28},
                 348: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 28},
                 349: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 28},
                 350: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 28},
                 351: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 28},
                 352: {'CY': 2018, 'FT': 'COAL', 'OU': 7618.0, 'WN': 28},
                 353: {'CY': 2018, 'FT': 'CCGT', 'OU': 22767.0, 'WN': 28},
                 354: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 1841.0, 'WN': 28},
                 355: {'CY': 2018, 'FT': 'WIND', 'OU': 2368.0, 'WN': 29},
                 356: {'CY': 2018, 'FT': 'PS', 'OU': 2440.0, 'WN': 29},
                 357: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 29},
                 358: {'CY': 2018, 'FT': 'OCGT', 'OU': 798.0, 'WN': 29},
                 359: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7240.0, 'WN': 29},
                 360: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 763.0, 'WN': 29},
                 361: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 29},
                 362: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 29},
                 363: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 29},
                 364: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 29},
                 365: {'CY': 2018, 'FT': 'COAL', 'OU': 8118.0, 'WN': 29},
                 366: {'CY': 2018, 'FT': 'CCGT', 'OU': 25222.0, 'WN': 29},
                 367: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2486.0, 'WN': 29},
                 368: {'CY': 2018, 'FT': 'WIND', 'OU': 2332.0, 'WN': 30},
                 369: {'CY': 2018, 'FT': 'PS', 'OU': 2440.0, 'WN': 30},
                 370: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 30},
                 371: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 30},
                 372: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7477.0, 'WN': 30},
                 373: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 763.0, 'WN': 30},
                 374: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 30},
                 375: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 30},
                 376: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 30},
                 377: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 30},
                 378: {'CY': 2018, 'FT': 'COAL', 'OU': 9103.0, 'WN': 30},
                 379: {'CY': 2018, 'FT': 'CCGT', 'OU': 26044.0, 'WN': 30},
                 380: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 30},
                 381: {'CY': 2018, 'FT': 'WIND', 'OU': 2330.0, 'WN': 31},
                 382: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 31},
                 383: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 31},
                 384: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 31},
                 385: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7919.0, 'WN': 31},
                 386: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 868.0, 'WN': 31},
                 387: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 31},
                 388: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 31},
                 389: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 31},
                 390: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 31},
                 391: {'CY': 2018, 'FT': 'COAL', 'OU': 10089.0, 'WN': 31},
                 392: {'CY': 2018, 'FT': 'CCGT', 'OU': 25451.0, 'WN': 31},
                 393: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 31},
                 394: {'CY': 2018, 'FT': 'WIND', 'OU': 2887.0, 'WN': 32},
                 395: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 32},
                 396: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 32},
                 397: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 32},
                 398: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7111.0, 'WN': 32},
                 399: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 931.0, 'WN': 32},
                 400: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 32},
                 401: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 32},
                 402: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 32},
                 403: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 32},
                 404: {'CY': 2018, 'FT': 'COAL', 'OU': 10092.0, 'WN': 32},
                 405: {'CY': 2018, 'FT': 'CCGT', 'OU': 26770.0, 'WN': 32},
                 406: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 32},
                 407: {'CY': 2018, 'FT': 'WIND', 'OU': 2995.0, 'WN': 33},
                 408: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 33},
                 409: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 33},
                 410: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 33},
                 411: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 6852.0, 'WN': 33},
                 412: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 938.0, 'WN': 33},
                 413: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 33},
                 414: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 33},
                 415: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 33},
                 416: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 33},
                 417: {'CY': 2018, 'FT': 'COAL', 'OU': 10092.0, 'WN': 33},
                 418: {'CY': 2018, 'FT': 'CCGT', 'OU': 27610.0, 'WN': 33},
                 419: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 33},
                 420: {'CY': 2018, 'FT': 'WIND', 'OU': 2997.0, 'WN': 34},
                 421: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 34},
                 422: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 34},
                 423: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 34},
                 424: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7157.0, 'WN': 34},
                 425: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 938.0, 'WN': 34},
                 426: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 34},
                 427: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 34},
                 428: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 34},
                 429: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 34},
                 430: {'CY': 2018, 'FT': 'COAL', 'OU': 9592.0, 'WN': 34},
                 431: {'CY': 2018, 'FT': 'CCGT', 'OU': 28445.0, 'WN': 34},
                 432: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 34},
                 433: {'CY': 2018, 'FT': 'WIND', 'OU': 2988.0, 'WN': 35},
                 434: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 35},
                 435: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 35},
                 436: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 35},
                 437: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7060.0, 'WN': 35},
                 438: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 938.0, 'WN': 35},
                 439: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 35},
                 440: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 35},
                 441: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 35},
                 442: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 35},
                 443: {'CY': 2018, 'FT': 'COAL', 'OU': 11226.0, 'WN': 35},
                 444: {'CY': 2018, 'FT': 'CCGT', 'OU': 27374.0, 'WN': 35},
                 445: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 35},
                 446: {'CY': 2018, 'FT': 'WIND', 'OU': 3587.0, 'WN': 36},
                 447: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 36},
                 448: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 36},
                 449: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 36},
                 450: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7763.0, 'WN': 36},
                 451: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 975.0, 'WN': 36},
                 452: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 36},
                 453: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 36},
                 454: {'CY': 2018, 'FT': 'INTFR', 'OU': 1000.0, 'WN': 36},
                 455: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 36},
                 456: {'CY': 2018, 'FT': 'COAL', 'OU': 11226.0, 'WN': 36},
                 457: {'CY': 2018, 'FT': 'CCGT', 'OU': 26411.0, 'WN': 36},
                 458: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 36},
                 459: {'CY': 2018, 'FT': 'WIND', 'OU': 3636.0, 'WN': 37},
                 460: {'CY': 2018, 'FT': 'PS', 'OU': 2368.0, 'WN': 37},
                 461: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 37},
                 462: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 37},
                 463: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7144.0, 'WN': 37},
                 464: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1007.0, 'WN': 37},
                 465: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 37},
                 466: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 37},
                 467: {'CY': 2018, 'FT': 'INTFR', 'OU': 1000.0, 'WN': 37},
                 468: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 37},
                 469: {'CY': 2018, 'FT': 'COAL', 'OU': 11726.0, 'WN': 37},
                 470: {'CY': 2018, 'FT': 'CCGT', 'OU': 24831.0, 'WN': 37},
                 471: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 37},
                 472: {'CY': 2018, 'FT': 'WIND', 'OU': 3637.0, 'WN': 38},
                 473: {'CY': 2018, 'FT': 'PS', 'OU': 2248.0, 'WN': 38},
                 474: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 38},
                 475: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 38},
                 476: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7110.0, 'WN': 38},
                 477: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1007.0, 'WN': 38},
                 478: {'CY': 2018, 'FT': 'INTNED', 'OU': 0.0, 'WN': 38},
                 479: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 38},
                 480: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 38},
                 481: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 38},
                 482: {'CY': 2018, 'FT': 'COAL', 'OU': 11726.0, 'WN': 38},
                 483: {'CY': 2018, 'FT': 'CCGT', 'OU': 26295.0, 'WN': 38},
                 484: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 38},
                 485: {'CY': 2018, 'FT': 'WIND', 'OU': 3626.0, 'WN': 39},
                 486: {'CY': 2018, 'FT': 'PS', 'OU': 2368.0, 'WN': 39},
                 487: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 39},
                 488: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 39},
                 489: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7545.0, 'WN': 39},
                 490: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1049.0, 'WN': 39},
                 491: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 39},
                 492: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 39},
                 493: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 39},
                 494: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 39},
                 495: {'CY': 2018, 'FT': 'COAL', 'OU': 11741.0, 'WN': 39},
                 496: {'CY': 2018, 'FT': 'CCGT', 'OU': 27864.0, 'WN': 39},
                 497: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 39},
                 498: {'CY': 2018, 'FT': 'WIND', 'OU': 4850.0, 'WN': 40},
                 499: {'CY': 2018, 'FT': 'PS', 'OU': 2448.0, 'WN': 40},
                 500: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 40},
                 501: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 40},
                 502: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7501.0, 'WN': 40},
                 503: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1049.0, 'WN': 40},
                 504: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 40},
                 505: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 40},
                 506: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 40},
                 507: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 40},
                 508: {'CY': 2018, 'FT': 'COAL', 'OU': 10874.0, 'WN': 40},
                 509: {'CY': 2018, 'FT': 'CCGT', 'OU': 27994.0, 'WN': 40},
                 510: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 40},
                 511: {'CY': 2018, 'FT': 'WIND', 'OU': 4858.0, 'WN': 41},
                 512: {'CY': 2018, 'FT': 'PS', 'OU': 2448.0, 'WN': 41},
                 513: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 41},
                 514: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 41},
                 515: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7671.0, 'WN': 41},
                 516: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1049.0, 'WN': 41},
                 517: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 41},
                 518: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 41},
                 519: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 41},
                 520: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 41},
                 521: {'CY': 2018, 'FT': 'COAL', 'OU': 10874.0, 'WN': 41},
                 522: {'CY': 2018, 'FT': 'CCGT', 'OU': 27474.0, 'WN': 41},
                 523: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 41},
                 524: {'CY': 2018, 'FT': 'WIND', 'OU': 4849.0, 'WN': 42},
                 525: {'CY': 2018, 'FT': 'PS', 'OU': 2448.0, 'WN': 42},
                 526: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 42},
                 527: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 42},
                 528: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7582.0, 'WN': 42},
                 529: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1039.0, 'WN': 42},
                 530: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 42},
                 531: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 42},
                 532: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 42},
                 533: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 42},
                 534: {'CY': 2018, 'FT': 'COAL', 'OU': 10874.0, 'WN': 42},
                 535: {'CY': 2018, 'FT': 'CCGT', 'OU': 28229.0, 'WN': 42},
                 536: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 42},
                 537: {'CY': 2018, 'FT': 'WIND', 'OU': 4827.0, 'WN': 43},
                 538: {'CY': 2018, 'FT': 'PS', 'OU': 2628.0, 'WN': 43},
                 539: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 43},
                 540: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 43},
                 541: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7204.0, 'WN': 43},
                 542: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1019.0, 'WN': 43},
                 543: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 43},
                 544: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 43},
                 545: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 43},
                 546: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 43},
                 547: {'CY': 2018, 'FT': 'COAL', 'OU': 10874.0, 'WN': 43},
                 548: {'CY': 2018, 'FT': 'CCGT', 'OU': 28937.0, 'WN': 43},
                 549: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 43},
                 550: {'CY': 2018, 'FT': 'WIND', 'OU': 4717.0, 'WN': 44},
                 551: {'CY': 2018, 'FT': 'PS', 'OU': 2628.0, 'WN': 44},
                 552: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 44},
                 553: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 44},
                 554: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8456.0, 'WN': 44},
                 555: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1039.0, 'WN': 44},
                 556: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 44},
                 557: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 44},
                 558: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 44},
                 559: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 44},
                 560: {'CY': 2018, 'FT': 'COAL', 'OU': 10874.0, 'WN': 44},
                 561: {'CY': 2018, 'FT': 'CCGT', 'OU': 28190.0, 'WN': 44},
                 562: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 44},
                 563: {'CY': 2018, 'FT': 'WIND', 'OU': 5317.0, 'WN': 45},
                 564: {'CY': 2018, 'FT': 'PS', 'OU': 2628.0, 'WN': 45},
                 565: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 45},
                 566: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 45},
                 567: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8466.0, 'WN': 45},
                 568: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1039.0, 'WN': 45},
                 569: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 45},
                 570: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 45},
                 571: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 45},
                 572: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 45},
                 573: {'CY': 2018, 'FT': 'COAL', 'OU': 10874.0, 'WN': 45},
                 574: {'CY': 2018, 'FT': 'CCGT', 'OU': 27762.0, 'WN': 45},
                 575: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 45},
                 576: {'CY': 2018, 'FT': 'WIND', 'OU': 5317.0, 'WN': 46},
                 577: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 46},
                 578: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 46},
                 579: {'CY': 2018, 'FT': 'OCGT', 'OU': 836.0, 'WN': 46},
                 580: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8429.0, 'WN': 46},
                 581: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1039.0, 'WN': 46},
                 582: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 46},
                 583: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 46},
                 584: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 46},
                 585: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 46},
                 586: {'CY': 2018, 'FT': 'COAL', 'OU': 10389.0, 'WN': 46},
                 587: {'CY': 2018, 'FT': 'CCGT', 'OU': 28986.0, 'WN': 46},
                 588: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 46},
                 589: {'CY': 2018, 'FT': 'WIND', 'OU': 5317.0, 'WN': 47},
                 590: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 47},
                 591: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 47},
                 592: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 47},
                 593: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 7680.0, 'WN': 47},
                 594: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1039.0, 'WN': 47},
                 595: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 47},
                 596: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 47},
                 597: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 47},
                 598: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 47},
                 599: {'CY': 2018, 'FT': 'COAL', 'OU': 10389.0, 'WN': 47},
                 600: {'CY': 2018, 'FT': 'CCGT', 'OU': 28991.0, 'WN': 47},
                 601: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 47},
                 602: {'CY': 2018, 'FT': 'WIND', 'OU': 5317.0, 'WN': 48},
                 603: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 48},
                 604: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 48},
                 605: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 48},
                 606: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8157.0, 'WN': 48},
                 607: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1039.0, 'WN': 48},
                 608: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 48},
                 609: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 48},
                 610: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 48},
                 611: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 48},
                 612: {'CY': 2018, 'FT': 'COAL', 'OU': 10389.0, 'WN': 48},
                 613: {'CY': 2018, 'FT': 'CCGT', 'OU': 29003.0, 'WN': 48},
                 614: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2476.0, 'WN': 48},
                 615: {'CY': 2018, 'FT': 'WIND', 'OU': 6483.0, 'WN': 49},
                 616: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 49},
                 617: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 49},
                 618: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 49},
                 619: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8581.0, 'WN': 49},
                 620: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1039.0, 'WN': 49},
                 621: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 49},
                 622: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 49},
                 623: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 49},
                 624: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 49},
                 625: {'CY': 2018, 'FT': 'COAL', 'OU': 8913.0, 'WN': 49},
                 626: {'CY': 2018, 'FT': 'CCGT', 'OU': 28808.0, 'WN': 49},
                 627: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2486.0, 'WN': 49},
                 628: {'CY': 2018, 'FT': 'WIND', 'OU': 6483.0, 'WN': 50},
                 629: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 50},
                 630: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 50},
                 631: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 50},
                 632: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8555.0, 'WN': 50},
                 633: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1039.0, 'WN': 50},
                 634: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 50},
                 635: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 50},
                 636: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 50},
                 637: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 50},
                 638: {'CY': 2018, 'FT': 'COAL', 'OU': 8913.0, 'WN': 50},
                 639: {'CY': 2018, 'FT': 'CCGT', 'OU': 29648.0, 'WN': 50},
                 640: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2486.0, 'WN': 50},
                 641: {'CY': 2018, 'FT': 'WIND', 'OU': 6483.0, 'WN': 51},
                 642: {'CY': 2018, 'FT': 'PS', 'OU': 2728.0, 'WN': 51},
                 643: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 51},
                 644: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 51},
                 645: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8076.0, 'WN': 51},
                 646: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1049.0, 'WN': 51},
                 647: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 51},
                 648: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 51},
                 649: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 51},
                 650: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 51},
                 651: {'CY': 2018, 'FT': 'COAL', 'OU': 8913.0, 'WN': 51},
                 652: {'CY': 2018, 'FT': 'CCGT', 'OU': 29851.0, 'WN': 51},
                 653: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2486.0, 'WN': 51},
                 654: {'CY': 2018, 'FT': 'WIND', 'OU': 6483.0, 'WN': 52},
                 655: {'CY': 2018, 'FT': 'PS', 'OU': 2548.0, 'WN': 52},
                 656: {'CY': 2018, 'FT': 'OTHER', 'OU': 6.0, 'WN': 52},
                 657: {'CY': 2018, 'FT': 'OCGT', 'OU': 837.0, 'WN': 52},
                 658: {'CY': 2018, 'FT': 'NUCLEAR', 'OU': 8966.0, 'WN': 52},
                 659: {'CY': 2018, 'FT': 'NPSHYD', 'OU': 1049.0, 'WN': 52},
                 660: {'CY': 2018, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 52},
                 661: {'CY': 2018, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 52},
                 662: {'CY': 2018, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 52},
                 663: {'CY': 2018, 'FT': 'INTEW', 'OU': 500.0, 'WN': 52},
                 664: {'CY': 2018, 'FT': 'COAL', 'OU': 8913.0, 'WN': 52},
                 665: {'CY': 2018, 'FT': 'CCGT', 'OU': 29851.0, 'WN': 52},
                 666: {'CY': 2018, 'FT': 'BIOMASS', 'OU': 2486.0, 'WN': 52},
                 667: {'CY': 2019, 'FT': 'WIND', 'OU': 6458.0, 'WN': 1},
                 668: {'CY': 2019, 'FT': 'PS', 'OU': 2548.0, 'WN': 1},
                 669: {'CY': 2019, 'FT': 'OTHER', 'OU': 0.0, 'WN': 1},
                 670: {'CY': 2019, 'FT': 'OCGT', 'OU': 836.0, 'WN': 1},
                 671: {'CY': 2019, 'FT': 'NUCLEAR', 'OU': 8853.0, 'WN': 1},
                 672: {'CY': 2019, 'FT': 'NPSHYD', 'OU': 1048.0, 'WN': 1},
                 673: {'CY': 2019, 'FT': 'INTNED', 'OU': 1000.0, 'WN': 1},
                 674: {'CY': 2019, 'FT': 'INTIRL', 'OU': 500.0, 'WN': 1},
                 675: {'CY': 2019, 'FT': 'INTFR', 'OU': 2000.0, 'WN': 1},
                 676: {'CY': 2019, 'FT': 'INTEW', 'OU': 500.0, 'WN': 1},
                 677: {'CY': 2019, 'FT': 'COAL', 'OU': 8913.0, 'WN': 1},
                 678: {'CY': 2019, 'FT': 'CCGT', 'OU': 29851.0, 'WN': 1},
                 679: {'CY': 2019, 'FT': 'BIOMASS', 'OU': 2486.0, 'WN': 1}}
                         }

        self.assertEqual(message_to_dict(input_str), expected_dict)

if __name__ == '__main__':
    unittest.main()
