from django.db import models

# This class represents 
class Node(models.Model):
    name = models.CharField(max_length=100, primary_key=True, blank=False, null=False, unique=True)
    body = models.CharField(max_length=1000, blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    # TODO: Add edge creation for node with parent edge
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Node, self).save(*args, **kwargs)

    def get_child_nodes(self):
        edges = self.outgoing_edges.all()
        nodes = map(lambda edge: edge.target, edges)
        return nodes

class Edge(models.Model):
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    votes = models.IntegerField(default=0)

class Ref(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    link = models.CharField(max_length=1000, blank=True, null=False)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='refs')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title