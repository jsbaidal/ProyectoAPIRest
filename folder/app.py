import pyodbc
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configuración para JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Establecer la conexión a SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-OC8AB8O\\SQLEXPRESS;DATABASE=testDB;Trusted_Connection=yes;')

# Ruta para autenticar usuarios y generar tokens JWT (POST)
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    # Validación de usuario (ejemplo)
    if username != "test" or password != "test":
        return jsonify({"msg": "Credenciales incorrectas"}), 401

    # Generación del token de acceso
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Ruta para obtener todos los equipos (GET)
@app.route('/equipos', methods=['GET'])
@jwt_required()
def obtener_equipos():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipos")
        rows = cursor.fetchall()

        equipos = [{'id': row[0], 'nombre': row[1], 'liga': row[2]} for row in rows]
        cursor.close()
        return jsonify({'equipos': equipos}), 200

    except Exception as e:
        return jsonify({'mensaje': f"Error al obtener equipos: {e}"}), 500

# Ruta para crear un nuevo equipo (POST)
@app.route('/equipos', methods=['POST'])
@jwt_required()
def crear_equipo():
    try:
        nombre = request.json.get('nombre')
        liga = request.json.get('liga')

        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO equipos (nombre, liga) VALUES (?, ?)", nombre, liga)
        conn.commit()
        cursor.close()

        return jsonify({'mensaje': 'Equipo creado correctamente'}), 201

    except Exception as e:
        return jsonify({'mensaje': f"Error al crear equipo: {e}"}), 500

# Ruta para actualizar un equipo existente por su ID (PUT)
@app.route('/equipos/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_equipo(id):
    try:
        nombre = request.json.get('nombre')
        liga = request.json.get('liga')

        cursor = conn.cursor()
        cursor.execute("UPDATE equipos SET nombre = ?, liga = ? WHERE id = ?", nombre, liga, id)
        conn.commit()
        cursor.close()

        return jsonify({'mensaje': 'Equipo actualizado correctamente'}), 200

    except Exception as e:
        return jsonify({'mensaje': f"Error al actualizar equipo: {e}"}), 500
    
# Ruta para obtener un equipo por su ID (GET)
@app.route('/equipos/<int:id>', methods=['GET'])
@jwt_required()
def obtener_equipo(id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipos WHERE id = ?", id)
        equipo = cursor.fetchone()

        if equipo:
            equipo_dict = {'id': equipo[0], 'nombre': equipo[1], 'liga': equipo[2]}
            cursor.close()
            return jsonify({'equipo': equipo_dict}), 200
        else:
            cursor.close()
            return jsonify({'mensaje': 'Equipo no encontrado'}), 404

    except Exception as e:
        return jsonify({'mensaje': f"Error al obtener equipo: {e}"}), 500

# Ruta de inicio simple

# Ruta para eliminar un equipo por su ID (DELETE)
@app.route('/equipos/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_equipo(id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM equipos WHERE id = ?", id)
        conn.commit()
        cursor.close()

        return jsonify({'mensaje': 'Equipo eliminado correctamente'}), 200

    except Exception as e:
        return jsonify({'mensaje': f"Error al eliminar equipo: {e}"}), 500
    
    
@app.route('/equipos/<int:id>/jugadores', methods=['GET'])
@jwt_required()
def obtener_jugadores_por_equipo(id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jugadores WHERE equipo_id = ?", id)
        rows = cursor.fetchall()

        jugadores = [{'nombre': row[0], 'posicion': row[1]} for row in rows]
        cursor.close()
        return jsonify({'jugadores': jugadores}), 200

    except Exception as e:
        return jsonify({'mensaje': f"Error al obtener jugadores: {e}"}), 500

# Ruta de inicio simple
@app.route('/')
def index():
    return '¡Bienvenido a la API de Equipos de Fútbol!'

# Ejecutar la aplicación si este archivo es ejecutado directamente
if __name__ == "__main__":
    app.run(debug=True)
