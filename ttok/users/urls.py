from django.urls import path, include
from rest_framework import routers
from .viewsets import (
    UserRegister,
    UserProfile,
    UserUpdateProfile,
    GetUsername
)

appname = 'users'

urlpatterns = [
    path(
        r'register/',
        UserRegister.as_view(),
        name='register'
    ),
    path(
        r'profile/<str:username>',
        UserProfile.as_view(),
        name='profile'
    ),
    path(
        r'profileupdate/<str:username>',
        UserUpdateProfile.as_view(),
        name='profileupdate'
    ),
    path(
        r'getusername/',
        GetUsername.as_view(),
        name='getusername'
    ),
]