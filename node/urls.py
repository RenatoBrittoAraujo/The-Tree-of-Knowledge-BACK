from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .viewsets import (
    NodeViewSet,
    RefViewSet,
    EdgeViewSet
)

router = DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'refs', RefViewSet)
router.register(r'edges', EdgeViewSet)

appname = 'nodes'

urlpatterns = [
    path('', include(router.urls)),
]