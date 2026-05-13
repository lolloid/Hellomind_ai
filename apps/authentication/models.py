from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    LANGUAGE_CHOICES = (
        ("id", "Indonesian"),
        ("en", "English"),
    )

    email = models.EmailField(unique=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default="id")
    ai_name = models.CharField(max_length=50, default="HelloMind")
    ai_persona = models.TextField(
        default="Kamu adalah AI pendamping kesehatan mental yang empatik, ramah, dan suportif."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.username
