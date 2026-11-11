from tournament.storage import save_tournament, fixtures, teams

def validate_score(score):
    if not isinstance(score, str):
        return False

    score = score.strip()

    return score.isdecimal()


def record_results(fixtures):
    if not fixtures:
        print("No fixtures available")
        return

    fixture_id = input("Enter fixture ID: ")

    for fixture in fixtures:
        if fixture["id"] == fixture_id:
            if fixture["status"] == "pending":

                home_score = input("Enter home score: ")
                away_score = input("Enter away score: ")

                if not validate_score(home_score) or not validate_score(away_score):
                    print("Score must be a number from 0 upwards\n")
                    return

                fixture["home_score"] = int(home_score)
                fixture["away_score"] = int(away_score)

                fixture["status"] = "played"

                save_tournament(teams, fixtures)

                print("Results recorded successfully\n")
                return

            print("This fixture has already been played\n")
            return

    print("Fixture for this ID does not exist\n")
    return
