from dotenv import load_dotenv
from flask import Flask, request
from db import db, setup_database

import os
# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
database_url = os.getenv('DATABASE_URL')
setup_database(app) 
from routes import main as main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
