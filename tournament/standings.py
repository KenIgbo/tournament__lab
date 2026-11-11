from tournament.storage import fixtures, teams

def cal_games_played(team_id, fixtures):
    played = 0

    for fixture in fixtures:
        if fixture["status"] == "played":
            if fixture["home_id"] == team_id or fixture["away_id"] == team_id:
                played += 1

    return played


def cal_wins(team_id, fixtures):
    wins = 0

    for fixture in fixtures:
        if fixture["status"] == "played":
            if fixture["home_id"] == team_id:
                if fixture["home_score"] > fixture["away_score"]:
                    wins += 1

            if fixture["away_id"] == team_id:
                if fixture["away_score"] > fixture["home_score"]:
                    wins += 1

    return wins


def cal_draws(team_id, fixtures):
    draws = 0

    for fixture in fixtures:
        if fixture["status"] == "played":
            if fixture["home_id"] == team_id:
                if fixture["home_score"] == fixture["away_score"]:
                    draws += 1

            if fixture["away_id"] == team_id:
                if fixture["away_score"] == fixture["home_score"]:
                    draws += 1

    return draws


def cal_losses(team_id, fixtures):
    losses = 0

    for fixture in fixtures:
        if fixture["status"] == "played":
            if fixture["home_id"] == team_id:
                if fixture["home_score"] < fixture["away_score"]:
                    losses += 1

            if fixture["away_id"] == team_id:
                if fixture["away_score"] < fixture["home_score"]:
                    losses += 1

    return losses


def cal_points(team_id, fixtures):
    points = 0

    for fixture in fixtures:
        if fixture["status"] == "played":
            if fixture["home_id"] == team_id:
                if fixture["home_score"] > fixture["away_score"]:
                    points += 3
                elif fixture["home_score"] == fixture["away_score"]:
                    points += 1
                else:
                    points += 0

            if fixture["away_id"] == team_id:
                if fixture["away_score"] > fixture["home_score"]:
                    points += 3
                elif fixture["away_score"] == fixture["home_score"]:
                    points += 1
                else:
                    points += 0

    return points


def cal_goal_for(team_id, fixtures):
    goal_for = 0

    for fixture in fixtures:
        if fixture["status"] == "played":
            if fixture["home_id"] == team_id:
                goal_for += fixture["home_score"]

            if fixture["away_id"] == team_id:
                goal_for += fixture["away_score"]

    return goal_for


def cal_goal_against(team_id, fixtures):
    goal_against = 0

    for fixture in fixtures:
        if fixture["status"] == "played":
            if fixture["home_id"] == team_id:
                goal_against += fixture["away_score"]

            if fixture["away_id"] == team_id:
                goal_against += fixture["home_score"]

    return goal_against


def cal_goal_diff(team_id, fixtures):
    goal_diff = cal_goal_for(team_id, fixtures) - cal_goal_against(team_id, fixtures)
    return goal_diff


def generate_standings(teams, fixtures):
    if not fixtures:
        print("No Standings for this Tournament yet")
        return

    standings = [{"name": team["name"], 
                  "played": cal_games_played(team["id"], fixtures), 
                  "wins": cal_wins(team["id"], fixtures), 
                  "draws": cal_draws(team["id"], fixtures), 
                  "losses": cal_losses(team["id"], fixtures), 
                  "points": cal_points(team["id"], fixtures), 
                  "for": cal_goal_for(team["id"], fixtures), 
                  "against": cal_goal_against(team["id"], fixtures), 
                  "diff": cal_goal_diff(team["id"], fixtures)
                 } for team in teams
                ]

    standings.sort(
        key=lambda team: (
                        -team["points"], 
                        -team["diff"], 
                        -team["for"], 
                        team["name"].casefold()
        )
    )

    cnt = 0
    for fixture in fixtures:
        if fixture["status"] == "pending":
            cnt += 1

    if cnt > 0:
        standings_status = "Tournament in Progress\n"

    else:
        standings_status = f'Tournament Over! Champion: {standings[0]["name"]}\n'

    headings = [["TEAM", "PLAYED", "WINS", "DRAWS", "LOSSES", "POINTS", "GF", "GA", "GD"]]

    bodies = [[team["name"], team["played"], team["wins"], team["draws"], team["losses"], team["points"], team["for"], team["against"], team["diff"]] for team in standings]
    
    headings.extend(bodies)

    col_widths = [max(len(str(item)) for item in col) for col in zip(*headings)]

    print(f'{"="*25} TOURNAMENT LAB STANDINGS {"="*25}')

    print(f'{" "*25} {standings_status} {" "*25}')

    for row in headings:
        formatted_row = " | ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row))
        print(formatted_row)