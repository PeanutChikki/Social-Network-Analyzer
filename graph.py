class SocialNetwork:
    def __init__(self):
        self.graph = {}

    def _validate_username(self, username):
        if not isinstance(username, str):
            return None

        username = username.strip()

        if not username:
            return None

        return username

    def add_user(self, username):
        username = self._validate_username(username)

        if username is None:
            return False

        if username in self.graph:
            return False

        self.graph[username] = set()
        return True

    def remove_user(self, username):
        username = self._validate_username(username)

        if username is None or username not in self.graph:
            return False

        for friend in self.graph[username]:
            self.graph[friend].discard(username)

        del self.graph[username]
        return True

    def add_friendship(self, user1, user2):
        user1 = self._validate_username(user1)
        user2 = self._validate_username(user2)

        if user1 is None or user2 is None:
            return False

        if user1 not in self.graph or user2 not in self.graph:
            return False

        if user1 == user2:
            return False

        if user2 in self.graph[user1]:
            return False

        self.graph[user1].add(user2)
        self.graph[user2].add(user1)

        return True

    def add_multiple_friends(self, username, friends):
        username = self._validate_username(username)

        if username is None or username not in self.graph:
            return False

        if not isinstance(friends, (list, tuple, set)):
            return False

        success = True

        for friend in friends:
            friend = self._validate_username(friend)

            if friend is None:
                success = False
                continue

            if friend not in self.graph:
                self.add_user(friend)

            if not self.add_friendship(username, friend):
                success = False

        return success

    def remove_friendship(self, user1, user2):
        user1 = self._validate_username(user1)
        user2 = self._validate_username(user2)

        if user1 is None or user2 is None:
            return False

        if user1 not in self.graph or user2 not in self.graph:
            return False

        if user2 not in self.graph[user1]:
            return False

        self.graph[user1].remove(user2)
        self.graph[user2].remove(user1)

        return True

    def get_friends(self, username):
        username = self._validate_username(username)

        if username is None or username not in self.graph:
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
            print(
                f"{username}: "
                f"{', '.join(friends) if friends else 'No friends'}"
            )

    def get_user_count(self):
        return len(self.graph)

    def get_friendship_count(self):
        # Each friendship is stored twice, so divide by two
        return sum(
            len(friends) for friends in self.graph.values()
        ) // 2


if __name__ == "__main__":
    network = SocialNetwork()

    print("Adding users:")
    print(network.add_user("David"))
    print(network.add_user("Alice"))
    print(network.add_user("Bob"))
    print(network.add_user("Charlie"))

    print("\nAdding friendships:")
    print(network.add_friendship("David", "Alice"))
    print(network.add_friendship("David", "Bob"))
    print(network.add_friendship("Alice", "Bob"))

    print("\nTesting validation:")
    print(network.add_user(" David "))  # Duplicate
    print(network.add_user(""))         # Empty username
    print(network.add_user(None))       # Invalid input

    print("\nDisplaying network:")
    network.display_graph()

    print("\nDavid's friends:", network.get_friends("David"))
    print("Total users:", network.get_user_count())
    print("Total friendships:", network.get_friendship_count())

    print("\nRemoving Alice:")
    print(network.remove_user("Alice"))

    network.display_graph()