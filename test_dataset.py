
import json
from pathlib import Path

base_path = Path(__file__).resolve().parent
json_file = base_path / "data" / "network.json"

with open(json_file, "r", encoding="utf-8") as file:
    graph = json.load(file)

# Test 1: Total users
print("Total users:", len(graph))

# Test 2: Total friendships
friendships = sum(len(friends) for friends in graph.values()) // 2
print("Total friendships:", friendships)

# Test 3: Check whether friendships are mutual
mutual = True

for user, friends in graph.items():
    for friend in friends:
        if user not in graph.get(friend, []):
            mutual = False
            break
    if not mutual:
        break

print("All friendships are mutual:", mutual)

# Test 4: Check for duplicate friendships
duplicates = any(
    len(friends) != len(set(friends))
    for friends in graph.values()
)

print("Duplicate friendships found:", duplicates)

# Test 5: Display a sample
print("\nSample users:")
for user in list(graph)[:5]:
    print(user, ":", graph[user])
