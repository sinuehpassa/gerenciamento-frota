from flask import Blueprint, jsonify, request
from flask_security import login_required
from flask_security.decorators import current_user, roles_accepted
from src.schemas.schema import VehicleSchema
from src.services.users_service import CarService
from src.extensions import db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/all/vehicles', methods=['GET'])
@login_required
@roles_accepted('admin', 'user')
def list_all_users():
    car_service = CarService(db.session, current_user)
    cars = car_service.list_all()
    schema = VehicleSchema(many=True)
    
    if not cars:
        return jsonify({"message": "Nenhum veículo encontrado"}), 404
    
    return jsonify(schema.dump(cars))