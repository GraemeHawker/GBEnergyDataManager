# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime as dt
from django.test import TestCase
from ElexonDataManager.utils import sp_to_dt, dt_to_sp

class TimeConversionCase(TestCase):

    def test_sp_to_dt_nonbst(self):
        """Can convert non-BST settlement period to datetime"""
        sd = dt.date(2018, 1, 1)
        sp = 12
        self.assertEqual(sp_to_dt(sd, sp), dt.datetime(2018, 1, 1, 5, 30))
        self.assertEqual(sp_to_dt(sd, sp, False), dt.datetime(2018, 1, 1, 6))

    def test_sp_to_dt_bst(self):
        """Can convert BST settlement period to datetime"""
        sd = dt.date(2018, 6, 1)
        sp = 12
        self.assertEqual(sp_to_dt(sd, sp), dt.datetime(2018, 1, 1, 5, 30))
        self.assertEqual(sp_to_dt(sd, sp, False), dt.datetime(2018, 1, 1, 6))

    def test_dt_to_sp_nonbst(self):
        """Can convert non-BST datetime to settlement period"""
        datetime = dt.date(2018, 1, 1, 5, 30)
        self.assertEqual(dt_to_sp(datetime), (dt.date(2018, 1, 1), 12))
        self.assertEqual(dt_to_sp(datetime, False), (dt.date(2018, 1, 1), 11))

    def test_dt_to_sp_bst(self):
        """Can convert BST datetime to settlement period"""
        datetime = dt.date(2018, 6, 1, 5, 30)
        self.assertEqual(dt_to_sp(datetime), (dt.date(2018, 6, 1), 12))
        self.assertEqual(dt_to_sp(datetime, False), (dt.date(2018, 6, 1), 11))
