from app import db
import uuid
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'

    # Primary key — UUID for security
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign keys — a review belongs to both a user and a store
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.String(36), db.ForeignKey('stores.id'), nullable=False)

    # Review content
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship — lets us do review.author to get the user who wrote it
    author = db.relationship('User', backref='reviews')

    # Enforce one review per user per store at the database level
    __table_args__ = (
        db.UniqueConstraint('user_id', 'store_id', name='unique_user_store_review'),
    )

    def __repr__(self):
        return f'<Review {self.id} — {self.rating} stars>'