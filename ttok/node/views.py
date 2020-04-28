from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404

import json, random

from .models import Ref, Node

def raiseIfNot(request, method):
    if request.method != method:
        raise Http404('well you are dumb')

def nodeObj(node):
    obj = {}
    obj['name'] = node.name
    obj['body'] = node.body
    obj['votes'] = node.votes
    return obj

def getRandomNode(request):
    raiseIfNot(request, 'GET')
    nodes = Node.objects.all()
    random_node = random.choice(nodes)
    return JsonResponse({ 'name' : random_node.name })

def getNode(request, name):
    raiseIfNot(request, 'GET')
    node = get_object_or_404(Node, pk=name)
    return JsonResponse(nodeObj(node))

def addNode(request):
    raiseIfNot(request, 'POST')
    data = json.loads(request.body)
    new_node = Node(name=data['name'], body=data['body'])
    if new_node.save():
        return JsonResponse({'saved':'hehe'})
    else:
        return JsonResponse({'notsaved':'hehe'})

def upvoteNode(request, name):
    pass
def downvoteNode(request, name):
    pass
def upvoteRef(request, name, ref):
    pass
def downvoteRef(request, name, ref):
    pass
def addRef(request, name):
    pass
def getRefs(request, name):
    pass

def index(request):
    raiseIfNot('GET')
    return JsonResponse({ 'batata': "Hello, world. You're at the polls index." })


