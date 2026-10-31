
from pathlib import Path
from graph import SocialNetwork
from jsonLoader import load_json
from visualization import create_visualization

# Load the dataset
network = SocialNetwork()

base_path = Path(__file__).resolve().parent
json_path = base_path / "data" / "network.json"

load_json(network, json_path)

# Visualize a small sample instead of all 4039 users
sample_graph = {}

for user in list(network.graph)[:20]:
    sample_graph[user] = {
        friend for friend in network.graph[user]
        if friend in network.graph and friend in list(network.graph)[:20]
    }

# Generate visualization
create_visualization(
    sample_graph,
    output_path="static/social_network.html"
)

print("Visualization created successfully!")
