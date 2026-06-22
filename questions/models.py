from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator

class Question(models.Model):
    class MultiplierChoices(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
    
    text = models.CharField(blank=False)
    is_active = models.BooleanField(default=False, blank=False)
    multiplier = models.IntegerField(choices=MultiplierChoices.choices, blank=False, default=MultiplierChoices.ONE)
    
    @property
    def points(self):
        return sum([option.points for option in self.options.all()])
    
    @property
    def available_points(self):
        return self.multiplier * sum([option.points if not option.hidden else 0 for option in self.options.all()])
    
    def __str__(self):
        return f"{self.text}"
    
class Option(models.Model):
    text = models.CharField(blank=False)
    points = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(100)])
    hidden = models.BooleanField(blank=False, default=True)
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    
    def __str__(self):
        return f"{self.text} [{self.points}]"