import json, math

teams = []
fixtures = []

def validate_structure(data):
    if type(data) != dict:
        return False

    if "teams" not in data or "fixtures" not in data:
        return False

    if type(data["teams"]) != list or type(data["fixtures"]) != list:
        return False

    return True


def validate_teams(data):

    if type(data["teams"]) != list:
        return False

    if len(data["teams"]) > 8:
        return False

    if data["fixtures"] and len(data["teams"]) < 4:
        return False

    id_list = []
    team_list = []

    for team in data["teams"]:

        if type(team) != dict:
            return False

        if "id" not in team or "name" not in team:
            return False

        if type(team["id"]) != str or type(team["name"]) != str:
            return False

        if team["name"] != team["name"].strip():
            return False

        id_list.append(team["id"])
        team_list.append(team["name"].casefold())

    for team_id in id_list:

        if id_list.count(team_id) > 1:
            return False

        if len(team_id) != 5 or team_id[:4] != "TM00":
            return False

        if not (team_id[4:].isdigit() and int(team_id[4:]) > 0):
            return False

    numbers = sorted(int(team_id[4:]) for team_id in id_list)
    if numbers != list(range(1, len(numbers) + 1)):
        return False

    for name in team_list:
        if team_list.count(name) > 1:
            return False

        if len(name) < 2 or len(name) > 30:
            return False

    return True


def validate_fixtures(data):
    if type(data["fixtures"]) != list:
        return False

    if data["fixtures"]:
        if len(data["fixtures"]) != math.comb(len(data["teams"]), 2):
            return False

    id_list = []
    for fixture in data["fixtures"]:
        if type(fixture) != dict:
            return False

        if "id" not in fixture or "home_id" not in fixture or "away_id" not in fixture or \
        "status" not in fixture or "home_score" not in fixture or "away_score" not in fixture:
            return False

        if type(fixture["id"]) != str or type(fixture["home_id"]) != str or type(fixture["away_id"]) != str or type(fixture["status"]) != str or \
        (type(fixture["home_score"]) != int and fixture["home_score"] is not None) or \
        (type(fixture["home_score"]) == int and fixture["home_score"] < 0) or \
        (type(fixture["away_score"]) != int and fixture["away_score"] is not None) or \
        (type(fixture["away_score"]) == int and fixture["away_score"] < 0):
            return False

        if fixture["home_id"] not in [team["id"] for team in data["teams"]]:
            return False

        if fixture["away_id"] not in [team["id"] for team in data["teams"]]:
            return False

        if fixture["home_id"] == fixture["away_id"]:
            return False

        if fixture["status"] != "pending" and fixture["status"] != "played":
            return False

        if fixture["status"] == "pending" and (fixture["home_score"] is not None or fixture["away_score"] is not None):
            return False

        if fixture["status"] == "played" and (fixture["home_score"] is None or fixture["away_score"] is None):
            return False

        id_list.append(fixture["id"])

    for fixture_id in id_list:
        if len(fixture_id) < 4 or len(fixture_id) > 5 or fixture_id[:3] != "M00" or not fixture_id[3:].isdigit() or \
        (fixture_id[3:].isdigit() and int(fixture_id[3:]) == 0) :
            return False

        if id_list.count(fixture_id) > 1:
            return False

    numbers = sorted(int(fixture_id[3:]) for fixture_id in id_list)
    if numbers != list(range(1, len(numbers) + 1)):
        return False
        
    all_fix = [frozenset([fixture["home_id"], fixture["away_id"]]) for fixture in data["fixtures"]]

    if len(all_fix) != len(set(all_fix)):
        return False

    return True


def validate_tournament(data):
    if not validate_structure(data):
        return False

    if not validate_teams(data):
        return False

    if not validate_fixtures(data):
        return False

    return True


def save_tournament(teams, fixtures, filename="tournament.json"):
    data = {"teams": teams, "fixtures": fixtures}

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_tournament(teams, fixtures, filename="tournament.json"):
    try:
        with open(filename, "r") as file:
            loaded = json.load(file)

    except FileNotFoundError:
        print("No previous tournament found. Starting a new tournament.")
        return "new"

    except json.JSONDecodeError:
        print("ERROR: Tournament JSON is corrupted.")
        return "invalid"

    if not validate_tournament(loaded):
        print("ERROR: Invalid tournament data.")
        return "invalid"

    teams.clear()
    teams.extend(loaded["teams"])

    fixtures.clear()
    fixtures.extend(loaded["fixtures"])

    return "loaded"
