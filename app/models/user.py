from app import db, login_manager
from flask_login import UserMixin
import uuid
from datetime import datetime

# This is the function Flask-Login was asking for
# Every time a page loads, Flask reads the user ID from the session cookie
# and calls this function to get the full user object from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # UUID as primary key instead of auto-increment integer
    # This is more secure because IDs are not guessable
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Basic user information
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Role controls what the user can do
    # Possible values: 'user', 'vendor', 'admin'
    role = db.Column(db.String(20), nullable=False, default='user')

    # Account status — admin can suspend accounts
    is_active = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    # Helper properties to check role easily in templates and routes
    @property
    def is_vendor(self):
        return self.role == 'vendor'

    @property
    def is_admin(self):
        return self.role == 'admin'