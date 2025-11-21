from datetime import datetime
import uuid
from flask_security.utils import hash_password
from flask_security import UserMixin, RoleMixin
from ..extensions import db, Security
from argon2 import PasswordHasher

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    @property
    def is_admin(self):
        return any(role.name == 'admin' for role in self.roles)

    @property
    def is_user(self):
        return any(role.name == 'user' for role in self.roles)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(10), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='disponível')  # disponível, em uso, manutenção
    criado_em = db.Column(db.DateTime(), default=datetime.utcnow)

class VehicleRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # pendente, aprovado, rejeitado
    return_date = db.Column(db.DateTime, nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Novos campos para horários e autorização
    pickup_time = db.Column(db.Time, nullable=True)  # Horário de retirada
    return_time = db.Column(db.Time, nullable=True)  # Horário de devolução
    authorized_by_name = db.Column(db.String(100), nullable=True)  # Nome de quem autorizou
    
    # Campos para quilometragem
    km_inicial = db.Column(db.Integer, nullable=True)
    km_final = db.Column(db.Integer, nullable=True)

    data_request = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    vehicle = db.relationship('Vehicle', foreign_keys=[vehicle_id], backref='vehicle_requests')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_requests', overlaps="requester,requests")
    

class VehicleInspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('vehicle_request.id'), nullable=True)
    inspector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    inspection_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Dados básicos
    current_mileage = db.Column(db.Integer, nullable=False)
    fuel_level = db.Column(db.String(20), nullable=False)  # cheio, 3/4, meio, 1/4, vazio
    
    # Itens de funcionamento
    foot_brake = db.Column(db.String(20), nullable=False)  # funciona, nao_funciona
    foot_brake_obs = db.Column(db.Text, nullable=True)
    parking_brake = db.Column(db.String(20), nullable=False)
    parking_brake_obs = db.Column(db.Text, nullable=True)
    starter_motor = db.Column(db.String(20), nullable=False)
    starter_motor_obs = db.Column(db.Text, nullable=True)
    wiper = db.Column(db.String(20), nullable=False)
    wiper_obs = db.Column(db.Text, nullable=True)
    washer = db.Column(db.String(20), nullable=False)
    washer_obs = db.Column(db.Text, nullable=True)
    toll_transponder = db.Column(db.String(20), nullable=False)
    toll_transponder_obs = db.Column(db.Text, nullable=True)
    headlights = db.Column(db.String(20), nullable=False)
    headlights_obs = db.Column(db.Text, nullable=True)
    front_turn_signals = db.Column(db.String(20), nullable=False)
    front_turn_signals_obs = db.Column(db.Text, nullable=True)
    rear_turn_signals = db.Column(db.String(20), nullable=False)
    rear_turn_signals_obs = db.Column(db.Text, nullable=True)
    brake_lights = db.Column(db.String(20), nullable=False)
    brake_lights_obs = db.Column(db.Text, nullable=True)
    reverse_lights = db.Column(db.String(20), nullable=False)
    reverse_lights_obs = db.Column(db.Text, nullable=True)
    internal_cleanliness = db.Column(db.String(20), nullable=False)
    internal_cleanliness_obs = db.Column(db.Text, nullable=True)
    dashboard_indicators = db.Column(db.String(20), nullable=False)
    dashboard_indicators_obs = db.Column(db.Text, nullable=True)
    radio = db.Column(db.String(20), nullable=False)
    radio_obs = db.Column(db.Text, nullable=True)
    tracker = db.Column(db.String(20), nullable=False)
    tracker_obs = db.Column(db.Text, nullable=True)
    
    # Itens de posse
    warning_triangle = db.Column(db.String(20), nullable=False)  # possui, nao_possui
    jack = db.Column(db.String(20), nullable=False)
    wheel_wrench = db.Column(db.String(20), nullable=False)
    
    # Condições dos pneus
    tire_condition = db.Column(db.String(20), nullable=False)  # bom, ruim, calibrado, descalibrado
    spare_tire = db.Column(db.String(20), nullable=False)
    
    # Condições da carroceria
    windows = db.Column(db.String(20), nullable=False)  # normal, possui_avarias
    doors = db.Column(db.String(20), nullable=False)
    front_bumper = db.Column(db.String(20), nullable=False)
    rear_bumper = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(20), nullable=False)
    mirrors = db.Column(db.String(20), nullable=False)
    
    # Níveis de fluidos
    oil_level = db.Column(db.String(20), nullable=False)  # no_nivel, completar
    brake_fluid = db.Column(db.String(20), nullable=False)
    water_level = db.Column(db.String(20), nullable=False)
    
    # Verificações adicionais
    valid_license = db.Column(db.String(5), nullable=False)  # sim, nao
    preventive_maintenance = db.Column(db.String(5), nullable=False)
    has_leaks = db.Column(db.String(5), nullable=False)
    
    # Campos legados (manter para compatibilidade)
    exterior_condition = db.Column(db.String(20), nullable=True)
    interior_condition = db.Column(db.String(20), nullable=True)
    tire_condition_old = db.Column(db.String(20), nullable=True)
    lights_working = db.Column(db.Boolean, nullable=True)
    brakes_working = db.Column(db.Boolean, nullable=True)
    has_scratches = db.Column(db.Boolean, nullable=True)
    has_dents = db.Column(db.Boolean, nullable=True)
    
    observations = db.Column(db.Text, nullable=True)
    inspection_type = db.Column(db.String(20), nullable=False)  # entrega, devolucao
    
    data_request = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    vehicle = db.relationship('Vehicle', backref='inspections')
    request = db.relationship('VehicleRequest', backref='inspections')
    inspector = db.relationship('User', backref='inspections')
    

def create_default_roles():
    default_roles = ['admin', 'user', 'root']
    for role_name in default_roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()

def create_default_users():
    ph = PasswordHasher()

    default_users = [
        {
            # users
            'username': 'user',
            'email': 'user@mail.com',
            'password': 'userpassword123',
            'active': True,
            'confirmed_at': datetime.utcnow(),
            'fs_uniquifier': str(uuid.uuid4()),
            'roles': ['user']
        },
        {
            # admins
            'username': 'admin',
            'email': 'admin@mail.com',
            'password': 'adminpassword123',
            'active': True,
            'confirmed_at': datetime.utcnow(),
            'fs_uniquifier': str(uuid.uuid4()),
            'roles': ['admin']
        },
        {
            # roots
            'username': 'root',
            'email': 'root@mail.com',
            'password': 'rootpassword123',
            'active': True,
            'confirmed_at': datetime.utcnow(),
            'fs_uniquifier': str(uuid.uuid4()),
            'roles': ['root']
        }
    ]

    create_default_roles()
    for u in default_users:
        existing_user = User.query.filter_by(email=u['email']).first()
        if existing_user:
            continue

        hashed_password = hash_password(u['password'])

        user = User(
            username=u['username'],
            email=u['email'],
            password=hashed_password,
            active=u.get('active', True),
            confirmed_at=u.get('confirmed_at', datetime.utcnow()),
            fs_uniquifier=u.get('fs_uniquifier', str(uuid.uuid4()))
        )

        for role_name in u.get('roles', []):
            role = Role.query.filter_by(name=role_name).first()
            if role:
                user.roles.append(role)

        db.session.add(user)

    db.session.commit()
