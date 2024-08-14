from flask import Flask, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from json import JSONEncoder
from datetime import datetime
from models import db 
import os
from werkzeug.security import generate_password_hash, check_password_hash
from resources.hashtag_filter import CoreByHashtagResource
from models import db, User, Message, Hashtag, Core, Follow, Comment, Like
from resources.user import UserResource, UserListResource
from resources.message import MessageResource, MessageListResource
from resources.hashtag import HashtagResource, HashtagListResource
from resources.core import CoreResource, CoreListResource, CoreSearchResource, CoreImageSearchResource
from resources.follow import FollowResource, FollowListResource
from resources.comment import CommentResource, CommentListResource
from resources.like import LikeResource, LikeListResource
from resources.save import SaveResource
from resources.flag import FlagResource
import ssl
import certifi
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

# Custom JSON Encoder to handle datetime serialization
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json_encoder = CustomJSONEncoder  # Use the custom JSON encoder

CORS(app)

# Initialize the database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Setup the Flask-RESTful API
api = Api(app)

# Configure JWT
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-secret-key")
jwt = JWTManager(app)

@app.route("/")
def index():
    return "<h1>Core Project</h1>"

@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Verify email and password with your database here
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad email or password"}), 401

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Check if the user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Generate a JWT token for the newly registered user
    access_token = create_access_token(identity=email)
    
    return jsonify(access_token=access_token), 201

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

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

if __name__ == "__main__":
    app.run(debug=True)
