from flask       import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime    import datetime, timedelta
from dotenv      import load_dotenv
from babel.dates import format_date 
# from app.points.points import contabilizar_puntos
import pytz
import json
import os


load_dotenv()

hora_silenciosa_bp = Blueprint('hora_silenciosa', __name__)

zhl = pytz.timezone('America/Mexico_City')
dias_semana = {
    'Monday'   : 'Lunes', 
    'Tuesday'  : 'Martes', 
    'Wednesday': 'Miércoles', 
    'Thursday' : 'Jueves', 
    'Friday'   : 'Viernes', 
    'Saturday' : 'Sábado', 
    'Sunday'   : 'Domingo'
}

FORMULARIOS_ENVIADOS_JSON = os.getenv('formularios_enviados_json')

@hora_silenciosa_bp.route('/hora_silenciosa', methods=['GET', 'POST'])
@login_required
def hora_silenciosa():

    rol                                        = current_user.role
    usuario                                    = current_user.id
    devocional, fecha_actual, dia, error_message = devocional_del_dia()

    fecha_actual = datetime.now(zhl)
    nombre_dia   = dias_semana[fecha_actual.strftime('%A').capitalize()]

    if request.method == 'POST':
        if usuario_ha_enviado_formulario_hoy(usuario):
            return render_template(os.getenv('formulario_enviado'))  # Mostrar un mensaje de error
        else:
            exp_autor                                           = request.form['exp_autor']
            apl_vida                                            = request.form['apl_vida']
            dudas                                               = request.form['dudas']
            fecha_domingo_anterior, fecha_sabado_siguiente, hoy = obtener_semana_actual()

            # contabilizar_puntos(usuario)  

            semana_actual = f'{fecha_domingo_anterior.day} al {fecha_sabado_siguiente.day} de {format_date(fecha_domingo_anterior, "MMMM", locale="es")}'
            ruta_archivo  = os.path.join('data', f'data/hora_silenciosa_de_{usuario}.json')

            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    datos_usuario = json.load(f)
            else:
                datos_usuario = {
                    'nombre': usuario,
                    'semana': []
                }

            semana_actual_existe = False
            for semana in datos_usuario['semana']:
                if semana['semanaActual'] == semana_actual:
                    semana_actual_existe = True
                    semana['info'].append({
                        'dia'        : nombre_dia,
                        'queExpresa' : exp_autor,
                        'comoaplicar': apl_vida,
                        'pregunta'   : dudas
                    })
                    break

            if not semana_actual_existe:
                datos_usuario['semana'].append({
                    'semanaActual': semana_actual,
                    'info': [{
                        'dia'        : nombre_dia,
                        'queExpresa' : exp_autor,
                        'comoaplicar': apl_vida,
                        'pregunta'   : dudas
                    }]
                })
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_usuario, f, ensure_ascii=False, indent=4)

            # Cierra la sesión del usuario
            if os.path.exists(FORMULARIOS_ENVIADOS_JSON):
                with open(FORMULARIOS_ENVIADOS_JSON, 'r', encoding='utf-8') as f:
                    datos_envio = json.load(f)
            else:
                datos_envio = {}

            fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')
            usuario_datos    = datos_envio.get(usuario, [])
            usuario_datos.append(fecha_actual_str)
            datos_envio[usuario] = usuario_datos

            with open(FORMULARIOS_ENVIADOS_JSON, 'w', encoding='utf-8') as f:
                json.dump(datos_envio, f, ensure_ascii=False, indent=4)

            return render_template(os.getenv('gracias')) 
        
    return render_template(
        os.getenv('hora_silenciosa'),
        rol                = rol, 
        usuario            = usuario, 
        entrada_dia_actual = devocional,
        fecha_actual       = fecha_actual, 
        dia                = dia, 
        error_message      = error_message
    )

def usuario_ha_enviado_formulario_hoy(usuario):
    fecha_actual = datetime.now(zhl)
    if os.path.exists(FORMULARIOS_ENVIADOS_JSON):
        with open(FORMULARIOS_ENVIADOS_JSON, 'r', encoding='utf-8') as f:
            datos_envio = json.load(f)
        usuario_datos    = datos_envio.get(usuario, [])
        fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')
        return fecha_actual_str in usuario_datos
    return False


# def devocional_del_dia():
#     with open(os.getenv('info_hora_silenciosa'), 'r', encoding='utf-8') as archivo_hs:
#         devocionales = json.load(archivo_hs)

#     fecha_actual       = datetime.now(zhl)
#     nombre_dia         = dias_semana[fecha_actual.strftime('%A')]
#     fecha_actual       = fecha_actual.strftime(f'{nombre_dia} %d, %Y').capitalize()
#     entrada_dia_actual = None

#     for devocional in devocionales:
#         if devocional['fecha'] == fecha_actual:
#             entrada_dia_actual = devocional

#     return entrada_dia_actual, fecha_actual, devocional['fecha'], nombre_dia
def devocional_del_dia():
    try:
        with open(os.getenv('info_hora_silenciosa'), 'r', encoding='utf-8') as archivo_hs:
            devocionales = json.load(archivo_hs)

        fecha_actual = datetime.now(zhl)
        nombre_dia = dias_semana[fecha_actual.strftime('%A')]
        fecha_actual_str = fecha_actual.strftime(f'{nombre_dia} %d, %Y').capitalize()
        entrada_dia_actual = None

        for devocional in devocionales:
            if devocional['fecha'] == fecha_actual_str:
                entrada_dia_actual = devocional
                return entrada_dia_actual, fecha_actual_str, devocional['fecha'], nombre_dia

    except FileNotFoundError:
        return None, None, None, "Archivo no encontrado"
    except json.JSONDecodeError:
        return None, None, None, "Error en formato de datos"
    except Exception as e:
        return None, None, None, str(e)

    return None, fecha_actual_str, None, nombre_dia  # Si no se encuentra una entrada para el día actual

def obtener_semana_actual():
    hoy                    = datetime.now(zhl)
    dias_domingo_anterior  = (hoy.weekday() + 1) % 7
    fecha_domingo_anterior = hoy - timedelta(days=dias_domingo_anterior)
    dias_sabado_siguiente  = (5 - hoy.weekday()) % 7
    fecha_sabado_siguiente = hoy + timedelta(days=dias_sabado_siguiente)

    return fecha_domingo_anterior, fecha_sabado_siguiente, hoy


# from flask import Blueprint, render_template, request, jsonify, redirect, url_for
# from flask_login import login_required, current_user
# from datetime import datetime, timedelta
# import pytz
# import json
# import os
# from babel.dates import format_date  # Agregar esta línea

# from app.points.points import contabilizar_puntos

# hora_silenciosa_bp = Blueprint('hora_silenciosa', __name__)

# zhl = pytz.timezone('America/Mexico_City')
# dias_semana = {'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
# FORMULARIOS_ENVIADOS_JSON = 'data/formulariosEnviados.json'

# @hora_silenciosa_bp.route('/hora_silenciosa', methods=['GET', 'POST'])
# @login_required
# def hora_silenciosa():
#     rol = current_user.role
#     usuario = current_user.id
#     devocional, fecha_actual, dia, nombre_dia1 = devocional_del_dia()

#     fecha_actual = datetime.now(zhl)
#     nombre_dia = dias_semana[fecha_actual.strftime('%A').capitalize()]
#     if request.method == 'POST':
#         if usuario_ha_enviado_formulario_hoy(usuario):
#             return render_template('formularioEnviado.html')  # Mostrar un mensaje de error
#         else:
#             exp_autor = request.form['exp_autor']
#             apl_vida = request.form['apl_vida']
#             dudas = request.form['dudas']
#             fecha_domingo_anterior, fecha_sabado_siguiente, hoy = obtener_semana_actual()
#             contabilizar_puntos(usuario)
#             semana_actual = f'{fecha_domingo_anterior.day} al {fecha_sabado_siguiente.day} de {format_date(fecha_domingo_anterior, "MMMM", locale="es")}'
#             ruta_archivo = os.path.join('data', f'data/hora_silenciosa_de_{usuario}.json')
#             if os.path.exists(ruta_archivo):
#                 with open(ruta_archivo, 'r', encoding='utf-8') as f:
#                     datos_usuario = json.load(f)
#             else:
#                 datos_usuario = {
#                     'nombre': usuario,
#                     'semana': []
#                 }

#             semana_actual_existe = False
#             for semana in datos_usuario['semana']:
#                 if semana['semanaActual'] == semana_actual:
#                     semana_actual_existe = True
#                     semana['info'].append({
#                         'dia': nombre_dia,
#                         'queExpresa': exp_autor,
#                         'comoaplicar': apl_vida,
#                         'pregunta': dudas
#                     })
#                     break

#             if not semana_actual_existe:
#                 datos_usuario['semana'].append({
#                     'semanaActual': semana_actual,
#                     'info': [{
#                         'dia': nombre_dia,
#                         'queExpresa': exp_autor,
#                         'comoaplicar': apl_vida,
#                         'pregunta': dudas
#                     }]
#                 })
#             with open(ruta_archivo, 'w', encoding='utf-8') as f:
#                 json.dump(datos_usuario, f, ensure_ascii=False, indent=4)

#             # Cierra la sesión del usuario
#             if os.path.exists(FORMULARIOS_ENVIADOS_JSON):
#                 with open(FORMULARIOS_ENVIADOS_JSON, 'r', encoding='utf-8') as f:
#                     datos_envio = json.load(f)
#             else:
#                 datos_envio = {}

#             fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')
#             usuario_datos = datos_envio.get(usuario, [])
#             usuario_datos.append(fecha_actual_str)
#             datos_envio[usuario] = usuario_datos

#             with open(FORMULARIOS_ENVIADOS_JSON, 'w', encoding='utf-8') as f:
#                 json.dump(datos_envio, f, ensure_ascii=False, indent=4)

#             return render_template('gracias.html')  # Muestra mensaje de agradecimiento
#     # Si el método de la solicitud es GET, muestra el formulario
#     return render_template('silentHour.html', rol=rol, usuario=usuario, entrada_dia_actual=devocional,
#                            fecha_actual=fecha_actual, dia=dia, nombre_dia1=nombre_dia1)


# # Función para verificar si un usuario ya envió el formulario hoy
# def usuario_ha_enviado_formulario_hoy(usuario):
#     fecha_actual = datetime.now(zhl)
#     if os.path.exists(FORMULARIOS_ENVIADOS_JSON):
#         with open(FORMULARIOS_ENVIADOS_JSON, 'r', encoding='utf-8') as f:
#             datos_envio = json.load(f)
#         usuario_datos = datos_envio.get(usuario, [])
#         fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')
#         return fecha_actual_str in usuario_datos
#     return False


# def devocional_del_dia():
#     with open('data/silentHour.json', 'r', encoding='utf-8') as archivo_hs:
#         devocionales = json.load(archivo_hs)

#     fecha_actual = datetime.now(zhl)
#     nombre_dia = dias_semana[fecha_actual.strftime('%A')]
#     fecha_actual = fecha_actual.strftime(f'{nombre_dia} %d, %Y').capitalize()
#     entrada_dia_actual = None
#     for devocional in devocionales:
#         if devocional['fecha'] == fecha_actual:
#             entrada_dia_actual = devocional

#     return entrada_dia_actual, fecha_actual, devocional['fecha'], nombre_dia


# def obtener_semana_actual():
#     hoy = datetime.now(zhl)
#     dias_domingo_anterior = (hoy.weekday() + 1) % 7
#     fecha_domingo_anterior = hoy - timedelta(days=dias_domingo_anterior)
#     dias_sabado_siguiente = (5 - hoy.weekday()) % 7
#     fecha_sabado_siguiente = hoy + timedelta(days=dias_sabado_siguiente)

#     return fecha_domingo_anterior, fecha_sabado_siguiente, hoy
