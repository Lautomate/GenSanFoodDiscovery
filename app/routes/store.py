from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.forms import StoreForm
from app.models.store import Store

store = Blueprint('store', __name__)

@store.route('/store/create', methods=['GET', 'POST'])
@login_required
def create_store():
    # Only vendors can create stores
    if not current_user.is_vendor:
        flash('You need a vendor account to create a store.', 'error')
        return redirect(url_for('main.index'))

    form = StoreForm()

    if form.validate_on_submit():
        new_store = Store(
            vendor_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            category=form.category.data,
            status='pending'
        )

        db.session.add(new_store)
        db.session.commit()

        flash('Store created successfully! It is now pending approval.', 'success')
        return redirect(url_for('main.index'))

    return render_template('store/create_store.html', form=form)


@store.route('/store/<store_id>')
def store_detail(store_id):
    # Get the store or return 404 if not found
    store = Store.query.get_or_404(store_id)
    return render_template('store/store_detail.html', store=store)