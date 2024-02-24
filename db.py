from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize SQLAlchemy and Migrate without the app
db = SQLAlchemy()
migrate = Migrate()

def setup_database(app):
    # Use DATABASE_URL directly if defined in .env or constructed dynamically
    DATABASE_URL = os.getenv('DATABASE_URL')  # This fetches the complete URL
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
