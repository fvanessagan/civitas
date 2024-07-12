from django.forms import ModelForm
from django.db import models
from django import forms
from .models import Lessons, Message

class addLesson(ModelForm):
   subjects = forms.TextInput()
   goals = forms.TextInput()
   reasons = forms.TextInput()
   start_level = forms.TextInput()
   strength = forms.TextInput()
   weakness = forms.TextInput()

   class Meta:
      model = Lessons
      fields = ['subjects', 'goals', 'reasons', 'start_level', 'strength', 'weakness']

class addMessage(ModelForm):
   message_content = forms.TextInput()

   class Meta: 
      model = Message
      fields = ['message_content']
