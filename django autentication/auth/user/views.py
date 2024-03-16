from django.shortcuts import render,redirect,HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from rest_framework.permissions import IsAuthenticated

# creating jwt tokens manually
from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
def login(request):
    context={
        'forms':LoginForm
    }
    return render(request,'user/index.html',context)

class UserRegistrationView(APIView):
    def post(self,request,format=None):
        
        serializer=UserRegistrationSerializer(data=request.data)
        print("inside seralizer"+"*"*10)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({ 'token':token , 'msg':'Registration successful'} ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# views for login
class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token ,   'msg':'login successful'},status=status.HTTP_200_OK)
            else:
                return Response({'error':'email or password is not correct'},status=status.HTTP_404_NOT_FOUND)
            

# to view user profile
class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
# to change password
class UserChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    def post(self , request, format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password changed sucessfully'},status=status.HTTP_200_OK)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# to reset password(email)
class SendPasswordResetEmail(APIView):
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset link send.Please check your Email.',},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

class UserPasswordResetView(APIView):
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data, context={'uid':uid ,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset successful'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    