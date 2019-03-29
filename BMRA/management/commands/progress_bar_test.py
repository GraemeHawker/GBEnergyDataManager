# -*- coding: utf-8 -*-
"""
command to download and process BMRA data for specific date
"""

from django_tqdm import BaseCommand
from time import sleep

def increment(t):
    t.update(1)

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Output directly
        #self.error('Error')
        #self.info('Info')

        # Output through tqdm
        t = self.tqdm(total=50)
        for x in range(50):
            sleep(0.5)
            increment(t)
'''
            if x == 10:
                t.info('X = 10')
            if x == 20:
                t.error('X = 20')
'''
