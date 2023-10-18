from agenda.db import db
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column


class User(db.Model):
    id = mapped_column(Integer, primary_key=True)
    first_name = db.Column(String(length=50), nullable=False)
    last_name = db.Column(String(length=50), nullable=True)
    email = db.Column(String, unique=True, nullable=False)
    password = db.Column(String, nullable=False)
    contact = db.relationship("Contact", back_populates="user")


class Contact(db.Model):
    """contact object"""

    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(length=50))
    last_name = db.Column(String(length=50))
    phone = db.Column(String(length=15))
    mobile = db.Column(String(length=15))
    email = db.Column(String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship("User", back_populates="contact")