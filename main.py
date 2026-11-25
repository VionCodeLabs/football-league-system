import sqlite3
from datetime import datetime

connection = sqlite3.connect("football.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id TEXT UNIQUE,
        team_name TEXT NOT NULL,
        coach TEXT NOT NULL,
        home_stadium TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id TEXT UNIQUE,
        player_name TEXT NOT NULL,
        position TEXT NOT NULL,

        team_id TEXT NOT NULL,
        
        FOREIGN KEY (team_id)
        REFERENCES teams(team_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT UNIQUE,
        home_team_id TEXT NOT NULL,
        away_team_id TEXT NOT NULL,
        match_date TEXT,

        FOREIGN KEY (home_team_id)
        REFERENCES teams(team_id),

        FOREIGN KEY (away_team_id)
        REFERENCES teams(team_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stats_id TEXT UNIQUE,
        player_id TEXT NOT NULL,
        match_id TEXT NOT NULL,
        goals INTEGER DEFAULT 0,
        assists INTEGER DEFAULT 0,
        
        FOREIGN KEY (player_id)
        REFERENCES players(player_id),
        
        FOREIGN KEY (match_id)
        REFERENCES matches(match_id)
    )
""")

connection.commit()
print("database and tables created successfully!\n")

#====================================================
#CRUD FUNCTIONS
#====================================================

def add_team():
    while True:
        team_id = input("enter team id (or type 'done' to terminate process): ")

        if team_id.lower() == "done":
           print("process terminated.\n")
           break

        if not team_id:
            print("team id required.\n")
            continue

        team_name = input("enter team name: ").strip().title()

        if not team_name:
            print("team name required.\n")
            continue

        coach = input("enter coach name: ").strip().title()

        if not coach:
            print("coach name required.\n")
            continue

        home_stadium = input("enter stadium name: ").strip().title()

        if not home_stadium:
            print("home stadium required.\n")
            continue

        try:
            cursor.execute("""
                INSERT INTO teams (team_id, team_name, coach, home_stadium)
                VALUES (?, ?, ?, ?)
            """, (team_id, team_name, coach, home_stadium))

            connection.commit()
            print("team added successfully.\n")

        except sqlite3.IntegrityError as e:
            print("database constaint violation error:", e)


def add_player():
    while True:
        player_id = input("enter player id (or tyoe 'done' to terminate process): ")

        if player_id.lower() == "done":
            print("process terminated.\n")
            break

        if not player_id:
            print("player id required.\n")
            continue

        player_name = input("enter player name: ").strip().title()

        if not player_name:
            print("player name required.\n")
            continue

        position = input("enter position: ").strip().title()

        if not position:
            print("position required.\n")
            continue

        team_id = input("enter team id: ")

        if not team_id:
            print("team id required.\n")
            continue

        team = cursor.execute("""
            SELECT * FROM teams
            WHERE team_id = ?
        """, (team_id,)).fetchone()

        if not team:
            print("team not available.\n")
            continue

        try:
            cursor.execute("""
                INSERT INTO players (player_id, player_name, position, team_id)
                VALUES (?, ?, ?, ?)
            """, (player_id, player_name, position, team_id))

            connection.commit()
            print("player added successfully.\n")

        except sqlite3.IntegrityError as e:
            print("database constraints error:", e)


def add_match():
    while True:
        match_id = input("enter match id (or type 'done' to terminate): ")

        if match_id.lower() == "done":
            print("process terminated.\n")
            break

        if not match_id:
            print("match id required.\n")
            continue

        home_team_id = input("enter home team id: ")

        if not home_team_id:
            print("home team id required.\n")
            continue

        team_1 = cursor.execute("""
            SELECT * FROM teams
            WHERE team_id = ?
            """, (home_team_id,)).fetchone()

        if not team_1:
            print("team not available.\n")
            continue

        away_team_id = input("enter away team id: ")

        if not away_team_id:
            print("away team id required.\n")
            continue

        team_2 = cursor.execute("""
            SELECT * FROM teams
            WHERE team_id = ?
        """, (away_team_id,)).fetchone()
        
        if not team_2:
            print("team not available.\n")
            continue

        match_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor.execute("""
                INSERT INTO matches (match_id, home_team_id, away_team_id, match_date)
                VALUES (?, ?, ?, ?)
            """, (match_id, home_team_id, away_team_id, match_date))

            connection.commit()
            print("match added successfully.\n")

        except sqlite3.IntegrityError as e:
            print("database constrains violation error:", e)


def add_player_stats():
    while True:
        stats_id = input("enter stat id (or type 'done' to terminate process): ")

        if stats_id.lower() == "done":
            print("process terminated.\n")
            break

        if not stats_id:
            print("stat id required.\n")
            continue

        player_id = input("enter player id: ")

        if not player_id:
            print("player id required.\n")
            continue

        player = cursor.execute("""
            SELECT * FROM players
            WHERE player_id = ?
        """, (player_id,)).fetchone()

        if not player:
            print("player not found.\n")
            continue

        match_id = input("enter match id: ")

        if not match_id:
            print("match id required.\n")
            continue

        match = cursor.execute("""
            SELECT * FROM matches
            WHERE match_id = ?
        """, (match_id,)).fetchone()

        if not match:
            print("match not found.\n")
            continue

        try:
            goals = int(input("enter goals: "))
            assists = int(input("enter assissts: "))

        except ValueError:
            print("goals and assists must be number.\n")
            continue

        try:
            cursor.execute("""
                INSERT INTO player_stats (stats_id, player_id, match_id, goals, assists)
                VALUES (?, ?, ?, ?, ?)
            """, (stats_id, player_id, match_id, goals, assists))

            connection.commit()
            print("player stats added successfully.\n")

        except sqlite3.IntegrityError as e:
            print("database contraints violation error:", e)


def view_team():

    teams = cursor.execute("""
        SELECT * FROM teams
    """).fetchall()

    if not teams:
        print("teams not found.\n")

    else:
        for team in teams:
            print(team)


def view_players():

    players = cursor.execute("""
        SELECT * FROM players
    """).fetchall()

    if not players:
        print("players not found.\n")

    else:
        for player in players:
            print(player)


def view_matches():

    matches = cursor.execute("""
        SELECT * FROM matches
    """).fetchall()

    if not matches:
        print("matches not found.\n")

    else:
        for match in matches:
            print(match)


def view_stats():

    stats = cursor.execute("""
        SELECT * FROM player_stats
    """).fetchall()

    if not stats:
        print("stats not found.\n")

    else:
        for stat in stats:
            print(stat)

#====================================================
#REPORTS FUNCTIONS
#====================================================

def total_team():

    teams = cursor.execute("""
        SELECT COUNT(*)
        FROM teams
    """).fetchone()[0]

    print(f"total_teams: {teams}")


def total_players():

    players = cursor.execute("""
        SELECT COUNT(*)
        FROM players
    """).fetchone()[0]

    print(f"total_players: {players}")


def player_stats_report():

    results = cursor.execute("""
        SELECT
            players.player_name,
            teams.team_name,
            player_stats.goals,
            player_stats.assists,
            matches.match_date
            
            FROM player_stats
            
            INNER JOIN players
            ON player_stats.player_id =
               players.player_id
               
            INNER JOIN teams
            ON players.team_id =
               teams.team_id
               
            INNER JOIN matches
            ON player_stats.match_id =
               matches.match_id
    """).fetchall()

    if not results:
        print("no results.\n")

    else:
        print("================== PLAYER STATISTICS ==================")
        for player_name, team_name, goals, assists, match_date in results:
            print(f"Player_Name: {player_name}")
            print(f"Team_Name: {team_name}")
            print(f"Goals: {goals}")
            print(f"Assists: {assists}")
            print(f"Match_Date: {match_date}")
            print("=" * 40, "\n")


def top_scorer():

    top_scorers = cursor.execute("""
        SELECT 
            players.player_name,
        
        SUM(player_stats.goals)
        AS total_goals

        FROM player_stats

        INNER JOIN players
        ON player_stats.player_id =
           players.player_id

        GROUP BY players.player_id

        ORDER BY total_goals DESC
        LIMIT 1 

    """).fetchall()

    if not top_scorers:
        print("no top_scorer found.\n")

    else:
        print(top_scorers)


def top_assists():

    top_assists = cursor.execute("""
        SELECT
            players.player_name,

        SUM(player_stats.assists)
            AS total_assists

        FROM player_stats

        INNER JOIN players
        ON player_stats.player_id =
           players.player_id

        GROUP BY players.player_id
        
        ORDER BY total_assists DESC
        LIMIT 1 
    """).fetchone()

    if not top_assists:
        print("no top_assists found.\n")

    else:
        player_name, top_assists = top_assists

        print(f"Top Assist Provider: {player_name}")
        print(f"Total Assists: {top_assists}")


def player_not_scorers():

    not_scorers = cursor.execute("""
        SELECT 
            players.player_name
        
        FROM player_stats

        INNER JOIN players
        ON player_stats.player_id =
           players.player_id

        WHERE goals = 0
    """).fetchall()

    if not not_scorers:
        print("no not_scorers found.\n")

    else:
        for player_name, in not_scorers:
            print(player_name)


def team_with_most_goals():

    highest_goals = cursor.execute("""
        SELECT
            teams.team_name,

        SUM(player_stats.goals)
        AS total_goals

        FROM teams

        INNER JOIN players
        ON teams.team_id =
            players.team_id

        INNER JOIN player_stats
        ON players.player_id =
            player_stats.player_id

        GROUP BY teams.team_id

        ORDER BY total_goals DESC
        LIMIT 1
    """).fetchone()

    if not highest_goals:
        print("no highest_goals found.\n")

    else:
        team_name, total_goals = highest_goals

        print(f"Team: {team_name}")
        print(f"Goals: {total_goals}\n")


def menu():

    while True:

        print("\n========== FOOTBALL LEAGUE SYSTEM ==========")

        print("1. Add Team")
        print("2. Add Player")
        print("3. Add Match")
        print("4. Add Player Stats")

        print("\n========== VIEWS ==========")

        print("5. View Teams")
        print("6. View Players")
        print("7. View Matches")
        print("8. View Stats")

        print("\n========== REPORTS ==========")

        print("9. Total Teams")
        print("10. Total Players")
        print("11. Player Statistics Report")
        print("12. Top Scorer")
        print("13. Top Assist Provider")
        print("14. Players Without Goals")
        print("15. Team With Most Goals")

        print("\n0. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            add_team()

        elif choice == "2":
            add_player()

        elif choice == "3":
            add_match()

        elif choice == "4":
            add_player_stats()

        elif choice == "5":
            view_team()

        elif choice == "6":
            view_players()

        elif choice == "7":
            view_matches()

        elif choice == "8":
            view_stats()

        elif choice == "9":
            total_team()

        elif choice == "10":
            total_players()

        elif choice == "11":
            player_stats_report()

        elif choice == "12":
            top_scorer()

        elif choice == "13":
            top_assists()

        elif choice == "14":
            player_not_scorers()

        elif choice == "15":
            team_with_most_goals()

        elif choice == "0":

            print("Thank you for using Football League System.\n")
            break

        else:

            print("Invalid Choice.\n")

if __name__ == "__main__":
    menu()