from flask import Blueprint, render_template, request, redirect, session
from models import User, VaccinationCenter, db

user_routes = Blueprint('user_routes', __name__)
admin_routes = Blueprint('admin_routes', __name__)

# User routes
@user_routes.route('/')
def index():
    return render_template('index.html')

@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic

@user_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    # Signup logic

@user_routes.route('/dashboard')
def dashboard():
    # Dashboard logic

@user_routes.route('/search', methods=['GET', 'POST'])
def search():
    # Search logic

@user_routes.route('/apply', methods=['GET', 'POST'])
def apply():
    # Apply logic

# Admin routes
@admin_routes.route('/admin')
def admin_dashboard():
    # Admin dashboard logic

@admin_routes.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # Admin login logic

@admin_routes.route('/admin/add', methods=['GET', 'POST'])
def add_center():
    # Add center logic

@admin_routes.route('/admin/dosage')
def dosage_details():
    # Dosage details logic

@admin_routes.route('/admin/remove/<center_id>')
def remove_center(center_id):
    # Remove center logic
