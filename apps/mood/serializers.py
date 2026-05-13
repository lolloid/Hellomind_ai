from rest_framework import serializers

from .models import MoodEntry


class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ("id", "emotion", "intensity", "source", "note", "created_at")


class MoodSummarySerializer(serializers.Serializer):
    total_entries = serializers.IntegerField()
    emotion_counts = serializers.DictField()
    avg_intensity = serializers.FloatField()
    dominant_emotion = serializers.CharField()
    daily_moods = serializers.ListField()
