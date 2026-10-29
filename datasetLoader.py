
def load_dataset(network, file_path, max_edges=1000):
    """
    Load friendships from an edge-list file into an existing
    SocialNetwork object.

    max_edges=1000 loads a small sample.
    max_edges=None loads every edge.
    """
    loaded_edges = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if max_edges is not None and loaded_edges >= max_edges:
                break

            parts = line.split()

            # Skip empty lines or malformed rows
            if len(parts) != 2:
                continue

            user1, user2 = parts

            # Add both users and their friendship.
            # setdefault avoids duplicate users and edges.
            network.graph.setdefault(user1, set())
            network.graph.setdefault(user2, set())

            if user1 != user2 and user2 not in network.graph[user1]:
                network.graph[user1].add(user2)
                network.graph[user2].add(user1)
                loaded_edges += 1

    print(f"Users loaded: {len(network.graph)}")
    print(f"Friendships loaded: {loaded_edges}")

    return network
