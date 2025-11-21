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
    cars = car_service.list_all()
    schema = VehicleSchema(many=True)
    vehicles = schema.dump(cars)

    em_uso = len([v for v in vehicles if v['status'] == 'em uso'])
    disponivel = len([v for v in vehicles if v['status'] == 'disponível'])
    em_manutencao = len([v for v in vehicles if v['status'] == 'em manutenção'])

    return jsonify({
        "em_uso": em_uso,
        "disponivel": disponivel,
        "em_manutencao": em_manutencao,
        "vehicles": vehicles
    })