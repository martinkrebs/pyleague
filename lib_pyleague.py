#!/usr/bin/env python
import sqlite3


db = sqlite3.connect('pyleague.db')


# tested
def update_game_results(home_team_name, home_team_goals,
                        away_team_name, away_team_goals):
    """
    Takes the results of a game and saves each teams record in the db
    Command line params are passed to this function
    """
    # home team
    results = team_game_results(home_team_goals, away_team_goals)
    results.insert(0, home_team_name)
    save_record(tuple(results))

    # away team
    results = team_game_results(away_team_goals, home_team_goals)
    results.insert(0, away_team_name)
    save_record(tuple(results))


# tested
def team_game_results(team_goals, opponent_goals):
    """
    Returns [w, d, l, pts] - results for a game played with an opponent team
    eg. if the team won the tuple would be (1 ,0 ,0, 3) for win, 3 points
    """
    w = 0
    d = 0
    l = 0
    if team_goals > opponent_goals:
        w = 1
        pts = 3
    elif team_goals < opponent_goals:
        l = 1
        pts = 0
    else:
        d = 1
        pts = 2

    return [w, d, l, pts]


# tested
def create_table_if_not_exists():
    query = """
    CREATE TABLE IF NOT EXISTS league_table(
        name TEXT,
        w INTEGER,
        d INTEGER,
        l INTEGER,
        pts INTEGER
    )
    """
    cursor = db.cursor()
    cursor.execute(query)


# tested
def create_record(values):
    """
    Creates a new team record from a tuple (name, w, d, l, pts)
    """
    cursor = db.cursor()

    cursor.execute("INSERT INTO league_table VALUES (?,?,?,?,?)", values)
    db.commit()
    cursor.close()


# tested
def get_record_by_name(name):
    """
    Get a record by name, returns <class 'tuple'> or None
    eg: ('chelsea', 24, 3, 5, 75) or None
    """
    cursor = db.cursor()

    cursor.execute("SELECT * FROM league_table WHERE name=?", (name,))
    row = cursor.fetchone()
    cursor.close()

    return row


# tested
def update_record(values):
    """
    Updates an existing record, from a tuple (name, w, d, l, pts)
    """
    cursor = db.cursor()

    row = get_record_by_name(values[0])

    # Add the passed in values to existing record values w, d, l & pts
    row_list = list(row)
    for i in range(1, 5):
        row_list[i] += values[i]

    # remove the name, we are not updating the name.
    row_list.pop(0)
    # but we do need the name at the end, for the WHERE name=? param below
    row_list.append(values[0])
    data = tuple(row_list)

    # update the record
    cursor.execute(
        "UPDATE league_table SET w=?, d=?, l=?, pts=? WHERE name=?", data)
    db.commit()
    cursor.close()


# tested
def save_record(values):
    """
    Creates a new record if it does not exist or updates existing one
    """
    cursor = db.cursor()

    cursor.execute(
        "SELECT count(*) FROM league_table WHERE name=?", (values[0],)
    )
    count = cursor.fetchone()[0]
    cursor.close()

    if count == 0:
        create_record(values)
    else:
        update_record(values)

# tested
def get_league_table():
    """
    Return a record set (list of tuples) of all records ordered by pts col
    """
    cursor = db.cursor()

    cursor.execute("SELECT * FROM league_table ORDER BY pts DESC")
    league_table = cursor.fetchall()
    cursor.close()

    return league_table

# tested
def delete_table():
    """
    Delete the db table!!
    """
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS league_table')
    db.commit()
    cursor.close()
