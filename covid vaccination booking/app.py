from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_connection_uri'

db = SQLAlchemy(app)

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

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/signup', methods=['GET', 'POST'])
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

@app.route('/dashboard')
def dashboard():
    # Get user ID from session
    user_id = session.get('user_id')
    if user_id:
        # Retrieve user information from the database
        user = User.query.get(user_id)
        return render_template('dashboard.html', user=user)
    else:
        return redirect('/login')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get search query from the form
        query = request.form['query']
        # Perform search logic and retrieve matching vaccination centers
        centers = VaccinationCenter.query.filter(VaccinationCenter.name.ilike(f'%{query}%')).all()
        return render_template('search.html', centers=centers)
    return render_template('search.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        # Get selected vaccination center and user ID from the form
        center_id = request.form['center']
        user_id = session.get('user_id')
        if user_id:
            # Check if the vaccination center has available slots
            center = VaccinationCenter.query.get(center_id)
            if center.slots_available >= 10:
                # Apply for a slot
                # Implement logic to decrement the available slots and save the application
                # Redirect to a confirmation page or display a success message
                return redirect('/confirmation')
            else:
                return render_template('apply.html', error='No available slots')
        else:
            return redirect('/login')
    # Retrieve vaccination centers for the dropdown
    centers = VaccinationCenter.query.all()
    return render_template('apply.html', centers=centers)

if __name__ == '__main__':
    db.create_all()
    app.run()
