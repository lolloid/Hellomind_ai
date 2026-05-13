from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class HelloMindUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("HelloMind", {"fields": ("language", "ai_name", "ai_persona")}),
    )
    list_display = ("username", "email", "language", "is_staff", "date_joined")
    search_fields = ("username", "email")
