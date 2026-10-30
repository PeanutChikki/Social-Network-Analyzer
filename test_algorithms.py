
import unittest
from graph import SocialNetwork
from Algorithms import bfs, dfs, shortest_path, degrees_of_separation


class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        self.network = SocialNetwork()

        for user in ["Alice", "Bob", "Charlie", "David", "Eve"]:
            self.network.add_user(user)

        self.network.add_friendship("Alice", "Bob")
        self.network.add_friendship("Alice", "Charlie")
        self.network.add_friendship("Bob", "David")
        self.network.add_friendship("Charlie", "David")

        # Eve is intentionally disconnected.

    def test_bfs(self):
        self.assertEqual(
            bfs(self.network, "Alice"),
            ["Alice", "Bob", "Charlie", "David"]
        )

    def test_dfs(self):
        self.assertEqual(
            dfs(self.network, "Alice"),
            ["Alice", "Bob", "David", "Charlie"]
        )

    def test_shortest_path(self):
        self.assertEqual(
            shortest_path(self.network, "Alice", "David"),
            ["Alice", "Bob", "David"]
        )

    def test_same_start_and_destination(self):
        self.assertEqual(
            shortest_path(self.network, "Alice", "Alice"),
            ["Alice"]
        )

    def test_disconnected_users(self):
        self.assertIsNone(
            shortest_path(self.network, "Alice", "Eve")
        )

    def test_degrees_of_separation(self):
        self.assertEqual(
            degrees_of_separation(self.network, "Alice", "David"),
            2
        )


if __name__ == "__main__":
    unittest.main()
