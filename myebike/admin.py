from django.contrib import admin

from .models import GpsLog, Ride

admin.site.register(Ride)
admin.site.register(GpsLog)
