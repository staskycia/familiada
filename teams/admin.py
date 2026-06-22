from django.contrib import admin
from django.db import transaction

from .models import TeamsState
from scoreboard.state import broadcast_scoreboard_update

@admin.register(TeamsState)
class TeamStateAdmin(admin.ModelAdmin):
    list_display = ["__str__", "left_team_name", "right_team_name", "left_team_mistakes", "right_team_mistakes", "is_active"]
    list_editable = ["left_team_name", "right_team_name", "left_team_mistakes", "right_team_mistakes", "is_active"]
    
    # exclude = ["is_active"]    
    
    def save_model(self, request, obj, form, change):
        if obj.is_active:
            with transaction.atomic():
                TeamsState.objects.exclude(pk=obj.pk).update(is_active=False)
                
        super().save_model(request, obj, form, change)
        broadcast_scoreboard_update()
        
    def save_formset(self, request, form, formset, change):
        result = super().save_formset(request, form, formset, change)
        broadcast_scoreboard_update()
        return result