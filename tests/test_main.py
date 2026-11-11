import unittest
from unittest.mock import patch
from main import main
from tournament.storage import teams, fixtures
from main import recovery_menu


class TestMain(unittest.TestCase):

    @patch("builtins.print")
    @patch("main.register_team")
    @patch("main.load_tournament", return_value="new")
    @patch("builtins.input", side_effect=["1", "7"])
    def test_register_team_option(self, mock_input, mock_load, mock_register, mock_print):
        main()

        mock_register.assert_called_once()


    @patch("builtins.print")
    @patch("main.gen_fixtures")
    @patch("main.load_tournament", return_value="new")
    @patch("builtins.input", side_effect=["2", "7"])
    def test_generate_fixtures_option(self, mock_input, mock_load, mock_gen, mock_print):
        main()

        mock_gen.assert_called_once()


    @patch("builtins.print")
    @patch("main.list_fixtures")
    @patch("main.load_tournament", return_value="new")
    @patch("builtins.input", side_effect=["3", "7"])
    def test_view_fixtures_option(self, mock_input, mock_load, mock_list, mock_print):
        main()

        mock_list.assert_called_once()


    @patch("builtins.print")
    @patch("main.record_results")
    @patch("main.load_tournament", return_value="new")
    @patch("builtins.input", side_effect=["4", "7"])
    def test_record_results_option(self, mock_input, mock_load, mock_record, mock_print):
        main()

        mock_record.assert_called_once()



    @patch("builtins.print")
    @patch("main.generate_standings")
    @patch("main.load_tournament", return_value="new")
    @patch("builtins.input", side_effect=["5", "7"])
    def test_view_standings_option(self, mock_input, mock_load, mock_standings, mock_print):
        main()

        mock_standings.assert_called_once()


    @patch("builtins.print")
    @patch("main.generate_standings")
    @patch("main.simulate_demo_fixtures")
    @patch("main.load_tournament", return_value="new")
    @patch("builtins.input", side_effect=["6", "7"])
    def test_simulate_standings_option(self, mock_input, mock_load, mock_simulate, mock_standings, mock_print):
        demo_fixtures = [{"id": "M001", "status": "played"}]

        mock_simulate.return_value = demo_fixtures

        main()

        mock_simulate.assert_called_once_with(fixtures)
        mock_standings.assert_called_once_with(teams, demo_fixtures)


    @patch("builtins.print")
    @patch("main.load_tournament", return_value="new")
    @patch("builtins.input", return_value="7")
    def test_exit_option(self, mock_input, mock_load, mock_print):
        main()

        mock_print.assert_called()


    @patch("builtins.print")
    @patch("main.load_tournament", return_value="new")
    @patch("builtins.input", side_effect=["9", "7"])
    def test_invalid_option(self, mock_input, mock_load, mock_print):
        main()

        mock_print.assert_any_call("Unsupported option")


    @patch("builtins.print")
    @patch("builtins.input", return_value="1")
    def test_recovery_retry(self, mock_input, mock_print):
        result = recovery_menu()

        self.assertEqual(result, "retry")


    @patch("builtins.print")
    @patch("builtins.input", side_effect=["2", "yes"])
    def test_recovery_new_tournament(self, mock_input, mock_print):
        teams.append({"id": "TM001", "name": "Red Comets"})
        fixtures.append({"id": "M001", "status": "pending"})

        result = recovery_menu()

        self.assertEqual(result, "new")
        self.assertEqual(teams, [])
        self.assertEqual(fixtures, [])


    @patch("builtins.print")
    @patch("builtins.input", side_effect=["2", "no", "3"])
    def test_recovery_decline_new_tournament(self, mock_input, mock_print):
        teams = []
        fixtures = []

        teams.append({"id": "TM001", "name": "Red Comets"})
        fixtures.append({"id": "M001", "status": "pending"})

        result = recovery_menu()

        self.assertEqual(result, "exit")
        self.assertEqual(len(teams), 1)
        self.assertEqual(len(fixtures), 1)


    @patch("builtins.print")
    @patch("builtins.input", return_value="3")
    def test_recovery_exit(self, mock_input, mock_print):
        result = recovery_menu()

        self.assertEqual(result, "exit")


    @patch("builtins.print")
    @patch("builtins.input", side_effect=["9", "3"])
    def test_invalid_recovery_option(self, mock_input, mock_print):
        result = recovery_menu()

        self.assertEqual(result, "exit")
        mock_print.assert_any_call("Invalid option.")


    @patch("builtins.print")
    @patch("main.recovery_menu", return_value="retry")
    @patch("main.load_tournament", side_effect=["invalid", "loaded"])
    @patch("builtins.input", return_value="7")
    def test_main_retries_loading(self, mock_input, mock_load, mock_recovery, mock_print):
        main()

        self.assertEqual(mock_load.call_count, 2)
        mock_recovery.assert_called_once()


    @patch("builtins.print")
    @patch("main.recovery_menu", return_value="new")
    @patch("main.load_tournament", return_value="invalid")
    @patch("builtins.input", return_value="7")
    def test_main_starts_new_tournament(self, mock_input, mock_load, mock_recovery, mock_print):
        main()

        mock_load.assert_called_once()
        mock_recovery.assert_called_once()


    @patch("builtins.print")
    @patch("main.recovery_menu", return_value="exit")
    @patch("main.load_tournament", return_value="invalid")
    def test_main_exits_after_invalid_data(self, mock_load, mock_recovery, mock_print):
        main()

        mock_load.assert_called_once()
        mock_recovery.assert_called_once()
        mock_print.assert_not_called()

if __name__ == "__main__":
    unittest.main()