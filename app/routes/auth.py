from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # For now just render the registration page
    # We'll add the form logic after we build the database models
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # For now just render the login page
    # We'll add the form logic after we build the database models
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))