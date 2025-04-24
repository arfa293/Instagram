# urls.py

from django.urls import path
from .views import register_user, create_post, Customlogin_view ,profile_view,my_post,update_bio,update_username,update_profile,delete_post,Follow_View,AllProfilesView
from .views import FollowerListView,FollowingListView,UserProfileView,FollowedPostsView,LikeCreateView,CommentCreateView,CommentListView
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
    path('update-username/',update_username,name='update-username'),
    path('update-profile-pic/',update_profile,name='update-pic'),
    path('delete-post/<int:post_id>/',delete_post, name='delete-post'),
    path('follow/<str:username>/', Follow_View.as_view(), name='follow-toggle'),
    path('other-users/', AllProfilesView.as_view(), name='all-profiles'),
    path('followers/', FollowerListView.as_view(), name='follower-list'),
    path('following/',FollowingListView.as_view(),name='following-list'),
    path('api/user/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('feed/', FollowedPostsView.as_view(), name='followed-posts'),
    path('like/', LikeCreateView.as_view(), name='like-create'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:post_id>/', CommentListView.as_view(), name='comment-list'),
]
