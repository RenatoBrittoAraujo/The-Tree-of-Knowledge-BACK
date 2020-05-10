from django.db import models
from users.models import User

# Delete params:

DELETE_EDGE_VOTES = -5

DELETE_REF_VOTES = -5

DELETE_NODE_VOTES = -1
DELETE_NODE_REPORTS = 5

class Node(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    body = models.CharField(max_length=1000, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nodes')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Node, self).save(*args, **kwargs)

    def get_child_nodes(self):
        edges = self.outgoing_edges.all()
        nodes = map(lambda edge: edge.target, edges)
        return list(nodes)

    def get_votes(self):
        edges = self.incoming_edges.all()
        sum = 0
        for edge in edges:
            sum = sum + edge.votes()
        return sum
    
    def get_reports(self):
        return self.reports.count()

    def report(self, user):
        reported = False
        if not user.nodereports.filter(node=self).exists():
            NodeReport(node=self, user=user).save()
            reported = True
        if self.get_reports() >= DELETE_NODE_REPORTS and \
            self.get_votes() <= DELETE_NODE_VOTES:
            self.delete()
        return reported

    def connect_with_parent(self, parent):
        if not self.incoming_edges.filter(source=parent).exists():
            Edge(source=parent, target=self).save()
    
    def connect_with_child(self, child):
        if not self.outgoing_edges.filter(target=child).exists():
            Edge(source=self, target=child).save()

    def vote(self, parent, user, voteparam):
        voted = False
        if parent and self.incoming_edges.filter(source=parent).exists():
            edge = self.incoming_edges.filter(source=parent).first()
            voted = edge.vote(user, voteparam)
        return voted

class Edge(models.Model):
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.source.name + ' -> ' + self.target.name
    
    def vote(self, user, voteparam):
        old_votes = self.votes()
        if user.edgevotes.filter(edge=self).exists():
            vote = user.edgevotes.filter(edge=self).first()
            vote.voteparam = voteparam
            vote.save()
        else:
            EdgeVote(edge=self, user=user, voteparam=voteparam).save()
        self.target.author.add_contribution_points(self.votes() - old_votes)
        return self.votes() != old_votes
    
    def votes(self):
        votes = self.edgevotes.all()
        sum = 0
        for vote in votes:
            sum = sum + vote.voteparam
        return sum

class Ref(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    link = models.CharField(max_length=1000, blank=True, null=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='refs')
    votes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refs')

    def __str__(self):
        return self.title
    
    def vote(self, user, voteparam):
        old_votes = self.votes()
        if user.refvotes.filter(ref=self).exists():
            vote = user.refvotes.filter(ref=self).first()
            vote.voteparam = voteparam
            vote.save()
        else:
            RefVote(ref=self, user=user, voteparam=voteparam).save()
        self.author.add_contribution_points(self.votes() - old_votes)
        return self.votes() != old_votes
    
    def votes(self):
        votes = self.refvotes.all()
        sum = 0
        for vote in votes:
            sum = sum + vote.voteparam
        return sum

class RefVote(models.Model):
    voteparam = models.IntegerField(blank=False, null=False)
    ref = models.ForeignKey(Ref, on_delete=models.CASCADE, related_name='refvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refvotes')

class EdgeVote(models.Model):
    voteparam = models.IntegerField(blank=False, null=False)
    edge = models.ForeignKey(Edge, on_delete=models.CASCADE, related_name='edgevotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edgevotes')

class NodeReport(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nodereports')
