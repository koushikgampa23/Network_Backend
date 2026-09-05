import heapq
from .models import Edges
from django.core.cache import cache
from django.conf import settings


def build_graph():
    cache_key = f"build_graph"

    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return cached_result

    graph = {}

    edges = Edges.objects.select_related("source", "destination").all()

    for edge in edges:
        source = edge.source.name
        destination = edge.destination.name

        if source not in graph:
            graph[source] = []

        graph[source].append((destination, edge.latency))

    cache.set(cache_key, graph, timeout=settings.CACHE_TTL)

    return graph


def find_shortest_path(source, destination):
    cache_key = f"shortest_path:{source}:{destination}"

    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return cached_result

    graph = build_graph()

    distances = {source: 0}

    previous = {}

    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances.get(current_node, float("inf")):
            continue

        if current_node == destination:
            break

        for neighbor, latency in graph.get(current_node, []):
            new_distance = current_distance + latency

            if new_distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor),
                )

    if destination not in distances:
        return None

    path = []
    current_node = destination

    while current_node:
        path.append(current_node)

        if current_node == source:
            break

        current_node = previous[current_node]

    path.reverse()

    result = {
        "total_latency": distances[destination],
        "path": path,
    }

    cache.set(cache_key, result, timeout=settings.CACHE_TTL)

    return result
