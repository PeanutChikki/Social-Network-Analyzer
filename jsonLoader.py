
import json


def load_json(network, file_path):
    """
    Load a JSON adjacency list into an existing SocialNetwork object.
    Converts friend lists into sets.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    network.graph = {
        user: set(friends)
        for user, friends in data.items()
    }

    print("JSON dataset loaded successfully!")
    print("Total users:", network.get_user_count())
    print("Total friendships:", network.get_friendship_count())

    return network
