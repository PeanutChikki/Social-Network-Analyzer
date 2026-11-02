import json
from pathlib import Path

from graph import SocialNetwork
from jsonLoader import load_json


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "data" / "network.json"


# --------------------------------------------------
# LOAD ORIGINAL NETWORK
# --------------------------------------------------

def load_original_network():
    """
    Load the original network.json dataset
    into a new SocialNetwork object.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    network = SocialNetwork()
    load_json(network, DATASET_PATH)

    return network


# --------------------------------------------------
# EXPORT NETWORK
# --------------------------------------------------

def export_network(network):
    """
    Convert the current network into a JSON-compatible
    dictionary.
    """

    return {
        user: sorted(list(friends))
        for user, friends in network.graph.items()
    }


# --------------------------------------------------
# SAVE NETWORK TO JSON
# --------------------------------------------------

def save_network(network, file_path):
    """
    Save the current network to a JSON file.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    data = export_network(network)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return file_path


# --------------------------------------------------
# IMPORT NETWORK FROM JSON
# --------------------------------------------------

def import_network(file):
    """
    Read an uploaded JSON file and reconstruct
    a SocialNetwork object.
    """

    data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Invalid network file.")

    network = SocialNetwork()

    # Validate and create all users
    for user, friends in data.items():

        if not isinstance(user, str) or not isinstance(friends, list):
            raise ValueError("Invalid network structure.")

        if not all(isinstance(friend, str) for friend in friends):
            raise ValueError("Invalid friendship data.")

        network.add_user(user)

    # Reconstruct friendships
    for user, friends in data.items():

        for friend in friends:

            if user == friend:
                continue

            if friend not in network.graph:
                network.add_user(friend)

            network.add_friendship(user, friend)

    return network


# --------------------------------------------------
# RESET NETWORK
# --------------------------------------------------

def reset_network():
    """
    Restore the original dataset.
    """

    return load_original_network()