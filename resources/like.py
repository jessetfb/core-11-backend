# resources/like.py
from flask_restful import Resource, reqparse
from models import db, Like

class LikeListResource(Resource):
    def get(self):
        likes = Like.query.all()
        return [like.to_dict() for like in likes], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('core_id', type=int, required=True)
        args = parser.parse_args()

        new_like = Like(
            user_id=args['user_id'],
            core_id=args['core_id']
        )
        db.session.add(new_like)
        db.session.commit()
        return new_like.to_dict(), 201

class LikeResource(Resource):
    def get(self, id):
        like = Like.query.get_or_404(id)
        return like.to_dict(), 200

    def delete(self, id):
        like = Like.query.get_or_404(id)
        db.session.delete(like)
        db.session.commit()
        return '', 204
