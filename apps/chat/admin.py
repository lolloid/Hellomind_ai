from django.contrib import admin

from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "updated_at")
    search_fields = ("title", "user__username")
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "role", "text_emotion", "mood_score", "created_at")
    list_filter = ("role", "text_emotion")
    search_fields = ("text",)
