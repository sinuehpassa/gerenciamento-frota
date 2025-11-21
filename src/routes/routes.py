from flask import Blueprint, render_template
from flask_security import login_required
from flask_security.decorators import roles_required, current_user, roles_accepted

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/root", methods=['GET'])
@login_required
@roles_required('root')
def home_root():
    return render_template("root_templates/home.html", message="Bem-vindo", username=current_user.username)

@routes_bp.route("/admin", methods=['GET'])
@login_required
@roles_accepted('admin', 'root')
def home_admins():
    return render_template("admin_templates/home.html", message="Bem-vindo", username=current_user.username)

@routes_bp.route("/users", methods=['GET'])
@login_required
@roles_accepted('user', 'admin', 'root')
def home_users():
    return render_template("users_templates/home.html", message="Bem-vindo", username=current_user.username)