from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

subjects_choice = {'Data Science':'Data Science', 'Web Development':'Web Development', 'AI':'AI', 'Calculus':'Calculus', 'Business':'Business'}
reasons_choice = {'For fun':'For fun', 'For study':'For study', 'Career Advancement':'Career Advancement', 'Career Change':'Career Change'}
start_level_choice = {'Total Beginner':'Total Beginner', 'High Beginner':'High Beginner', 'Intermediate':'Intermediate', 'High Intermediate':'High Intermediate', 'Expert':'Expert'}

class Lessons(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    subjects = models.CharField(max_length=20, choices=subjects_choice)
    reasons = models.CharField(max_length=20, choices=reasons_choice)
    start_level = models.CharField(max_length=20, choices=start_level_choice)

    goals = models.CharField(max_length=50)
    strength = models.CharField(max_length=50)
    weakness = models.CharField(max_length=50)

    slug = models.SlugField(unique=True)
    roadmap = models.CharField(max_length=500, default="")

    def subject_name(self):
            return str(self.subjects)

class Groups(models.Model):
    subject = models.CharField(max_length=20, choices=subjects_choice)
    start_level = models.CharField(max_length=20, choices=start_level_choice)

    slug = models.SlugField(unique=True)

    def subject_name(self):
         return self.subject
    
    def level(self):
         return self.start_level

class Message(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message_content = models.CharField(max_length=50)
    
    def chat_content(self):
         return self.message_content
    
    def group(self):
         return self.group
    
    def user(self):
         return self.user.username
