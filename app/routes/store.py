from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.image import FoodItem
from app.forms import StoreForm, FoodItemForm
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


@store.route('/store/<store_id>/add-food', methods=['GET', 'POST'])
@login_required
def add_food_item(store_id):
    # Get the store or 404
    current_store = Store.query.get_or_404(store_id)

    # Only the vendor who owns this store can add food items
    if current_store.vendor_id != current_user.id:
        flash('You do not have permission to add food items to this store.', 'error')
        return redirect(url_for('main.index'))

    form = FoodItemForm()

    if form.validate_on_submit():
        food_item = FoodItem(
            store_id=current_store.id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category_1=form.category_1.data,
            # Save None if vendor selected empty option
            category_2=form.category_2.data or None,
            category_3=form.category_3.data or None
        )

        db.session.add(food_item)
        db.session.commit()

        flash(f'"{food_item.name}" has been added to your store!', 'success')
        return redirect(url_for('store.store_detail', store_id=current_store.id))

    return render_template('store/add_food_item.html',
                           form=form,
                           store=current_store)