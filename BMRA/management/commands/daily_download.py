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
        parser.add_argument('days_back', nargs='?', type=int, default=0)

    def handle(self, *args, **options):
        email_log = {}
        formatted_report = ''
        self.stdout.write('Started: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        email_log[dt.datetime.now()] = 'Started'
        date = dt.date.today()-dt.timedelta(days=options['days_back']+1)
        self.stdout.write('downloading data for {:%Y-%m-%d}'.format(date))
        email_log[dt.datetime.now()] = 'downloading data for {:%Y-%m-%d}'.format(date)
        try:
            combined_insert_log = process_bmra_file(date)
            email_log[dt.datetime.now()] = 'BMRA processing completed'
            formatted_report += '\n {} BMRA messages processed'.format(combined_insert_log['count'])
            for new_bmu in combined_insert_log['new_bmus']:
                formatted_report += '\n New BMU created: {}'.format(new_bmu)
            for key, value in combined_insert_log['inserts'].items():
                formatted_report += '\n {} {} messages processed'.format(key,value)
            for key, value in combined_insert_log['unprocessed_msg'].items():
                formatted_report += '\n {} {} messages not processed'.format(key,value)
            for key, value in combined_insert_log['duplicate_msg'].items():
                formatted_report += '\n {} {} messages duplicates'.format(key,value)
        except Exception as e:
            email_log[dt.datetime.now()] = 'BMRA processing failed with error: {} {}'.format(type(e).__name__, e.args)
        try:
            p114_processed_log = process_p114_date(date)
            email_log[dt.datetime.now()] = 'P114 processing completed'
        except Exception as e:
            email_log[dt.datetime.now()] = 'P114 processing failed with error: {} {}'.format(type(e).__name__, e.args)
        self.stdout.write('Finished: {:%Y-%m-%d %H:%M:%S}'.format(dt.datetime.now()))
        email_log[dt.datetime.now()] = 'Finished'
        formatted_report +='\n'+'\n'.join("{:%Y-%m-%d %H:%M:%S} {}".format(k,v) for (k,v) in email_log.items())
        send_mail(
            'File processing report for {:%Y-%m-%d}'.format(date),
            formatted_report,
            'graeme.hawker@strath.ac.uk',
            ['graeme.hawker@strath.ac.uk'],
            fail_silently=False,
        )
