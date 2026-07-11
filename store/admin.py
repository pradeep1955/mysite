from django.contrib import admin

from .models import Category, KitComponent, PreorderInterest, Product, ProjectKit


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_display", "reason", "affiliate_url", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "specification")
    prepopulated_fields = {"slug": ("name",)}


class KitComponentInline(admin.TabularInline):
    model = KitComponent
    extra = 1
    autocomplete_fields = ["product"]


@admin.register(ProjectKit)
class ProjectKitAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "total_price_display")
    list_filter = ("status",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [KitComponentInline]


@admin.register(PreorderInterest)
class PreorderInterestAdmin(admin.ModelAdmin):
    list_display = ("name", "kit", "quantity", "contacted", "created_at")
    list_filter = ("contacted", "kit")
    search_fields = ("name", "email", "phone")
