def parse_team_info(parser):
    number_of_teams = parser.uint8()
    teams = []
    if number_of_teams > 0:
        for player in range(0, 8):
            team_id = parser.uint8()
            teams.append(team_id)
    else:
        pass
        for player in range(0, 8):
            # TODO: Exclude single player teams if they can't be played
            # if can_computer_play or can_human_play:
            team_id = parser.uint8()
            teams.append(team_id)

    return teams

