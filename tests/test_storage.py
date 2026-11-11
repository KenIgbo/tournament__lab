import unittest
import tempfile
import os
import json

from contextlib import redirect_stdout
from io import StringIO

from tournament import storage
from tournament.standings import generate_standings


class TestStorage(unittest.TestCase):

    def setUp(self):
        storage.teams.clear()
        storage.fixtures.clear()

        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Eagles"},
            {"id": "TM003", "name": "Yellow Ravens"},
            {"id": "TM004", "name": "Black Panthers"}
        ]

        self.fixtures = [
            {
                "id": "M001",
                "home_id": "TM001",
                "away_id": "TM002",
                "status": "played",
                "home_score": 3,
                "away_score": 1
            },
            {
                "id": "M002",
                "home_id": "TM001",
                "away_id": "TM003",
                "status": "played",
                "home_score": 2,
                "away_score": 0
            },
            {
                "id": "M003",
                "home_id": "TM001",
                "away_id": "TM004",
                "status": "pending",
                "home_score": None,
                "away_score": None
            },
            {
                "id": "M004",
                "home_id": "TM002",
                "away_id": "TM003",
                "status": "played",
                "home_score": 1,
                "away_score": 1
            },
            {
                "id": "M005",
                "home_id": "TM002",
                "away_id": "TM004",
                "status": "pending",
                "home_score": None,
                "away_score": None
            },
            {
                "id": "M006",
                "home_id": "TM003",
                "away_id": "TM004",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

        storage.teams.extend(self.teams)
        storage.fixtures.extend(self.fixtures)

        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = os.path.join(self.temp_dir.name, "test_tournament.json")

    def tearDown(self):
        storage.teams.clear()
        storage.fixtures.clear()
        self.temp_dir.cleanup()

    def test_reject_bad_references_without_state_change(self):
        # Keep copies of the current tournament.
        original_teams = [team.copy() for team in storage.teams]
        original_fixtures = [fixture.copy() for fixture in storage.fixtures]

        # Create invalid tournament data.
        invalid_teams = [team.copy() for team in self.teams]
        invalid_fixtures = [fixture.copy() for fixture in self.fixtures]

        # Reference a team that does not exist.
        invalid_fixtures[0]["home_id"] = "TM999"

        with open(self.filename, "w") as file:
            json.dump({
                "teams": invalid_teams,
                "fixtures": invalid_fixtures
            }, file)

        status = storage.load_tournament(
            storage.teams,
            storage.fixtures,
            self.filename
        )

        self.assertEqual(status, "invalid")
        self.assertEqual(storage.teams, original_teams)
        self.assertEqual(storage.fixtures, original_fixtures)

    def test_reload_preserves_ids_and_standings(self):
        # Save the original tournament.
        storage.save_tournament(
            storage.teams,
            storage.fixtures,
            self.filename
        )

        # Capture standings before reloading.
        before = StringIO()

        with redirect_stdout(before):
            generate_standings(storage.teams, storage.fixtures)

        # Clear memory to simulate a fresh application start.
        storage.teams.clear()
        storage.fixtures.clear()

        status = storage.load_tournament(
            storage.teams,
            storage.fixtures,
            self.filename
        )

        # Capture standings after reloading.
        after = StringIO()

        with redirect_stdout(after):
            generate_standings(storage.teams, storage.fixtures)

        self.assertEqual(status, "loaded")

        self.assertEqual(
            [team["id"] for team in storage.teams],
            ["TM001", "TM002", "TM003", "TM004"]
        )

        self.assertEqual(
            [fixture["id"] for fixture in storage.fixtures],
            ["M001", "M002", "M003", "M004", "M005", "M006"]
        )

        self.assertEqual(before.getvalue(), after.getvalue())

    def test_missing_file_returns_new(self):
        status = storage.load_tournament(
            storage.teams,
            storage.fixtures,
            self.filename
        )

        self.assertEqual(status, "new")

    def test_reject_malformed_fixture_id(self):
        invalid_teams = [team.copy() for team in self.teams]
        invalid_fixtures = [fixture.copy() for fixture in self.fixtures]
        invalid_fixtures[0]["id"] = "M00ABC"
        
        data = {
            "teams": invalid_teams,
            "fixtures": invalid_fixtures
        }
            
        self.assertFalse(storage.validate_tournament(data))

    def test_reject_duplicate_team_ids(self):
        invalid_teams = [team.copy() for team in self.teams]
        invalid_fixtures = [fixture.copy() for fixture in self.fixtures]
        
        invalid_teams[1]["id"] = "TM001"
        
        data = {
            "teams": invalid_teams,
            "fixtures": invalid_fixtures
        }
        
        self.assertFalse(storage.validate_tournament(data))

    def test_reject_duplicate_team_names(self):
        invalid_teams = [team.copy() for team in self.teams]
        invalid_fixtures = [fixture.copy() for fixture in self.fixtures]

        invalid_teams[1]["name"] = "red comets"
        
        data = {
            "teams": invalid_teams,
            "fixtures": invalid_fixtures
        }
        
        self.assertFalse(storage.validate_tournament(data))

    def test_reject_boolean_scores(self):
        invalid_teams = [team.copy() for team in self.teams]
        invalid_fixtures = [fixture.copy() for fixture in self.fixtures]
        
        invalid_fixtures[0]["home_score"] = True
        
        data = {
            "teams": invalid_teams,
            "fixtures": invalid_fixtures
        }
        
        self.assertFalse(storage.validate_tournament(data))


if __name__ == "__main__":
    unittest.main()