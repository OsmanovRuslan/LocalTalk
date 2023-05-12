from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from django.http import HttpRequest

from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from chat.models import Thread


@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    if request.user.is_authenticated:
        context = {
            'Threads': threads,
            'username': request.user.username
        }
    else: 
        context = {
            'Threads': threads
        }
    return render(request, 'chat/messages.html', context)


def home_view(request: HttpRequest):

    context = {}

    if request.user.is_authenticated:
        context = { 'username': request.user.username }

    return render(request, 'chat/index.html', context)

def auth_view(request: HttpRequest):

    if request.method == 'POST':

        if 'register' in request.POST:

            form = RegistrationForm(request.POST)

            if form.is_valid():

                username = form.cleaned_data.get('reg_login')
                email = form.cleaned_data.get('reg_email')
                password = form.cleaned_data.get('reg_password')

                user = User.objects.filter(username=username).exists()

                if user:
                    return render(request, 'chat/auth.html', { 'reg_error': 'Этот логин уже занят'})
                
                user = User.objects.filter(email=email).exists()

                if user:
                    return render(request, 'chat/auth.html', { 'reg_error': 'Эта почта уже занята'})
                
                user = User.objects.create_user(username, email, password)
                login(request, user)

                return redirect('chat')
        elif 'login' in request.POST:

            form = LoginForm(request.POST)

            if form.is_valid():

                username = form.cleaned_data.get('log_login')
                password = form.cleaned_data.get('log_password')

                user = authenticate(username=username, password=password)

                if user is None:
                    return render(request, 'chat/auth.html', { 'log_error': 'Неверный логин или пароль'})
                
                login(request, user)

                return redirect('chat')

    return render(request, 'chat/auth.html')

def profile_view(request: HttpRequest):

    if not request.user.is_authenticated:
        return redirect('home')
    
    context = {}

    context['username'] = request.user.username
    context['email'] = request.user.email

    if request.method == 'POST':
        if 'exit' in request.POST:
            logout(request)
            return redirect('home')

    return render(request, 'chat/profile.html', context)
