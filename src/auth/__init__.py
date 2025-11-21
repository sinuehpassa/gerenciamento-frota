from src.auth.datastore import user_datastore
from src.auth.auth import auth_bp, on_user_registered
from flask_security import user_registered

def init_app(app):
    # Registra o blueprint de autenticação
    app.register_blueprint(auth_bp)
    
    # Conecta os signals
    user_registered.connect(on_user_registered, app)
