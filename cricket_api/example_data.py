# Import necessary modules and classes
from app import db,app

from models import User, Team, Player, Match, PlayerStats

# Create a Flask app context
app.app_context().push()

# Create a new database session
db.create_all()
# app.app_context().push()
# Example data for Users
admin_user = User(username='admin_user', password='admin_password')
guest_user = User(username='guest_user', password='guest_password')

# Add Users to the session and commit
db.session.add(admin_user)
db.session.add(guest_user)
db.session.commit()

# Example data for Teams
india_team = Team(name='India')
australia_team = Team(name='Australia')

# Add Teams to the session and commit
db.session.add(india_team)
db.session.add(australia_team)
db.session.commit()

# Example data for Players
virat_kohli = Player(name='Virat Kohli', role='Batsman', team_id=india_team.id)
steve_smith = Player(name='Steve Smith', role='Batsman', team_id=australia_team.id)

# Add Players to the session and commit
db.session.add(virat_kohli)
db.session.add(steve_smith)
db.session.commit()

# Example data for Matches
match_1 = Match(team_1='India', team_2='Australia', date='2023-07-12', venue='Sydney Cricket Ground')
match_2 = Match(team_1='Australia', team_2='England', date='2023-07-15', venue='Melbourne Cricket Ground')

# Add Matches to the session and commit
db.session.add(match_1)
db.session.add(match_2)
db.session.commit()

# Example data for PlayerStats
stats_kohli = PlayerStats(player_id=virat_kohli.id, matches_played=200, runs=12000, average=59.8, strike_rate=92.5)
stats_smith = PlayerStats(player_id=steve_smith.id, matches_played=180, runs=11000, average=61.1, strike_rate=88.7)

# Add PlayerStats to the session and commit
db.session.add(stats_kohli)
db.session.add(stats_smith)
db.session.commit()

# Close the database session
db.session.close()

print("Data added to the database successfully!")
