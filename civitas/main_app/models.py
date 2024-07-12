from django.db import models
from django.contrib.auth.models import User
# Create your models here.

subjects_choice = {'data science':'data science', 'web development':'web development', 'AI':'AI'}
reasons_choice = {'for fun':'for fun', 'for study':'for study', 'career advancement':'career advancement', 'career change':'career change'}
start_level_choice = {'total beginner':'total beginner', 'high beginner':'high beginner', 'intermediate':'intermediate', 'high intermediate':'high intermediate', 'expert':'expert'}

class Lessons(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    subjects = models.CharField(max_length=20, choices=subjects_choice)
    reasons = models.CharField(max_length=20, choices=reasons_choice)
    start_level = models.CharField(max_length=20, choices=start_level_choice)

    goals = models.CharField(max_length=50)
    strength = models.CharField(max_length=50)
    weakness = models.CharField(max_length=50)

    def subject_name(self):
            return str(self.subjects)

class Steps(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    subjects = models.ForeignKey(Lessons, on_delete=models.CASCADE)


