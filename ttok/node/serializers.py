from rest_framework import serializers

from .models import Node, Ref

class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ['name', 'body', 'votes']

class RefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ref
        fields = ['title', 'link', 'node']