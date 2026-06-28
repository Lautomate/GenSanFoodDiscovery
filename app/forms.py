from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models.user import User

class RegistrationForm(FlaskForm):
    # Username field — required, between 3 and 80 characters
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])

    # Email field — required, must be valid email format
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])

    # Password field — required, minimum 6 characters
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])

    # Confirm password — must match password field
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    # Role selector — user or vendor only
    # Admin accounts are created manually, never through registration
    role = SelectField('Register as', choices=[
        ('user', 'User — I want to discover food'),
        ('vendor', 'Vendor — I want to list my store')
    ])

    submit = SubmitField('Create Account')

    # Custom validators — these run automatically when the form is submitted
    # Flask-WTF looks for methods named validate_<fieldname>
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')
        
class LoginForm(FlaskForm):
    # Email field — required, must be valid email format
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])

    # Password field — required
    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    # Remember me checkbox — keeps user logged in after browser closes
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')


class StoreForm(FlaskForm):
    # Store name — required
    name = StringField('Store Name', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])

    # Store description — optional
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=500)
    ])

    # Store address — optional but recommended
    address = StringField('Address', validators=[
        Optional(),
        Length(max=255)
    ])

    # Store category — required, must pick from the list
    category = SelectField('Category', choices=[
        ('cafe', 'Cafe'),
        ('restaurant', 'Restaurant'),
        ('street_food', 'Street Food'),
        ('fast_food', 'Fast Food'),
        ('bakery', 'Bakery'),
        ('dessert_shop', 'Dessert Shop'),
        ('food_stall', 'Food Stall'),
        ('catering', 'Catering')
    ], validators=[DataRequired()])

    submit = SubmitField('Create Store')

class FoodItemForm(FlaskForm):
    # Food name — required
    name = StringField('Food Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])

    # Short description — optional
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=300)
    ])

    # Price — required
    price = DecimalField('Price (₱)', validators=[
        DataRequired()
    ], places=2)

    # Category 1 — required, at least one category
    category_1 = SelectField('Primary Category', choices=[
        ('coffee', 'Coffee'),
        ('milk_tea', 'Milk Tea'),
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
        ('desserts', 'Desserts'),
        ('street_food', 'Street Food'),
        ('drinks', 'Drinks'),
        ('meals', 'Meals')
    ], validators=[DataRequired()])

    # Category 2 — optional
    category_2 = SelectField('Secondary Category', choices=[
        ('', 'None'),
        ('coffee', 'Coffee'),
        ('milk_tea', 'Milk Tea'),
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
        ('desserts', 'Desserts'),
        ('street_food', 'Street Food'),
        ('drinks', 'Drinks'),
        ('meals', 'Meals')
    ], validators=[Optional()])

    # Category 3 — optional
    category_3 = SelectField('Third Category', choices=[
        ('', 'None'),
        ('coffee', 'Coffee'),
        ('milk_tea', 'Milk Tea'),
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
        ('desserts', 'Desserts'),
        ('street_food', 'Street Food'),
        ('drinks', 'Drinks'),
        ('meals', 'Meals')
    ], validators=[Optional()])

    submit = SubmitField('Add Food Item')