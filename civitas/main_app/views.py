from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .signup_form import SignUpForm
from .forms import addLesson
from .models import Lessons

# Create your views here.

def home(request):
    return render(request, 'home.html')

def steps(request):
    your_lesson = Lessons.objects.filter(user_name=request.user)
    lesson_list = []

    for val in your_lesson:
        lesson_list.append(val.subject_name())

    return render(request, 'steps.html', {'lesson_list' : lesson_list})

def newlesson(request):

    if request.method == "POST":
        form = addLesson(request.POST)
        if form.is_valid():
            lesson_data = form.save(commit=False)
            lesson_data.user_name = request.user
            lesson_data.save()
            return redirect("/home")
    else:
        form = addLesson(request.POST)
    return render(request, "add_lesson_form.html", {'form':form})

def group(request):
    return render(request, 'group.html')

def account(request):
    return render(request, 'account.html')

def login(request):
    username = request.POST(username)
    password = request.POST(password)

    user = authenticate(request, username, password)
    if user != None:
        login(request, user)

def sign_up(response):
    if response.method == "POST":
        form = SignUpForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else: 
        form = SignUpForm()

    return render(response, "sign_up.html", {"form": form})
    
