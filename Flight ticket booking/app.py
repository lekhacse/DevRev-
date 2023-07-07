# app.py

from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Flight, Booking
from helpers import get_user_by_username, get_flight_by_id, get_bookings_by_user
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform data validations

        # Generate password hash
        password_hash = generate_password_hash(password)

        # Create new user
        user = User(username=username, password=password_hash)
        user.save()

        return redirect('/login')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect('/dashboard')

        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        flight_number = request.form['flight_number']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        seat_count = request.form['seat_count']

        flight = Flight(flight_number=flight_number, departure_time=departure_time, arrival_time=arrival_time,
                        seat_count=seat_count)
        flight.save()

        return redirect('/dashboard')
    return render_template('add_flight.html')


@app.route('/remove_flight/<flight_id>')
def remove_flight(flight_id):
    if 'username' not in session:
        return redirect('/login')

    flight = get_flight_by_id(flight_id)
    if flight:
        flight.delete()

    return redirect('/dashboard')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']

        flights = Flight.query.filter(Flight.departure_time >= date + ' ' + time).all()

        return render_template('search_results.html', flights=flights)
    return render_template('search.html')


@app.route('/flight/<flight_id>', methods=['GET', 'POST'])
def flight_details(flight_id):
    if 'username' not in session:
        return redirect('/login')

    flight = get_flight_by_id(flight_id)
    if not flight:
        return redirect('/search')

    if request.method == 'POST':
        # Perform seat availability check
        if flight.seat_count > 0:
            # Book ticket
            booking = Booking(user=session['username'], flight_number=flight.flight_number,
                              departure_time=flight.departure_time, arrival_time=flight.arrival_time)
            booking.save()

            # Update seat count
            flight.seat_count -= 1
            flight.save()

            return redirect('/my_bookings')
        else:
            return render_template('booking_error.html')

    return render_template('flight_details.html', flight=flight)


@app.route('/my_bookings')
def my_bookings():
    if 'username' not in session:
        return redirect('/login')

    bookings = get_bookings_by_user(session['username'])

    return render_template('my_bookings.html', bookings=bookings)


if __name__ == '__main__':
    app.run(debug=True)
