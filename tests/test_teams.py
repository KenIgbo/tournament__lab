import unittest
from unittest.mock import patch

from tournament.teams import register_team
from tournament.storage import teams, fixtures


class TestTeams(unittest.TestCase):

    def setUp(self):
        teams.clear()
        fixtures.clear()

    @patch("tournament.teams.save_tournament")
    @patch("builtins.input", return_value="Red Comets")
    def test_duplicate_casefolded_name(self, mock_input, mock_save):
        teams.append({"id": "TM001", "name": "Red Comets"})

        register_team(teams)

        self.assertEqual(len(teams), 1)
        mock_save.assert_not_called()

    @patch("tournament.teams.save_tournament")
    @patch("builtins.input", return_value=" ")
    def test_reject_blank_name(self, mock_input, mock_save):
        register_team(teams)

        self.assertEqual(len(teams), 0)
        mock_save.assert_not_called()

    @patch("tournament.teams.save_tournament")
    @patch("builtins.input", return_value="A" * 31)
    def test_reject_too_long_name(self, mock_input, mock_save):
        register_team(teams)

        self.assertEqual(len(teams), 0)
        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()