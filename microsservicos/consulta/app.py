from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

consultas = []

@app.route('/consultas', methods=['POST'])
def agendar_consulta():
    
    # Verifica se o conteúdo é JSON
    if not request.is_json:
        return jsonify({"erro": "Content-Type deve ser application/json"}), 415
    
    dados = request.get_json()
    
    
    if not all(key in dados for key in ['id_paciente', 'data_hora', 'especialidade']):
        return jsonify({"erro": "Dados incompletos. Necessário: id_paciente, data_hora, especialidade"}), 400
    
    try:
        # Integração com serviço de Paciente
        id_paciente = dados['id_paciente']
        resposta = requests.get(
            f'http://localhost:5001/pacientes/{id_paciente}',
            timeout=5
        )
        
       
        if resposta.status_code == 404:
            return jsonify({"erro": f"Paciente com ID {id_paciente} não encontrado"}), 404
        elif resposta.status_code != 200:
            return jsonify({"erro": f"Erro ao acessar serviço de pacientes: {resposta.text}"}), 502
        
        paciente = resposta.json()
        
        # Cria consulta
        nova_consulta = {
            "id": len(consultas) + 1,
            "id_paciente": id_paciente,
            "paciente": paciente['nome'],
            "data_hora": dados['data_hora'],
            "especialidade": dados['especialidade'],
            "status": "agendada",
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        consultas.append(nova_consulta)
        
        return jsonify(nova_consulta), 201
    
    except requests.exceptions.ConnectionError:
        return jsonify({"erro": "Não foi possível conectar ao serviço de pacientes"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"erro": "Timeout ao acessar serviço de pacientes"}), 504
    except KeyError as e:
        return jsonify({"erro": f"Campo obrigatório não encontrado: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500

@app.route('/consultas', methods=['GET'])
def listar_consultas():
    """Retorna todas as consultas agendadas"""
    return jsonify(consultas)

@app.route('/consultas/<int:id_consulta>', methods=['GET'])
def obter_consulta(id_consulta):
    """Retorna uma consulta específica por ID"""
    consulta = next((c for c in consultas if c['id'] == id_consulta), None)
    if consulta:
        return jsonify(consulta)
    return jsonify({"erro": f"Consulta com ID {id_consulta} não encontrada"}), 404

@app.route('/consultas/paciente/<int:id_paciente>', methods=['GET'])
def obter_consultas_por_paciente(id_paciente):
    """Retorna todas as consultas de um paciente"""
    consultas_paciente = [c for c in consultas if c['id_paciente'] == id_paciente]
    return jsonify(consultas_paciente)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)