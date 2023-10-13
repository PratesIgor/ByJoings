from flask import Flask, jsonify, request
from marshmallow import Schema, fields, validate
from marshmallow import ValidationError
import json

# Inicia aplicação flask

app = Flask(__name__)

# Cria lista chamada equipamentos
equipamentos = []

# Classe para validação marshmawllow (validação dos campos únicos)
class EquipamentoSchema(Schema):
    id = fields.Int(dump_only=True)  # ID é gerado automaticamente e não deve ser inserido
    equipamento = fields.Str(required=True, validate=validate.Length(min=1))  # Equipamento é obrigatório e deve ter pelo menos 1 caractere
    valor = fields.Float(required=True, validate=validate.Range(min=0))  # Valor é obrigatório e deve ser um número não negativo
    serial = fields.Str(required=True, validate=validate.Length(min=1))  # Serial é obrigatório e deve ter pelo menos 1 caractere
    departamento = fields.Str(required=True, validate=validate.Length(min=1))  # Departamento é obrigatório e deve ter pelo menos 1 caractere

    # Restrição dos campos para não permitir atualização de campos inexistentes
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields_to_validate = {
            "equipamento": self.fields["equipamento"],
            "valor": self.fields["valor"],
            "serial": self.fields["serial"],
            "departamento": self.fields["departamento"]
        }

# Abre arquivo para o modo leitura
def load_equipamentos_from_json():
    try:
        with open("equipamentos.json", "r") as bd_json:
            return json.load(bd_json)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

# Cria arquivo json para armazenamento
def save_equipamentos_to_json(equipamentos):
    with open("equipamentos.json", "w") as bd_json:
        json.dump(equipamentos, bd_json)

# Método GET para listar registros cadastrados até o momento
@app.route('/equipamentos', methods=['GET'])
def get_equipamentos():
    try:
        equipamentos = load_equipamentos_from_json()
        return jsonify({'equipamentos': equipamentos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Método POST para criar um equipamento
@app.route('/equipamentos', methods=['POST'])
def create_equipamento():
    try:
        data = EquipamentoSchema().load(request.json)
        new_equipamento = {
            'id': len(equipamentos) + 1,
            'equipamento': data['equipamento'],
            'valor': data['valor'],
            'serial': data['serial'],
            'departamento': data['departamento']
        }
        equipamentos.append(new_equipamento)
        save_equipamentos_to_json(equipamentos)
        return jsonify({'equipamento': new_equipamento}), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}, 400)
    
# Método GET para consultar um equipamento por ID
@app.route('/equipamentos/id/<int:equipamento_id>', methods=['GET'])
def get_equipamento(equipamento_id):
    equipamento = next((equipamento for equipamento in equipamentos if equipamento['id'] == equipamento_id), None)
    if equipamento is None:
        return jsonify({'error': 'Equipamento não encontrado'}), 404
    return jsonify({'equipamento': equipamento})

# Método PUT para atualizar um equipamento por ID
@app.route('/equipamentos/id/<int:equipamento_id>', methods=['PUT'])
def update_equipamento(equipamento_id):
    equipamento = next((equipamento for equipamento in equipamentos if equipamento['id'] == equipamento_id), None)
    if equipamento is None:
        return jsonify({'error': 'Equipamento não encontrado'}), 404
    
    try:
        data = EquipamentoSchema().load(request.json)
        
        for field_name in data:
            if field_name not in EquipamentoSchema().fields_to_validate:
                return jsonify({'error': f'Campo inválido: {field_name}'}, 400)
        
        equipamento.update(data)
        save_equipamentos_to_json(equipamentos)
        return jsonify({'equipamento': equipamento})
    except ValidationError as e:
        return jsonify({'error': str(e)}, 400)

# Método DELETE para excluir um equipamento por ID
@app.route('/equipamentos/id/<int:equipamento_id>', methods=['DELETE'])
def delete_equipamento(equipamento_id):
    equipamento = next((equipamento for equipamento in equipamentos if equipamento['id'] == equipamento_id), None)
    if equipamento is None:
        return jsonify({'error': 'Equipamento não encontrado'}), 404
    equipamentos.remove(equipamento)
    save_equipamentos_to_json(equipamentos)  # Salva as alterações no arquivo JSON
    return jsonify({'result': True})

# Carrega servidor flask e arquivo com os registros
if __name__ == '__main__':
    equipamentos = load_equipamentos_from_json()
    app.run(debug= True)
