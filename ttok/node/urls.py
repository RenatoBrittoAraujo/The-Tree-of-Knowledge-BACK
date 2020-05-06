from django.urls import path, include
from rest_framework import routers

from .viewsets import (
    QueryNode,
    GetNode,
    GetRandomNode,
    EditRef,
    EditNode,
    AddNode,
    AddEdge,
    AddRef,
    VoteNode,
    VoteRef,
    DeleteNode,
    DeleteRef,
    ReportNode,
)

appname = 'nodes'

urlpatterns = [
    path(
        r'querynode/<int:pk>',
        QueryNode.as_view(),
        name='querynode'
    ),
    path(
        r'getnode/<int:pk>',
        GetNode.as_view(),
        name='getnode'
    ),
    path(
        r'randomnode/',
        GetRandomNode.as_view(),
        name='randomnode'
    ),
    path(
        r'report/<int:pk>',
        ReportNode.as_view(),
        name='reportnode'
    ),
    path(
        r'editnode/<int:pk>',
        EditNode.as_view(),
        name='editnode'
    ),
    path(
        r'addnode/',
        AddNode.as_view(),
        name='addnode'
    ),
    path(
        r'addedge/',
        AddEdge.as_view(),
        name='addedge'
    ),
    path(
        r'addref/',
        AddRef.as_view(),
        name='addref'
    ),
    path(
        r'votenode/<int:pk>',
        VoteNode.as_view(),
        name='votenode'
    ),
    path(
        r'voteref/<int:pk>',
        VoteRef.as_view(),
        name='voteref'
    ),
    path(
        r'editref/<int:pk>',
        EditRef.as_view(),
        name='editref'
    ),
    path(
        r'deletenode/<int:pk>',
        DeleteNode.as_view(),
        name='deletenode'
    ),
    path(
        r'deleteref/<int:pk>',
        DeleteRef.as_view(),
        name='deleteref'
    ),
]