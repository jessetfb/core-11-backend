from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AdminResource(Resource):
    @jwt_required()
    def post(self):
        '''adding a new core'''
        data = request.get_json()
        admin_id= get_jwt_identity() ['id']

        try :
            admin = user.query.get(admin_id)
            if admin.role!= 'admin':
                return jsonify({"message": "You are not an admin"}), 403
            
            new_user = user(username=data['username'], email=data['email'], password=data['password'], role=data['role'])
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict(), 201
        except Exception as e:
            logger.error(f"Error while adding user: {str(e)}")
            return jsonify({"message": "An error occurred while adding the user"}), 500
        

    @jwt_required()
    def delete(self):

            '''deleting a core'''
            user_id = request.args.get('id')
            admin_id = get_jwt_identity() ['id']

            try :
                admin = user.query.get(admin_id)
                if admin.role!= 'admin':
                    return jsonify({"message": "You are not an admin"}), 403
                
                user_to_delete = user.query.get(user_id)
                db.session.delete(user_to_delete)
                db.session.commit()
                return {"message": "User deleted successfully"}, 200
            except Exception as e:
                logger.error(f"Error while deleting user: {str(e)}")
                return jsonify({"message": "An error occurred while deleting the user"}), 500
    @jwt_required()
    def get(self):
        '''getting all cores'''
        admin_id = get_jwt_identity() ['id']

        try :
            admin = user.query.get(admin_id)
            if admin.role!= 'admin':
                return jsonify({"message": "You are not an admin"}), 403
            
            users = user.query.all()
            return [user.to_dict() for user in users]
        except Exception as e:
            logger.error(f"Error while getting users: {str(e)}")
            return jsonify({"message": "An error occurred while getting the users"}), 500
        

