from flask import Flask, request, jsonify
from datetime import datetime  # Adicionado

app = Flask(__name__)

pacientes = {}

@app.route('/pacientes', methods=['POST']) 
def cadastrar_paciente():
    data = request.get_json()
    if not data.get('data_nascimento'): 
        return jsonify({'erro': 'data_nascimento é obrigatório'}), 400
        
    paciente_id = len(pacientes) + 1  
    pacientes[paciente_id] = {
        'id': paciente_id,
        'nome': data['nome'],
        'cpf': data['cpf'],
        'data_nascimento': data['data_nascimento'],
        'data_cadastro': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(pacientes[paciente_id]), 201 

@app.route('/pacientes/<int:id>', methods=['GET'])  
def buscar_paciente(id):
    paciente = pacientes.get(id)
    if paciente:
        return jsonify(paciente), 200
    return jsonify({'erro': 'Paciente não encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)