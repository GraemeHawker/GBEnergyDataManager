# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime as dt
from django.test import TestCase
from django.utils import timezone
from ElexonDataManager.utils import sp_to_dt, dt_to_sp

class TimeConversionCase(TestCase):

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
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 1), dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 1, True), dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 1, False), dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 2), dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 2, True), dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 2, False), dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 3), dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 3, True), dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 3, False), dt.datetime(2018, 7, 1, 0, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 47), dt.datetime(2018, 7, 1, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 47, True), dt.datetime(2018, 7, 1, 23, 30, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 47, False), dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 48), dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 48, True), dt.datetime(2018, 7, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 7, 1), 48, False), dt.datetime(2018, 7, 1, 0, 30, tzinfo=timezone.utc))

        #checks for times on DST changeover
        self.assertEqual(sp_to_dt(dt.datetime(2018, 3, 25), 1), dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 3, 25), 1, True), dt.datetime(2018, 6, 30, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(sp_to_dt(dt.datetime(2018, 3, 25), 1, False), dt.datetime(2018, 6, 30, 23, 30, tzinfo=timezone.utc))

    '''
    def test_dt_to_sp_nonbst(self):
        """Can convert non-BST datetime to settlement period"""
        datetime = dt.datetime(2018, 1, 1, 5, 30, tzinfo=timezone.utc)
        self.assertEqual(dt_to_sp(datetime), (dt.date(2018, 1, 1), 12))
        self.assertEqual(dt_to_sp(datetime, False), (dt.date(2018, 1, 1), 11))

    def test_dt_to_sp_bst(self):
        """Can convert BST datetime to settlement period"""
        datetime = dt.datetime(2018, 6, 1, 5, 30, tzinfo=timezone.utc)
        self.assertEqual(dt_to_sp(datetime), (dt.date(2018, 6, 1), 12))
        self.assertEqual(dt_to_sp(datetime, False), (dt.date(2018, 6, 1), 11))
    '''
