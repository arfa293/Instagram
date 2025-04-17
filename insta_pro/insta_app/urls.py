# urls.py

from django.urls import path
from .views import register_user, create_post, Customlogin_view ,profile_view,my_post,update_bio,update_username
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('register/', register_user, name='register'),
    path('create-post/', create_post, name='create_post'),
    path('login/', Customlogin_view.as_view(), name='login'),  
    path('profile/', profile_view, name='profile'),
    path('posts/', my_post, name='posts'),
    path('update-bio/',update_bio,name='update-bio'),
    path('update-username/',update_username,name='update-username')
]
