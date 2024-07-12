from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .signup_form import SignUpForm
from .forms import addLesson
from .models import Lessons
import openai
from django.conf import settings
from .forms import LearningRoadmapForm

openai.api_key = settings.OPENAI_API_KEY

def generate_roadmap(request):
    if request.method == 'POST':
        form = LearningRoadmapForm(request.POST)
        if form.is_valid():
            subjects = form.cleaned_data['subjects']
            goals = form.cleaned_data['goals']
            reasons = form.cleaned_data['reasons']
            start_level = form.cleaned_data['start_level']
            strengths = form.cleaned_data['strengths']
            weaknesses = form.cleaned_data['weaknesses']

            prompt = (
                "You are an AI that will help people learn. You will generate a roadmap based on the topic the user wants to learn. "
                "First, you will ask what subjects the user wants to learn. After that, you will ask what goal the user wants to achieve and their reason for learning it. "
                "Then, you will ask about the user's start level (total beginner, beginner, intermediate, advanced, expert), and if they are not a total beginner, provide examples of things they might have mastered at their level. "
                "Finally, you will ask what are their strengths and weaknesses. "
                f"Subjects: {subjects}\nGoals: {goals}\nReasons: {reasons}\nStart Level: {start_level}\nStrengths: {strengths}\nWeaknesses: {weaknesses}"
            )

            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1000
            )

            roadmap = response.choices[0].text.strip()
            return render(request, 'roadmap.html', {'roadmap': roadmap})

    else:
        form = LearningRoadmapForm()

    return render(request, 'learning_form.html', {'form': form})




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
    
