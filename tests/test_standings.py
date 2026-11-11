import unittest
from contextlib import redirect_stdout
from io import StringIO

from tournament.standings import cal_points, generate_standings


class TestStandings(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Alpha"},
            {"id": "TM002", "name": "Beta"},
            {"id": "TM003", "name": "Gamma"},
            {"id": "TM004", "name": "Delta"}
        ]

        self.fixtures = []

    def add_fixture(self, fixture_id, home, away, home_score, away_score):
        self.fixtures.append({
            "id": fixture_id,
            "home_id": home,
            "away_id": away,
            "status": "played",
            "home_score": home_score,
            "away_score": away_score
        })

    def get_standings_output(self):
        output = StringIO()

        with redirect_stdout(output):
            generate_standings(self.teams, self.fixtures)

        return output.getvalue()

    def test_correct_3_1_0_points(self):
        self.add_fixture("M001", "TM001", "TM002", 2, 0)
        self.add_fixture("M002", "TM003", "TM004", 1, 1)

        self.assertEqual(cal_points("TM001", self.fixtures), 3)
        self.assertEqual(cal_points("TM002", self.fixtures), 0)
        self.assertEqual(cal_points("TM003", self.fixtures), 1)
        self.assertEqual(cal_points("TM004", self.fixtures), 1)

    def test_tie_break_sorting(self):
        self.teams = [
            {"id": "TM001", "name": "Aardvark"},
            {"id": "TM002", "name": "Zebra"},
            {"id": "TM003", "name": "Gamma"},
            {"id": "TM004", "name": "Beta"},
            {"id": "TM005", "name": "Opponent1"},
            {"id": "TM006", "name": "Opponent2"},
            {"id": "TM007", "name": "Opponent3"},
            {"id": "TM008", "name": "Opponent4"}
        ]

        # Gamma: 3 points, GD +3, GF 3
        self.add_fixture("M001", "TM003", "TM007", 3, 0)

        # Beta: 3 points, GD +2, GF 3
        self.add_fixture("M002", "TM004", "TM008", 3, 1)

        # Aardvark: 3 points, GD +2, GF 2
        self.add_fixture("M003", "TM001", "TM005", 2, 0)

        # Zebra: 3 points, GD +2, GF 2
        self.add_fixture("M004", "TM002", "TM006", 2, 0)

        output = self.get_standings_output()

        # Check the order of the four teams.
        self.assertLess(output.index("Gamma"), output.index("Beta"))
        self.assertLess(output.index("Beta"), output.index("Aardvark"))
        self.assertLess(output.index("Aardvark"), output.index("Zebra"))

    def test_standings_recomputed_from_matches(self):
        self.add_fixture("M001", "TM001", "TM002", 2, 0)

        first_output = self.get_standings_output()

        # Alpha initially has 3 points.
        self.assertLess(
            first_output.index("Alpha"),
            first_output.index("Beta")
        )

        # Change the result so Beta wins instead.
        self.fixtures[0]["home_score"] = 0
        self.fixtures[0]["away_score"] = 3

        second_output = self.get_standings_output()

        # Beta should now appear above Alpha.
        self.assertLess(
            second_output.index("Beta"),
            second_output.index("Alpha")
        )

    def test_champion_only_shown_when_all_matches_played(self):
        self.add_fixture("M001", "TM001", "TM002", 2, 0)

        # Add another fixture that is still pending.
        self.fixtures.append({
            "id": "M002",
            "home_id": "TM001",
            "away_id": "TM003",
            "status": "pending",
            "home_score": None,
            "away_score": None
        })

        first_output = self.get_standings_output()

        self.assertIn("Tournament in Progress", first_output)
        self.assertNotIn("Champion:", first_output)

        # Record the remaining result.
        self.fixtures[1]["home_score"] = 1
        self.fixtures[1]["away_score"] = 0
        self.fixtures[1]["status"] = "played"

        second_output = self.get_standings_output()

        self.assertIn("Champion: Alpha", second_output)


if __name__ == "__main__":
    unittest.main()