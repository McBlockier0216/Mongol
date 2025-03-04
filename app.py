from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo.mongo_client import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib

app = Flask(__name__)

# URL de acceso a la API MongoDB
uri = "mongodb+srv://alexsony0216:Alex0216@cluster0.dm9sz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Configuración de los parámetros de MongoDB
client = MongoClient(uri)
db = client['hotel']  # Nombre de la base de datos


class User:
    def __init__(self):
        self.coleccion = db['usuarios']

    def obtener_usuario(self, username):
        # Busca un usuario por nombre de usuario
        return self.coleccion.find_one({"user": username})

class Cliente:
    def __init__(self):
        self.coleccion = db['clientes']

    def obtener_todos(self):
        clientes = list(self.coleccion.find())
        for cliente in clientes:
            cliente["_id"] = str(cliente["_id"])
        return clientes

    def crear(self, data):
        print("Registrando cliente")
        return self.coleccion.insert_one(data)

    def actualizar(self, cliente_id, data):
        actualizacion = {
            "nombre": data.get("nombre"),
            "correo": data.get("correo"),
            "telefono": data.get("telefono"),
            "reservas_previas": data.get("reservas_previas", [])
        }
        return self.coleccion.update_one({"_id": cliente_id}, {"$set": actualizacion})

    def eliminar(self, cliente_id):
        return self.coleccion.delete_one({"_id": cliente_id})


class Habitacion:
    def __init__(self):
        self.coleccion = db['habitaciones']

    def obtener_todos(self):
        habitaciones = list(self.coleccion.find())
        for habitacion in habitaciones:
            habitacion["_id"] = str(habitacion["_id"])
            if isinstance(habitacion['numero'], dict) and '$numberInt' in habitacion['numero']:
                habitacion['numero'] = int(habitacion['numero']['$numberInt'])
            if isinstance(habitacion['precio_por_noche'], dict) and '$numberInt' in habitacion['precio_por_noche']:
                habitacion['precio_por_noche'] = int(habitacion['precio_por_noche']['$numberInt'])
        return habitaciones

    def crear(self, data):
        print("Registrando habitacione")
        return self.coleccion.insert_one(data)

    def actualizar(self, habitacion_id, data):
        actualizacion = {
            "numero": {"$numberInt": str(data.get("numero"))},
            "tipo": data.get("tipo"),
            "precio_por_noche": {"$numberInt": str(data.get("precio_por_noche"))},
            "disponibilidad": data.get("disponibilidad", True)
        }
        return self.coleccion.update_one({"_id": habitacion_id}, {"$set": actualizacion})

    def eliminar(self, habitacion_id):
        return self.coleccion.delete_one({"_id": habitacion_id})


class Reserva:
    def __init__(self):
        self.coleccion = db['reservas']

    def obtener_todos(self):
        reservas = list(self.coleccion.find())
        for reserva in reservas:
            reserva["_id"] = str(reserva["_id"])
        return reservas

    def crear(self, data):
        print("Creando reserva")
        return self.coleccion.insert_one(data)

    def actualizar(self, reserva_id, data):
        actualizacion = {
            "cliente_id": data.get("cliente_id"),
            "habitacion_id": data.get("habitacion_id"),
            "fecha_entrada": data.get("fecha_entrada"),
            "fecha_salida": data.get("fecha_salida"),
            "estado": data.get("estado")
        }
        return self.coleccion.update_one({"_id": reserva_id}, {"$set": actualizacion})

    def eliminar(self, reserva_id):
        try:
            return self.coleccion.delete_one({"_id": reserva_id})
        except Exception as e:
            print(f"Error al eliminar la reserva: {e}")
            return type('DeleteResult', (object,), {"deleted_count": 0})()


# Instancias de clases
cliente_crud = Cliente()
habitacion_crud = Habitacion()
reserva_crud = Reserva()
usuarios = User()


# Ruta de inicio
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')


# Rutas CRUD para Clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        clientes = cliente_crud.obtener_todos()
        return render_template('clientes.html', clientes=clientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/crearCliente', methods=['POST'])
def create_cliente():
    try:
        # Obtenemos los datos del formulario
        data = {
            "_id": request.form.get("id"),
            "nombre": request.form.get("nombre"),
            "correo": request.form.get("correo"),
            "telefono": request.form.get("telefono"),
            "reservas_previas": request.form.getlist("reservas_previas")  # Para obtener todas las reservas previas
        }

        # Llamamos al método de creación del cliente
        cliente_crud.crear(data)

        # Redirigimos a la vista de clientes
        return redirect(url_for('get_clientes'))

    except Exception as e:
        # Si ocurre un error, retornamos un mensaje
        return jsonify({"error": str(e)}), 500


@app.route('/clientes/delete/<cliente_id>', methods=['POST'])
def delete_cliente(cliente_id):
    try:
        resultado = cliente_crud.eliminar(cliente_id)
        if resultado.deleted_count > 0:
            return redirect(url_for('get_clientes'))
        else:
            return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/clientes/update/<cliente_id>', methods=['POST'])
def update_cliente(cliente_id):
    try:
        data = {
            "nombre": request.form.get("nombre"),
            "correo": request.form.get("correo"),
            "telefono": request.form.get("telefono"),
            "reservas_previas": request.form.getlist("reservas_previas")
        }
        resultado = cliente_crud.actualizar(cliente_id, data)
        if resultado.modified_count > 0:
            return redirect(url_for('get_clientes'))
        else:
            return jsonify({"error": "No se pudo actualizar el cliente"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rutas CRUD para Habitaciones
@app.route('/habitaciones', methods=['GET'])
def get_habitaciones():
    try:
        habitaciones = habitacion_crud.obtener_todos()
        return render_template('habitaciones.html', habitaciones=habitaciones)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/crearHabitaciones', methods=['POST'])
def create_habitacion():
    try:
        # Usando request.form para obtener los datos del formulario
        data = {
            "_id": request.form.get("id"),
            "numero": request.form.get("numero"),
            "tipo": request.form.get("tipo"),
            "precio_por_noche": request.form.get("precio"),
            "disponibilidad": request.form.get("disponibilidad").lower() == 'true'
            # Asumiendo que el valor es 'true' o 'false' en el input
        }

        habitacion_crud.crear(data)
        return redirect(url_for('get_habitaciones'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/habitaciones/delete/<habitacion_id>', methods=['POST'])
def delete_habitacion(habitacion_id):
    try:
        resultado = habitacion_crud.eliminar(habitacion_id)
        if resultado.deleted_count > 0:
            return redirect(url_for('get_habitaciones'))
        else:
            return jsonify({"error": "Habitación no encontrada"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/habitaciones/update/<habitacion_id>', methods=['POST'])
def update_habitacion(habitacion_id):
    try:
        data = {
            "numero": int(request.form.get("numero")),
            "tipo": request.form.get("tipo"),
            "precio_por_noche": int(request.form.get("precio_por_noche")),
            "disponibilidad": request.form.get("disponibilidad") == "True"
        }
        resultado = habitacion_crud.actualizar(habitacion_id, data)
        if resultado.modified_count > 0:
            return redirect(url_for('get_habitaciones'))
        else:
            return jsonify({"error": "No se pudo actualizar la habitación"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rutas CRUD para Reservas
@app.route('/reservas', methods=['GET'])
def get_reservas():
    try:
        reservas = reserva_crud.obtener_todos()
        return render_template('reservas.html', reservas=reservas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/crearReservas', methods=['POST'])
def create_reserva():
    try:
        data = {
            "_id": request.form.get("id"),
            "cliente_id": request.form.get("cliente_id"),
            "habitacion_id": request.form.get("habitacion_id"),
            "fecha_entrada": request.form.get("fecha_entrada"),
            "fecha_salida": request.form.get("fecha_salida"),
            "estado": request.form.get("estado")
        }
        reserva_crud.crear(data)
        return redirect(url_for('get_reservas'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reservas/delete/<reserva_id>', methods=['POST'])
def delete_reserva(reserva_id):
    try:
        resultado = reserva_crud.eliminar(reserva_id)
        if resultado.deleted_count > 0:
            return redirect(url_for('get_reservas'))
        else:
            return jsonify({"error": "Reserva no encontrada"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/reservas/update/<reserva_id>', methods=['POST'])
def update_reserva(reserva_id):
    try:
        data = {
            "cliente_id": request.form.get("cliente_id"),
            "habitacion_id": request.form.get("habitacion_id"),
            "fecha_entrada": request.form.get("fecha_entrada"),
            "fecha_salida": request.form.get("fecha_salida"),
            "estado": request.form.get("estado")
        }
        resultado = reserva_crud.actualizar(reserva_id, data)
        if resultado.modified_count > 0:
            return redirect(url_for('get_reservas'))
        else:
            return jsonify({"error": "No se pudo actualizar la reserva"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/inicioSesion', methods=['POST'])
def login():
    try:
        # Obtenemos los datos del formulario
        user = request.form.get("user")
        password = request.form.get("password")

        hashed_user = hashlib.sha256(user.encode()).hexdigest()
        hashed_password = generate_password_hash(password)

        print(f"Usuario: {hashed_user},"
              f" Password: {hashed_password}")

        if not user or not password:
            return jsonify({"error": "Usuario y contraseña son requeridos"}), 400

        user_obj = User()
        dataUser = user_obj.obtener_usuario(user)

        if dataUser and dataUser["password"] == password:
            return redirect(url_for('home'))  # Redirigir a la página principal
        else:
            return jsonify({"error": "Usuario o contraseña incorrectos", "showError": True}), 401

    except Exception as e:
        # Si ocurre un error, retornamos un mensaje
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
