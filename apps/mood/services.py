from collections import Counter, defaultdict
from datetime import timedelta

from django.utils import timezone

from .models import MoodEntry


def get_mood_history(user, days: int = 30):
    since = timezone.now() - timedelta(days=days)
    return MoodEntry.objects.filter(user=user, created_at__gte=since).order_by("-created_at")[:500]


def get_mood_summary(user, days: int = 7) -> dict:
    since = timezone.now() - timedelta(days=days)
    entries = list(MoodEntry.objects.filter(user=user, created_at__gte=since))

    if not entries:
        return {
            "total_entries": 0,
            "emotion_counts": {},
            "avg_intensity": 0,
            "dominant_emotion": "neutral",
            "daily_moods": [],
        }

    emotion_counts = Counter(entry.emotion for entry in entries)
    avg_intensity = round(sum(entry.intensity for entry in entries) / len(entries), 1)
    dominant_emotion = emotion_counts.most_common(1)[0][0]

    daily = defaultdict(lambda: {"emotions": [], "intensities": []})
    for entry in entries:
        day = timezone.localtime(entry.created_at).strftime("%Y-%m-%d")
        daily[day]["emotions"].append(entry.emotion)
        daily[day]["intensities"].append(entry.intensity)

    daily_moods = []
    for day, values in sorted(daily.items()):
        daily_moods.append(
            {
                "date": day,
                "dominant_emotion": Counter(values["emotions"]).most_common(1)[0][0],
                "avg_intensity": round(sum(values["intensities"]) / len(values["intensities"]), 1),
                "count": len(values["emotions"]),
            }
        )

    return {
        "total_entries": len(entries),
        "emotion_counts": dict(emotion_counts),
        "avg_intensity": avg_intensity,
        "dominant_emotion": dominant_emotion,
        "daily_moods": daily_moods,
    }
