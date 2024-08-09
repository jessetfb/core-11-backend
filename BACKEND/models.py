from sqlalchemy import MetaData, DateTime, func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    is_admin = db.Column(db.Boolean, default=False)

    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient')
    hashtags = db.relationship('Hashtag', back_populates='user')
    follows = db.relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower')
    followed_by = db.relationship('Follow', foreign_keys='Follow.followee_id', back_populates='followee')
    comments = db.relationship('Comment', back_populates='user')
    likes = db.relationship('Like', back_populates='user')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_admin': self.is_admin
        }

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='messages_sent')
    recipient = db.relationship('User', foreign_keys=[recipient_id], back_populates='messages_received')

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read': self.read
        }

class Hashtag(db.Model, SerializerMixin):
    __tablename__ = 'hashtags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    user = db.relationship('User', back_populates='hashtags')
    cores = db.relationship('Core', back_populates='hashtag')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Core(db.Model, SerializerMixin):
    __tablename__ = 'core'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    link_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    image_features = db.Column(db.LargeBinary)  # Store features as binary

    hashtag = db.relationship('Hashtag', back_populates='cores')
    comments = db.relationship('Comment', back_populates='core')
    likes = db.relationship('Like', back_populates='core')

    def to_dict(self):
        return {
            'id': self.id,
            'hashtag_id': self.hashtag_id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'link_url': self.link_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Follow(db.Model, SerializerMixin):
    __tablename__ = 'follows'

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    followee_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='follows')
    followee = db.relationship('User', foreign_keys=[followee_id], back_populates='followed_by')

    def to_dict(self):
        return {
            'follower_id': self.follower_id,
            'followee_id': self.followee_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    core_id = db.Column(db.Integer, db.ForeignKey('core.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    user = db.relationship('User', back_populates='comments')
    core = db.relationship('Core', back_populates='comments')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'core_id': self.core_id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Like(db.Model, SerializerMixin):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    core_id = db.Column(db.Integer, db.ForeignKey('core.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    user = db.relationship('User', back_populates='likes')
    core = db.relationship('Core', back_populates='likes')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'core_id': self.core_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
