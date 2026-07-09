from django.contrib import admin

from .models import SensorReading, Subscriber

admin.site.register(SensorReading)
admin.site.register(Subscriber)
