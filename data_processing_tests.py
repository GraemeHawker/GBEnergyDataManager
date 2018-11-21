"""

"""
__author__ = 'graeme.hawker'

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
                         'SD' : dt.datetime(2017,3,29),
                         'SP' : 5,
                         'pairs':
                                { '1' :
                                  { 'timestamp' : dt.datetime(2017, 3, 29, 1, 0, 0),
                                    'value' : 0.0},
                                  '2' :
                                  { 'timestamp' : dt.datetime(2017, 3, 29, 1, 30, 0),
                                    'value' : 0.0}}
                         }
        self.assertEqual(message_to_dict(input_str), expected_dict)

if __name__ == '__main__':
    unittest.main()
