from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serilizer import Userserilizer,Postseriliazer,profiledisplaySerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView 
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serilizer import postdisplaySerializer,PostViewSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import Post,CustomUser
from django.contrib.auth import get_user_model
from .models import Follow
from rest_framework.generics import RetrieveAPIView
from .models import like, Comment
from .serilizer import LikeSerializer,CommentCreateSerializer,CommentRetrieveSerializer
from rest_framework import generics


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    
    if request.method == 'POST':
        email=request.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error":"email already exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = Userserilizer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer=Postseriliazer(data=request.data ,  context={'request': request})
    if serializer.is_valid():
        serializer.save()   
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Customlogin_view(APIView):
    permission_classes=[AllowAny]
    def post(self,request,*args, **kwargs):
        email=request.data.get('email')
        username=request.data.get('username')
        password=request.data.get('password')
        print(username,password)

        user=authenticate(request , email=email , password=password)
        print(user)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'username': user.username
            }, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    profile_photo_url = request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
    return Response({
        "username":user.username,
        "profile_picture": profile_photo_url,
        "bio":user.bio
    })
   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_post(request):
    posts=Post.objects.filter(author=request.user)
    serilizer=postdisplaySerializer(posts,many=True, context={'request':request})
    return Response(serilizer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_bio(request):
    user=request.user
    new_bio=request.data.get('bio')

    if new_bio is None:
        return Response({"error":"bio is required"},status=status.HTTP_400_BAD_REQUEST)
    
    user.bio=new_bio
    user.save()

    return Response({'message':'bio created successfully','bio':user.bio} ,status=status.HTTP_200_OK)

User = get_user_model()

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_username(request):
    user = request.user
    new_username = request.data.get('username')

    if not new_username:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)


    if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    user.username = new_username
    user.save()

    return Response({'username': user.username}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    new_profile = request.data.get('profile_pic')

    if not new_profile:
        return Response({'error': 'Profile picture is required'}, status=status.HTTP_400_BAD_REQUEST)

    user.profile_picture = new_profile
    user.save()

    return Response({'message': 'Profile picture updated successfully'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id, author=request.user)
        post.delete()
        return Response({'message': 'Post deleted successfully'})
    except Post.DoesNotExist:
        return Response({'error': 'Post not found or not owned by user'}, status=404)     
    
class Follow_View(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if target_user == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if created:
            return Response({'status': 'followed', 'message': f'You are now following {target_user.username}'})
        else:
            follow.delete()
            return Response({'status': 'unfollowed', 'message': f'You have unfollowed {target_user.username}'})


class AllProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.exclude(id=request.user.id) 
        serializer = profiledisplaySerializer(users, many=True, context={"request": request})
        return Response(serializer.data)    

class FollowerListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        followers = Follow.objects.filter(following=request.user)
        follower_names = [follow.follower.username for follow in followers]
    
        return Response(follower_names)

class FollowingListView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        followings = Follow.objects.filter(follower=request.user).select_related('following')
        following_names = [f.following.username for f in followings] 
        print(following_names)
        return Response({'following': following_names})
    
class UserProfileView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = profiledisplaySerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
class FollowedPostsView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self,request):
        followed_user_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        posts = Post.objects.filter(author__id__in=followed_user_ids).order_by('-created_at')
        serializer = PostViewSerializer(posts, many=True)
        return Response(serializer.data)
    
class LikeCreateView(generics.CreateAPIView):
    queryset = like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.exceptions import NotFound

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        post_id = self.request.data.get('post')
        
        # Ensure the post exists
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found.")

        # Save the comment with the Post object
        serializer.save(user=user, post=post)
        
class CommentListView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentRetrieveSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')  # Get the post ID from the URL
        return Comment.objects.filter(post_id=post_id)   
    