# resources/user.py
from flask_restful import Resource, reqparse
from models import db, User

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        new_user = User(
            username=args['username'],
            email=args['email'],
            password=args['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user.to_dict(), 200

    def put(self, id):
        user = User.query.get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        user.username = args['username']
        user.email = args['email']
        user.password = args['password']
        db.session.commit()
        return user.to_dict(), 200

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
