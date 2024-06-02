from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://my_user:my_password@localhost/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(255), nullable=False)

@app.before_request
def setup():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Todo List API"

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todo_list = [{"id": todo.id, "task": todo.task} for todo in todos]
    return jsonify(todo_list), 200

@app.route('/todos', methods=['POST'])
def add_todo():
    new_todo = request.json
    if 'task' not in new_todo:
        return jsonify({"error": "Task is required"}), 400

    todo = Todo(task=new_todo['task'])
    db.session.add(todo)
    db.session.commit()
    return jsonify({"id": todo.id, "task": todo.task}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    updates = request.json
    if 'task' not in updates:
        return jsonify({"error": "Task is required"}), 400

    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo item not found"}), 404

    todo.task = updates['task']
    db.session.commit()
    return jsonify({"id": todo.id, "task": todo.task}), 200

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo item not found"}), 404

    db.session.delete(todo)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
