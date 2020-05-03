from rest_framework import serializers

from .models import Node, Ref, Edge

class RefSerializer(serializers.ModelSerializer):
    
    author = serializers.CharField(source='author.username', read_only=True)
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ref
        fields = ['id', 'title', 'link', 'node', 'author', 'votes']
        read_only_fields = ['id', 'author', 'votes']

class FullNodeSerializer(serializers.ModelSerializer):

    votes = serializers.IntegerField(source='get_votes', read_only=True)
    refs = RefSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Node
        fields = ['id', 'name', 'body', 'votes', 'refs', 'author']
        read_only_fields = ['id', 'votes', 'refs', 'author']

class QueryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name']

class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ['source', 'target']
        write_only = True

class NodeEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['body']

class RefEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['title', 'link']