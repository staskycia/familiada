from django.contrib import admin

from .models import Option, Question
from django.db import transaction
from django.contrib import messages
from scoreboard.state import broadcast_scoreboard_update

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "is_active"]
    list_editable = ["is_active"]
    
    # exclude = ["is_active"]
    
    inlines = [OptionInline]
    actions = ["hide_all_options", "reset_multiplier"]
    
    @admin.action(description="Hide all options")
    def hide_all_options(self, request, queryset):
        counter = 0
        for question in queryset:
            for option in question.options.all():
                if not option.hidden:
                    option.hidden = True
                    option.save()
                    counter += 1
        if counter > 0:
            broadcast_scoreboard_update()
            messages.success(request, f"{counter} options hidden")
            
    @admin.action(description="Reset multiplier")
    def reset_multiplier(self, request, queryset):
        queryset.update(multiplier=Question.MultiplierChoices.ONE)
        messages.success(request, "Multiplier reseted")
    
    def save_model(self, request, obj, form, change):
        if obj.is_active:
            with transaction.atomic():
                Question.objects.exclude(pk=obj.pk).update(is_active=False)
                
        super().save_model(request, obj, form, change)
        broadcast_scoreboard_update()
        
    def save_formset(self, request, form, formset, change):
        result = super().save_formset(request, form, formset, change)
        broadcast_scoreboard_update()
        return result