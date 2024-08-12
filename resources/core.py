from flask_restful import Resource, reqparse
from models import db, Core
from sqlalchemy import or_
import base64
from image_recognition import extract_features
import numpy as np
from flask import request, abort, url_for
from werkzeug.utils import secure_filename
import os
from werkzeug.exceptions import BadRequest
from mimetypes import guess_type
from flask import jsonify

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class CoreListResource(Resource):
    def get(self):
    # Use query parameters for GET requests
     parser = reqparse.RequestParser()
     parser.add_argument('page', type=int, default=1, help="Page number", location='args')
     parser.add_argument('per_page', type=int, default=10, help="Cores per page", location='args')
     args = parser.parse_args()

     cores = Core.query.paginate(page=args['page'], per_page=args['per_page']).items
     core_dicts = [core.to_dict() for core in cores]
     return core_dicts, 200
 
    def post(self):
        # Expect JSON data in the body for POST requests
        if not request.is_json:
            abort(400, message="Request body must be JSON")

        data = request.form
        hashtag_id = data.get('hashtag_id')
        title = data.get('title')
        description = data.get('description')
        image_url = data.get('image_url')
        link_url = data.get('link_url')
        media_file = request.files.get('media_file')

        if not hashtag_id or not title:
            abort(400, message="Hashtag ID and title are required.")

        try:
            features_binary = None
            media_url = None

            # Handle image URL if provided
            if image_url:
                features = extract_features(image_url)
                features_binary = base64.b64encode(features.tobytes())

            # Handle uploaded media file
            if media_file and allowed_file(media_file.filename):
                filename = secure_filename(media_file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                media_file.save(file_path)

                # Generate URL for the uploaded file
                media_url = url_for('uploaded_file', filename=filename, _external=True)

                mime_type, _ = guess_type(file_path)
                if mime_type and mime_type.startswith('image'):
                    features = extract_features(file_path)
                    features_binary = base64.b64encode(features.tobytes())
                elif mime_type and mime_type.startswith('video'):
                    # Handle video case if needed
                    pass
                else:
                    abort(400, message="Unsupported media type")

            # Create the new Core entry
            new_core = Core(
                hashtag_id=hashtag_id,
                title=title,
                description=description,
                image_url=media_url if media_url else image_url,
                link_url=link_url,
                image_features=features_binary
            )
            db.session.add(new_core)
            db.session.commit()
            return new_core.to_dict(), 201

        except Exception as e:
            abort(400, message=f"Error creating core: {str(e)}")

class CoreResource(Resource):
    def get(self, id):
        core = Core.query.get_or_404(id)
        return core.to_dict(), 200

    def put(self, id):
        core = Core.query.get_or_404(id)
        data = request.json

        hashtag_id = data.get('hashtag_id')
        title = data.get('title')
        description = data.get('description')
        image_url = data.get('image_url')
        link_url = data.get('link_url')
        media_file = request.files.get('media_file')

        try:
            if hashtag_id is not None:
                core.hashtag_id = hashtag_id
            if title is not None:
                core.title = title
            if description is not None:
                core.description = description
            if link_url is not None:
                core.link_url = link_url

            # Handle uploaded media file
            if media_file and allowed_file(media_file.filename):
                filename = secure_filename(media_file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                media_file.save(file_path)

                # Generate URL for the uploaded file
                media_url = url_for('uploaded_file', filename=filename, _external=True)

                mime_type, _ = guess_type(file_path)
                if mime_type and mime_type.startswith('image'):
                    core.image_url = media_url
                    # Update image features if the file is an image
                    features = extract_features(file_path)
                    core.image_features = base64.b64encode(features.tobytes())
                elif mime_type.startswith('video'):
                    core.video_url = media_url  # Assuming a video_url field exists
                else:
                    abort(400, message="Unsupported media type")

            db.session.commit()
        except Exception as e:
            abort(400, message=f"Error updating core: {str(e)}")

        return core.to_dict(), 200

    def delete(self, id):
        core = Core.query.get_or_404(id)
        db.session.delete(core)
        db.session.commit()
        return '', 204


class CoreSearchResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', required=True, help="Search query cannot be blank!")
        parser.add_argument('page', type=int, default=1, help="Page number")
        parser.add_argument('per_page', type=int, default=10, help="Cores per page")
        args = parser.parse_args()

        search_query = args['query']
        results = Core.query.filter(
            or_(
                Core.title.ilike(f'%{search_query}%'),
                Core.description.ilike(f'%{search_query}%')
            )
        ).paginate(page=args['page'], per_page=args['per_page']).items

        return [result.to_dict() for result in results], 200


class CoreImageSearchResource(Resource):
    def post(self):
        data = request.json
        image_url = data.get('image_url')

        if not image_url:
            abort(400, message="Image URL is required.")

        try:
            search_features = extract_features(image_url)
            search_features_binary = base64.b64encode(search_features.tobytes())
        except Exception as e:
            abort(400, message=f"Error extracting features from image: {str(e)}")

        all_cores = Core.query.limit(1000).all()  # Limit the number of cores fetched to avoid performance issues
        matches = []

        for core in all_cores:
            if core.image_features:
                stored_features = np.frombuffer(base64.b64decode(core.image_features), dtype=np.float32)
                similarity = np.dot(stored_features, search_features.flatten()) / (
                            np.linalg.norm(stored_features) * np.linalg.norm(search_features))
                if similarity > 0.9:  # Define a similarity threshold
                    matches.append(core.to_dict())

        return matches, 200
