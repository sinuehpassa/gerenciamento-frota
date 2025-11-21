from flask import Blueprint, jsonify, request
from flask_security import login_required
from flask_security.decorators import current_user, roles_accepted
from src.schemas.schema import SchemaSchema
from src.services.service import ServiceService
from src.extensions import db

controller_bp = Blueprint('carro', __name__, url_prefix='/endpoint')

@controller_bp.route('/list/all/carro', methods=['GET'])
@login_required
@roles_accepted('admin', 'root', 'user')
def listar_carros():
    service = ServiceService(db.session, current_user)
    carro = service.list_all()
    schema = SchemaSchema(many=True)
    return jsonify(schema.dump(carro)), 200

@controller_bp.route('/list/one/carro/<int:id>', methods=['GET'])
@login_required
@roles_accepted('admin', 'root', 'user')
def listar_carro(id):
    service = ServiceService(db.session, current_user)
    carro = service.list_one(id)
    if not carro:
        return jsonify({"message": "Carro not found"}), 404
    schema = SchemaSchema()
    return jsonify(schema.dump(carro)), 200

@controller_bp.route('/create/carro', methods=['POST'])
@login_required
@roles_accepted('admin', 'root')
def criar_carro():
    schema = SchemaSchema()
    data = schema.load(request.get_json())
    service = ServiceService(db.session, current_user)
    carro = service.create(data)
    return jsonify(schema.dump(carro)), 201

@controller_bp.route('/update/carro/<int:id>', methods=['PUT'])
@login_required
@roles_accepted('admin', 'root')
def atualizar_carro(id):
    schema = SchemaSchema()
    data = schema.load(request.get_json())
    service = ServiceService(db.session, current_user)
    carro = service.update(id, data)
    
    if not carro:
        return jsonify({"message": "Carro not found"}), 404
    
    return jsonify(schema.dump(carro)), 200

@controller_bp.route('/delete/carro/<int:id>', methods=['DELETE'])
@login_required
@roles_accepted('admin', 'root')
def deletar_carro(id):
    service = ServiceService(db.session, current_user)
    carro = service.delete(id)
    
    if not carro:
        return jsonify({"message": "Carro not found"}), 404
    
    schema = SchemaSchema()
    return jsonify(schema.dump(carro)), 200