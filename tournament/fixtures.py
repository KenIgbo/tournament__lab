import itertools

from tournament.storage import save_tournament, fixtures, teams

def gen_fixtures(teams):
    if fixtures:
        print("Fixtures already generated\n")
        return

    if len(teams) < 4 or len(teams) > 8:
        print("4-8 teams required for this tournament\n")
        return

    selections = list(itertools.combinations([team['id'] for team in teams], 2))
    for i in range(len(selections)):
        fixtures.append({"id": "M00"+str(i+1), 
                         "home_id": selections[i][0], 
                         "away_id": selections[i][1], 
                         "status": "pending", 
                         "home_score": None, 
                         "away_score": None
                        }
                       )       
    save_tournament(teams, fixtures)
    print("Fixtures generated successfully\n")


def get_team_name(teams, team_id):
    name = None
    for team in teams:
        if team["id"] == team_id:
            name = team["name"]
    return name


def get_team_score(fixtures, fix_id):
    scores = None
    for fixture in fixtures:
        if fixture["id"] == fix_id:
            scores = (fixture["home_score"], fixture["away_score"])

    return scores


def list_fixtures(fixtures):
    if len(fixtures) == 0:
        print("No fixtures available\n")
        return

    headings = [["ID", "TEAMS", "STATUS"]]

    bodies = [[fixture["id"], f'{get_team_name(teams, fixture["home_id"])} {get_team_score(fixtures, fixture["id"])[0]} - {get_team_score(fixtures, fixture["id"])[1]} {get_team_name(teams, fixture["away_id"])}', fixture["status"]] for fixture in fixtures]

    headings.extend(bodies)

    col_widths = [max(len(str(item)) for item in col) for col in zip(*headings)]

    print(f'{"="*20} TOURNAMENT LAB FIXTURES {"="*20}\n')

    for row in headings:
        formatted_row = "    |    ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row))
        print(formatted_row)
