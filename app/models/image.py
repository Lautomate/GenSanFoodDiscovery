from app import db
import uuid
from datetime import datetime

class StoreImage(db.Model):
    __tablename__ = 'store_images'

    # Primary key — UUID for security
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key — links this image to a store
    store_id = db.Column(db.String(36), db.ForeignKey('stores.id'), nullable=False)

    # The filename saved on disk inside app/static/uploads/
    filename = db.Column(db.String(255), nullable=False)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StoreImage {self.filename}>'


class FoodItem(db.Model):
    __tablename__ = 'food_items'

    # Primary key — UUID for security
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign key — links this food item to a store
    store_id = db.Column(db.String(36), db.ForeignKey('stores.id'), nullable=False)

    # Food details
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # Category of the food item
    # Examples: Coffee, Breakfast, Lunch, Dinner, Snacks, Desserts, Street Food, Milk Tea
    # Vendors can assign up to three categories per food item
    # This gives justice to foods that belong to multiple categories
    # Example: Sandwich = category_1: breakfast, category_2: snacks, category_3: lunch
    category_1 = db.Column(db.String(50), nullable=False)   # Required — at least one category
    category_2 = db.Column(db.String(50), nullable=True)    # Optional
    category_3 = db.Column(db.String(50), nullable=True)    # Optional

    # The filename saved on disk inside app/static/uploads/
    # nullable=True because vendor may not always upload a photo
    image_filename = db.Column(db.String(255), nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<FoodItem {self.name}>'