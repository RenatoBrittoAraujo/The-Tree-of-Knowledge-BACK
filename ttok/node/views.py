from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

import random

from .serializers import *
from .models import Ref, Node

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def get_random_node(self, request, *args, **kwargs):
        instance = random.choice(self.queryset)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_all_refs(self, request, *args, **kwargs):
        instance = self.get_object()
        refs = instance.refs.all().order_by('votes')
        response = []
        for ref in refs:
            response.append(ref)
        return Response(RefSerializer(response, many=True, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def query_node(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(instance.get_child_nodes())
    
    # TODO: complete authentication before this
    # @action(detail=True, methods=['post'])
    # def post_upvote_node(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.votes = instance.votes


class RefViewSet(viewsets.ModelViewSet):
    queryset = Ref.objects.all()
    serializer_class = RefSerializer
    permission_classes = [permissions.AllowAny]


# def upvoteNode(request, name):
#     pass
# def downvoteNode(request, name):
#     pass
# def upvoteRef(request, name, ref):
#     pass
# def downvoteRef(request, name, ref):
#     pass
# def addRef(request, name):
#     pass
# def getRefs(request, name):
#     pass

# def index(request):
#     raiseIfNot('GET')
#     return JsonResponse({ 'batata': "Hello, world. You're at the polls index." })


