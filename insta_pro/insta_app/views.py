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
@api_view(['POST'])
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