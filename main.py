from flask import Flask
from flask_login import LoginManager

from app.devocional.devocional import hora_silenciosa_bp
from app.auth.auth import auth_bp, users
from app.calendar.calendar_ import calendar_bp  
from app.prayer.prayer import oracion_bp
from app.points.points import puntos_bp

from datetime import timedelta

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar la clave secreta para la sesión
app.secret_key = 'S0l03nt1D10s'

# Configurar el tiempo de vida de la sesión
app.config['PERMANENT_SESSION_LIFETIME'] = 5  # timedelta(seconds=5)

# Configurar Flask-Login
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

login_manager.login_view = 'auth.login'

# Registrar blueprints en la aplicación
app.register_blueprint(auth_bp)
app.register_blueprint(calendar_bp) 
app.register_blueprint(hora_silenciosa_bp)
app.register_blueprint(oracion_bp)
app.register_blueprint(puntos_bp)

if __name__ == '__main__':
    app.run(debug=True)
