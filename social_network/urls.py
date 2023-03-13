from django.urls import include, path
from . import views
from . import api
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile/<username>', views.ProfileDetail.as_view(), name='profile'),
    path('post', views.post, name='post'),
    path('search', views.search, name='search'),
    path('addfriend/<username>', views.addfriend, name='addfriend'),
    path('accept_friend/<username>', views.accept_friend, name='addfriend'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('notifications', views.notifications, name='notifications'),
    path('chat', views.chat, name='chat'),
    path('send_message/<username>', views.send_message, name='send_message'),
    path('api/profile/<username>/', api.ProfileDetail.as_view(), name='profile_api'),
    path('api/user/<username>/', api.UserDetail.as_view(), name="user_api"),
    path('api/friends/<username>/', api.FriendsList.as_view(), name="friends_api"),
    path('api/posts/', api.PostList.as_view(), name="posts_api"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
