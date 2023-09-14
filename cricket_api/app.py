# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY,SQLALCHEMY_DATABASE_URI


app = Flask(__name__)

# Configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for JWT token encoding (replace with your actual secret key)
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)

# Import your routes here, but only if the script is run directly
if __name__ == '__main__':
    from routes import *

    # Run the Flask app
    app.run(debug=True)
