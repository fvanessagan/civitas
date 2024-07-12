# forms.py

from django import forms

class LearningRoadmapForm(forms.Form):
    subjects = forms.CharField(widget=forms.Textarea, label="Subjects you want to learn")
    goals = forms.CharField(widget=forms.Textarea, label="Your learning goals")
    reasons = forms.CharField(widget=forms.Textarea, label="Reasons for learning")
    start_level = forms.ChoiceField(choices=[
        ('total beginner', 'Total Beginner'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ], label="Your current level")
    strengths = forms.CharField(widget=forms.Textarea, label="Your strengths")
    weaknesses = forms.CharField(widget=forms.Textarea, label="Your weaknesses")
