from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from django.shortcuts import get_object_or_404

from .models import User, UserReport

from .serializers import (
    UserRegisterSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UsernameSerializer
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
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
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserProfileUpdateSerializer
    queryset = User.objects.all()

    lookup_field = 'username'

class GetUsername(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UsernameSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        username = self.request.user.username
        return Response(username)

class ReportUser(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UsernameSerializer
    queryset = User.objects.all()

    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        reporter = self.request.user
        reportee = self.get_object()
        if reportee.report(reporter):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)