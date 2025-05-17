from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

prontuarios = []

@app.route('/prontuarios', methods=['POST'])
def novo_prontuario():
    
    if not request.is_json:
        return jsonify({"erro": "Content-Type deve ser application/json"}), 415
        
    dados = request.get_json()
    
    
    id_paciente = dados.get('id_paciente')
    
    if not id_paciente:
        return jsonify({"erro": "ID do paciente é obrigatório"}), 400
    
    try:
       
        resposta = requests.get(
            f'http://localhost:5001/pacientes/{id_paciente}',
            timeout=5
        )
        
        
        if resposta.status_code == 404:
            return jsonify({"erro": "Paciente não encontrado"}), 404
        elif resposta.status_code != 200:
            return jsonify({"erro": "Erro ao acessar serviço de pacientes"}), 502
            
        paciente = resposta.json()
        
        # Criação do prontuário
        novo_prontuario = {
            "id": len(prontuarios) + 1,
            "id_paciente": id_paciente,
            "paciente": paciente["nome"],
            "cpf": paciente["cpf"],
            "data_nascimento": paciente["data_nascimento"],
            "diagnostico": dados.get("diagnostico", ""),
            "tratamento": dados.get("tratamento", ""),
            "observacoes": dados.get("observacoes", ""),
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        prontuarios.append(novo_prontuario)
        return jsonify(novo_prontuario), 201
        
    except requests.exceptions.ConnectionError:
        return jsonify({"erro": "Não foi possível conectar ao serviço de pacientes"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"erro": "Timeout ao acessar serviço de pacientes"}), 504
    except Exception as e:
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500

@app.route('/prontuarios', methods=['GET'])
def listar_prontuarios():
    """Retorna todos os prontuários cadastrados"""
    return jsonify(prontuarios)

@app.route('/prontuarios/<int:id_prontuario>', methods=['GET'])
def obter_prontuario(id_prontuario):
    """Retorna um prontuário específico"""
    prontuario = next((p for p in prontuarios if p['id'] == id_prontuario), None)
    if prontuario:
        return jsonify(prontuario)
    return jsonify({"erro": "Prontuário não encontrado"}), 404

@app.route('/prontuarios/paciente/<int:id_paciente>', methods=['GET'])
def obter_prontuarios_por_paciente(id_paciente):
    """Retorna prontuários de um paciente específico"""
    prontuarios_paciente = [p for p in prontuarios if p['id_paciente'] == id_paciente]
    return jsonify(prontuarios_paciente)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)