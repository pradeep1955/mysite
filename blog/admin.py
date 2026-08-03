#admin.site.register(Post)

from django.contrib import admin
from .models import Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date_posted", "is_hidden")
    list_filter = ("categories", "is_hidden")
    filter_horizontal = ("categories",)
