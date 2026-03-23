from datetime import datetime
from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(120))
    items_text = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(32), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notifications = db.relationship("Notification", backref="prescription", lazy=True)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey("prescription.id"), nullable=False)
    channel = db.Column(db.String(32), default="sms", nullable=False)
    message = db.Column(db.Text, nullable=False)
    success = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

