from django.contrib import admin

# Register your models here.
from .models import GSP

class GSPAdmin(admin.ModelAdmin):
    list_display = ('gsp_group_id', 'id', 'name')
    ordering = ('gsp_group_id', 'id',)

admin.site.register(GSP, GSPAdmin)
