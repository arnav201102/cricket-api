# Cricket Match Management API

The Cricket Match Management API is a Flask-based web application designed to manage cricket match data, teams, players, and more. It provides endpoints for registering admin users, managing matches, and retrieving match schedules.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Register Admin](#1-register-admin)
  - [Login User](#2-login-user)
  - [Create Match](#3-create-match)
  - [Get Match Schedules](#4-get-match-schedules)
  - [Add a Team Member to a Squad](#6-add-a-team-member-to-a-squad)
- [Database](#database)
- [Authentication](#authentication)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/workindia.git
   ```

2. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database connection and secret key in `app.py`:

   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'
   app.config['SECRET_KEY'] = 'your_secret_key_here'
   ```

4. Run the application:

   ```bash
   python app.py
   ```

## Usage

### 1. Register Admin

- Endpoint: [POST] `/api/admin/signup`
- Request Data:

   ```json
   {
       "username": "example_user",
       "password": "example_password",
       "email": "user@example.com"
   }
   ```

- Response Data:

   ```json
   {
       "status": "Admin Account successfully created",
       "status_code": 200,
       "user_id": "12345"
   }
   ```

### 2. Login User

- Endpoint: [POST] `/api/admin/login`
- Request Data:

   ```json
   {
       "username": "example_user",
       "password": "example_password"
   }
   ```

- Successful Login Response:

   ```json
   {
       "status": "Login successful",
       "status_code": 200,
       "user_id": "12345",
       "access_token": "your_access_token_here"
   }
   ```

- Failure Response:

   ```json
   {
       "status": "Incorrect username/password provided. Please retry",
       "status_code": 401
   }
   ```

### 3. Create Match

- Endpoint: [POST] `/api/matches`
- Headers:

   ```json
   {
       "Authorization": "Bearer your_access_token_here"
   }
   ```

- Request Data:

   ```json
   {
       "team_1": "India",
       "team_2": "Australia",
       "date": "2023-07-12",
       "venue": "Sydney Cricket Ground"
   }
   ```

- Response Data:

   ```json
   {
       "message": "Match created successfully",
       "match_id": "3"
   }
   ```

### 4. Get Match Schedules

- Endpoint: [GET] `/api/matches`
- Request Data: None
- Response Data:

   ```json
   {
       "matches": [
           {
               "match_id": "1",
               "team_1": "India",
               "team_2": "England",
               "date": "2023-07-10",
               "venue": "Lord's Cricket Ground"
           },
           {
               "match_id": "2",
               "team_1": "Australia",
               "team_2": "New Zealand",
               "date": "2023-07-11",
               "venue": "Melbourne Cricket Ground"
           }
           // Add more matches here
       ]
   }
   ```

### 6. Add a Team Member to a Squad

- Endpoint: [POST] `/api/teams/{team_id}/squad`
- Request Data:

   ```json
   {
       "name": "Rishabh Pant",
       "role": "Wicket-Keeper"
   }
   ```

- Response Data:

   ```json
   {
       "message": "Player added to squad successfully",
       "player_id": "789"
   }
   ```

## Database

The API uses a PostgreSQL database to store user, team, player, match, and player statistics data. You can configure the database connection in the `app.py` file.

## Authentication

Authentication is implemented using JWT (JSON Web Tokens). Admin users receive access tokens upon login, which are required to access admin-only endpoints.

## Contributing

Contributions to the Cricket Match Management API are welcome! You can contribute by opening issues, creating pull requests, or suggesting improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
