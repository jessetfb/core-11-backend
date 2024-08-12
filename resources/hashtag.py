# resources/hashtag.py
from flask_restful import Resource, reqparse
from models import db, Hashtag

class HashtagListResource(Resource):
    def get(self):
        hashtags = Hashtag.query.all()
        return [hashtag.to_dict() for hashtag in hashtags], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('description')
        args = parser.parse_args()

        new_hashtag = Hashtag(
            user_id=args['user_id'],
            name=args['name'],
            description=args.get('description')
        )
        db.session.add(new_hashtag)
        db.session.commit()
        return new_hashtag.to_dict(), 201

class HashtagResource(Resource):
    def get(self, id):
        hashtag = Hashtag.query.get_or_404(id)
        return hashtag.to_dict(), 200

    def put(self, id):
        hashtag = Hashtag.query.get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('name')
        parser.add_argument('description')
        args = parser.parse_args()

        if args['user_id'] is not None:
            hashtag.user_id = args['user_id']
        if args['name'] is not None:
            hashtag.name = args['name']
        if args['description'] is not None:
            hashtag.description = args['description']
        db.session.commit()
        return hashtag.to_dict(), 200

    def delete(self, id):
        hashtag = Hashtag.query.get_or_404(id)
        db.session.delete(hashtag)
        db.session.commit()
        return '', 204
