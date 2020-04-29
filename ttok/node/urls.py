from django.urls import path, include
from rest_framework import routers
from .views import NodeViewSet, RefViewSet

router = routers.DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'refs', RefViewSet)

appname = 'nodes'

urlpatterns = [
    path('', include(router.urls))
]