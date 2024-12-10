// Obtener los elementos
const openButton = document.getElementById('btnNuevaReserva');
const closeButton = document.getElementById('closeButton');
const overlay = document.getElementById('overlay');

// Mostrar el contenedor cuando se presiona el botón "Abrir"
openButton.addEventListener('click', () => {
    overlay.style.display = 'flex';  // Mostrar el contenedor emergente
});

// Cerrar el contenedor cuando se presiona el botón "Cerrar"
closeButton.addEventListener('click', () => {
    overlay.style.display = 'none';  // Ocultar el contenedor emergente
});

function eliminarReserva(reservaId) {
    fetch(`/reservas/${reservaId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            // Actualizar la lista de reservas o recargar la página
            location.reload();
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

