# from flask import Blueprint, render_template, request, jsonify
# from flask_login import current_user 
# import json
# import os

# puntos_bp = Blueprint('puntos', __name__)

# def abrir_usuarios():
#     ruta_usuarios = 'data/usuarios.json'
#     datos_usuarios = None

#     if os.path.exists(ruta_usuarios):
#         with open(ruta_usuarios, 'r', encoding='utf-8') as f:
#             datos_usuarios = json.load(f)

#     return datos_usuarios

# def abrir_equipos():
#     ruta_equipo = 'data/equipos.json'
#     datos_equipo = None

#     if os.path.exists(ruta_equipo):
#         with open(ruta_equipo, 'r', encoding='utf-8') as f:
#             datos_equipo = json.load(f)

#     return datos_equipo

# def escribir_usuarios(datos_usuarios):
#     ruta_usuarios = 'data/usuarios.json'

#     with open(ruta_usuarios, 'w', encoding='utf-8') as f:
#         json.dump(datos_usuarios, f, ensure_ascii=False)

# def escribir_equipos(datos_equipos):
#     ruta_equipos = 'data/equipos.json'

#     with open(ruta_equipos, 'w', encoding='utf-8') as f:
#         json.dump(datos_equipos, f, ensure_ascii=False)

# def contabilizar_puntos(usuario):
#     ruta_equipos = 'data/equipos.json'

#     datos_usuarios = abrir_usuarios()
#     datos_equipos = abrir_equipos()

#     if usuario in datos_usuarios:
#         puntos_actual = datos_usuarios[usuario][2]
#         datos_usuarios[usuario][2] = puntos_actual + 100

#         # Obtener el equipo del usuario
#         equipo = datos_usuarios[usuario][3]

#         # Verificar el equipo y agregar puntos correspondientes
#         if equipo == "CP":  # Chicas Super Poderosas
#             puntos_equipo = int(datos_equipos["Chicas Super Poderosas"])
#             puntos_equipo += 100
#             datos_equipos["Chicas Super Poderosas"] = puntos_equipo
#         elif equipo == "CB":  # Chicos del Barrio
#             puntos_equipo = int(datos_equipos["Chicos del Barrio"])
#             puntos_equipo += 100
#             datos_equipos["Chicos del Barrio"] = puntos_equipo

#         escribir_usuarios(datos_usuarios)
#         escribir_equipos(datos_equipos)

#     else:
#         print("El usuario no se encontró en el archivo JSON.")

# @puntos_bp.route('/ruta-en-tu-servidor-flask', methods=['POST'])
# def manejar_puntos():
#     data = request.json
#     equipos = abrir_equipos()
#     opcion = data.get('opcion')
#     puntos = int (data.get('puntos'))
#     equipoVF = True

#     for equipo in equipos:
#         # Verificar el equipo y agregar puntos correspondientes
#         if opcion == "CP+":
#             equipos['Chicas Super Poderosas'] += puntos
#             equipoVF = False
#             break
#         elif opcion == "CB+":
#             equipos['Chicos del Barrio'] += puntos
#             equipoVF = True
#             break
#         elif opcion == "CP-":
#             equipos['Chicas Super Poderosas'] -= puntos
#             equipoVF = False
#             break
#         elif opcion == "CB-":
#             equipos['Chicos del Barrio'] -= puntos
#             equipoVF = True
#             break

#     escribir_equipos(equipos)
#     if equipoVF == True:
#         print(equipoVF)
#         return jsonify(equipos['Chicos del Barrio'])
#     else:
#         print(equipoVF)
#         return jsonify(equipos['Chicas Super Poderosas'])

# @puntos_bp.route('/tabla_puntos_sumar')
# def tabla_puntos_sumar():
#     return render_template("scorePoints.html")

# @puntos_bp.route('/mostrar_usuarios_admin')
# def mostrar_usuarios_admin():
#     usuarios = abrir_usuarios()
#     rol = current_user.role
#     usuarios_ordenados = dict(sorted(usuarios.items(), key=lambda item: item[1][2], reverse=True))
#     return render_template("scorePoints.html", usuarios=usuarios_ordenados, mostrar_usuarios=True, rol = rol)

# @puntos_bp.route('/mostrar_equipos_admin')
# def mostrar_equipos_admin():
#     rol = current_user.role
#     equipos = abrir_equipos()
#     return render_template("scorePoints.html", mostrar_equipos=True, equipos=equipos, rol = rol)

# def cargar_usuarios():
#     with open('data/usuarios.json', 'r') as file:
#         return json.load(file)

# def guardar_usuarios(usuarios):
#     with open('data/usuarios.json', 'w') as file:
#         json.dump(usuarios, file)

# @puntos_bp.route('/sumar_puntos/<usuario>', methods=['POST'])
# def sumar_puntos(usuario):
#     try:
#         cantidad = int(request.json.get('cantidad', 0))
#         if cantidad < 0:
#             raise ValueError("La cantidad debe ser un número positivo.")

#         usuarios = cargar_usuarios()

#         if usuario in usuarios:
#             contabilizar_puntos_extra(usuarios[usuario][3], cantidad, True)
#             usuarios[usuario][2] += cantidad
#             guardar_usuarios(usuarios)

#             return jsonify({'mensaje': f'Puntos sumados correctamente a {usuario}'})
#         else:
#             return jsonify({'error': f'El usuario {usuario} no existe.'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# @puntos_bp.route('/restar_puntos/<usuario>', methods=['POST'])
# def restar_puntos(usuario):
#     try:
#         cantidad = int(request.json.get('cantidad', 0))
#         if cantidad < 0:
#             raise ValueError("La cantidad debe ser un número positivo.")

#         usuarios = cargar_usuarios()

#         if usuario in usuarios and usuarios[usuario][2] >= cantidad:
#             contabilizar_puntos_extra(usuarios[usuario][3], cantidad, False)
#             usuarios[usuario][2] -= cantidad
#             guardar_usuarios(usuarios)

#             return jsonify({'mensaje': f'Puntos restados correctamente a {usuario}'})
#         else:
#             return jsonify({'error': f'El usuario {usuario} no existe o no tiene suficientes puntos.'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# def contabilizar_puntos_extra(equipo, cantidad, isPlus):
#     datos_usuarios = abrir_usuarios()
#     datos_equipos = abrir_equipos()

#     if equipo in datos_equipos:
#         puntos_equipo = datos_equipos[equipo]
#         if isPlus:
#             puntos_equipo += cantidad
#         else:
#             puntos_equipo -= cantidad
#         datos_equipos[equipo] = puntos_equipo

#     escribir_usuarios(datos_usuarios)
#     escribir_equipos(datos_equipos)