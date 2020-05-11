from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import (
    permissions, mixins, 
    filters, generics, status,
    viewsets, filters,
)
from django.db.models import Q
import random

from .models import Ref, Node, Edge

from .permissions import (
    IsOwner
)

from .serializers import (
    QueryNodeSerializer,
    FullNodeSerializer,
    EdgeSerializer,
    RefSerializer,
    NodeEditSerializer,
    RefEditSerializer
)

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = FullNodeSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'body')

    def get_permissions(self):
        action = self.action
        if action in ['create', 'vote', 'report', 'update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        elif action in ['destroy']:
            permission_classes = [IsOwner]
        elif action in ['retrieve', 'query', 'list', 'search']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self): 
        serializer_class = self.serializer_class 
        if self.request.method in ['PUT', 'PATCH']: 
            serializer_class = NodeEditSerializer 
        return serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nodeData = serializer.data
        nodeName = nodeData['name']
        nodeBody = ''
        if 'body' in nodeData.keys():
            nodeBody = nodeData['body']
        node = Node(name=nodeName, body=nodeBody, author=request.user)
        node.save()
        node.author.add_contribution(
            'Created node ' + node.name
        )
        node.author.add_contribution_points(+1)
        serializer = self.get_serializer(node)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        instance = random.choice(self.get_queryset())
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search/(?P<search_term>[^/.]+)')
    def search(self, request, search_term=None):
        if len(search_term) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fullset = self.get_queryset()
        queryset = fullset.filter(name__startswith=search_term)
        if queryset.count() < 10:
            other_queryset = fullset.filter(name__contains=search_term)
            queryset = queryset.union(other_queryset)
        if queryset.count() < 10:
            other_queryset = fullset.filter(name__icontains=search_term)
            queryset = queryset.union(other_queryset)
        return Response(QueryNodeSerializer(queryset[:10], many=True).data)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        instance = self.get_object()
        reported = instance.report(request.user)
        return Response(reported)
        
    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        node = Node.objects.filter(pk=pk).first()
        parent = request.data['parent']
        voteparam = request.data['voteparam']
        parent = Node.objects.filter(pk=parent).first()
        return Response(node.vote(parent, request.user, voteparam))

    @action(detail=True, methods=['get'])
    def query(self, request, pk=None):
        instance = self.get_object()
        queryset = instance.get_child_nodes()
        serializer = QueryNodeSerializer(queryset, many=True)
        return Response(serializer.data)

class RefViewSet(viewsets.ModelViewSet):
    queryset = Ref.objects.all()
    serializer_class = RefSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'vote':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update' or\
             self.action == 'destroy':
            permission_classes = [IsOwner]
        elif self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self): 
        serializer_class = self.serializer_class 
        if self.request.method == 'PUT': 
            serializer_class = RefEditSerializer 
        return serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Ref.objects.create(author=request.user, **serializer.validated_data)
        instance.author.add_contribution(
            'Create reference ' + instance.title[:20]
        )
        instance.author.add_contribution_points(+1)
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        ref = Ref.objects.filter(pk=pk).first()
        voteparam = request.data['voteparam']
        return Response(ref.vote(request.user, voteparam))
        

class EdgeViewSet(  viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        target = data['target']
        source = data['source']
        err400 = status.HTTP_400_BAD_REQUEST
        if target == source:
            return Response('Cannot connect a node to itself', status=err400)
        if Edge.objects.filter(target=target, source=source).exists():
            return Response('Edge already exists', status=err400)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'])
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        target = data['target']
        source = data['source']
        err400 = status.HTTP_400_BAD_REQUEST
        if not Edge.objects.filter(target=target, source=source).exists():
            return Response('Edge does not exist', status=err400)
        Edge.objects.filter(target=target, source=source).first().delete()
        return Response(status=status.HTTP_200_OK)
