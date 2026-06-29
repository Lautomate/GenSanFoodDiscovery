from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.forms import StoreForm, FoodItemForm, ReviewForm
from app.models.store import Store
from app.models.image import StoreImage, FoodItem
from app.models.review import Review
from app.utils.helpers import save_image

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
        db.session.flush()  # Gets the new store ID before committing

        # Handle image upload if vendor uploaded one
        if form.image.data:
            filename = save_image(form.image.data, 'stores')
            if filename:
                store_image = StoreImage(
                    store_id=new_store.id,
                    filename=filename
                )
                db.session.add(store_image)

        db.session.commit()

        flash('Store created successfully! It is now pending approval.', 'success')
        return redirect(url_for('main.index'))

    return render_template('store/create_store.html', form=form)


@store.route('/store/<store_id>')
def store_detail(store_id):
    current_store = Store.query.get_or_404(store_id)

    # Get the current user's existing review for this store
    user_review = None
    review_form = None

    if current_user.is_authenticated:
        user_review = Review.query.filter_by(
            user_id=current_user.id,
            store_id=store_id
        ).first()

        # Only regular users get the review form
        if not current_user.is_vendor and not current_user.is_admin:
            review_form = ReviewForm()

    return render_template('store/store_detail.html',
                           store=current_store,
                           user_review=user_review,
                           review_form=review_form)


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
        # Handle image upload if vendor uploaded one
        image_filename = None
        if form.image.data:
            image_filename = save_image(form.image.data, 'foods')

        food_item = FoodItem(
            store_id=current_store.id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category_1=form.category_1.data,
            category_2=form.category_2.data or None,
            category_3=form.category_3.data or None,
            image_filename=image_filename
        )       

        db.session.add(food_item)
        db.session.commit()

        flash(f'"{food_item.name}" has been added to your store!', 'success')
        return redirect(url_for('store.store_detail', store_id=current_store.id))

    return render_template('store/add_food_item.html',
                           form=form,
                           store=current_store)