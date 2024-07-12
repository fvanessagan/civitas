from django.shortcuts import render, redirect
from .forms import UnifiedForm
from .models import Lessons
from openai import OpenAI

client = OpenAI(api_key="sk-proj-nantiajah")

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
        form = UnifiedForm(request.POST)
        if form.is_valid():
            messages = [get_initial_system_message()]
            topic = form.cleaned_data['topic']
            goal = form.cleaned_data['goal']
            reason = form.cleaned_data['reason']
            knowledge_level = form.cleaned_data['knowledge_level']
            
            messages.append({'role': 'user', 'content': f'Topic: {topic}'})
            messages.append({'role': 'user', 'content': f'Goal: {goal}'})
            messages.append({'role': 'user', 'content': f'Reason: {reason}'})
            messages.append({'role': 'user', 'content': f'Knowledge Level: {knowledge_level}'})

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
                
                content = chat_gpt(messages)
                return render(request, 'learn_app/roadmap.html', {'roadmap': content})
    else:
        form = UnifiedForm()
    
    return render(request, 'learn_app/learn.html', {'form': form})
