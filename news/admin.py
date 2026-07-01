from django.contrib import admin

from .models import DailyNews


@admin.register(DailyNews)
class DailyNewsAdmin(admin.ModelAdmin):
    list_display = ("date",)
