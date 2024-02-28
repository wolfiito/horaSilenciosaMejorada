function toggleDescripcion(iconElement) {
    const contenedorPeticion = iconElement.closest('.contenedor-peticion');
    const descripcionElement = contenedorPeticion.querySelector('.descripcion');
    iconElement.classList.toggle('rotar'); // Agregar o quitar la clase 'rotar'
    if (descripcionElement) {
        descripcionElement.classList.toggle('descripcion-visible');
    }
}

function sumarOracion(index) {
    // Realiza una solicitud POST al servidor Flask
    fetch('/sumar_oracion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `index=${index}`,
    })
    .then(response => response.json())
    .then(data => {
        // Maneja la respuesta del servidor, si es necesario
        alert(data.message);
    })
    .catch(error => {
        console.error('Error al enviar la solicitud:', error);
    });
}

function marcarCompleta(index) {
    // Pedir al usuario que ingrese su testimonio
    const testimonio = prompt("Ingresa tu testimonio:");

    if (testimonio !== null) {  // El usuario hizo clic en "Aceptar"
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/marcar_completa', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        actualizarInterfaz(response.tareas_actualizadas);
                    } else {
                        console.error('Error al marcar la tarea como completa');
                    }
                }
            }
        };

        xhr.send(JSON.stringify({ index: index, testimonio: testimonio }));
    }
}

function actualizarInterfaz() {
    // Redirigir a la página principal
    window.location.href = '/oracion';
}

function mostrarTareas(tipo) {
    var tareasActivas = document.getElementById('contenido-tareas-activas');
    var tareasFinalizadas = document.getElementById('contenido-tareas-finalizadas');

    if (tipo === 'activas') {
        tareasActivas.style.display = 'flex';
        tareasFinalizadas.style.display = 'none';
    } else if (tipo === 'finalizadas') {
        tareasActivas.style.display = 'none';
        tareasFinalizadas.style.display = 'flex';
    }
}

document.getElementById('formAgregarTarea').addEventListener('submit', function(event) {
    event.preventDefault();

    const titulo = document.getElementById('titulo').value;
    const descripcion = document.getElementById('descripcion').value;

    // Realizar la solicitud POST para agregar una nueva tarea
    fetch('/agregar_oracion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            titulo: titulo,
            descripcion: descripcion,
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Mostrar mensaje de éxito o error
        if (data.success) {
            // Recargar la página para mostrar la nueva tarea
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error al agregar la tarea:', error);
    });
});

function cerrarModal() {
    var modal = document.getElementById('modalAgregarTarea');
    modal.style.display = 'none';
}

document.getElementById('formCerrarPeticion').addEventListener('submit', function(event) {
    event.preventDefault();

    const testimonio = document.getElementById('testimonio').value;

    // Realizar la solicitud POST para agregar una nueva tarea
    fetch('/marcar_completa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            testimonio: testimonio
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Mostrar mensaje de éxito o error
        if (data.success) {
            // Recargar la página para mostrar la nueva tarea
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error al cerrar la tarea:', error);
    });
});

function cerrarModal() {
    var modal = document.getElementById('modalAgregarTarea');
    modal.style.display = 'none';
}
