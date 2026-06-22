from django.shortcuts import render
from django.views.generic import TemplateView

class ScoreboardView(TemplateView):
    template_name = "scoreboard/scoreboard.html"