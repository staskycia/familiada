from django.urls import path
from .views import ScoreboardView

app_name = "scoreboard"

urlpatterns = [
    path("", ScoreboardView.as_view(), name="scoreboard")
]