# models.py

from app import db

# User Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # role = db.Column(db.String(20), nullable=False)  # 'admin' or 'guest'

    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        # self.role = role

# Team Model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    squad = db.relationship('Player', back_populates='team')

    def __init__(self, name):
        self.name = name

# Player Model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team = db.relationship('Team', back_populates='squad')
    stats = db.relationship('PlayerStats',  uselist=False) 
    def __init__(self, name, role, team_id):
        self.name = name
        self.role = role
        self.team_id = team_id

# Match Model
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_1 = db.Column(db.String(80), nullable=False)
    team_2 = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(120), nullable=False)

    def __init__(self, team_1, team_2, date, venue):
        self.team_1 = team_1
        self.team_2 = team_2
        self.date = date
        self.venue = venue

# PlayerStats Model
class PlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', back_populates='stats')
    matches_played = db.Column(db.Integer, nullable=False)
    runs = db.Column(db.Integer, nullable=False)
    average = db.Column(db.Float, nullable=False)
    strike_rate = db.Column(db.Float, nullable=False)

    def __init__(self, player_id, matches_played, runs, average, strike_rate):
        self.player_id = player_id
        self.matches_played = matches_played
        self.runs = runs
        self.average = average
        self.strike_rate = strike_rate
