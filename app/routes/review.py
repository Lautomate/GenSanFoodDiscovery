from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import ReviewForm
from app.models.review import Review
from app.models.store import Store

review = Blueprint('review', __name__)


def recalculate_store_rating(store):
    """
    Recalculates and updates the store's average rating
    and review count based on all existing reviews.

    Called every time a review is created, edited, or deleted.
    """
    reviews = store.reviews.all()
    store.review_count = len(reviews)

    if reviews:
        total = sum(r.rating for r in reviews)
        store.average_rating = round(total / len(reviews), 1)
    else:
        # No reviews left — reset to zero
        store.average_rating = 0.0


@review.route('/store/<store_id>/review/create', methods=['GET', 'POST'])
@login_required
def create_review(store_id):
    current_store = Store.query.get_or_404(store_id)

    # Vendors and admins cannot submit reviews
    if current_user.is_vendor or current_user.is_admin:
        flash('Vendors and admins cannot submit reviews.', 'error')
        return redirect(url_for('store.store_detail', store_id=store_id))

    # Check if user already reviewed this store
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        store_id=store_id
    ).first()

    if existing_review:
        flash('You have already reviewed this store.', 'error')
        return redirect(url_for('store.store_detail', store_id=store_id))

    form = ReviewForm()

    if form.validate_on_submit():
        new_review = Review(
            user_id=current_user.id,
            store_id=store_id,
            # SelectField returns string — convert to integer
            rating=int(form.rating.data),
            review_text=form.review_text.data
        )

        db.session.add(new_review)
        db.session.flush()  # Save review before recalculating

        # Recalculate store rating
        recalculate_store_rating(current_store)

        db.session.commit()

        flash('Your review has been submitted!', 'success')
        return redirect(url_for('store.store_detail', store_id=store_id))

    return render_template('review/review_form.html',
                           form=form,
                           store=current_store,
                           action='create')


@review.route('/store/<store_id>/review/edit', methods=['GET', 'POST'])
@login_required
def edit_review(store_id):
    current_store = Store.query.get_or_404(store_id)

    # Find the user's existing review
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        store_id=store_id
    ).first_or_404()

    form = ReviewForm()

    if form.validate_on_submit():
        existing_review.rating = int(form.rating.data)
        existing_review.review_text = form.review_text.data

        # Recalculate store rating
        recalculate_store_rating(current_store)

        db.session.commit()

        flash('Your review has been updated!', 'success')
        return redirect(url_for('store.store_detail', store_id=store_id))

    # Pre-fill the form with existing review data
    if request.method == 'GET':
        form.rating.data = str(existing_review.rating)
        form.review_text.data = existing_review.review_text

    return render_template('review/review_form.html',
                           form=form,
                           store=current_store,
                           action='edit')


@review.route('/store/<store_id>/review/delete', methods=['POST'])
@login_required
def delete_review(store_id):
    current_store = Store.query.get_or_404(store_id)

    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        store_id=store_id
    ).first_or_404()

    db.session.delete(existing_review)
    db.session.flush()

    # Recalculate store rating after deletion
    recalculate_store_rating(current_store)

    db.session.commit()

    flash('Your review has been deleted.', 'success')
    return redirect(url_for('store.store_detail', store_id=store_id))