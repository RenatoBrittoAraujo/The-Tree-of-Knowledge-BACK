from rest_framework import serializers

from .models import Node, Ref, Edge

class RefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ref
        fields = ['id', 'title', 'link', 'node']
        read_only_fields = ['id']

class FullNodeSerializer(serializers.HyperlinkedModelSerializer):

    votes = serializers.IntegerField(source='get_votes', read_only=True)
    refs = RefSerializer(many=True, read_only=True)

    class Meta:
        model = Node
        fields = ['id', 'name', 'body', 'votes', 'refs']
        read_only_fields = ['id', 'votes', 'refs']

class QueryNodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name']

class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ['source', 'target']
        write_only = True