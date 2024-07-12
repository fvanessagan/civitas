from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("home/", views.home),

    path("sign-up/", views.sign_up),
    path("account/", views.account),

    path("learning-steps/", views.steps),
    path("learning-steps/new/", views.newlesson, name="add-lesson"),
    path("group/", views.group),
]