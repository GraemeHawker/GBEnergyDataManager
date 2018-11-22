"""
Copyright (C) 2018 ElexonDataManager contributors listed in AUTHORS.
Licensed under the Apache 2.0 License (see LICENSE file).

data_processing_test.py
~~~~~~~~
Unit tests for the data processing functions

"""

import unittest
import datetime as dt
from upload_functions import message_to_dict

class DataProcessingTestCase(unittest.TestCase):
    """
    Tests data processing functions
    """
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
                         'data_pairs':
                         {1:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 0, 0),
                           'VP' : 0.0},
                          2:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 30, 0),
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
                         'data_pairs':
                         {1:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 0, 0),
                           'VP' : 0.0},
                          2:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 30, 0),
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
                         'data_pairs':
                         {1:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 0, 0),
                           'VE' : 602.0},
                          2:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 30, 0),
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
                         'data_pairs':
                         {1:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 0, 0),
                           'VF' : 0.0},
                          2:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 30, 0),
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
                         'data_pairs':
                         {1:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 0, 0),
                           'VB' : -645.0},
                          2:
                          {'timestamp' : dt.datetime(2017, 3, 29, 1, 30, 0),
                           'VB' : -645.0}}}
        self.assertEqual(message_to_dict(input_str), expected_dict)

if __name__ == '__main__':
    unittest.main()
