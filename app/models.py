"""
Database models for GLH system.
"""

from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Customer or producer account."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # True = producer, False = customer
    is_producer = db.Column(db.Boolean, default=False)

    # Relationships
    loyalty_records = db.relationship("Loyalty", backref="user", lazy=True)
    orders = db.relationship("Order", backref="customer", lazy=True)


class Producer(db.Model):
    """Information about local farmers / growers."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    farming_method = db.Column(db.String(255), nullable=False)

    # One producer can have many products
    products = db.relationship("Product", backref="producer", lazy=True)


class Product(db.Model):
    """Product listing with stock control."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    # Foreign key linking to Producer
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"), nullable=False)


class Order(db.Model):
    """Customer order with scheduling."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(80), default="Pending")


class Loyalty(db.Model):
    """Loyalty rewards system."""
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer, default=0)

    # Each loyalty record belongs to a user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))