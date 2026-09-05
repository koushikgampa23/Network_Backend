from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Edges, Nodes, RouteHistory


@receiver([post_save, post_delete], sender=Nodes)
def invalidate_node_cache(sender, instance, **kwargs):
    cache.delete_pattern("*nodes_list*")
    cache.delete_pattern("*edges_list*")


@receiver([post_save, post_delete], sender=Edges)
def invalidate_edge_cache(sender, instance, **kwargs):
    cache.delete_pattern("*edges_list*")
    cache.delete_pattern("*build_graph*")
    cache.delete_pattern("*shortest_path*")


@receiver([post_save, post_delete], sender=RouteHistory)
def invalidate_route_history_cache(sender, instance, **kwargs):
    cache.delete_pattern("*route_history_list*")
