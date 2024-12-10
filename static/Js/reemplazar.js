
document.addEventListener("DOMContentLoaded", function() {
    // Cargar contenido de archivo al cargar la página
    loadContent("inicio");

    // Configurar el botón para actualizar la sección
    document.getElementById("reservasBtn").addEventListener("click", function() {
        //loadContent("reservas");
        window.location.href = "/reservasPage";
    });

    document.getElementById("inicioBtn").addEventListener("click", function() {
        loadContent("inicio");
    });
    document.getElementById("clientesBtn").addEventListener("click", function() {
        loadContent("clientes");
    });
    document.getElementById("habBtn").addEventListener("click", function() {
        loadContent("habitaciones");
    });
});


// Función para cargar el contenido de un archivo en la sección
function loadContent(page) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/load_content/" + page, true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Reemplazar el contenido de la sección con la respuesta
            document.getElementById("contenedor").innerHTML = xhr.responseText;

        } else {
            alert("Hubo un error al cargar el contenido.");
        }
    };
    xhr.send();
}






