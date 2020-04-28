from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

appname = 'nodes'

urlpatterns = [
    path('random', views.getRandomNode, name='randomNode'),
    path('get/<str:name>', views.getNode, name='getNode'),
    path('new', views.addNode, name='createNode')
    path('', include(router.urls)),
]