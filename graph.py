
class SocialNetwork:
    def __init__(self):
        # Each user maps to a set of their friends
        self.graph = {}

    def add_user(self, username):
        username = username.strip()

        if not username:
            print("Username cannot be empty.")
            return False

        if username in self.graph:
            print(f"{username} already exists.")
            return False

        self.graph[username] = set()
        print(f"User {username} added successfully.")
        return True

    def remove_user(self, username):
        if username not in self.graph:
            print(f"{username} does not exist.")
            return False

        # Remove this user from all their friends
        for friend in self.graph[username]:
            self.graph[friend].discard(username)

        del self.graph[username]
        print(f"User {username} removed successfully.")
        return True

    def add_friendship(self, user1, user2):
        if user1 not in self.graph or user2 not in self.graph:
            print("Both users must exist first.")
            return False

        if user1 == user2:
            print("A user cannot be friends with themselves.")
            return False

        if user2 in self.graph[user1]:
            print("These users are already friends.")
            return False

        # Friendships go in both directions
        self.graph[user1].add(user2)
        self.graph[user2].add(user1)

        print(f"{user1} and {user2} are now friends.")
        return True

    def add_multiple_friends(self, username, friends):
        if username not in self.graph:
            print(f"{username} does not exist.")
            return

        for friend in friends:
            if friend not in self.graph:
                self.add_user(friend)

            self.add_friendship(username, friend)

    def remove_friendship(self, user1, user2):
        if user1 not in self.graph or user2 not in self.graph:
            print("Both users must exist.")
            return False

        if user2 not in self.graph[user1]:
            print("These users are not friends.")
            return False

        self.graph[user1].remove(user2)
        self.graph[user2].remove(user1)

        print(f"Friendship between {user1} and {user2} removed.")
        return True

    def get_friends(self, username):
        if username not in self.graph:
            print(f"{username} does not exist.")
            return []

        return sorted(self.graph[username])

    def get_all_users(self):
        return sorted(self.graph.keys())

    def display_graph(self):
        if not self.graph:
            print("The social network is empty.")
            return

        print("\n--- Social Network ---")
        for username in sorted(self.graph):
            friends = sorted(self.graph[username])
            print(f"{username}: {', '.join(friends) if friends else 'No friends'}")

    def get_user_count(self):
        return len(self.graph)

    def get_friendship_count(self):
        # Each friendship is stored twice, so divide by two
        return sum(len(friends) for friends in self.graph.values()) // 2


# Run this example only when graph.py is executed directly
if __name__ == "__main__":
    network = SocialNetwork()

    network.add_user("David")
    network.add_multiple_friends(
        "David",
        ["Alice", "Bob", "Charlie"]
    )   

    network.add_friendship("Alice", "Bob")

    network.display_graph()

    print("\nDavid's friends:", network.get_friends("David"))
    print("Total users:", network.get_user_count())
    print("Total friendships:", network.get_friendship_count())
