# app.py

from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
DATABASE = 'flight_booking.db'


# User registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Perform data validations

        # Generate password hash
        password_hash = generate_password_hash(password)

        # Store user in the database

        return redirect('/login')
    return render_template('signup.html')


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user from the database based on username

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect('/dashboard')

        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


# User logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


# Add flight
@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        flight_number = request.form['flight_number']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        seat_count = request.form['seat_count']

        # Store flight in the database

        return redirect('/dashboard')
    return render_template('add_flight.html')


# Remove flight
@app.route('/remove_flight/<flight_id>')
def remove_flight(flight_id):
    if 'username' not in session:
        return redirect('/login')

    # Remove flight from the database based on flight_id

    return redirect('/dashboard')


# Flight search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']

        # Fetch flights from the database based on date and time

        return render_template('search_results.html', flights=flights)
    return render_template('search.html')


# Flight details and booking
@app.route('/flight/<flight_id>', methods=['GET', 'POST'])
def flight_details(flight_id):
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        # Perform seat availability check

        if seats_available:
            # Book ticket
            # Update seat count in the database

            return redirect('/my_bookings')
        else:
            return render_template('booking_error.html')

    # Retrieve flight details from the database based on flight_id

    return render_template('flight_details.html', flight=flight)


# User bookings
@app.route('/my_bookings')
def my_bookings():
    if 'username' not in session:
        return redirect('/login')

    # Retrieve user's bookings from the database

    return render_template('my_bookings.html', bookings=bookings)


if __name__ == '__main__':
    app.run(debug=True)
