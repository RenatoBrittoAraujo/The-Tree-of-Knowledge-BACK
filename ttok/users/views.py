from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from django.shortcuts import get_object_or_404

from .models import User

from .serializers import (
    UserRegisterSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)

from .permissions import IsOwner

class UserRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

class UserProfile(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    lookup_field = 'username'

class UserUpdateProfile(generics.UpdateAPIView):
    permission_classes = (IsOwner, )
    serializer_class = UserProfileUpdateSerializer
    queryset = User.objects.all()

    lookup_field = 'username'
