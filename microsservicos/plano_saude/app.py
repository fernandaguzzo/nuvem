from flask import Flask, request, jsonify

app = Flask(__name__)


planos = {
    1: {"nome": "Plano1", "cobertura": ["CON001", "CON002", "EXA001"]},
    2: {"nome": "Plano2","cobertura": ["CON001"]},
    3: {"nome": "Plano3","cobertura": []}
}


valores_procedimentos = {
    "CON001": 7.00,  
    "CON002": 50.00,  
    "EXA001": 3.00   
}

@app.route('/validar-procedimento', methods=['POST'])
def validar_procedimento():
    """
    Valida se um procedimento é coberto pelo plano do paciente
    Retorna se é coberto e o valor coberto (pode ser parcial)
    """
    dados = request.json
    codigo_procedimento = dados['procedimento']
    id_paciente = dados['id_paciente']
    
   
    id_plano = 1 if id_paciente % 2 == 1 else 2
    
    plano = planos[id_plano]
    coberto = codigo_procedimento in plano['cobertura']
    
    
    valor_coberto = valores_procedimentos.get(codigo_procedimento, 0) * (0.8 if id_plano == 2 else 1) if coberto else 0
    
    return jsonify({
        "codigo_procedimento": codigo_procedimento,
        "id_paciente": id_paciente,
        "plano": plano['nome'],
        "coberto": coberto,
        "valor_coberto": valor_coberto
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)