from django.conf import settings
from django.db import models


class Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chats")
    title = models.CharField(max_length=200, default="Obrolan Baru")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "-updated_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.user_id}: {self.title}"


class Message(models.Model):
    ROLE_USER = "user"
    ROLE_BOT = "bot"
    ROLE_CHOICES = (
        (ROLE_USER, "User"),
        (ROLE_BOT, "Bot"),
    )

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    text = models.TextField()
    face_emotion = models.CharField(max_length=20, blank=True, default="")
    text_emotion = models.CharField(max_length=20, blank=True, default="")
    mood_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["chat", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.role}: {self.text[:40]}"
