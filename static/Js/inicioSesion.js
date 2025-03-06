document.getElementById('botonLog').addEventListener('click', function(event) {
    const user = document.getElementById('user').value;
    const password = document.getElementById('password').value;

    if (!user || !password) {
        // Muestra el mensaje de error
        const mensajeError = document.getElementById('mensajeError');
        const e400 = document.getElementById('e400');
        mensajeError.style.display = 'block';
        e400.style.display = 'block';

        // Oculta el mensaje después de 3 segundos
        setTimeout(() => {
            mensajeError.style.display = 'none';
            e400.style.display = 'none';
        }, 3000);
        //event.preventDefault(); // Evita el envío del formulario
        //alert('Por favor, completa todos los campos.');
    }
});

document.querySelector('form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Evita que el formulario se envíe de manera tradicional

    const formData = new FormData(event.target);
    const response = await fetch('/inicioSesion', {
        method: 'POST',
        body: formData
    });

    if (response.redirected) {
        // Si el servidor redirigió, navega a la nueva URL
        window.location.href = response.url;
    } else if (response.status === 401) {
        // Muestra el mensaje de error
        const mensajeError = document.getElementById('mensajeError');
        const e401 = document.getElementById('e401');
        mensajeError.style.display = 'block';
        e401.style.display = 'block';

        // Oculta el mensaje después de 3 segundos
        setTimeout(() => {
            mensajeError.style.display = 'none';
            e401.style.display = 'none';
        }, 2500);
    }else {
        // Manejo de otros errores (opcional)
        const result = await response.json();
        console.error("Error:", result.error);
    }
});
