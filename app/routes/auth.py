from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the password before saving — never store plain text passwords
        hashed_password = generate_password_hash(form.password.data)

        # Create the new user object
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password,
            role=form.role.data
        )

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        # Find the user by email
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))