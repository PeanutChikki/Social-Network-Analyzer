import json
from pathlib import Path
from graph import SocialNetwork
from jsonLoader import load_json

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "network.json"

def load_original_network():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )
    network = SocialNetwork()
    load_json(network, DATASET_PATH)

    return network

def export_network(network):
    return {
        user: sorted(list(friends))
        for user, friends in network.graph.items()
    }

def save_network(network, file_path):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    data = export_network(network)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return file_path

def import_network(file):
    data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Invalid network file.")

    network = SocialNetwork()
    for user, friends in data.items():
        if not isinstance(user, str) or not isinstance(friends, list):
            raise ValueError("Invalid network structure.")

        if not all(isinstance(friend, str) for friend in friends):
            raise ValueError("Invalid friendship data.")

        network.add_user(user)

    for user, friends in data.items():
        for friend in friends:
            if user == friend:
                continue
            if friend not in network.graph:
                network.add_user(friend)

            network.add_friendship(user, friend)

    return network

def reset_network():
    return load_original_network()