from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout

# Create your views here.

def home(request):
    return render(request, 'social_network/index.html', {})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myUser = User.objects.create_user(username, email, pass1)
        myUser.first_name = fname
        myUser.last_name = lname
        
        myUser.save()

        messages.success(request, 'You are now registered and can log in')

        return redirect('login')
    return render(request, 'social_network/signup.html', {})

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
    return render(request, 'social_network/profile.html', {})