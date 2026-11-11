import unittest
from unittest.mock import patch

from tournament.results import validate_score, record_results
from tournament.storage import fixtures, teams


class TestResults(unittest.TestCase):

    def setUp(self):
        teams.clear()
        fixtures.clear()

        fixtures.append({
            "id": "M001",
            "home_id": "TM001",
            "away_id": "TM002",
            "status": "pending",
            "home_score": None,
            "away_score": None
        })

        self.save_patcher = patch("tournament.results.save_tournament")
        self.mock_save = self.save_patcher.start()

    def tearDown(self):
        self.save_patcher.stop()

    def test_reject_invalid_scores(self):
        invalid_scores = ["-1", "1.5", True, 1.5, False]

        for score in invalid_scores:
            with self.subTest(score=score):
                self.assertFalse(validate_score(score))

    def test_accept_valid_scores(self):
        valid_scores = ["0", "1", "10", "25"]

        for score in valid_scores:
            with self.subTest(score=score):
                self.assertTrue(validate_score(score))

    @patch("builtins.input", side_effect=["M999"])
    def test_reject_unknown_fixture(self, mock_input):
        record_results(fixtures)

        self.assertEqual(fixtures[0]["status"], "pending")
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["M001", "3", "2"])
    def test_reject_duplicate_result(self, mock_input):
        fixtures[0]["status"] = "played"
        fixtures[0]["home_score"] = 3
        fixtures[0]["away_score"] = 2

        record_results(fixtures)

        self.assertEqual(fixtures[0]["home_score"], 3)
        self.assertEqual(fixtures[0]["away_score"], 2)
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["M001", "3", "-2"])
    def test_invalid_away_score_does_not_modify_fixture(self, mock_input):
        record_results(fixtures)

        self.assertEqual(fixtures[0]["status"], "pending")
        self.assertIsNone(fixtures[0]["home_score"])
        self.assertIsNone(fixtures[0]["away_score"])
        self.mock_save.assert_not_called()

    @patch("builtins.input", side_effect=["M001", "3", "2"])
    def test_successfully_record_result(self, mock_input):
        record_results(fixtures)

        self.assertEqual(fixtures[0]["status"], "played")
        self.assertEqual(fixtures[0]["home_score"], 3)
        self.assertEqual(fixtures[0]["away_score"], 2)
        self.mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()