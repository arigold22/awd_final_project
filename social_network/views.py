from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .models import Profile, PostImages, Post, Friendship, Messages
from .forms import RegisterForm, PostForm, SearchForm, UpdateProfileForm
from django.views.generic import DetailView
from django.db.models import Q
# Create your views here.

def home(request): 
    user = request.user
    if user.is_authenticated:
        form = PostForm()
        profile_data = Profile.objects.get(user=user)
        fname = user.first_name
        friends = Friendship.objects.filter(Q(from_user=user) | Q(to_user=user), status=True)
        posts = Post.objects.filter(Q(user__in=friends.values_list('from_user', flat=True),) | Q(user__in=friends.values_list('to_user', flat=True))).order_by('-date')
        postImages = [PostImages.objects.filter(post=post) for post in posts]
        context = {'fname': fname,'profile_data': profile_data, 'username': user.username, 'form': form, 'posts': posts, 'postImages': postImages}
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
        context['posts'] = Post.objects.filter(user=kwargs['object'].user).order_by('-date')
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

def edit_profile(request):
    user = request.user
    form = UpdateProfileForm
    profile_data = Profile.objects.get(user=user)
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        if request.method == 'POST':
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            profile.profile_bio = request.POST['Bio']
            if('image_remove_checkbox' in request.POST and request.POST['image_remove_checkbox'] == 'on'):
                profile.profile_cover_photo = None
            else:
                if 'profile_cover_photo' in request.FILES:
                    profile.profile_cover_photo = request.FILES['profile_cover_photo']
            if ('profile_remove_checkbox' in request.POST and request.POST['profile_remove_checkbox'] == 'on'):
                profile.profile_image = 'default.png'
            else:
                if 'profile_photo' in request.FILES:    
                    profile.profile_photo = request.FILES['profile_photo']
            user.save()
            profile.save()
            return redirect('profile', username=user.username)
            
    return render(request, 'social_network/edit_profile.html', {'profile_data': profile_data, 'form': form})

def notifications(request):
    user = request.user
    friend_requests = Friendship.objects.filter(to_user=user)
    print(friend_requests[0].status)
    for friend_request in friend_requests:
        friend_request.from_user.profile = Profile.objects.get(user=friend_request.from_user)
    if user.is_authenticated:
        return render(request, 'social_network/notifications.html', {'friend_requests': friend_requests})
    return redirect('login')

def accept_friend(request, username):
    user = request.user
    friend = User.objects.get(username=username)
    print(username)
    if user.is_authenticated:
        friendship = Friendship.objects.get(from_user=friend, to_user=user)
        friendship.status = True
        friendship.save()
        return redirect('notifications')
    return redirect('notifications')

def messages(request):
    user = request.user
    if user.is_authenticated:
        messages = Messages.objects.filter(Q(from_user=user) | Q(to_user=user))
        messages = messages.order_by('date')
        users = messages.values_list('from_user', 'to_user').distinct()
        users = [User.objects.get(id=user[0]) if user[0] != user[1] else User.objects.get(id=user[1]) for user in users]

        for user in users:
            user.profile = Profile.objects.get(user=user)
            user.last_message = Messages.objects.filter(Q(from_user=user) | Q(to_user=user)).order_by('-date')[0]
            user.last_message.from_user.profile = Profile.objects.get(user=user.last_message.from_user)
            user.last_message.to_user.profile = Profile.objects.get(user=user.last_message.to_user)
        
        return render(request, 'social_network/messages.html', {'users': users})
        
    return redirect('login')