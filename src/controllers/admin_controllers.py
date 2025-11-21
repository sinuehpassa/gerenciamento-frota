from flask import Blueprint, jsonify, request
from flask_security import login_required
from flask_security.decorators import current_user, roles_accepted
from src.schemas.schema import VehicleSchema
from src.services.admin_service import CarService
from src.extensions import db
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/register/vehicle', methods=['POST'])
@login_required
@roles_accepted('admin')
def register_vehicle():
    schema = VehicleSchema()
    try:
        data = schema.load(request.get_json())
        service = CarService(db.session, current_user)
        vehicle = service.register_vehicle(data)
        return jsonify({"message": "Veículo criado com sucesso!"}), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except IntegrityError as err:
        db.session.rollback()
        return jsonify({"error": "Já existe um veículo cadastrado com essa placa."}), 409