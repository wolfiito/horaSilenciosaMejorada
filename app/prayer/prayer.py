from flask       import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime    import datetime
from babel.dates import format_date
from dotenv      import load_dotenv
import json
import random
import os


oracion_bp = Blueprint('oracion', __name__)
load_dotenv()


def cargar_tareas():
    with open(os.getenv('oraciones'), 'r', encoding='utf-8') as json_file:
        tareas = json.load(json_file)
    return tareas


@oracion_bp.route('/oracion')
@login_required
def mostrar_tareas_activas():
    tareas = cargar_tareas()
    rol    = current_user.role
    user   = current_user.id
    return render_template(
        os.getenv('ver_oraciones_activas'), 
        tareas = tareas, 
        rol    = rol, 
        user   = user)

@oracion_bp.route('/sumar_oracion', methods=['POST'])
def sumar_veces_oradas():
    versiculo = random.choice(os.getenv('versiculo'))
    index     = int(request.form.get('index')) - 1

    with open(os.getenv('oraciones'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 0 <= index < len(data):
        data[index]['total'] += 1
        with open(os.getenv('oraciones'), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return jsonify({'message': versiculo})
    else:
        return jsonify({'message': 'Índice fuera de rango'}), 400

@oracion_bp.route('/marcar_completa', methods=['POST'])
def marcar_completa():
    data       = request.json
    index      = int(data.get('index')) - 1
    testimonio = data.get('testimonio')

    with open(os.getenv('oraciones'), 'r') as file:
        tareas = json.load(file)

    if index is not None and 0 <= index < len(tareas):
        tareas[index]['isActive']   = "False"
        tareas[index]['testimonio'] = testimonio

        with open(os.getenv('oraciones'), 'w') as file:
            json.dump(tareas, file)
        return jsonify({'message': 'Tarea actualizada correctamente'})
    else:
        return jsonify({'error': 'Índice de tarea inválido'})

@oracion_bp.route('/agregar_oracion', methods=['POST'])
def agregar_oracion():
    data = request.json
    if data:
        titulo      = data.get('titulo', '')
        descripcion = data.get('descripcion', '')
        visibilidad =  data.get('visibilidad', '')
        rol         = current_user.role

        creator = current_user.id

        if visibilidad == 'lideres':
            isAdmin = "True"
        elif visibilidad == 'todos':
            isAdmin = "False"

        nueva_oracion = {
            "titulo"     : titulo,
            "descripcion": descripcion,
            "fechaInicio": format_date(datetime.now(), format='d-MMMM-y', locale='es_ES'),
            "fechaFinal" : "",
            "testimonio" : "",
            "total"      : 1,
            "isActive"   : "True",
            "visibility" : isAdmin,
            "creator"    : creator
        }

        with open(os.getenv('oraciones'), 'r+', encoding='utf-8') as json_file:
            tareas = json.load(json_file)
            tareas.append(nueva_oracion)
            json_file.seek(0)
            json.dump(tareas, json_file, indent=4)
            json_file.truncate()

        return jsonify({'success': True, 'message': 'Oración agregada correctamente.'})
    else:
        return jsonify({'success': False, 'message': 'Datos no proporcionados.'}), 400