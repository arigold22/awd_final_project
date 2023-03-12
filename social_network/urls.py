from django.urls import include, path
from . import views
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
    path('messages', views.messages, name='messages'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
