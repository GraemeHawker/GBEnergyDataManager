"""
Tests for functions contained in ElexonDataManager.utils
"""
from __future__ import unicode_literals
import datetime as dt
from django.test import TestCase
from django.utils import timezone
from ElexonDataManager.utils import sp_to_dt, dt_to_sp, get_sp_list

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

        #checks for date within DST
        self.assertEqual(dt_to_sp(dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 7, 1), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 7, 1), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 7, 1), 1))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 7, 1), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc), True),
                         (dt.date(2018, 7, 1), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc), False),
                         (dt.date(2018, 7, 1), 2))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 7, 1), 3))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 7, 1), 3))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 0, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 7, 1), 3))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 22, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 7, 1), 47))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 22, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 7, 1), 47))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 22, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 7, 1), 47))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 22, 40, tzinfo=timezone.utc)),
                         (dt.date(2018, 7, 1), 48))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 22, 30, tzinfo=timezone.utc), True),
                         (dt.date(2018, 7, 1), 48))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 7, 1, 23, 0, tzinfo=timezone.utc), False),
                         (dt.date(2018, 7, 1), 48))


        #checks for times on DST changeover - clocks going forward
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 0, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 25), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 0, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 3, 25), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 0, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 3, 25), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 0, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 25), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 1, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 25), 3))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 1, 0, tzinfo=timezone.utc),False),
                         (dt.date(2018, 3, 25), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 1, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 25), 4))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 1, 30, tzinfo=timezone.utc), True),
                         (dt.date(2018, 3, 25), 4))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 1, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 3, 25), 3))

        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 22, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 25), 45))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 22, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 25), 46))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 22, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 3, 25), 45))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 23, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 26), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 25, 23, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 26), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 3, 26, 0, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 3, 26), 3))


        #checks for times on DST changeover - clocks going back
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 27, 23, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 27, 23, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 10, 28), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 27, 23, 0, tzinfo=timezone.utc), False),
                         (dt.date(2018, 10, 27), 48))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 27, 23, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 0, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 3))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 0, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 4))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 1, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 5))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 21, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 45))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 21, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 46))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 21, 30, tzinfo=timezone.utc), True),
                         (dt.date(2018, 10, 28), 46))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 21, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 10, 28), 45))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 22, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 47))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 22, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 48))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 23, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 49))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 23, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 28), 50))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 23, 30, tzinfo=timezone.utc), True),
                         (dt.date(2018, 10, 28), 50))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 28, 23, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 10, 28), 49))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 29), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 10, 29), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 0, 0, tzinfo=timezone.utc), False),
                         (dt.date(2018, 10, 28), 50))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 29), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc), True),
                         (dt.date(2018, 10, 29), 2))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 0, 30, tzinfo=timezone.utc), False),
                         (dt.date(2018, 10, 29), 1))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc)),
                         (dt.date(2018, 10, 29), 3))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc), True),
                         (dt.date(2018, 10, 29), 3))
        self.assertEqual(dt_to_sp(dt.datetime(2018, 10, 29, 1, 0, tzinfo=timezone.utc), False),
                         (dt.date(2018, 10, 29), 2))

class TimeListCase(TestCase):
    """
    Tests for generating SD/SP lists
    """
    def test_get_sp_list(self):
        """Can generate sp lists"""
        #check for basic non-DST dates
        self.assertEqual(get_sp_list(dt.date(2018, 1, 1), dt.date(2018, 1, 2)),
                         [(dt.date(2018, 1, 1), 1),
                          (dt.date(2018, 1, 1), 2),
                          (dt.date(2018, 1, 1), 3),
                          (dt.date(2018, 1, 1), 4),
                          (dt.date(2018, 1, 1), 5),
                          (dt.date(2018, 1, 1), 6),
                          (dt.date(2018, 1, 1), 7),
                          (dt.date(2018, 1, 1), 8),
                          (dt.date(2018, 1, 1), 9),
                          (dt.date(2018, 1, 1), 10),
                          (dt.date(2018, 1, 1), 11),
                          (dt.date(2018, 1, 1), 12),
                          (dt.date(2018, 1, 1), 13),
                          (dt.date(2018, 1, 1), 14),
                          (dt.date(2018, 1, 1), 15),
                          (dt.date(2018, 1, 1), 16),
                          (dt.date(2018, 1, 1), 17),
                          (dt.date(2018, 1, 1), 18),
                          (dt.date(2018, 1, 1), 19),
                          (dt.date(2018, 1, 1), 20),
                          (dt.date(2018, 1, 1), 21),
                          (dt.date(2018, 1, 1), 22),
                          (dt.date(2018, 1, 1), 23),
                          (dt.date(2018, 1, 1), 24),
                          (dt.date(2018, 1, 1), 25),
                          (dt.date(2018, 1, 1), 26),
                          (dt.date(2018, 1, 1), 27),
                          (dt.date(2018, 1, 1), 28),
                          (dt.date(2018, 1, 1), 29),
                          (dt.date(2018, 1, 1), 30),
                          (dt.date(2018, 1, 1), 31),
                          (dt.date(2018, 1, 1), 32),
                          (dt.date(2018, 1, 1), 33),
                          (dt.date(2018, 1, 1), 34),
                          (dt.date(2018, 1, 1), 35),
                          (dt.date(2018, 1, 1), 36),
                          (dt.date(2018, 1, 1), 37),
                          (dt.date(2018, 1, 1), 38),
                          (dt.date(2018, 1, 1), 39),
                          (dt.date(2018, 1, 1), 40),
                          (dt.date(2018, 1, 1), 41),
                          (dt.date(2018, 1, 1), 42),
                          (dt.date(2018, 1, 1), 43),
                          (dt.date(2018, 1, 1), 44),
                          (dt.date(2018, 1, 1), 45),
                          (dt.date(2018, 1, 1), 46),
                          (dt.date(2018, 1, 1), 47),
                          (dt.date(2018, 1, 1), 48),
                          (dt.date(2018, 1, 2), 1),
                          (dt.date(2018, 1, 2), 2),
                          (dt.date(2018, 1, 2), 3),
                          (dt.date(2018, 1, 2), 4),
                          (dt.date(2018, 1, 2), 5),
                          (dt.date(2018, 1, 2), 6),
                          (dt.date(2018, 1, 2), 7),
                          (dt.date(2018, 1, 2), 8),
                          (dt.date(2018, 1, 2), 9),
                          (dt.date(2018, 1, 2), 10),
                          (dt.date(2018, 1, 2), 11),
                          (dt.date(2018, 1, 2), 12),
                          (dt.date(2018, 1, 2), 13),
                          (dt.date(2018, 1, 2), 14),
                          (dt.date(2018, 1, 2), 15),
                          (dt.date(2018, 1, 2), 16),
                          (dt.date(2018, 1, 2), 17),
                          (dt.date(2018, 1, 2), 18),
                          (dt.date(2018, 1, 2), 19),
                          (dt.date(2018, 1, 2), 20),
                          (dt.date(2018, 1, 2), 21),
                          (dt.date(2018, 1, 2), 22),
                          (dt.date(2018, 1, 2), 23),
                          (dt.date(2018, 1, 2), 24),
                          (dt.date(2018, 1, 2), 25),
                          (dt.date(2018, 1, 2), 26),
                          (dt.date(2018, 1, 2), 27),
                          (dt.date(2018, 1, 2), 28),
                          (dt.date(2018, 1, 2), 29),
                          (dt.date(2018, 1, 2), 30),
                          (dt.date(2018, 1, 2), 31),
                          (dt.date(2018, 1, 2), 32),
                          (dt.date(2018, 1, 2), 33),
                          (dt.date(2018, 1, 2), 34),
                          (dt.date(2018, 1, 2), 35),
                          (dt.date(2018, 1, 2), 36),
                          (dt.date(2018, 1, 2), 37),
                          (dt.date(2018, 1, 2), 38),
                          (dt.date(2018, 1, 2), 39),
                          (dt.date(2018, 1, 2), 40),
                          (dt.date(2018, 1, 2), 41),
                          (dt.date(2018, 1, 2), 42),
                          (dt.date(2018, 1, 2), 43),
                          (dt.date(2018, 1, 2), 44),
                          (dt.date(2018, 1, 2), 45),
                          (dt.date(2018, 1, 2), 46),
                          (dt.date(2018, 1, 2), 47),
                          (dt.date(2018, 1, 2), 48)])

        self.assertEqual(get_sp_list(dt.date(2018, 1, 1), dt.date(2018, 1, 2), 21 , 4),
                         [(dt.date(2018, 1, 1), 21),
                          (dt.date(2018, 1, 1), 22),
                          (dt.date(2018, 1, 1), 23),
                          (dt.date(2018, 1, 1), 24),
                          (dt.date(2018, 1, 1), 25),
                          (dt.date(2018, 1, 1), 26),
                          (dt.date(2018, 1, 1), 27),
                          (dt.date(2018, 1, 1), 28),
                          (dt.date(2018, 1, 1), 29),
                          (dt.date(2018, 1, 1), 30),
                          (dt.date(2018, 1, 1), 31),
                          (dt.date(2018, 1, 1), 32),
                          (dt.date(2018, 1, 1), 33),
                          (dt.date(2018, 1, 1), 34),
                          (dt.date(2018, 1, 1), 35),
                          (dt.date(2018, 1, 1), 36),
                          (dt.date(2018, 1, 1), 37),
                          (dt.date(2018, 1, 1), 38),
                          (dt.date(2018, 1, 1), 39),
                          (dt.date(2018, 1, 1), 40),
                          (dt.date(2018, 1, 1), 41),
                          (dt.date(2018, 1, 1), 42),
                          (dt.date(2018, 1, 1), 43),
                          (dt.date(2018, 1, 1), 44),
                          (dt.date(2018, 1, 1), 45),
                          (dt.date(2018, 1, 1), 46),
                          (dt.date(2018, 1, 1), 47),
                          (dt.date(2018, 1, 1), 48),
                          (dt.date(2018, 1, 2), 1),
                          (dt.date(2018, 1, 2), 2),
                          (dt.date(2018, 1, 2), 3),
                          (dt.date(2018, 1, 2), 4)])

        self.assertEqual(get_sp_list(dt.date(2018, 3, 25), dt.date(2018, 3, 26), 21 , 4),
                         [(dt.date(2018, 3, 25), 21),
                          (dt.date(2018, 3, 25), 22),
                          (dt.date(2018, 3, 25), 23),
                          (dt.date(2018, 3, 25), 24),
                          (dt.date(2018, 3, 25), 25),
                          (dt.date(2018, 3, 25), 26),
                          (dt.date(2018, 3, 25), 27),
                          (dt.date(2018, 3, 25), 28),
                          (dt.date(2018, 3, 25), 29),
                          (dt.date(2018, 3, 25), 30),
                          (dt.date(2018, 3, 25), 31),
                          (dt.date(2018, 3, 25), 32),
                          (dt.date(2018, 3, 25), 33),
                          (dt.date(2018, 3, 25), 34),
                          (dt.date(2018, 3, 25), 35),
                          (dt.date(2018, 3, 25), 36),
                          (dt.date(2018, 3, 25), 37),
                          (dt.date(2018, 3, 25), 38),
                          (dt.date(2018, 3, 25), 39),
                          (dt.date(2018, 3, 25), 40),
                          (dt.date(2018, 3, 25), 41),
                          (dt.date(2018, 3, 25), 42),
                          (dt.date(2018, 3, 25), 43),
                          (dt.date(2018, 3, 25), 44),
                          (dt.date(2018, 3, 25), 45),
                          (dt.date(2018, 3, 25), 46),
                          (dt.date(2018, 3, 26), 1),
                          (dt.date(2018, 3, 26), 2),
                          (dt.date(2018, 3, 26), 3),
                          (dt.date(2018, 3, 26), 4)])

        self.assertEqual(get_sp_list(dt.date(2018, 10, 28), dt.date(2018, 10, 29), 21 , 4),
                         [(dt.date(2018, 10, 28), 21),
                          (dt.date(2018, 10, 28), 22),
                          (dt.date(2018, 10, 28), 23),
                          (dt.date(2018, 10, 28), 24),
                          (dt.date(2018, 10, 28), 25),
                          (dt.date(2018, 10, 28), 26),
                          (dt.date(2018, 10, 28), 27),
                          (dt.date(2018, 10, 28), 28),
                          (dt.date(2018, 10, 28), 29),
                          (dt.date(2018, 10, 28), 30),
                          (dt.date(2018, 10, 28), 31),
                          (dt.date(2018, 10, 28), 32),
                          (dt.date(2018, 10, 28), 33),
                          (dt.date(2018, 10, 28), 34),
                          (dt.date(2018, 10, 28), 35),
                          (dt.date(2018, 10, 28), 36),
                          (dt.date(2018, 10, 28), 37),
                          (dt.date(2018, 10, 28), 38),
                          (dt.date(2018, 10, 28), 39),
                          (dt.date(2018, 10, 28), 40),
                          (dt.date(2018, 10, 28), 41),
                          (dt.date(2018, 10, 28), 42),
                          (dt.date(2018, 10, 28), 43),
                          (dt.date(2018, 10, 28), 44),
                          (dt.date(2018, 10, 28), 45),
                          (dt.date(2018, 10, 28), 46),
                          (dt.date(2018, 10, 28), 47),
                          (dt.date(2018, 10, 28), 48),
                          (dt.date(2018, 10, 28), 49),
                          (dt.date(2018, 10, 28), 50),
                          (dt.date(2018, 10, 29), 1),
                          (dt.date(2018, 10, 29), 2),
                          (dt.date(2018, 10, 29), 3),
                          (dt.date(2018, 10, 29), 4)])
