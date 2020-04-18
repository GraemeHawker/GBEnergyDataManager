# -*- coding: utf-8 -*-
"""
command to generate annual datafiles for given data subsets
"""
import datetime as dt
import pandas as pd
import numpy as np
import pytz
import psycopg2
import os
from tqdm import tqdm
from django.core.management.base import BaseCommand, CommandError
from GBEnergyDataManager.settings import BASE_DIR, DATABASES, NETA_USER, NETA_PWD, NETA_BMU_LIST_URL, DATA_SUMMARY_LOCS

class Command(BaseCommand):
    help = 'downloads BMRA data for specific date range, expected 2 arguments of form yyyy-m-d'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
