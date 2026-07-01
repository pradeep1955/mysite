from django.contrib import admin

from .models import Contact, DailyMessage, Hotel, Video, Visitor

admin.site.register(Contact)
admin.site.register(Hotel)
admin.site.register(DailyMessage)
admin.site.register(Video)


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "user_agent", "visit_time")
    list_filter = ("visit_time",)
