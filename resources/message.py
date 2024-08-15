# resources/message.py
from flask_restful import Resource, reqparse
from models import db, Message

class MessageListResource(Resource):
    def get(self):
        messages = Message.query.all()
        return [message.to_dict() for message in messages], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', type=int, required=True)
        parser.add_argument('recipient_id', type=int, required=True)
        parser.add_argument('content', required=True)
        args = parser.parse_args()

        new_message = Message(
            sender_id=args['sender_id'],
            recipient_id=args['recipient_id'],
            content=args['content']
        )
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201

class MessageResource(Resource):
    def get(self, id):
        message = Message.query.get_or_404(id)
        return message.to_dict(), 200

    def put(self, id):
        message = Message.query.get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', type=int)
        parser.add_argument('recipient_id', type=int)
        parser.add_argument('content')
        parser.add_argument('read', type=bool)
        args = parser.parse_args()

        if args['sender_id'] is not None:
            message.sender_id = args['sender_id']
        if args['recipient_id'] is not None:
            message.recipient_id = args['recipient_id']
        if args['content'] is not None:
            message.content = args['content']
        if args['read'] is not None:
            message.read = args['read']
        db.session.commit()
        return message.to_dict(), 200

    def delete(self, id):
        message = Message.query.get_or_404(id)
        db.session.delete(message)
        db.session.commit()
        return '', 204
