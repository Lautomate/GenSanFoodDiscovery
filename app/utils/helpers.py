import os
import uuid
from flask import current_app

# Allowed file extensions — matches config.py
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    Example: 'photo.jpg' → True
             'virus.exe' → False
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, subfolder):
    """
    Validates, renames, and saves an uploaded image file.

    Parameters:
        file      — the uploaded file object from the form
        subfolder — either 'stores' or 'foods'

    Returns:
        The generated UUID filename (e.g. 'a1b2c3d4.jpg')
        or None if the file is invalid
    """
    if not file or file.filename == '':
        return None

    if not allowed_file(file.filename):
        return None

    # Get the file extension e.g. 'jpg'
    extension = file.filename.rsplit('.', 1)[1].lower()

    # Generate a unique filename using UUID
    # Example: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg'
    unique_filename = f"{str(uuid.uuid4())}.{extension}"

    # Build the full path where the file will be saved
    upload_path = os.path.join(
        current_app.root_path,
        'static', 'uploads', subfolder,
        unique_filename
    )

    # Save the file to disk
    file.save(upload_path)

    return unique_filename


def delete_image(filename, subfolder):
    """
    Deletes an image file from disk.
    Called when a vendor replaces or removes an image.

    Parameters:
        filename  — the UUID filename stored in the database
        subfolder — either 'stores' or 'foods'
    """
    if not filename:
        return

    file_path = os.path.join(
        current_app.root_path,
        'static', 'uploads', subfolder,
        filename
    )

    # Only delete if the file actually exists
    if os.path.exists(file_path):
        os.remove(file_path)