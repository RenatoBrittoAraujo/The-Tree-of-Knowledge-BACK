from rest_framework.response import Response
from rest_framework import (
    permissions, mixins, 
    filters, generics, status,
    viewsets,
)
from rest_framework.decorators import action
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

# NODE SEARCH - https://medium.com/quick-code/searchfilter-using-django-and-vue-js-215af82e12cd

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = FullNodeSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'vote' or\
           self.action == 'report':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update' or\
             self.action == 'destroy':
            permission_classes = [IsOwner]
        elif self.action == 'retrieve' or self.action == 'query' or\
             self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self): 
        serializer_class = self.serializer_class 
        if self.request.method == 'PUT' or self.request.method == 'PATCH': 
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
        serializer = self.get_serializer(node)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        instance = random.choice(self.get_queryset())
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        ref = Ref.objects.filter(pk=pk).first()
        voteparam = request.data['voteparam']
        return Response(ref.vote(request.user, voteparam))
        

class AddEdge(generics.CreateAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        target = data['target']
        source = data['source']
        if Edge.objects.filter(target=target, source=source).exists():
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
