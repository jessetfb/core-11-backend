# resources/hashtag_filter.py
from flask_restful import Resource
from flask import request
from models import Core, Hashtag

class CoreByHashtagResource(Resource):
    def get(self, hashtag_name):
        hashtag = Hashtag.query.filter_by(name=hashtag_name).first()
        if not hashtag:
            return {"message": "Hashtag not found"}, 404

        cores = Core.query.filter(Core.hashtags.contains(hashtag)).all()
        if not cores:
            return {"message": "No cores found for this hashtag"}, 404

        return [core.to_dict() for core in cores], 200
