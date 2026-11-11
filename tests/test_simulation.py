import unittest
from unittest.mock import patch

from tournament.simulation import simulate_demo_fixtures


class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.fixtures = [
            {
                "id": "M001",
                "home_id": "TM001",
                "away_id": "TM002",
                "status": "pending",
                "home_score": None,
                "away_score": None
            },
            {
                "id": "M002",
                "home_id": "TM001",
                "away_id": "TM003",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

    def test_empty_fixtures(self):
        result = simulate_demo_fixtures([])

        self.assertEqual(result, [])

    def test_original_fixtures_remain_unchanged(self):
        original = [fixture.copy() for fixture in self.fixtures]

        simulate_demo_fixtures(self.fixtures)

        self.assertEqual(self.fixtures, original)

    def test_simulation_returns_copies(self):
        result = simulate_demo_fixtures(self.fixtures)

        self.assertIsNot(result[0], self.fixtures[0])

    def test_all_fixtures_are_simulated(self):
        result = simulate_demo_fixtures(self.fixtures)

        self.assertEqual(len(result), len(self.fixtures))

        for fixture in result:
            self.assertEqual(fixture["status"], "played")
            self.assertIsInstance(fixture["home_score"], int)
            self.assertIsInstance(fixture["away_score"], int)

    def test_scores_are_between_zero_and_five(self):
        result = simulate_demo_fixtures(self.fixtures)

        for fixture in result:
            self.assertGreaterEqual(fixture["home_score"], 0)
            self.assertLessEqual(fixture["home_score"], 5)

            self.assertGreaterEqual(fixture["away_score"], 0)
            self.assertLessEqual(fixture["away_score"], 5)

    @patch("tournament.simulation.random.randint", return_value=42)
    def test_same_seed_produces_same_results(self, mock_randint):
        first_result = simulate_demo_fixtures(self.fixtures)
        second_result = simulate_demo_fixtures(self.fixtures)

        self.assertEqual(first_result, second_result)


if __name__ == "__main__":
    unittest.main()