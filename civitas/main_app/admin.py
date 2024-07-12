from django.contrib import admin
from .models import Lessons, Groups, Message

# Register your models here.
admin.site.register(Lessons)
admin.site.register(Groups)
admin.site.register(Message)