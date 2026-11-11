import unittest
from unittest.mock import patch

from tournament.fixtures import gen_fixtures
from tournament.storage import teams, fixtures


class TestFixtures(unittest.TestCase):

    def setUp(self):
        # Start every test with empty tournament data.
        teams.clear()
        fixtures.clear()

        # Prevent tests from writing to the actual JSON file.
        self.save_patcher = patch("tournament.fixtures.save_tournament")
        self.mock_save = self.save_patcher.start()

    def tearDown(self):
        self.save_patcher.stop()

    def add_teams(self, number):
        """Create the requested number of sample teams."""
        for i in range(number):
            teams.append({
                "id": f"TM{i + 1:03d}",
                "name": f"Team {i + 1}"
            })

    def test_reject_fewer_than_four_teams(self):
        self.add_teams(3)

        gen_fixtures(teams)

        self.assertEqual(len(fixtures), 0)
        self.mock_save.assert_not_called()

    def test_four_teams_produce_six_fixtures(self):
        self.add_teams(4)

        gen_fixtures(teams)

        self.assertEqual(len(fixtures), 6)

    def test_six_teams_produce_fifteen_fixtures(self):
        self.add_teams(6)

        gen_fixtures(teams)

        self.assertEqual(len(fixtures), 15)

    def test_no_self_matches(self):
        self.add_teams(4)

        gen_fixtures(teams)

        for fixture in fixtures:
            self.assertNotEqual(
                fixture["home_id"],
                fixture["away_id"]
            )

    def test_no_duplicate_unordered_pairs(self):
        self.add_teams(6)

        gen_fixtures(teams)

        pairs = [
            frozenset([fixture["home_id"], fixture["away_id"]])
            for fixture in fixtures
        ]

        self.assertEqual(len(pairs), len(set(pairs)))

    def test_fixtures_cannot_be_generated_twice(self):
        self.add_teams(4)

        gen_fixtures(teams)
        first_generation = fixtures.copy()

        gen_fixtures(teams)

        self.assertEqual(fixtures, first_generation)
        self.assertEqual(len(fixtures), 6)


if __name__ == "__main__":
    unittest.main()