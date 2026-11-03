from pathlib import Path

from graph import SocialNetwork
from jsonLoader import load_json
from visualization import create_visualization

# PATHS
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "network.json"
OUTPUT_FILE = BASE_DIR / "static" / "test_visualization.html"

def main():

    print("Loading Facebook dataset...")
    if not DATA_FILE.exists():
        print("ERROR: Dataset file not found!")
        print(f"Expected location: {DATA_FILE}")
        return

    network = SocialNetwork()
    load_json(network, DATA_FILE)
    print("Dataset loaded successfully!")
    print(f"Total users: {network.get_user_count()}")
    print(f"Total friendships: {network.get_friendship_count()}")

    print("\nGenerating visualization...")

    create_visualization(
        network,
        output_path=str(OUTPUT_FILE)
    )

    print("\nVisualization generated successfully!")
    print(f"File location: {OUTPUT_FILE}")
    print("\nOpen test_visualization.html in your browser.")


if __name__ == "__main__":
    main()