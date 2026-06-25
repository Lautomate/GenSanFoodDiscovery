from app import db
import uuid
from datetime import datetime

class Store(db.Model):
    __tablename__ = 'stores'

    # Primary key — UUID for security
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key — links this store to the vendor who owns it
    vendor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Basic store information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=True)

    # Store approval status
    # Possible values: 'pending', 'approved', 'rejected'
    status = db.Column(db.String(20), nullable=False, default='pending')

    # Average rating — recalculated every time a review is added, edited, or deleted
    average_rating = db.Column(db.Float, default=0.0)

    # Total number of reviews — stored here so we don't have to count every time
    review_count = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships — lets us do store.reviews or store.vendor in Python
    vendor = db.relationship('User', backref='stores')
    reviews = db.relationship('Review', backref='store', lazy='dynamic', cascade='all, delete-orphan')
    images = db.relationship('StoreImage', backref='store', lazy='dynamic', cascade='all, delete-orphan')
    food_items = db.relationship('FoodItem', backref='store', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Store {self.name}>'