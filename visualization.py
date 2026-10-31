
from pyvis.network import Network
from pathlib import Path


def create_visualization(graph, shortest_path=None,
                         output_path="static/social_network.html"):

    # Accept either a SocialNetwork object or its dictionary
    if hasattr(graph, "graph"):
        graph = graph.graph

    # Create output directory if it does not exist
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Create interactive network
    net = Network(
        height="650px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#222222",
        directed=False
    )

    # Convert shortest path into a set for highlighting
    path_nodes = set(shortest_path) if shortest_path else set()
    path_edges = set()

    if shortest_path:
        for i in range(len(shortest_path) - 1):
            path_edges.add(
                frozenset((shortest_path[i], shortest_path[i + 1]))
            )

    # Add all users as nodes
    for username in graph:

        if username in path_nodes:
            net.add_node(
                username,
                label=username,
                color="#22c55e",
                size=30
            )
        else:
            net.add_node(
                username,
                label=username,
                color="#60a5fa",
                size=22
            )

    # Add friendships as edges
    added_edges = set()

    for username, friends in graph.items():
        for friend in friends:

            edge = frozenset((username, friend))

            # Avoid adding the same undirected edge twice
            if edge in added_edges:
                continue

            added_edges.add(edge)

            if edge in path_edges:
                net.add_edge(
                    username,
                    friend,
                    color="#16a34a",
                    width=5
                )
            else:
                net.add_edge(
                    username,
                    friend,
                    color="#cbd5e1",
                    width=1
                )

    # Configure interactive physics
    net.toggle_physics(True)

    # Generate HTML file
    net.write_html(str(output_file))

    return str(output_file)
