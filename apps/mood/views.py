from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MoodEntrySerializer
from .services import get_mood_history, get_mood_summary


def parse_days(request, default: int) -> int:
    try:
        return max(1, min(int(request.query_params.get("days", default)), 365))
    except (TypeError, ValueError):
        return default


class MoodHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = parse_days(request, 30)
        entries = get_mood_history(request.user, days)
        return Response(MoodEntrySerializer(entries, many=True).data)


class MoodSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = parse_days(request, 7)
        return Response(get_mood_summary(request.user, days))
