from django.db import models

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
    
class TeamsState(models.Model):
    class MistakesCountChoices(models.IntegerChoices):
        ZERO = 0, "0"
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        
    left_team_name = models.CharField(blank=True, max_length=128)
    right_team_name = models.CharField(blank=True, max_length=128)
    
    left_team_mistakes = models.IntegerField(choices=MistakesCountChoices.choices, blank=False, default=MistakesCountChoices.ZERO)
    right_team_mistakes = models.IntegerField(choices=MistakesCountChoices.choices, blank=False, default=MistakesCountChoices.ZERO)
    
    is_active = models.BooleanField(default=False, blank=False)
    
    def __str__(self):
        return f"{self.left_team_name} [{self.left_team_mistakes}] vs {self.right_team_name} [{self.right_team_mistakes}]"