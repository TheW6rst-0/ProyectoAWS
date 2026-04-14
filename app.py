from flask import Flask, request, jsonify

app = Flask(__name__)

# Arreglos en memoria
alumnos = []
profesores = []

# --- Funciones Auxiliares de Validación ---
def validar_alumno(data):
    if not data: return False
    campos_requeridos = {"nombres": str, "apellidos": str, "matricula": str, "promedio": (int, float)}
    for campo, tipo in campos_requeridos.items():
        # Validar existencia, nulos, tipo de dato y vacíos
        if campo not in data or data[campo] is None or not isinstance(data[campo], tipo) or data[campo] == "":
            return False
    # El test exige rechazar promedios negativos
    if data['promedio'] < 0:
        return False
    return True

def validar_profesor(data):
    if not data: return False
    # El test de Java envía numeroEmpleado como un número entero (int), no string
    campos_requeridos = {"numeroEmpleado": int, "nombres": str, "apellidos": str, "horasClase": int}
    for campo, tipo in campos_requeridos.items():
        if campo not in data or data[campo] is None or not isinstance(data[campo], tipo) or data[campo] == "":
            return False
    # El test exige rechazar horas negativas
    if data['horasClase'] < 0:
        return False
    return True

def obtener_nuevo_id(coleccion):
    return 1 if not coleccion else max(item['id'] for item in coleccion) + 1

# ================= ENDPOINTS ALUMNOS =================
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    try:
        return jsonify(alumnos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    alumno = next((a for a in alumnos if a['id'] == id), None)
    if alumno:
        return jsonify(alumno), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

@app.route('/alumnos', methods=['POST'])
def create_alumno():
    data = request.get_json()
    if not validar_alumno(data):
        return jsonify({"error": "Datos inválidos o incompletos"}), 400
    
    nuevo_alumno = {
        # Si el test envía un ID, lo respetamos; si no, generamos uno
        "id": data.get('id', obtener_nuevo_id(alumnos)),
        "nombres": data['nombres'],
        "apellidos": data['apellidos'],
        "matricula": data['matricula'],
        "promedio": data['promedio']
    }
    alumnos.append(nuevo_alumno)
    return jsonify(nuevo_alumno), 201

@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    data = request.get_json()
    if not validar_alumno(data):
        return jsonify({"error": "Datos inválidos o incompletos"}), 400
    
    alumno = next((a for a in alumnos if a['id'] == id), None)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    alumno.update({
        "nombres": data['nombres'],
        "apellidos": data['apellidos'],
        "matricula": data['matricula'],
        "promedio": data['promedio']
    })
    return jsonify(alumno), 200

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    global alumnos
    alumno = next((a for a in alumnos if a['id'] == id), None)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    alumnos = [a for a in alumnos if a['id'] != id]
    return jsonify({"mensaje": "Alumno eliminado"}), 200

# ================= ENDPOINTS PROFESORES =================
@app.route('/profesores', methods=['GET'])
def get_profesores():
    return jsonify(profesores), 200

@app.route('/profesores/<int:id>', methods=['GET'])
def get_profesor(id):
    profesor = next((p for p in profesores if p['id'] == id), None)
    if profesor:
        return jsonify(profesor), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

@app.route('/profesores', methods=['POST'])
def create_profesor():
    data = request.get_json()
    if not validar_profesor(data):
        return jsonify({"error": "Datos inválidos o incompletos"}), 400
    
    nuevo_profesor = {
        # Respetamos el ID forzado por el test
        "id": data.get('id', obtener_nuevo_id(profesores)),
        "numeroEmpleado": data['numeroEmpleado'],
        "nombres": data['nombres'],
        "apellidos": data['apellidos'],
        "horasClase": data['horasClase']
    }
    profesores.append(nuevo_profesor)
    return jsonify(nuevo_profesor), 201

@app.route('/profesores/<int:id>', methods=['PUT'])
def update_profesor(id):
    data = request.get_json()
    if not validar_profesor(data):
        return jsonify({"error": "Datos inválidos o incompletos"}), 400
    
    profesor = next((p for p in profesores if p['id'] == id), None)
    if not profesor:
        return jsonify({"error": "Profesor no encontrado"}), 404
    
    profesor.update({
        "numeroEmpleado": data['numeroEmpleado'],
        "nombres": data['nombres'],
        "apellidos": data['apellidos'],
        "horasClase": data['horasClase']
    })
    return jsonify(profesor), 200

@app.route('/profesores/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    global profesores
    profesor = next((p for p in profesores if p['id'] == id), None)
    if not profesor:
        return jsonify({"error": "Profesor no encontrado"}), 404
    profesores = [p for p in profesores if p['id'] != id]
    return jsonify({"mensaje": "Profesor eliminado"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)