from flask       import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from dotenv      import load_dotenv
import json
import os

auth_bp       = Blueprint ('auth', __name__)
login_manager = LoginManager()
load_dotenv()
class User(UserMixin):
    def __init__(self, id, role):
        self.id   = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        password       = request.form['contrasena']
        user           = users.get(nombre_usuario)
        if user and password == users_data.get(nombre_usuario, [None])[0]:
            login_user(user)
            return redirect(url_for('auth.inicio'))
    return render_template(os.getenv('login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/inicio', methods=['GET', 'POST'])
@login_required
def inicio():
    rol     = current_user.role
    usuario = current_user.id
    return render_template(os.getenv('index'), rol = rol, usuario = usuario)

with open(os.getenv('route_user'), 'r', encoding='utf-8') as user_file:
    users_data = json.load(user_file)

users = {username: User(username, data[1]) for username, data in users_data.items()}