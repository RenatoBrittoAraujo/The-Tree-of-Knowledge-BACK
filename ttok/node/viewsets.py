from rest_framework import permissions, mixins, filters, generics, status
from rest_framework.response import Response
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
)

# GET queryNode(id) - done
# GET getNode(id) - done
# GET getRandomNode() - done
# GET reportNode(id) - done
# POST addNode(id, body) - done
# POST addEdge(from, to) - done
# POST addRef(id, title)
# PUT/PATCH editNode(id, data) 
# PUT/PATCH editRef(id, data) 
# GET upvoteNode(id), downvoteNode(id)
# GET upvoteRef(nodeName, refID), downvoteRef(nodeName, refID)
# NODE SEARCH - https://medium.com/quick-code/searchfilter-using-django-and-vue-js-215af82e12cd

class QueryNode(generics.RetrieveAPIView):
    queryset = Node.objects.all()
    serializer_class = QueryNodeSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.get_child_nodes()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class GetNode(generics.RetrieveAPIView):
    queryset = Node.objects.all()
    serializer_class = FullNodeSerializer
    permission_classes = [permissions.AllowAny]

class GetRandomNode(generics.ListAPIView):
    queryset = Node.objects.all()
    serializer_class = FullNodeSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        instance = random.choice(self.get_queryset())
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ReportNode(generics.RetrieveAPIView):
    queryset = Node.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        reported = instance.report(request.user)
        return Response(reported)

class EditNode(generics.UpdateAPIView):
    queryset = Node.objects.all()
    serializer_class = FullNodeSerializer
    permission_classes = [IsOwner]

class AddNode(generics.CreateAPIView):
    queryset = Node.objects.all()
    serializer_class = FullNodeSerializer
    permission_classes = [permissions.IsAuthenticated]

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

class AddRef(generics.CreateAPIView):
    queryset = Edge.objects.all()
    serializer_class = RefSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Ref.objects.create(author=request.user, **serializer.validated_data)
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
