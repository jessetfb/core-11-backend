from flask_restful import Resource
from flask import request
from models import db, Flag
from flask_jwt_extended import jwt_required, get_jwt_identity

class FlagResource(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        user_id = get_jwt_identity()
        core_id = data.get('core_id')
        reason = data.get('reason')

        flag = Flag(user_id=user_id, core_id=core_id, reason=reason)
        db.session.add(flag)
        db.session.commit()
        return flag.to_dict(), 201
