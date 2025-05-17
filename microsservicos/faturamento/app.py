from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

faturas = []

@app.route('/faturas', methods=['POST'])
def gerar_fatura():
    """
    Gera uma nova fatura para uma consulta
    Requer: id_consulta (int), procedimentos (array)
    Exemplo de procedimento: {"codigo": "CON001", "valor": 150.00}
    """
    if not request.is_json:
        return jsonify({"erro": "Content-Type deve ser application/json"}), 415

    dados = request.get_json()
    
    if not dados.get('id_consulta'):
        return jsonify({"erro": "ID da consulta é obrigatório"}), 400

    try:
        
        consulta_url = 'http://localhost:5003/consultas'  
        
        
        resposta_consulta = requests.get(
            f'{consulta_url}/{dados["id_consulta"]}',
            timeout=10
        )

        if resposta_consulta.status_code != 200:
            return jsonify({"erro": "Consulta não encontrada"}), 404

        consulta = resposta_consulta.json()

        # Conexão com Plano de Saúde 
        plano_url = 'http://localhost:5005/validar-procedimento'  
        

        procedimentos_validados = []
        valor_total = 0

        for proc in dados.get('procedimentos', []):
            try:
                resposta_plano = requests.post(
                    plano_url,
                    json={
                        "procedimento": proc['codigo'],
                        "id_paciente": consulta['id_paciente']
                    },
                    timeout=5
                )

                if resposta_plano.status_code == 200:
                    cobertura = resposta_plano.json()
                    valor_coberto = cobertura['valor_coberto'] if cobertura['coberto'] else 0
                else:
                    valor_coberto = 0

            except requests.exceptions.RequestException:
                valor_coberto = 0

            valor_total += valor_coberto
            procedimentos_validados.append({
                "codigo": proc['codigo'],
                "valor": proc['valor'],
                "coberto": valor_coberto > 0,
                "valor_coberto": valor_coberto
            })

        nova_fatura = {
            "id": len(faturas) + 1,
            "id_consulta": dados["id_consulta"],
            "id_paciente": consulta["id_paciente"],
            "paciente": consulta["paciente"],
            "data_consulta": consulta["data_hora"],
            "procedimentos": procedimentos_validados,
            "valor_total": valor_total,
            "status": "pendente",
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        faturas.append(nova_fatura)
        return jsonify(nova_fatura), 201

    except requests.exceptions.RequestException as e:
        return jsonify({"erro": f"Falha na comunicação com outros serviços: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500

@app.route('/faturas', methods=['GET'])
def listar_faturas():
    """Retorna todas as faturas"""
    return jsonify(faturas)

@app.route('/faturas/<int:id_fatura>', methods=['GET'])
def obter_fatura(id_fatura):
    """Retorna uma fatura específica"""
    fatura = next((f for f in faturas if f['id'] == id_fatura), None)
    if fatura:
        return jsonify(fatura)
    return jsonify({"erro": "Fatura não encontrada"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)