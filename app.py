from flask import Flask, jsonify, Request

app = Flask(__name__)

# Simulando uma lista de tarefas
equipamentos = [{'id': 1, 'equipamento': 'NT', 'valor': '255.57', 'serial': '123', 'departamento': 'MKT'},
         {'id': 2, 'equipamento': 'CD', 'valor': '25.47', 'serial': '1234', 'departamento': 'TI'},
         {'id': 3, 'equipamento': 'AE', 'valor': '38.57', 'serial': '12', 'departamento': 'RH'},
         {'id': 4, 'equipamento': 'WF', 'valor': '25', 'serial': '126', 'departamento': 'DP'},
         {'id': 5, 'equipamento': 'GT', 'valor': '260', 'serial': '1289', 'departamento': 'COM'}]

@app.route('/equipamentos', methods=['GET'])
def get_equipamentos():
    return jsonify({'equipamentos': equipamentos})

@app.route('/equipamentos', methods=['POST'])
def create_equipamento():
    new_equipamento = request.json
    new_equipamento['id'] = len(equipamentos) + 1
    equipamentos.append(new_equipamento)
    return jsonify({'equipamentos': new_equipamento}), 201


@app.route('/equipamentos/id/<int:equipamento_id>', methods=['GET'])
def get_equipamento(equipamento_id):
    equipamento = next((equipamento for equipamento in equipamentos if equipamento['id'] == equipamento_id), None)
    if equipamento is None:
        return jsonify({'error': 'Equipamento não encontrada'}), 404
    return jsonify({'equipamentos': equipamento})

@app.route('/equipamentos/id/<int:equipamento_id>', methods=['PUT'])
def update_equipamento(equipamento_id):
    equipamento = next((equipamento for equipamento in equipamentos if equipamento['id'] == equipamento_id), None)
    if equipamento is None:
        return jsonify({'error': 'Equipamento não encontrada'}), 404
    updated_equipamento = request.json
    equipamento.update(updated_equipamento)
    return jsonify({'equipamentos': equipamento})

@app.route('/equipamentos/id/<int:equipamento_id>', methods=['DELETE'])
def delete_equipamento(equipamento_id):
    equipamento = next((equipamento for equipamento in equipamentos if equipamento['id'] == equipamento_id), None)
    if equipamento is None:
        return jsonify({'error': 'Equipamento não encontrada'}), 404
    equipamentos.remove(equipamento)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug= True)
