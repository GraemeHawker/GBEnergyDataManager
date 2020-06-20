from django.contrib import admin

from .models import PowerStation, StationType, TO_zone, OC2_zone, \
 ConnectionSite, PowerStationBMU

class OC2_zoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_zone')
    ordering = ('id',)

class PowerStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'station_type', 'to_zone', 'OC2_zone',
                    'connection_site', 'embedded')
    ordering = ('name',)

# Register your models here.
admin.site.register(PowerStation, PowerStationAdmin)
admin.site.register(PowerStationBMU)
admin.site.register(StationType)
admin.site.register(TO_zone)
admin.site.register(OC2_zone, OC2_zoneAdmin)
admin.site.register(ConnectionSite)
