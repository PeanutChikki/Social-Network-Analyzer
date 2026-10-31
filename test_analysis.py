
import unittest

from graph import SocialNetwork
from analysis import (
    mutual_friends,
    recommend_friends,
    most_connected_users,
    network_statistics,
    connected_components
)


class TestAnalysis(unittest.TestCase):

    def setUp(self):
        self.network = SocialNetwork()

        users = [
            "Alice", "Bob", "Charlie",
            "David", "Eve", "Frank", "Grace"
        ]

        for user in users:
            self.network.add_user(user)

        # First community
        self.network.add_friendship("Alice", "Bob")
        self.network.add_friendship("Alice", "Charlie")
        self.network.add_friendship("Bob", "Charlie")
        self.network.add_friendship("Bob", "David")
        self.network.add_friendship("Charlie", "David")

        # Second community
        self.network.add_friendship("Eve", "Frank")

        # Grace is intentionally isolated (no friends).

    # 1. Test mutual friends
    def test_mutual_friends(self):
        result = mutual_friends(
            self.network, "Alice", "David"
        )

        self.assertEqual(result, {"Bob", "Charlie"})

    def test_mutual_friends_invalid_user(self):
        result = mutual_friends(
            self.network, "Alice", "Unknown"
        )

        self.assertEqual(result, set())

    # 2. Test friend recommendations
    def test_recommend_friends(self):
        result = recommend_friends(
            self.network, "Alice"
        )

        self.assertEqual(result, [("David", 2)])

    def test_recommend_friends_invalid_user(self):
        result = recommend_friends(
            self.network, "Unknown"
        )

        self.assertEqual(result, [])

    def test_recommend_friends_no_candidates(self):
        result = recommend_friends(
            self.network, "Grace"
        )

        self.assertEqual(result, [])

    # 3. Test most connected users
    def test_most_connected_users(self):
        result = most_connected_users(self.network)

        self.assertEqual(result, ["Bob", "Charlie"])

    def test_most_connected_users_empty_network(self):
        empty_network = SocialNetwork()

        result = most_connected_users(empty_network)

        self.assertEqual(result, [])

    # 4. Test network statistics
    def test_network_statistics(self):
        result = network_statistics(self.network)

        self.assertEqual(result["total_users"], 7)
        self.assertEqual(result["total_friendships"], 6)

        self.assertEqual(
            result["friends_per_user"],
            {
                "Alice": 2,
                "Bob": 3,
                "Charlie": 3,
                "David": 2,
                "Eve": 1,
                "Frank": 1,
                "Grace": 0
            }
        )

        self.assertAlmostEqual(
            result["average_friends"], 12 / 7
        )

        self.assertEqual(result["maximum_degree"], 3)
        self.assertEqual(result["minimum_degree"], 0)

        self.assertEqual(
            result["users_without_friends"],
            ["Grace"]
        )

    def test_network_statistics_empty_network(self):
        empty_network = SocialNetwork()

        result = network_statistics(empty_network)

        self.assertEqual(result["total_users"], 0)
        self.assertEqual(result["total_friendships"], 0)
        self.assertEqual(result["friends_per_user"], {})
        self.assertEqual(result["average_friends"], 0)
        self.assertEqual(result["maximum_degree"], 0)
        self.assertEqual(result["minimum_degree"], 0)
        self.assertEqual(result["users_without_friends"], [])

    # 5. Test connected components
    def test_connected_components(self):
        result = connected_components(self.network)

        expected = [
            {"Alice", "Bob", "Charlie", "David"},
            {"Eve", "Frank"},
            {"Grace"}
        ]

        self.assertEqual(
            {frozenset(c) for c in result},
            {frozenset(c) for c in expected}
        )

    def test_connected_components_empty_network(self):
        empty_network = SocialNetwork()

        result = connected_components(empty_network)

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
