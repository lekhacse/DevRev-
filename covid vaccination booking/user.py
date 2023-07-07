from flask import Blueprint, render_template, request, redirect, session
from models import User, db

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@user_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Perform data validations
        # Create a new user and store it in the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('signup.html')

@user_routes.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('dashboard.html', user=user)
    else:
        return redirect('/login')

@user_routes.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        # Perform search logic and retrieve matching vaccination centers
        # Display search results
    return render_template('search.html')

@user_routes.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        center_id = request.form['center']
        user_id = session.get('user_id')
        if user_id:
            # Check if the vaccination center has available slots
            # Apply for a slot
            return redirect('/confirmation')
        else:
            return redirect('/login')
    # Retrieve vaccination centers for the dropdown
    # Display apply form
    return render_template('apply.html')
