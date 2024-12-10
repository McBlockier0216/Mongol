document.getElementById('botonLog').addEventListener('click', function(event) {
    const user = document.getElementById('user').value;
    const password = document.getElementById('password').value;

    if (!user || !password) {
        event.preventDefault(); // Evita el envío del formulario
        alert('Por favor, completa todos los campos.');
    }
});
