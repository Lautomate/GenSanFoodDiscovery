from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# These are extensions we create here but connect to the app later
# This pattern is called the "Application Factory" pattern
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)

    # Load all settings from config.py
    app.config.from_object(Config)

    # Connect extensions to the app
    db.init_app(app)
    login_manager.init_app(app)

    # Tell Flask where to redirect users who are not logged in
    # 'auth.login' means the login route inside the auth blueprint
    login_manager.login_view = 'auth.login'

    # Import models so SQLAlchemy knows about the tables
    from app.models.user import User
    from app.models.store import Store
    from app.models.review import Review
    from app.models.image import StoreImage, FoodItem

    # Register Blueprints (each blueprint is one feature area)
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.store import store

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(store)

    return app