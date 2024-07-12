from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .signup_form import SignUpForm
from .forms import addLesson
from .models import Lessons
from openai import OpenAI

# Create your views here.

client = OpenAI(api_key="ntarduluyhkeynya")

def chat_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def get_initial_system_message():
    return {
        'role': 'system',
        'content': (
            'You are an AI that will help people learn. You will generate a roadmap based on the topic the user wants to learn. '
            'First, you will ask what topic the user wants to learn. After that, you will ask what goal the user wants to achieve and their reason for learning it. '
            'Then, you will ask about the user\'s knowledge level (total beginner to advanced), and if they are not a beginner, provide examples of things they might have mastered at their level. '
            'Finally, you will ask what they have already mastered.'
        )
    }

def learn_view(request):
    if request.method == 'POST':
        form = LearnForm(request.POST)
        if form.is_valid():
            messages = [get_initial_system_message()]
            topic = form.cleaned_data['topic']
            goal = form.cleaned_data['goal']
            reason = form.cleaned_data['reason']
            knowledge_level = form.cleaned_data['knowledge_level']
            
            # Adding user responses to messages
            messages.append({'role': 'user', 'content': f'Topic: {topic}'})
            messages.append({'role': 'user', 'content': f'Goal: {goal}'})
            messages.append({'role': 'user', 'content': f'Reason: {reason}'})
            messages.append({'role': 'user', 'content': f'Knowledge Level: {knowledge_level}'})

            # If the user is not a total beginner, ask for examples of what they might have mastered
            if knowledge_level != 'total beginner' and 'mastered_parts' not in request.POST:
                examples_request = f'Based on the knowledge level {knowledge_level}, can you provide examples of what they might have mastered?'
                messages.append({'role': 'user', 'content': examples_request})
                examples_response = chat_gpt(messages)
                messages.append({'role': 'assistant', 'content': examples_response})
                # Render examples to ask for actual mastered parts
                return render(request, 'learn_app/confirm_mastered.html', {
                    'form': form,
                    'examples': examples_response
                })
            else:
                if 'mastered_parts' in request.POST:
                    mastered_parts = request.POST['mastered_parts']
                    messages.append({'role': 'user', 'content': f'Mastered Parts: {mastered_parts}'})
                
                # Generate the roadmap
                content = chat_gpt(messages)
                return render(request, 'learn_app/roadmap.html', {'roadmap': content})
    else:
        form = LearnForm()
    
    return render(request, 'learn_app/learn.html', {'form': form})

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
    
