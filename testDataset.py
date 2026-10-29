
from graph import SocialNetwork
from datasetLoader import load_dataset

network = SocialNetwork()

load_dataset(
    network,
    "data/facebook_combined.txt",
    max_edges=1000
)

# Check that the graph was loaded
print("Total users:", network.get_user_count())
print("Total friendships:", network.get_friendship_count())

# Inspect a user's friends
friends = network.get_friends("0")
print("Number of friends of user 0:", len(friends))
print("First 10 friends:", friends[:10])
