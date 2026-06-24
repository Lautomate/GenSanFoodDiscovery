import os

class Config:
    # Secret key is used by Flask to securely sign session cookies
    # Without this, users could tamper with their session data
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # This tells SQLAlchemy which database to connect to
    # We use SQLite for development because it requires zero setup
    # It creates a single file called app.db in your project folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'

    # This disables a Flask-SQLAlchemy feature we don't need
    # It saves memory and suppresses a warning message
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # This is the folder where uploaded images will be saved
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')

    # Only these image file types are allowed to be uploaded
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

    # Maximum upload size: 5MB
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024