from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
from threading import Thread
import time

# Load environment variables from .env file
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

app = Flask(__name__)
CORS(app)

# SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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

def dump_database():
    # Adjust the database connection according to your database
    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    
    # Dumping the database content
    dump_file_path = 'database_dump.sql'
    with open(dump_file_path, 'w') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    
    conn.close()
    
    return dump_file_path

def send_to_discord(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(DISCORD_WEBHOOK_URL, files={'file': f})
    
    if response.status_code == 204:
        print("File sent successfully")
    else:
        print(f"Failed to send file: {response.status_code}")

def daily_database_dump():
    while True:
        current_time = time.localtime()
        if current_time.tm_hour == 0 and current_time.tm_min == 0:  # Check if it's midnight
            file_path = dump_database()
            send_to_discord(file_path)
            time.sleep(60)  # Sleep for a minute to avoid multiple dumps within the same minute
        time.sleep(30)  # Check every 30 seconds

# Start the thread for daily database dump
dump_thread = Thread(target=daily_database_dump)
dump_thread.daemon = True  # Ensure the thread will close when the main program exits
dump_thread.start()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
