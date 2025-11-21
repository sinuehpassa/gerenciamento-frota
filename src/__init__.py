from flask import Flask, app, render_template, redirect, url_for
from .config import ConfigDev, ConfigProd
from .extensions import db, csrf, limiter, security
from .models.models import User, Role, create_default_roles, create_default_users
from flask_security import SQLAlchemyUserDatastore, LoginForm
from flask_security.utils import verify_and_update_password
from src.auth.datastore import user_datastore  
from src.auth import init_app as init_auth
from src.routes.routes import routes_bp

def create_app(config_class=ConfigDev):
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(config_class)

    # inicializa as extensoes do extensions.py
    db.init_app(app)
    csrf.init_app(app)


    # configuração do Flask-Security
    security.init_app(app, user_datastore)

    # registra blueprint de autenticação antes das rotas protegidas
    init_auth(app)
    app.register_blueprint(routes_bp)

    # Cria todas as tabelas do banco de dados automaticamente
    with app.app_context():
        db.create_all()
        create_default_roles()
        create_default_users()

    @app.route("/")
    def index():
        form = LoginForm()
        return render_template('security/login_user.html', login_user_form=form)

    @app.route("/home")
    def home():
        from flask_security import current_user
        if current_user.is_authenticated:
            from src.auth.auth import role_redirect
            return role_redirect()
        return render_template('home.html')

    return app
#          Sins everywhere