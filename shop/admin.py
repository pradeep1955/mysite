from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "description")


admin.site.register(Product, ProductAdmin)
