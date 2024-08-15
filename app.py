from flask import Flask, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from json import JSONEncoder
from datetime import datetime
import os
import ssl
import certifi

# Import models and resources
from models import db, User, Message, Hashtag, Core, Follow, Comment, Like
from resources.hashtag_filter import CoreByHashtagResource
from resources.user import UserResource, UserListResource
from resources.message import MessageResource, MessageListResource
from resources.hashtag import HashtagResource, HashtagListResource
from resources.core import CoreResource, CoreListResource, CoreSearchResource, CoreImageSearchResource
from resources.follow import FollowResource, FollowListResource
from resources.comment import CommentResource, CommentListResource
from resources.like import LikeResource, LikeListResource
from resources.save import SaveResource
from resources.flag import FlagResource
from resources.admin import AdminResource

# SSL configuration
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

# Custom JSON Encoder to handle datetime serialization
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Load configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-secret-key")
app.json_encoder = CustomJSONEncoder  # Use the custom JSON encoder

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Setup Flask-RESTful API
api = Api(app)

# Configure JWT
jwt = JWTManager(app)

# Home route
@app.route("/")
def index():
    return "<h1>Core Project</h1>"

# Token creation route
@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email")
    password = request.json.get("password")
    
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad email or password"}), 401

# User registration route
@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 201

# Protected route
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Core retrieval route
@app.route('/cores/<int:id>', methods=['GET'])
def get_core(id):
    core = Core.query.get(id)
    if core is None:
        return jsonify({'error': 'Core not found'}), 404
    return jsonify(core.to_dict())

# Add resources to the API
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(MessageListResource, '/messages')
api.add_resource(MessageResource, '/messages/<int:id>')
api.add_resource(CoreByHashtagResource, '/cores/hashtag/<string:hashtag_name>')
api.add_resource(HashtagListResource, '/hashtags')
api.add_resource(HashtagResource, '/hashtags/<int:id>')
api.add_resource(CoreListResource, '/core')
api.add_resource(CoreResource, '/core/<int:id>')
api.add_resource(CoreSearchResource, '/search')  # Register the search resource
api.add_resource(CoreImageSearchResource, '/search/image')  # Register the image search resource
api.add_resource(FollowListResource, '/follows')
api.add_resource(FollowResource, '/follows/<int:follower_id>/<int:followee_id>')
api.add_resource(CommentListResource, '/comments')
api.add_resource(CommentResource, '/comments/<int:id>')
api.add_resource(LikeListResource, '/likes')
api.add_resource(LikeResource, '/likes/<int:id>')
api.add_resource(SaveResource, '/cores/<int:core_id>/saves')
api.add_resource(FlagResource, '/flags')
api.add_resource(AdminResource, '/admin')  # Register the admin resource


if __name__ == "__main__":
    app.run(debug=True)
