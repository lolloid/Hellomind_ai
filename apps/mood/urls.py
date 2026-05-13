from django.urls import path

from .views import MoodHistoryView, MoodSummaryView


urlpatterns = [
    path("history", MoodHistoryView.as_view(), name="mood-history"),
    path("history/", MoodHistoryView.as_view(), name="mood-history-slash"),
    path("summary", MoodSummaryView.as_view(), name="mood-summary"),
    path("summary/", MoodSummaryView.as_view(), name="mood-summary-slash"),
]
