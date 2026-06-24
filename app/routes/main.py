from flask import Blueprint, render_template

# Create the Blueprint
# 'main' is the name we use to reference this blueprint elsewhere
main = Blueprint('main', __name__)

@main.route('/')
def index():
    # For now we just render the home page template
    # Later we'll pass store data from the database here
    return render_template('main/index.html')