from django.urls import path, include
from rest_framework import routers
from .views import (
    UserRegister,
    UserProfile,
    UserUpdateProfile
)

appname = 'users'

urlpatterns = [
    path(
        'register',
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
]