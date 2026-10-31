
import json
from pathlib import Path


def convert_to_json(input_file, output_file):
    graph = {}

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.split()

            if len(parts) != 2:
                continue

            user1, user2 = parts

            if user1 == user2:
                continue

            # Create users if they don't exist
            graph.setdefault(user1, set())
            graph.setdefault(user2, set())

            # Add undirected friendship
            graph[user1].add(user2)
            graph[user2].add(user1)

    # Convert sets into sorted lists for JSON
    json_graph = {
        user: sorted(friends)
        for user, friends in graph.items()
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(json_graph, file, indent=4)

    print("Dataset converted successfully!")
    print("Total users:", len(json_graph))
    print(
        "Total friendships:",
        sum(len(friends) for friends in json_graph.values()) // 2
    )


if __name__ == "__main__":
    base_path = Path(__file__).resolve().parent

    input_file = base_path / "data" / "facebook_combined.txt"
    output_file = base_path / "data" / "network.json"

    convert_to_json(input_file, output_file)
