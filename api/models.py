from django.db import models


# Create your models here.
class Nodes(models.Model):
    name = models.CharField(unique=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Edges(models.Model):
    source = models.ForeignKey(Nodes, on_delete=models.CASCADE, related_name="sources")
    destination = models.ForeignKey(
        Nodes, on_delete=models.CASCADE, related_name="destinations"
    )
    latency = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Edge: {self.source} -> {self.destination}"


class RouteHistory(models.Model):
    source = models.CharField()
    destination = models.CharField()
    total_latency = models.FloatField()
    path = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Source: {self.source} -> {self.destination},total latency {self.total_latency}"
