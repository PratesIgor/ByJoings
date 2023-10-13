from flask import Flask, jsonify, request
from marshmallow import Schema, fields, validate
from marshmallow import ValidationError
import json

# Inicia aplicação flask

app = Flask(__name__)

# Cria lista chamada equipamentos
equipamentos = []
total = 0

# Classe para validação marshmawllow (validação dos campos únicos)
class EquipamentoSchema(Schema):
    id = fields.Int(dump_only=True)  # ID é gerado automaticamente e não deve ser inserido
    equipamento = fields.Str(required=True, validate=validate.Length(min=1))  # Equipamento é obrigatório e deve ter pelo menos 1 caractere
    valor = fields.Float(required=True, validate=validate.Range(min=0))  # Valor é obrigatório e deve ser um número não negativo
    serial = fields.Str(required=True, validate=validate.Length(min=1))  # Serial é obrigatório e deve ter pelo menos 1 caractere
    departamento = fields.Str(required=True, validate=validate.Length(min=1))  # Departamento é obrigatório e deve ter pelo menos 1 caractere
    nome_responsavel = fields.Str(required=True, validate=validate.Length(min=1)) # Nome do responsável é obrigatório e deve ter pelo menos 1 caractere
    telefone = fields.Str(required=True, validate=validate.Length(min=1))  # Telefone é obrigatório e deve ter pelo menos 1 caractere
    email = fields.Email(required=True)  # Email é obrigatório e deve ter pelo menos 1 caractere

    # Restrição dos campos para não permitir atualização de campos inexistentes
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields_to_validate = {
            "equipamento": self.fields["equipamento"],
            "valor": self.fields["valor"],
            "serial": self.fields["serial"],
            "departamento": self.fields["departamento"],
            "nome_responsavel": self.fields["nome_responsavel"],
            "telefone": self.fields["telefone"],
            "email": self.fields["email"]

        }

# Método para carregar os equipamentos do arquivo JSON e ordená-los
def load_equipamentos_from_json():
    try:
        with open("Equipamentos_API/equipamentos.json", "r") as bd_json:
            equipamentos = json.load(bd_json)
            equipamentos_sorted = sorted(equipamentos, key=lambda x: (x['id'], x['serial'], x['nome_responsavel'], x['telefone'], x['email'], x['equipamento'], x['departamento'], x['valor']))
            return equipamentos_sorted
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

# Cria arquivo json para armazenamento
def save_equipamentos_to_json(equipamentos):
    with open("Equipamentos_API/equipamentos.json", "w") as bd_json:
        json.dump(equipamentos, bd_json)

# Ordenação para listar usando o método get
def custom_sort(equipamento):
    return (
        equipamento['id'],
        equipamento['serial'],
        equipamento['nome_responsavel'],
        equipamento['telefone'],
        equipamento['email'],
        equipamento['equipamento'],
        equipamento['departamento'],
        equipamento['valor']
    )

# Método GET para consultar todos os equipamentos
@app.route('/equipamentos', methods=['GET'])
def get_equipamentos():
    try:
        equipamentos_sorted = sorted(equipamentos, key=lambda x: (x['id'], x['serial'], x['nome_responsavel'], x['telefone'], x['email'], x['equipamento'], x['departamento'], x['valor']))
        total_items = len(equipamentos_sorted)
        response = {'equipamentos': equipamentos_sorted, 'total': total_items}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}, 500)

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
            'departamento': data['departamento'],
            "nome_responsavel": data["nome_responsavel"],
            "telefone": data["telefone"],
            "email": data["email"]
        }
        equipamentos.append(new_equipamento)
        equipamentos.sort(key=lambda x: (x['id'], x['serial'], x['nome_responsavel'], x['telefone'], x['email'], x['equipamento'], x['departamento'], x['valor'])) #ordena inserção
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

# Método GET para consultar um equipamento por Email
@app.route('/equipamentos/email/<string:email>', methods=['GET'])
def get_equipamentos_por_email(email):
    equipamentos_por_email = [equipamento for equipamento in equipamentos if equipamento['email'] == email]
    total_items = len(equipamentos_por_email)
    if not equipamentos_por_email:
        return jsonify({'error': 'Nenhum equipamento encontrado com o email fornecido'}), 404
    response = {'equipamentos': equipamentos_por_email, 'total': total_items}
    return jsonify(response)


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
    app.run(host='0.0.0.0', port=5000)
