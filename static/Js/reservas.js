// Asegurarse de que el contenido se cargue después de que el DOM esté listo
        document.addEventListener("DOMContentLoaded", function() {
            loadReservas(); // Llama a la función para cargar los datos de la colección 'reservas'
        });

        // Función para cargar los datos de la colección `reservas`
        function loadReservas() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/coleccion/reservas", true);
            xhr.onload = function() {
                if (xhr.status === 500) {
                    var reservas = JSON.parse(xhr.responseText);
                    renderReservasTable(reservas);
                } else {
                    alert("Error al cargar las reservas.");
                }
            };
            xhr.send();
        }

        // Función para mostrar los datos en una tabla
        function renderReservasTable(reservas) {
            console.log(reservas); // Verificar el contenido de reservas
            alert(reservas);

            // Verificar si reservas es un array y tiene elementos
            if (!Array.isArray(reservas) || reservas.length === 0) {
                console.error("No se encontraron datos en la colección de reservas.");
                alert("No se encontraron datos en la colección de reservas.");
                return;
            }

            var contenedor = document.getElementById("contenedorRes");
            if (!contenedor) {
                console.error("No se encontró el contenedor para la tabla de reservas.");
                alert("No se encontró el contenedor para la tabla de reservas.")
                return;
            }

            contenedor.innerHTML = "<h1>HOLA</h1>"; // Limpia el contenido previo

             // Construcción de la tabla manualmente
             var table = document.createElement("table");

             // Cabecera de la tabla
            var thead = document.createElement("thead");
            thead.innerHTML = `
                <tr>
                    <th>ID de Reserva</th>
                    <th>Cliente</th>
                    <th>Habitación</th>
                    <th>Fecha de Entrada</th>
                    <th>Fecha de Salida</th>
                    <th>Estado</th>
                </tr>
            `;
            table.appendChild(thead);

            // Cuerpo de la tabla
            var tbody = document.createElement("tbody");
            reservas.forEach(reserva => {
                var row = document.createElement("tr");

                row.innerHTML = `
                    <td>${reserva._id}</td>
                    <td>${reserva.cliente_id}</td>
                    <td>${reserva.habitacion_id}</td>
                    <td>${reserva.fecha_entrada}</td>
                    <td>${reserva.fecha_salida}</td>
                    <td>${reserva.estado}</td>
                `;

                tbody.appendChild(row);
            });

            table.appendChild(tbody);
            contenedor.appendChild(table); // Inserta la tabla en el contenedor

            //contenedor.appendChild(table);
        }