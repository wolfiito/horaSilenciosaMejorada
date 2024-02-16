from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import json
from datetime import timedelta

# Crear un blueprint para la autenticación
auth_bp = Blueprint('auth', __name__)

# Configurar Flask-Login
login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        password = request.form['contrasena']

        user = users.get(nombre_usuario)
        if user and password == users_data.get(nombre_usuario, [None])[0]:
            login_user(user)
            return redirect(url_for('auth.inicio'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/inicio', methods=['GET', 'POST'])
@login_required
def inicio():
    rol = current_user.role
    usuario = current_user.id
    return render_template('calendar.html', rol=rol, usuario=usuario)

# Cargar usuarios desde el archivo JSON
with open('data/usuarios.json', 'r', encoding='utf-8') as users_file:
    users_data = json.load(users_file)

# Crear objetos de usuario a partir de los datos cargados
users = {username: User(username, data[1]) for username, data in users_data.items()}
