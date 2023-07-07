# helpers.py

from models import User, Flight, Booking


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_flight_by_id(flight_id):
    return Flight.query.get(flight_id)


def get_bookings_by_user(username):
    return Booking.query.filter_by(user=username).all()
