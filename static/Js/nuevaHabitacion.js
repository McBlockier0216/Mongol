// Obtener los elementos
const openButton = document.getElementById('nuevaHab');
const closeButton = document.getElementById('closeButton3');
const overlay = document.getElementById('overlay3');

// Mostrar el contenedor cuando se presiona el botón "Abrir"
openButton.addEventListener('click', () => {
    overlay.style.display = 'flex';  // Mostrar el contenedor emergente
});

// Cerrar el contenedor cuando se presiona el botón "Cerrar"
closeButton.addEventListener('click', () => {
    overlay.style.display = 'none';  // Ocultar el contenedor emergente
});