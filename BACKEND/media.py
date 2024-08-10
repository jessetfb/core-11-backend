import os
from werkzeug.utils import secure_filename

def save_media_file(media):
    # Assume you're saving locally; adjust this for your actual storage solution
    filename = secure_filename(media.filename)
    media_path = os.path.join('uploads', filename)  # Ensure this directory exists
    media.save(media_path)
    return f'/uploads/{filename}'
