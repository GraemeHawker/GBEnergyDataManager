# -*- coding: utf-8 -*-
"""
testing sending email
"""
#import datetime as dt
#import pandas as pd
#import numpy as np
#import pytz
#import psycopg2
#import os
#from tqdm import tqdm
from django.core.management.base import BaseCommand, CommandError
#from GBEnergyDataManager.settings import BASE_DIR, DATABASES, NETA_USER, NETA_PWD, NETA_BMU_LIST_URL, DATA_SUMMARY_LOCS
from django.core.mail import send_mail
from django.core.mail import EmailMessage


class Command(BaseCommand):
    help = 'sends a test email'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        email = EmailMessage(
            subject='test',
            body='test',
            from_email='graeme@lutralutra.co.uk',
            to=['graeme.hawker@strath.ac.uk'],
            reply_to=['graeme@lutralutra.co.uk'],
            headers={'Content-Type': 'text/plain'},
        )
        email.send()
