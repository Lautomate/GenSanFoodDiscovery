from flask import Blueprint, render_template, request
from app.models.store import Store

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get search query from URL — e.g. /?q=tuna
    search_query = request.args.get('q', '').strip()

    # Get active category from URL — e.g. /?category=cafe
    active_category = request.args.get('category', '').strip()

    # Start with only approved stores
    query = Store.query.filter_by(status='approved')

    # Apply category filter if selected
    if active_category:
        query = query.filter_by(category=active_category)

    # Apply search filter if search query exists
    # ilike means case-insensitive LIKE — works for SQLite and PostgreSQL
    if search_query:
        query = query.filter(Store.name.ilike(f'%{search_query}%'))

    # Sort by highest rated first
    stores = query.order_by(Store.average_rating.desc()).all()

    return render_template('main/index.html',
                           stores=stores,
                           search_query=search_query,
                           active_category=active_category)
