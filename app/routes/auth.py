from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import logout_user, login_required
from werkzeug.security import generate_password_hash
from app import db
from app.forms import RegistrationForm
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
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))