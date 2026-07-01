from django.contrib import admin

from .models import Holding


class HoldingAdmin(admin.ModelAdmin):
    list_display = ("user", "symbol", "quantity", "purchase_price", "purchase_date")
    list_filter = ("user", "purchase_date")
    search_fields = ("symbol",)
    ordering = ("symbol",)


admin.site.register(Holding, HoldingAdmin)
