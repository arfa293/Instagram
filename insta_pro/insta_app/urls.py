# urls.py

from django.urls import path
from .views import register_user, create_post, Customlogin_view

urlpatterns = [
    path('register/', register_user, name='register'),
    path('create-post/', create_post, name='create_post'),
    path('login/', Customlogin_view.as_view(), name='login'),  
]
