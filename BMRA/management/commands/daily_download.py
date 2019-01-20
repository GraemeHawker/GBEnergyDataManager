# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    self.stdout.write("downloading data for yesterday")
