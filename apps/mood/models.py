from django.conf import settings
from django.db import models


class MoodEntry(models.Model):
    SOURCE_TEXT = "text"
    SOURCE_FACE = "face"
    SOURCE_COMBINED = "combined"
    SOURCE_CHOICES = (
        (SOURCE_TEXT, "Text"),
        (SOURCE_FACE, "Face"),
        (SOURCE_COMBINED, "Combined"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mood_entries")
    emotion = models.CharField(max_length=20)
    intensity = models.PositiveSmallIntegerField(default=3)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_TEXT)
    note = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["emotion"]),
        ]

    def __str__(self) -> str:
        return f"{self.user_id}: {self.emotion} ({self.intensity})"
