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
