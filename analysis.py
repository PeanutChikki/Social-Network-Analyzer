
# analysis.py


# 1. Find mutual friends
def mutual_friends(network, user1, user2):
    graph = network.graph

    if user1 not in graph or user2 not in graph:
        return set()

    return graph[user1] & graph[user2]


# 2. Recommend new friends
def recommend_friends(network, username):
    graph = network.graph

    if username not in graph:
        return []

    existing_friends = graph[username]
    recommendations = {}

    for friend in existing_friends:
        for candidate in graph[friend]:

            # Do not recommend the user or their existing friends
            if candidate == username or candidate in existing_friends:
                continue

            common = graph[username] & graph[candidate]
            recommendations[candidate] = len(common)

    # Sort by mutual friends (highest first), then alphabetically
    return sorted(
        recommendations.items(),
        key=lambda item: (-item[1], item[0])
    )


# 3. Find the most-connected users
def most_connected_users(network):
    graph = network.graph

    if not graph:
        return []

    max_friends = max(len(friends) for friends in graph.values())

    return sorted(
        username
        for username in graph
        if len(graph[username]) == max_friends
    )


# 4. Calculate network statistics
def network_statistics(network):
    graph = network.graph

    user_count = len(graph)
    friendship_count = network.get_friendship_count()

    degrees = {
        username: len(friends)
        for username, friends in graph.items()
    }

    if user_count == 0:
        return {
            "total_users": 0,
            "total_friendships": 0,
            "friends_per_user": {},
            "average_friends": 0,
            "maximum_degree": 0,
            "minimum_degree": 0,
            "users_without_friends": []
        }

    return {
        "total_users": user_count,
        "total_friendships": friendship_count,
        "friends_per_user": degrees,
        "average_friends": (2 * friendship_count) / user_count,
        "maximum_degree": max(degrees.values()),
        "minimum_degree": min(degrees.values()),
        "users_without_friends": sorted(
            username for username in graph
            if len(graph[username]) == 0
        )
    }


# 5. Find connected components
def connected_components(network):
    graph = network.graph
    visited = set()
    components = []

    for username in graph:
        if username in visited:
            continue

        component = set()
        stack = [username]
        visited.add(username)

        while stack:
            current = stack.pop()
            component.add(current)

            for friend in graph[current]:
                if friend not in visited:
                    visited.add(friend)
                    stack.append(friend)

        components.append(component)

    return components
