# pyleague

***Before use install a virtualenv specified by requirements.txt

***Terminal help:***

usage: pyleague [-h] [-t] [--DELETE_TABLE]
                [home_team_name] [home_team_goals] [away_team_name]
                [away_team_goals]

Manage and display a football league table

positional arguments:
  home_team_name   home team name (string)
  home_team_goals  home team goals (int)
  away_team_name   away team name (string)
  away_team_goals  away team goals (int)

optional arguments:
  -h, --help       show this help message and exit
  -t, --table      Display League Table
  --DELETE_TABLE   Deletes the league_table WARNING: is not executed if any
                   postioinal arguments are also supplied, for safety.
