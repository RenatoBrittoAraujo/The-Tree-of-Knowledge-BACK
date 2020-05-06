from rest_framework import serializers
import collections

from .models import Node, Ref, Edge

class RefSerializer(serializers.ModelSerializer):
    
    author = serializers.CharField(source='author.username', read_only=True)
    votes = serializers.IntegerField(read_only=True)
    thumb = serializers.SerializerMethodField()

    class Meta:
        model = Ref
        fields = ['id', 'title', 'link', 'node', 'author', 'votes', 'thumb']
        read_only_fields = ['id', 'author', 'votes', 'thumb']
    
    def get_thumb(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return 0
        else:
            vote = current_user.refvotes.filter(ref=obj)
            if vote.exists():
                return vote.first().voteparam
            else:
                return 0

class RefEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ref
        fields = ['title', 'link']

class NodeEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['name', 'body']

class FullNodeSerializer(serializers.ModelSerializer):

    votes = serializers.IntegerField(source='get_votes', read_only=True)
    refs = RefSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)
    thumb = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = ['id', 'name', 'body', 'votes', 'refs', 'author', 'thumb']
        read_only_fields = ['id', 'votes', 'refs', 'author', 'thumb']

    def get_thumb(self, obj):
        if type(obj) == collections.OrderedDict:
            return 0
        nodeid = obj.id
        if self.context['request'].GET.get('parent', '') == '':
            return 0
        parentid = int(self.context['request'].GET.get('parent', ''))
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return 0
        edge = Edge.objects.filter(source=parentid, target=nodeid)
        if not edge.exists():
            return 0
        edge = edge.first()
        targetVote = current_user.edgevotes.filter(edge=edge, user=current_user)
        if targetVote.exists():
            return targetVote.first().voteparam
        else:
            return 0

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
