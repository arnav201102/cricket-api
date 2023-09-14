# routes.py

from flask import Flask, request, jsonify
from app import app, db  # Import the Flask app and the database instance
from models import Users, Match, Team, Player, PlayerStats
import jwt
from functools import wraps
from config import SECRET_KEY  # Import the secret key from your config file

# Define a decorator to check the authorization token
def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401

        try:
            data = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=['HS256'])
            user_id = data['user_id']
            user = Users.query.get(user_id)

            if not user or user.role != 'admin':
                return jsonify({'error': 'Unauthorized'}), 403

        except:
            return jsonify({'error': 'Invalid token'}), 401

        return f(user, *args, **kwargs)

    return decorated

@app.route('/api/admin/signup', methods=['POST'])
def register_admin():
    # Get user data from the request JSON
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Check if the username is already taken
    if username in db:
        return jsonify({"status": "Username already exists. Please choose another.", "status_code": 400}), 400

    # Create a new user entry (you should hash the password in a real application)
    user_id = len(db) + 1
    db[username] = {"user_id": user_id, "username": username, "email": email, "password": password}

    return jsonify({"status": "Admin Account successfully created", "status_code": 200, "user_id": user_id}), 200


@app.route('/api/admin/login', methods=['POST'])
def login_user():
    # Get user data from the request JSON
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists and the password is correct (you should validate against the database)
    if username in db and db[username]["password"] == password:
        # Generate an access token (you should use a proper JWT library in a real application)
        access_token = "your_access_token_here"

        # Return a successful login response with the access token
        response_data = {
            "status": "Login successful",
            "status_code": 200,
            "user_id": db[username]["user_id"],
            "access_token": access_token
        }
        return jsonify(response_data), 200
    else:
        # Return a failure response for incorrect username/password
        response_data = {
            "status": "Incorrect username/password provided. Please retry",
            "status_code": 401
        }
        return jsonify(response_data), 401
    

admin_token = "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

# Endpoint to create a new match
@app.route('/api/matches', methods=['POST'])
@admin_token_required
def create_match():
    # Check if the authorization token is provided and valid
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Bearer '):
        return jsonify({"message": "Unauthorized. Missing or invalid authorization token.", "status_code": 401}), 401

    token = authorization_header.split(' ')[1]
    if token != admin_token:
        return jsonify({"message": "Unauthorized. Invalid authorization token.", "status_code": 401}), 401

    # Get match data from the request JSON
    data = request.json
    team_1 = data.get('team_1')
    team_2 = data.get('team_2')
    date = data.get('date')
    venue = data.get('venue')

    # Create a new match entry (you should use a real database)
    match_id = len(db) + 1
    match = {
        "match_id": match_id,
        "team_1": team_1,
        "team_2": team_2,
        "date": date,
        "venue": venue
    }
    db.append(match)

    return jsonify({"message": "Match created successfully", "match_id": match_id}), 200



# Endpoint to get all match schedules for guest users
@app.route('/api/matches', methods=['GET'])
def get_match_schedules():
    matches = Match.query.all()
    match_list = []

    for match in matches:
        match_info = {
            'match_id': match.id,
            'team_1': match.team_1,
            'team_2': match.team_2,
            'date': match.date.strftime('%Y-%m-%d'),
            'venue': match.venue
        }
        match_list.append(match_info)

    return jsonify({'matches': match_list})


# @app.route('/api/matches', methods=['GET'])
# def get_match_schedules():
#     # Retrieve all match data from the database or list
#     matches = db

#     # Prepare the response JSON
#     response_data = {"matches": matches}

#     return jsonify(response_data), 200

# Endpoint to get match details for guest users
@app.route('/api/matches/<int:match_id>', methods=['GET'])
def get_match_details(match_id):
    match = Match.query.get(match_id)

    if match is None:
        return jsonify({'error': 'Match not found'}), 404

    # Define the match status based on the current date (you may need to implement this logic)
    status = "upcoming"  # Example status

    match_details = {
        'match_id': match.id,
        'team_1': match.team_1,
        'team_2': match.team_2,
        'date': match.date.strftime('%Y-%m-%d'),
        'venue': match.venue,
        'status': status
    }

    return jsonify(match_details)

# Endpoint to add a player to a team's squad
@app.route('/api/teams/<int:team_id>/squad', methods=['POST'])
@admin_token_required
def add_player_to_squad(admin_user, team_id):
    data = request.json
    name = data.get('name')
    role = data.get('role')

    # Check if the team exists
    team = Team.query.get(team_id)

    if team is None:
        return jsonify({'error': 'Team not found'}), 404

    # Create a new player and add them to the team's squad
    player = Player(name=name, role=role, team_id=team.id)

    # Add the player to the database
    db.session.add(player)
    db.session.commit()

    return jsonify({
        'message': 'Player added to squad successfully',
        'player_id': player.id
    }), 200

# Endpoint to get player statistics
@app.route('/api/players/<int:player_id>/stats', methods=['GET'])
# @admin_token_required
def get_player_stats(admin_user, player_id):
    player = Player.query.get(player_id)

    if player is None:
        return jsonify({'error': 'Player not found'}), 404

    # Fetch player statistics from the database (you need to define PlayerStats model)
    player_stats = PlayerStats.query.filter_by(player_id=player.id).first()

    if player_stats is None:
        return jsonify({'error': 'Player statistics not available'}), 404

    player_info = {
        'player_id': player.id,
        'name': player.name,
        'matches_played': player_stats.matches_played,
        'runs': player_stats.runs,
        'average': player_stats.average,
        'strike_rate': player_stats.strike_rate
    }

    return jsonify(player_info)

if __name__ == '__main__':
    app.run(debug=True)
