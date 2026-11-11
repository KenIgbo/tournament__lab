from tournament.teams import register_team
from tournament.fixtures import gen_fixtures, list_fixtures
from tournament.storage import load_tournament, teams, fixtures
from tournament.results import record_results
from tournament.standings import generate_standings
from tournament.simulation import simulate_demo_fixtures


def recovery_menu():
    while True:
        print("\nTOURNAMENT RECOVERY")
        print("1. Try loading again")
        print("2. Start a new tournament")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            return "retry"

        elif choice == "2":
            confirm = input("Start a new tournament? (yes/no): ").lower()

            if confirm == "yes":
                teams.clear()
                fixtures.clear()
                return "new"

        elif choice == "3":
            return "exit"

        else:
            print("Invalid option.")


def main():
    status = load_tournament(teams, fixtures)

    while status == "invalid":
        choice = recovery_menu()

        if choice == "retry":
            status = load_tournament(teams, fixtures)

        elif choice == "new":
            status = "new"

        elif choice == "exit":
            return

    while True:
        print(f'\n{"="*50} TOURNAMENT LAB {"="*50}')
        print("1. Register teams\n2. Generate fixtures\n3. View fixtures\n4. Record results\n5. View standings\n6. Simulate standings\n7. Exit")

        option = input("\nSelect an option: ").strip()

        if option == "1":
            register_team(teams)

        elif option == "2":
            gen_fixtures(teams)

        elif option == "3":
            list_fixtures(fixtures)

        elif option == "4":
            record_results(fixtures)

        elif option == "5":
            generate_standings(teams, fixtures)

        elif option == "6":
            demo_fixtures = simulate_demo_fixtures(fixtures)
            generate_standings(teams, demo_fixtures)

        elif option == "7":
            return

        else:
            print("Unsupported option")


if __name__ == "__main__":
    main()