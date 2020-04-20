# -*- coding: utf-8 -*-
"""
command to download and process BMRA data for specific date
"""
import sys
import datetime as dt
from django.core.management.base import BaseCommand, CommandError
from ._download_functions import process_bmra_file
from P114.management.commands._download_functions import process_p114_date
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'downloads all data for previous day'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        email_log = {}
        self.stdout.write('Started: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        email_log[dt.datetime.now()] = 'Started'
        date = dt.date.today()-dt.timedelta(days=1)
        self.stdout.write('downloading data for {:%Y-%m-%d}'.format(date))
        email_log[dt.datetime.now()] = 'downloading data for {:%Y-%m-%d}'.format(date)
        try:
            bmra_processed_log = process_bmra_file(date)
            if 
            email_log[dt.datetime.now()] = 'BMRA processing completed, {} files and {} messages processed'.format(p114_processed)
        except:
            email_log[dt.datetime.now()] = 'BMRA processing failed with error: {}'.format(sys.exc_info()[0])
        try:
            p114_processed_log = process_p114_date(date)
            email_log[dt.datetime.now()] = 'P114 processing completed, {} files processed'.format(p114_processed)
        except:
            email_log[dt.datetime.now()] = 'P114 processing failed with error: {}'.format(sys.exc_info()[0])
        self.stdout.write('Finished: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        email_log[dt.datetime.now()] = 'Finished'
        formatted_report = '\n'.join("{:%Y-%m-%d %H:%M:%S} {}".format(k,v) for (k,v) in email_log.items())
        send_mail(
            'File processing report for {:%Y-%m-%d}'.format(date),
            formatted_report,
            'graeme.hawker@strath.ac.uk',
            ['graeme.hawker@strath.ac.uk'],
            fail_silently=False,
        )
