from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mood.services import get_mood_history, get_mood_summary
from apps.mood.serializers import MoodEntrySerializer


class DashboardOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get("days", 7))
        return Response(
            {
                "summary": get_mood_summary(request.user, days),
                "recent": MoodEntrySerializer(get_mood_history(request.user, days)[:20], many=True).data,
            }
        )
