from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

import MySQLdb.cursors

app = Flask(__name__)
CORS(app)
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'my_user'
app.config['MYSQL_PASSWORD'] = 'my_password'
app.config['MYSQL_DB'] = 'my_database'

mysql = MySQL(app)

def initialize_database():
    cursor = mysql.connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS todos (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      task VARCHAR(255) NOT NULL
                    )''')
    mysql.connection.commit()

@app.before_request
def setup():
    cursor = mysql.connection.cursor()
    cursor.execute('''CREATE DATABASE IF NOT EXISTS my_database''')
    cursor.execute('USE my_database')
    initialize_database()

@app.route('/')
def home():
    return "Welcome to the Todo List API"

@app.route('/todos', methods=['GET'])
def get_todos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM todos')
    todo_list = cursor.fetchall()
    return jsonify(todo_list), 200

@app.route('/todos', methods=['POST'])
def add_todo():
    new_todo = request.json
    if 'task' not in new_todo:
        return jsonify({"error": "Task is required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO todos (task) VALUES (%s)', (new_todo['task'],))
    mysql.connection.commit()
    new_todo['id'] = cursor.lastrowid
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    updates = request.json
    if 'task' not in updates:
        return jsonify({"error": "Task is required"}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
    todo = cursor.fetchone()
    if not todo:
        return jsonify({"error": "Todo item not found"}), 404

    cursor.execute('UPDATE todos SET task = %s WHERE id = %s', (updates['task'], todo_id))
    mysql.connection.commit()
    todo['task'] = updates['task']
    return jsonify(todo), 200

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
    todo = cursor.fetchone()
    if not todo:
        return jsonify({"error": "Todo item not found"}), 404

    cursor.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
    mysql.connection.commit()
    return '', 204

if __name__ == "__main__":
    app.run(debug=True, port=5001)
