from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .models import Profile
from .forms import RegisterForm
# Create your views here.

def home(request): 
    user = request.user
    if user.is_authenticated:
        profile_data = Profile.objects.get(user=user)
        fname = user.first_name
        context = {'fname': fname,'profile_data': profile_data, 'username': user.username}
        return render(request, 'social_network/index.html', context)
    return render(request, 'social_network/index.html', {})

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'social_network/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            dj_login(request, user)
            fname = user.first_name
            return render(request, 'social_network/index.html', {'fname': fname})
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
        
    return render(request, 'social_network/login.html', {})

def logout(request):
    dj_logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')

def profile(request):
    user = request.user
    if user.is_authenticated:
        profile_data = Profile.objects.get(user=user)
        fname = user.first_name
        lname = user.last_name
        print(user)
        context = {'fname': fname,'lname': lname,'profile_data': profile_data, 'username': user.username}
        return render(request, 'social_network/profile.html', context)
    return render(request, 'social_network/login.html', {})