from django.contrib import admin

from .models import MoodEntry


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "emotion", "intensity", "source", "created_at")
    list_filter = ("emotion", "source")
    search_fields = ("note", "user__username")
