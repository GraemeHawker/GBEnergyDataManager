"""
Tests for functions contained in ElexonDataManager.utils
"""
from __future__ import unicode_literals
import datetime as dt
from django.test import TestCase
from django.utils import timezone
from ElexonDataManager.utils import sp_to_dt, dt_to_sp

class TimeConversionCase(TestCase):
    """
    Tests for SD/SP timestamp conversion functions
    """
    def test_sp_to_dt(self):
        """Can convert settlement period to datetime"""
        #checks for basic non-DST date
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 1),
                         dt.datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 1, True),
                         dt.datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 1, False),
                         dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 2),
                         dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 2, True),
                         dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 2, False),
                         dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 3),
                         dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 3, True),
                         dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 3, False),
                         dt.datetime(2018, 1, 1, 1, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 47),
                         dt.datetime(2018, 1, 1, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 47, True),
                         dt.datetime(2018, 1, 1, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 47, False),
                         dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 48),
                         dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 48, True),
                         dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 1, 1), 48, False),
                         dt.datetime(2018, 1, 2, 0, 0, tzinfo=timezone.utc))

        #checks for date within DST
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 1),
                         dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 1, True),
                         dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 1, False),
                         dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 2),
                         dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 2, True),
                         dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 2, False),
                         dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 3),
                         dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 3, True),
                         dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 3, False),
                         dt.datetime(2018, 7, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 47),
                         dt.datetime(2018, 7, 1, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 47, True),
                         dt.datetime(2018, 7, 1, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 47, False),
                         dt.datetime(2018, 7, 1, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 48),
                         dt.datetime(2018, 7, 1, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 48, True),
                         dt.datetime(2018, 7, 1, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 7, 1), 48, False),
                         dt.datetime(2018, 7, 1, 23, 0, tzinfo=timezone.utc))

        #checks for times on DST changeover - clocks going forward
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 1),
                         dt.datetime(2018, 3, 25, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 1, True),
                         dt.datetime(2018, 3, 25, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 1, False),
                         dt.datetime(2018, 3, 25, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 2),
                         dt.datetime(2018, 3, 25, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 3),
                         dt.datetime(2018, 3, 25, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 45),
                         dt.datetime(2018, 3, 25, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 46),
                         dt.datetime(2018, 3, 25, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 46, True),
                         dt.datetime(2018, 3, 25, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 25), 46, False),
                         dt.datetime(2018, 3, 25, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 1),
                         dt.datetime(2018, 3, 25, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 1, True),
                         dt.datetime(2018, 3, 25, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 1, False),
                         dt.datetime(2018, 3, 25, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 2),
                         dt.datetime(2018, 3, 25, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 2, True),
                         dt.datetime(2018, 3, 25, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 2, False),
                         dt.datetime(2018, 3, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 3),
                         dt.datetime(2018, 3, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 3, True),
                         dt.datetime(2018, 3, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 3, 26), 3, False),
                         dt.datetime(2018, 3, 26, 0, 30, tzinfo=timezone.utc))

        #checks for times on DST changeover - clocks going back
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 1),
                         dt.datetime(2018, 10, 27, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 1, True),
                         dt.datetime(2018, 10, 27, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 1, False),
                         dt.datetime(2018, 10, 27, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 2),
                         dt.datetime(2018, 10, 27, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 3),
                         dt.datetime(2018, 10, 28, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 4),
                         dt.datetime(2018, 10, 28, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 5),
                         dt.datetime(2018, 10, 28, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 45),
                         dt.datetime(2018, 10, 28, 21, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 46),
                         dt.datetime(2018, 10, 28, 21, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 46, True),
                         dt.datetime(2018, 10, 28, 21, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 46, False),
                         dt.datetime(2018, 10, 28, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 47),
                         dt.datetime(2018, 10, 28, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 48),
                         dt.datetime(2018, 10, 28, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 49),
                         dt.datetime(2018, 10, 28, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 50),
                         dt.datetime(2018, 10, 28, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 50, True),
                         dt.datetime(2018, 10, 28, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 28), 50, False),
                         dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 1),
                         dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 1, True),
                         dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 1, False),
                         dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 2),
                         dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 2, True),
                         dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 2, False),
                         dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 3),
                         dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 3, True),
                         dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.date(2018, 10, 29), 3, False),
                         dt.datetime(2018, 10, 29, 1, 30, tzinfo=timezone.utc))

        #checks for invalid SP
        self.assertRaises(ValueError, sp_to_dt, dt.date(2018, 1, 1), 0)
        self.assertRaises(ValueError, sp_to_dt, dt.date(2018, 1, 1), -1)
        self.assertRaises(ValueError, sp_to_dt, dt.date(2018, 1, 1), 49)
        self.assertRaises(ValueError, sp_to_dt, dt.date(2018, 3, 25), 47)

        #check for invalid SD Type
        self.assertRaises(ValueError, sp_to_dt, dt.datetime(2018, 1, 1), 0)

    def test_dt_to_sp(self):
        """Can convert datetime to settlement period"""

        #checks for basic non-DST date
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 1, 1), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 1, 1), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 1, 1), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 0, 10, tzinfo=timezone.utc)),
                         (dt.date(2018, 1, 1), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 0, 10, tzinfo=timezone.utc), True),
                         (dt.date(2018, 1, 1), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 0, 10, tzinfo=timezone.utc), False),
                         (dt.date(2018, 1, 1), 1))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 1, 1), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc), True),
                         (dt.date(2018, 1, 1), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc), False),
                         (dt.date(2018, 1, 1), 2))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 1, 1), 3))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 1, 1), 3))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 1, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 1, 1), 3))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 23, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 1, 1), 47))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 23, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 1, 1), 47))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 1, 1), 47))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 1, 1), 48))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc), True),
                         (dt.date(2018, 1, 1), 48))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 1, 2, 0, 0, tzinfo=timezone.utc), False),
                         (dt.date(2018, 1, 1), 48))

        '''
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 1, True),
                         dt.datetime(2018, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 1, False),
                         dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 2),
                         dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 2, True),
                         dt.datetime(2018, 1, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 2, False),
                         dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 3),
                         dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 3, True),
                         dt.datetime(2018, 1, 1, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 3, False),
                         dt.datetime(2018, 1, 1, 1, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 47),
                         dt.datetime(2018, 1, 1, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 47, True),
                         dt.datetime(2018, 1, 1, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 47, False),
                         dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 48),
                         dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 48, True),
                         dt.datetime(2018, 1, 1, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 1, 1), 48, False),
                         dt.datetime(2018, 1, 2, 0, 0, tzinfo=timezone.utc))

        #checks for date within DST
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 1),
                         dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 1, True),
                         dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 1, False),
                         dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 2),
                         dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 2, True),
                         dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 2, False),
                         dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 3),
                         dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 3, True),
                         dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 3, False),
                         dt.datetime(2018, 7, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 47),
                         dt.datetime(2018, 7, 1, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 47, True),
                         dt.datetime(2018, 7, 1, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 47, False),
                         dt.datetime(2018, 7, 1, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 48),
                         dt.datetime(2018, 7, 1, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 48, True),
                         dt.datetime(2018, 7, 1, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 7, 1), 48, False),
                         dt.datetime(2018, 7, 1, 23, 0, tzinfo=timezone.utc))

        #checks for times on DST changeover - clocks going forward
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 1),
                         dt.datetime(2018, 3, 25, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 1, True),
                         dt.datetime(2018, 3, 25, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 1, False),
                         dt.datetime(2018, 3, 25, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 2),
                         dt.datetime(2018, 3, 25, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 3),
                         dt.datetime(2018, 3, 25, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 45),
                         dt.datetime(2018, 3, 25, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 46),
                         dt.datetime(2018, 3, 25, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 46, True),
                         dt.datetime(2018, 3, 25, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 25), 46, False),
                         dt.datetime(2018, 3, 25, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 1),
                         dt.datetime(2018, 3, 25, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 1, True),
                         dt.datetime(2018, 3, 25, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 1, False),
                         dt.datetime(2018, 3, 25, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 2),
                         dt.datetime(2018, 3, 25, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 2, True),
                         dt.datetime(2018, 3, 25, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 2, False),
                         dt.datetime(2018, 3, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 3),
                         dt.datetime(2018, 3, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 3, True),
                         dt.datetime(2018, 3, 26, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 3, 26), 3, False),
                         dt.datetime(2018, 3, 26, 0, 30, tzinfo=timezone.utc))

        #checks for times on DST changeover - clocks going back
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 1),
                         dt.datetime(2018, 10, 27, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 1, True),
                         dt.datetime(2018, 10, 27, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 1, False),
                         dt.datetime(2018, 10, 27, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 2),
                         dt.datetime(2018, 10, 27, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 3),
                         dt.datetime(2018, 10, 28, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 4),
                         dt.datetime(2018, 10, 28, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 5),
                         dt.datetime(2018, 10, 28, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 45),
                         dt.datetime(2018, 10, 28, 21, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 46),
                         dt.datetime(2018, 10, 28, 21, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 46, True),
                         dt.datetime(2018, 10, 28, 21, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 46, False),
                         dt.datetime(2018, 10, 28, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 47),
                         dt.datetime(2018, 10, 28, 22, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 48),
                         dt.datetime(2018, 10, 28, 22, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 49),
                         dt.datetime(2018, 10, 28, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 50),
                         dt.datetime(2018, 10, 28, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 50, True),
                         dt.datetime(2018, 10, 28, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 28), 50, False),
                         dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 1),
                         dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 1, True),
                         dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 1, False),
                         dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 2),
                         dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 2, True),
                         dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 2, False),
                         dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 3),
                         dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 3, True),
                         dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(dt_to_sp(dt.date(2018, 10, 29), 3, False),
                         dt.datetime(2018, 10, 29, 1, 30, tzinfo=timezone.utc))
        '''
