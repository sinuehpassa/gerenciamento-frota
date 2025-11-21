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
def list_all_vehicles():
    car_service = CarService(db.session, current_user)
    result = car_service.list_all()
    schema = VehicleSchema(many=True)

    return jsonify({
        "vehicles": schema.dump(result["vehicles"]),
        "counts": result["counts"]
    })