from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    # Add more user fields as per your requirements

# Vaccination center model
class VaccinationCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    working_hours = db.Column(db.String(100))
    slots_available = db.Column(db.Integer)
    # Add more center fields as per your requirements
