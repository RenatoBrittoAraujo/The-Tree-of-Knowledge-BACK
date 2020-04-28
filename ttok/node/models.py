from django.db import models

class Ref(models.Model):
    description = models.CharField(max_length=100)
    link = models.CharField(max_length=1000, default='')

class Node(models.Model):
    name = models.CharField(max_length=100, primary_key=True, blank=False, null=False, unique=True)
    body = models.CharField(max_length=1000, blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Node, self).save(*args, **kwargs)