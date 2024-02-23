from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from babel.dates import format_date
import json
import random

# Crear el blueprint para la gestión de tareas de oración
oracion_bp = Blueprint('oracion', __name__)

# Función para cargar las tareas de oración desde el archivo JSON
def cargar_tareas():
    with open('data/prayers.json', 'r', encoding='utf-8') as json_file:
        tareas = json.load(json_file)
    return tareas

# Ruta para mostrar las tareas activas de oración
@oracion_bp.route('/oracion')
@login_required
def mostrar_tareas_activas():
    tareas = cargar_tareas()
    rol = current_user.role
    user = current_user.id
    return render_template('showActivePrayers.html', tareas=tareas, rol=rol, user=user)

# Ruta para sumar las veces que se ha orado sobre un versículo
@oracion_bp.route('/sumar_oracion', methods=['POST'])
def sumar_veces_oradas():
    # Obtener el índice del elemento que se está sumando
    versiculo = [
    "Mateo 6:6 - 'Pero tú, cuando ores, entra en tu aposento, y cerrada la puerta, ora a tu Padre que está en secreto; y tu Padre que ve en lo secreto te recompensará en público.'",
    "Filipenses 4:6-7 - 'Por nada estéis afanosos; antes bien, en todo, mediante oración y súplica con acción de gracias, sean dadas a conocer vuestras peticiones delante de Dios. Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.'",
    "1 Tesalonicenses 5:16-18 - 'Estad siempre gozosos. Orad sin cesar. Dad gracias en todo, porque esta es la voluntad de Dios para con vosotros en Cristo Jesús.'",
    "Santiago 5:16 - 'Confesaos vuestras ofensas unos a otros y orad unos por otros, para que seáis sanados. La oración eficaz del justo puede mucho.'",
    "Mateo 7:7-8 - 'Pedid, y se os dará; buscad, y hallaréis; llamad, y se os abrirá. Porque todo aquel que pide, recibe; y el que busca, halla; y al que llama, se le abrirá.'",
    "Jeremías 29:12 - 'Entonces me invocaréis, y vendréis y oraréis a mí, y yo os oiré.'",
    "Lucas 11:1-4 - 'Y sucedió que estaba Jesús orando en cierto lugar, y cuando terminó, uno de sus discípulos le dijo: \'Señor, enséñanos a orar, así como Juan enseñó a sus discípulos.'",
    "Efesios 6:18 - 'Orando en todo tiempo con toda oración y súplica en el Espíritu, y velando en ello con toda perseverancia y súplica por todos los santos.'",
    "Colosenses 4:2 - 'Perseverad en la oración, velando en ella con acción de gracias.'",
    "1 Timoteo 2:1-2 - 'Exhorto ante todo, a que se hagan rogativas, oraciones, peticiones y acciones de gracias, por todos los hombres; por los reyes y por todos los que están en eminencia, para que vivamos quieta y reposadamente en toda piedad y honestidad.'",
    "Mateo 21:22 - 'Y todo lo que pidiereis en oración, creyendo, lo recibiréis.'",
    "Marcos 11:24 - 'Por tanto, os digo que todo lo que pidiereis orando, creed que lo recibiréis, y os vendrá.'",
    "Juan 15:7 - 'Si permanecéis en mí, y mis palabras permanecen en vosotros, pedid todo lo que queréis, y os será hecho.'",
    "Romanos 12:12 - 'Gozaos en la esperanza; estad firmes en la tribulación; perseverad en la oración.'",
    "Efesios 3:20 - 'Y a Aquel que es poderoso para hacer todas las cosas mucho más abundantemente de lo que pedimos o entendemos, según el poder que actúa en nosotros.'",
    "1 Juan 5:14 - 'Y esta es la confianza que tenemos en él, que si pedimos alguna cosa conforme a su voluntad, él nos oye.'",
    "Salmos 145:18 - 'Cercano está Jehová a todos los que le invocan, a todos los que le invocan de veras.'",
    "Jeremías 33:3 - 'Clama a mí, y yo te responderé, y te enseñaré cosas grandes y ocultas que tú no conoces.'",
    "Lucas 6:12 - 'En aquellos días él fue al monte a orar, y pasó la noche orando a Dios.'",
    "1 Tesalonicenses 5:17 - 'Orad sin cesar.'",
    "Mateo 26:41 - 'Velad y orad, para que no entréis en tentación; el espíritu a la verdad está dispuesto, pero la carne es débil.'",
    "Lucas 18:1 - 'También les refirió Jesús una parábola sobre la necesidad de orar siempre y no desmayar.'",
    "Colosenses 4:2-3 - 'Perseverad en la oración, velando en ella con acción de gracias; orando también al mismo tiempo por nosotros, para que el Señor nos abra puerta para la palabra, a fin de dar a conocer el misterio de Cristo, por el cual también estoy preso.'",
    "1 Pedro 5:7 - 'Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.'",
    "Hebreos 4:16 - 'Acerquémonos, pues, confiadamente al trono de la gracia, para alcanzar misericordia y hallar gracia para el oportuno socorro.'",
    "Filipenses 4:19 - 'Mi Dios, pues, suplirá todo lo que os falta conforme a sus riquezas en gloria en Cristo Jesús.'",
    "Lucas 11:9 - 'Pedid, y se os dará; buscad, y hallaréis; llamad, y se os abrirá.'",
    "Salmo 17:1 - 'Escucha, oh Jehová, una causa justa; está atento a mi clamor. Presta oído a mi oración, que no procede de labios engañosos.'",
    "Mateo 26:36 - 'Entonces Jesús fue con ellos a un lugar llamado Getsemaní, y dijo a sus discípulos: Sentaos aquí, entre tanto que voy allí y oro.'",
    "1 Reyes 8:28 - 'Mas ahora inclina, oh Jehová Dios mío, tu oído a la oración de tu siervo, y a su súplica; escucha el clamor y la oración que tu siervo hace hoy delante de ti.'",
    "Mateo 18:19-20 - 'Otra vez os digo, que si dos de vosotros se pusieren de acuerdo en la tierra acerca de cualquiera cosa que pidieren, les será hecho por mi Padre que está en los cielos. Porque donde están dos o tres congregados en mi nombre, allí estoy yo en medio de ellos.'",
    "1 Juan 3:22 - 'Y cualquier cosa que pidamos la recibimos de él, porque guardamos sus mandamientos, y hacemos las cosas que son agradables delante de él.'",
    "Lucas 6:28 - 'Bendecid a los que os maldicen, y orad por los que os calumnian.'",
    "Efesios 1:18 - 'Alumbrando los ojos de vuestro entendimiento, para que sepáis cuál es la esperanza a que él os ha llamado, y cuáles las riquezas de la gloria de su herencia en los santos.'",
    "Jeremías 29:7 - 'Y procurad la paz de la ciudad a la cual os hice transportar, y rogad por ella a Jehová; porque en su paz tendréis vosotros paz.'",
    "Mateo 26:42 - 'Otra vez fue, por segunda vez, y oró diciendo: Padre mío, si no puede pasar de mí esta copa sin que yo la beba, hágase tu voluntad.'",
    "1 Timoteo 2:8 - 'Quiero, pues, que los hombres oren en todo lugar, levantando manos santas, sin ira ni contienda.'",
    "Salmo 145:19 - 'Cumplirá el deseo de los que le temen; Oirá asimismo el clamor de ellos, y los salvará.'",
    "Lucas 22:44 - 'Y estando en agonía, oraba más intensamente; y era su sudor como grandes gotas de sangre que caían hasta la tierra.'",
    "Santiago 1:6 - 'Pero pida con fe, no dudando nada; porque el que duda es semejante a la onda del mar, que es arrastrada por el viento y echada de una parte a otra.'",
    "Juan 14:13-14 - 'Y todo lo que pidiereis al Padre en mi nombre, lo haré, para que el Padre sea glorificado en el Hijo. Si algo pidiereis en mi nombre, yo lo haré.'",
    "Mateo 5:44 - 'Pero yo os digo: Amad a vuestros enemigos, bendecid a los que os maldicen, haced bien a los que os aborrecen, y orad por los que os ultrajan y os persiguen.'",
    "Colosenses 1:9 - 'Por lo cual también nosotros, desde el día que lo oímos, no cesamos de orar por vosotros, y de pedir que seáis llenos del conocimiento de su voluntad en toda sabiduría e inteligencia espiritual.'",
    "Efesios 6:18-19 - 'Orando en todo tiempo con toda oración y súplica en el Espíritu, y velando en ello con toda perseverancia y súplica por todos los santos; también por mí, para que me sea dada palabra al abrir mi boca, para dar a conocer con denuedo el misterio del evangelio.'",
    "2 Crónicas 7:14 - 'si se humillare mi pueblo, sobre el cual mi nombre es invocado, y oraren, y buscaren mi rostro, y se convirtieren de sus malos caminos; entonces yo oiré desde los cielos, perdonaré sus pecados y sanaré su tierra.'",
    "Salmo 17:1 - 'Escucha, oh Jehová, una causa justa; está atento a mi clamor. Presta oído a mi oración, que no procede de labios engañosos.'",
    "Mateo 14:23 - 'Despedida la gente, subió al monte a orar aparte; y cuando llegó la noche, estaba allí solo.'",
    "Mateo 26:39 - 'Yendo un poco adelante, se postró sobre su rostro, orando y diciendo: Padre mío, si es posible, pase de mí esta copa; pero no sea como yo quiero, sino como tú quieras.'",
    "1 Samuel 12:23 - 'Lejos esté de mí tal pecado contra Jehová, dejando de orar por vosotros; antes os enseñaré el camino bueno y recto.'",
    "Hechos 6:4 - 'Y nosotros persistiremos en la oración y en el ministerio de la palabra.'"
];
    versiculo = random.choice(versiculo)
    index = int(request.form.get('index')) - 1

    # Leer el JSON desde el archivo
    with open('data/data/prayers.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 0 <= index < len(data):
        # Acceder al elemento en la posición especificada y actualizar el 'total'
        data[index]['total'] += 1

        # Escribir el JSON actualizado de vuelta al archivo
        with open('data/prayers.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        return jsonify({'message': versiculo})
    else:
        return jsonify({'message': 'Índice fuera de rango'}), 400

# Ruta para marcar una tarea como completa
@oracion_bp.route('/marcar_completa', methods=['POST'])
def marcar_completa():
    data = request.get_json()
    index = data.get('index', None)
    testimonio = data.get('testimonio', '')  # Obtener el testimonio ingresado por el usuario

    if index is not None:
        index = int(index) - 1

        with open('data/prayers.json', 'r', encoding='utf-8') as json_file:
            tareas = json.load(json_file)

            if 0 <= index < len(tareas):
                tarea = tareas[index]

                if tarea['isActive'] == 'True':
                    tarea['isActive'] = 'False'
                    tarea['fechaFinal'] = format_date(datetime.now(), format='d-MMMM-y', locale='es_ES')

                    # Agregar el testimonio si se proporciona
                    if testimonio:
                        tarea['testimonio'] = testimonio

        with open('data/prayers.json', 'w', encoding='utf-8') as json_file:
            json.dump(tareas, json_file, indent=2)

        # Devolver las tareas actualizadas en la respuesta
        return jsonify(success=True, tareas_actualizadas=tareas)
    else:
        return jsonify(success=False, error='Índice no proporcionado')


@oracion_bp.route('/agregar_oracion', methods=['POST'])
def agregar_oracion():
    data = request.json
    if data:
        titulo = data.get('titulo', '')
        descripcion = data.get('descripcion', '')
        
        # Obtener el rol del usuario actual (esto dependerá de cómo obtengas el rol en tu aplicación Flask)
        rol = current_user.role

        # Obtener el usuario creador (esto dependerá de cómo obtengas el usuario en tu aplicación Flask)
        creator = current_user.id

        if rol == 'Admin':
            isAdmin = "True"
        else:
            isAdmin = "False"

        nueva_oracion = {
            "titulo": titulo,
            "descripcion": descripcion,
            "fechaInicio": format_date(datetime.now(), format='d-MMMM-y', locale='es_ES'),
            "fechaFinal": "",
            "testimonio": "",
            "total": 1,
            "isActive": "True",
            "isAdmin": isAdmin,
            "creator": creator
        }

        with open('data/prayers.json', 'r+', encoding='utf-8') as json_file:
            tareas = json.load(json_file)
            tareas.append(nueva_oracion)
            json_file.seek(0)
            json.dump(tareas, json_file, indent=4)
            json_file.truncate()

        return jsonify({'success': True, 'message': 'Oración agregada correctamente.'})
    else:
        return jsonify({'success': False, 'message': 'Datos no proporcionados.'}), 400