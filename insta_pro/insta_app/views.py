from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serilizer import Userserilizer,Postseriliazer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView 
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serilizer import postdisplaySerializer
from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import Post,CustomUser
from django.contrib.auth import get_user_model





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
    
