from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .models import Profile, PostImages, Post, Friendship
from .forms import RegisterForm, PostForm, SearchForm
from django.views.generic import DetailView
from django.db.models import Q
# Create your views here.

def home(request): 
    user = request.user
    if user.is_authenticated:
        form = PostForm()
        profile_data = Profile.objects.get(user=user)
        fname = user.first_name
        context = {'fname': fname,'profile_data': profile_data, 'username': user.username, 'form': form}
        return render(request, 'social_network/index.html', context)
    return render(request, 'social_network/index.html', {})

def post(request):
    user = request.user
    if user.is_authenticated:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if request.method == 'POST':
                post = Post()
                post.user = user
                post.profile = Profile.objects.get(user=user)
                post.text = request.POST['text']
                if 'anonymous' in request.POST:
                    post.anonymous = True
                post.save()
                for image in request.FILES.getlist('images'):
                    ("reached image loop")
                    post_image = PostImages()
                    post_image.post = post
                    post_image.image = image
                    post_image.save()
                return redirect('home')
        else:
            profile_data = Profile.objects.get(user=user)
            fname = user.first_name
            context = {'fname': fname,'profile_data': profile_data, 'username': user.username, 'form': form}
            return render(request, 'social_network/index.html', context)
    redirect('home')
    
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
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
        
    return render(request, 'social_network/login.html', {})

def logout(request):
    dj_logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')

# def profile(request):
#     user = request.user
#     if user.is_authenticated:
#         profile_data = Profile.objects.get(user=user)
#         posts = Post.objects.filter(username=user)
#         postImages = [PostImages.objects.filter(post=post) for post in posts]
#         fname = user.first_name
#         lname = user.last_name
                
#         context = {'fname': fname,'lname': lname,'profile_data': profile_data, 'username': user.username, 'posts': posts, 'postImages': postImages}
#         return render(request, 'social_network/profile.html', context)
#     return render(request, 'social_network/login.html', {})

# def other_profile(request, username):
#     user = request.user
#     if user.is_authenticated:
#         other_user = User.objects.get(username=username)
#         profile_data = Profile.objects.get(user=other_user)
#         posts = Post.objects.filter(username=other_user)
#         postImages = [PostImages.objects.filter(post=post) for post in posts]
#         fname = other_user.first_name
#         lname = other_user.last_name

#         context = {'fname': fname,'lname': lname,'profile_data': profile_data, 'username': other_user.username, 'posts': posts, 'postImages': postImages}
#         return render(request, 'social_network/profile.html', context)
#     return render(request, 'social_network/login.html', {})

# def friends(request):
#     user = request.user
#     if user.is_authenticated:
#         friends = Friendship.objects.filter(from_user=user,)
#     return render(request, 'social_network/login.html', {})

def search(request):
    user = request.user
    form = SearchForm(request.POST)
    if user.is_authenticated:
        if form.is_valid():
            userSearch = User.objects.filter(username__icontains=form.cleaned_data['search'])
            profileSearch = Profile.objects.filter(user__in=userSearch)
            posts = Post.objects.filter(text__icontains=form.cleaned_data['search'])
            postImages = [PostImages.objects.filter(post=post) for post in posts]
            friends = Friendship.objects.filter(Q(from_user=user) | Q(to_user=user))
            for profile in profileSearch:
                for friend in friends:
                    if profile.user == friend.from_user or profile.user == friend.to_user:
                        if friend.status == True:
                            profile.friend = True
                        else:
                            profile.requested = True
                    
            return render(request, 'social_network/search.html', {'form': form, 'profileSearch': profileSearch, 'posts': posts, 'postImages': postImages, 'friends':friends, 'user': user})
        else:
            return render(request, 'social_network/search.html', {'form': form})
    return render(request, 'social_network/login.html', {})

class ProfileDetail(DetailView):
    model = Profile
    template_name = 'social_network/profile.html'
    context_object_name = 'profile_data'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = Friendship.objects.filter(Q(from_user=kwargs['object'].user) | Q(to_user=kwargs['object'].user))
        context['posts'] = Post.objects.filter(user=kwargs['object'].user)
        context['postImages'] = [PostImages.objects.filter(post=post) for post in context['posts']]
        return context

def addfriend(request, username):
    user = request.user
    if user.is_authenticated:
        friend = User.objects.get(username=username)
        if friend != user:
            friendship = Friendship()
            friendship.from_user = user
            friendship.to_user = friend
            friendship.save()
            messages.success(request, 'Friend request sent')
    else:
        messages.error(request, 'You must be logged in to add a friend')
    return redirect('profile', username=username)
 