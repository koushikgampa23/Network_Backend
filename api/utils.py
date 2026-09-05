import heapq
from .models import Edges


def build_graph():
    graph = {}

    edges = Edges.objects.select_related("source", "destination").all()

    for edge in edges:
        source = edge.source.name
        destination = edge.destination.name

        if source not in graph:
            graph[source] = []

        graph[source].append((destination, edge.latency))

    return graph


def find_shortest_path(source, destination):
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

    return {
        "total_latency": distances[destination],
        "path": path,
    }
