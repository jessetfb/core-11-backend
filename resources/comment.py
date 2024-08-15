# resources/comment.py
from flask_restful import Resource, reqparse
from models import db, Comment

class CommentListResource(Resource):
    def get(self):
        comments = Comment.query.all()
        return [comment.to_dict() for comment in comments], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('core_id', type=int, required=True)
        parser.add_argument('content', required=True)
        args = parser.parse_args()

        new_comment = Comment(
            user_id=args['user_id'],
            core_id=args['core_id'],
            content=args['content']
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment.to_dict(), 201

class CommentResource(Resource):
    def get(self, id):
        comment = Comment.query.get_or_404(id)
        return comment.to_dict(), 200

    def put(self, id):
        comment = Comment.query.get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('core_id', type=int)
        parser.add_argument('content')
        args = parser.parse_args()

        if args['user_id'] is not None:
            comment.user_id = args['user_id']
        if args['core_id'] is not None:
            comment.core_id = args['core_id']
        if args['content'] is not None:
            comment.content = args['content']
        db.session.commit()
        return comment.to_dict(), 200

    def delete(self, id):
        comment = Comment.query.get_or_404(id)
        db.session.delete(comment)
        db.session.commit()
        return '', 204
