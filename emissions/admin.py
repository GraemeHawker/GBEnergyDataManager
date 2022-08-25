from django.contrib import admin

from .models import StationTypeEmissions
from .models import BMUEmissions

# Register your models here.
admin.site.register(StationTypeEmissions)
admin.site.register(BMUEmissions)
