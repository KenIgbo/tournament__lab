from tournament.storage import save_tournament, fixtures, teams

def gen_team_id(teams):
    team_id = None
    if len(teams) == 0:
        team_id = "TM001"
    else:
        team_id = "TM00" + str(max([int(team["id"][4:]) for team in teams]) + 1)
    
    return team_id


def register_team(teams):
    if len(teams) >= 8:
        print("Maximum number of teams already reached! 8 required\n")
        return

    if fixtures:
        print("Cannot register teams after generating fixtures\n")
        return

    name = input("Enter team name: ").strip()

    if len(name) < 2 or len(name) > 30:
        print("Team name must be between 2 and 30 characters\n")
        return

    for team in teams:
        if team["name"].casefold() == name.casefold():
            print("Team already exists\n")
            return

    teams.append({"id":gen_team_id(teams), "name":name})
    print(f'Team "{name}" registered successfully\n')

    save_tournament(teams, fixtures)
