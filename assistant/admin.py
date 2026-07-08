from django.contrib import admin

from .models import ChatQuery, Intent


@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ("name", "priority", "is_active", "query_count")
    list_filter = ("is_active",)
    filter_horizontal = ("products",)
    search_fields = ("name", "keywords")

    def query_count(self, obj):
        return obj.queries.count()
    query_count.short_description = "Times matched"


@admin.register(ChatQuery)
class ChatQueryAdmin(admin.ModelAdmin):
    """
    Mostly a read-only log. Sort by 'matched = No' to see the questions
    nothing answered — that list is your next blog post / FAQ backlog.
    """
    list_display = ("question", "matched_intent", "matched", "created_at")
    list_filter = ("matched", "created_at")
    search_fields = ("question",)
    readonly_fields = ("question", "matched_intent", "matched", "created_at")

    def has_add_permission(self, request):
        return False
