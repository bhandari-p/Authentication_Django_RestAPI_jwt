
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from .views import *



urlpatterns = [
    path('',login),
    path('register/',UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('profile/',UserProfileView.as_view()),
    path('changepassword/',UserChangePassword.as_view()),
    path('send-reset-password-email/',SendPasswordResetEmail.as_view()),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view())

]
