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

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        print('lookup_url_kwarg:', lookup_url_kwarg)
        print('lookup_field:', self.lookup_field)
        print('self.kwargs', self.kwargs)

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        print(filter_kwargs)
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

class UserUpdateProfile(generics.UpdateAPIView):
    permission_classes = (IsOwner, )
    serializer_class = UserProfileUpdateSerializer
    queryset = User.objects.all()

    lookup_field = 'username'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj