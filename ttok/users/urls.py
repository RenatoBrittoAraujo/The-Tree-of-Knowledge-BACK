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
        r'profile/<str:pk>',
        UserProfile.as_view(),
        name='profile'
    ),
    path(
        r'profileupdate/<str:pk>',
        UserUpdateProfile.as_view(),
        name='profileupdate'
    ),
]