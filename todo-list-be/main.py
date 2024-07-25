from flask import Flask, jsonify, request

app = Flask(__name__)

todos = []

status_mapping = {
            0: 'Not started',
            1: 'In Progress',
            2: 'Completed'
        }

# Define the Todo class
class Todo:
    def __init__(self, id, description, status):
        self.id = id
        self.description = description
        self._status = status

    @property
    def status(self):
        return status_mapping.get(self._status, None)

    @status.setter
    def status(self, status):
        self._status = status


# Get all todo items
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify([{
        'id': todo.id,
        'description': todo.description,
        'status': todo.status
    } for todo in todos])

# Get todo item by ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    try:
        todo = next(todo for todo in todos if todo.id == todo_id)
    except StopIteration:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({
        'id': todo.id,
        'description': todo.description,
        'status': todo.status
    })

# Create a new todo item
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    status = data.get('status', '0')
    if status not in status_mapping:
        return jsonify({'error': 'Invalid status'}), 400
    todo = Todo(len(todos) + 1, data['description'], status)
    todos.append(todo)
    return jsonify({'message': 'Todo created successfully'}), 201

# Update a todo item
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    status = data.get('status', '0')
    if status not in status_mapping:
        return jsonify({'error': 'Invalid status'}), 400
    try:
        todo = next(todo for todo in todos if todo.id == todo_id)
    except StopIteration:
        return jsonify({'error': 'Todo not found'}), 404
    todo.description = data.get('description', todo.description)
    todo.status = status
    return jsonify({'message': 'Todo updated successfully'}), 200

# Delete a todo item
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    # Iterate over the todos list and find the todo with the matching ID
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            # Delete the todo from the list and return a success message
            del todos[i]
            return jsonify({'message': 'Todo deleted successfully'}), 200
    # If the todo is not found, return an error message
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)