from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .signup_form import SignUpForm
from .forms import addLesson, addMessage
from .models import Lessons, Groups, Message

# Create your views here.

def home(request):
    return render(request, 'home.html')

def steps(request):
    your_lesson = Lessons.objects.filter(user_name=request.user.id)
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

def group(request, slug):
    group = Groups.objects.get(slug=slug)
    message = Message.objects.filter(id = group.id)

    if request.method == "POST":
        form = addMessage(request.POST)
        if form.is_valid():
            message_data = form.save(commit=False)
            message_data.user = request.user
            message_data.group = group
            message_data.save()
            return redirect(".")
    else:
        form = addMessage(request.POST)

    return render(request, 'group.html', {'group': group, 'message':message, 'form':form})

def group_list(request):
    grouplist = Groups.objects.all() 

    return render(request, 'group_list.html', {'grouplist': grouplist})

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
    
