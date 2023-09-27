from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulando uma lista de tarefas
tasks = [{'id': 1, 'title': 'Comprar leite', 'done': False},
         {'id': 2, 'title': 'Ir à academia', 'done': True}]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.json
    new_task['id'] = len(tasks) + 1
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    return jsonify({'task': task})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    updated_task = request.json
    task.update(updated_task)
    return jsonify({'task': task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    tasks.remove(task)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug= True)
