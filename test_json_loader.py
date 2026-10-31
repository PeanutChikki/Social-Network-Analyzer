
from pathlib import Path
from graph import SocialNetwork
from jsonLoader import load_json

base_path = Path(__file__).resolve().parent
json_path = base_path / "data" / "network.json"

# Create an empty network
network = SocialNetwork()

# Load JSON into the network
load_json(network, json_path)

# Test basic graph operations
print("\n--- Testing Graph Operations ---")

print("Friends of user 0:", network.get_friends("0"))

print("Does user 0 exist?", "0" in network.graph)

print("Total users:", network.get_user_count())

print("Total friendships:", network.get_friendship_count())
