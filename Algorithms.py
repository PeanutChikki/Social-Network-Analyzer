
from collections import deque


def bfs(graph, start):
    """Return users in breadth-first traversal order."""
    if start not in graph.adjacency_list:
        raise ValueError("Starting user does not exist.")

    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

        for friend in sorted(graph.adjacency_list[current]):
            if friend not in visited:
                visited.add(friend)
                queue.append(friend)

    return order


def dfs(graph, start):
    """Return users in depth-first traversal order."""
    if start not in graph.adjacency_list:
        raise ValueError("Starting user does not exist.")

    visited = set()
    order = []
    stack = [start]

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        order.append(current)

        for friend in sorted(graph.adjacency_list[current], reverse=True):
            if friend not in visited:
                stack.append(friend)

    return order


def shortest_path(graph, start, destination):
    """Return the shortest path as a list of usernames."""
    if start not in graph.adjacency_list:
        raise ValueError("Starting user does not exist.")

    if destination not in graph.adjacency_list:
        raise ValueError("Destination user does not exist.")

    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == destination:
            break

        for friend in sorted(graph.adjacency_list[current]):
            if friend not in parent:
                parent[friend] = current
                queue.append(friend)

    if destination not in parent:
        return None

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = parent[current]

    return path[::-1]


def degrees_of_separation(graph, user1, user2):
    """Return the number of friendship links in the shortest path."""
    path = shortest_path(graph, user1, user2)

    if path is None:
        return None

    return len(path) - 1
