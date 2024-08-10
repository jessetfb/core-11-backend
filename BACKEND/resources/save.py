from flask_restful import Resource
from flask import request
from models import db, Save
from flask_jwt_extended import jwt_required, get_jwt_identity

class SaveResource(Resource):
    @jwt_required()
    def post(self, core_id):
        user_id = get_jwt_identity()
        save = Save(user_id=user_id, core_id=core_id)
        db.session.add(save)
        db.session.commit()
        return {'message': 'Core saved successfully'}, 201