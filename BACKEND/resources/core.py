from flask_restful import Resource, reqparse
from models import db, Core
from sqlalchemy import or_
import base64
from image_recognition import extract_features

class CoreListResource(Resource):
    def get(self):
        cores = Core.query.all()
        return [core.to_dict() for core in cores], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hashtag_id', type=int, required=True)
        parser.add_argument('title', required=True)
        parser.add_argument('description')
        parser.add_argument('image_url')
        parser.add_argument('link_url')
        args = parser.parse_args()

        if args['image_url']:
            features = extract_features(args['image_url'])
            features_binary = base64.b64encode(features.tobytes())
        else:
            features_binary = None

        new_core = Core(
            hashtag_id=args['hashtag_id'],
            title=args['title'],
            description=args.get('description'),
            image_url=args.get('image_url'),
            link_url=args.get('link_url'),
            image_features=features_binary
        )
        db.session.add(new_core)
        db.session.commit()
        return new_core.to_dict(), 201

class CoreResource(Resource):
    def get(self, id):
        core = Core.query.get_or_404(id)
        return core.to_dict(), 200

    def put(self, id):
        core = Core.query.get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('hashtag_id', type=int)
        parser.add_argument('title')
        parser.add_argument('description')
        parser.add_argument('image_url')
        parser.add_argument('link_url')
        args = parser.parse_args()

        if args['hashtag_id'] is not None:
            core.hashtag_id = args['hashtag_id']
        if args['title'] is not None:
            core.title = args['title']
        if args['description'] is not None:
            core.description = args['description']
        if args['image_url'] is not None:
            core.image_url = args['image_url']
        if args['link_url'] is not None:
            core.link_url = args['link_url']
        db.session.commit()
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
        args = parser.parse_args()

        search_query = args['query']
        results = Core.query.filter(
            or_(
                Core.title.ilike(f'%{search_query}%'),
                Core.description.ilike(f'%{search_query}%')
            )
        ).all()

        return [result.to_dict() for result in results], 200

class CoreImageSearchResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image_url', required=True, help="Image URL cannot be blank!")
        args = parser.parse_args()

        search_features = extract_features(args['image_url'])
        search_features_binary = base64.b64encode(search_features.tobytes())

        all_cores = Core.query.all()
        matches = []

        for core in all_cores:
            if core.image_features:
                stored_features = np.frombuffer(base64.b64decode(core.image_features), dtype=np.float32)
                similarity = np.dot(stored_features, search_features.flatten())
                if similarity > 0.9:  # Define a similarity threshold
                    matches.append(core.to_dict())

        return matches, 200
