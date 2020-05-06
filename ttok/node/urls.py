from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .viewsets import (
    AddEdge,
    NodeViewSet,
    RefViewSet
)

router = DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'refs', RefViewSet)

appname = 'nodes'

urlpatterns = [
    path('', include(router.urls)),
    path(
        r'addedge/',
        AddEdge.as_view(),
        name='addedge'
    ),
]