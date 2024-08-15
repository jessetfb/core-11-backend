# resources/follow.py
from flask_restful import Resource, reqparse
from models import db, Follow

class FollowListResource(Resource):
    def get(self):
        follows = Follow.query.all()
        return [follow.to_dict() for follow in follows], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('follower_id', type=int, required=True)
        parser.add_argument('followee_id', type=int, required=True)
        args = parser.parse_args()

        new_follow = Follow(
            follower_id=args['follower_id'],
            followee_id=args['followee_id']
        )
        db.session.add(new_follow)
        db.session.commit()
        return new_follow.to_dict(), 201

class FollowResource(Resource):
    def get(self, follower_id, followee_id):
        follow = Follow.query.filter_by(follower_id=follower_id, followee_id=followee_id).first_or_404()
        return follow.to_dict(), 200

    def delete(self, follower_id, followee_id):
        follow = Follow.query.filter_by(follower_id=follower_id, followee_id=followee_id).first_or_404()
        db.session.delete(follow)
        db.session.commit()
        return '', 204
