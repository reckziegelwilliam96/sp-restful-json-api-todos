from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Todo

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

connect_db(app)

@app.route('/')
def index_page():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

"""GET Requests: READ ALL"""
@app.route('/api/todos')
def list_todos():
    all_todos = [todo.serialize_todo() for todo in Todo.query.all()]
    return jsonify(todos=all_todos)

"""GET Requests: READ ONE"""
@app.route('/api/todos/<int:id>')
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return jsonify(todo=todo.serialize_todo())

"""POST Requests: CREATE ONE"""
@app.route('/api/todos', methods=["POST"])
def create_todo():
    new_todo = Todo(title=request.json["title"])
    db.session.add(new_todo)
    db.session.commit()
    response_json = jsonify(todo=new_todo.serialize_todo())
    return (response_json, 201)

"""PUT / PATCH: UPDATE ONE"""
@app.route('/api/todos/<int:id>', methods=["PATCH"])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    # if title is not found, set default to original value ex. todo.title OR todo.done
    todo.title = request.json.get('title', todo.title)
    todo.done = request.json.get('done', todo.done) 
    db.session.commit()
    return jsonify(todo=todo.serialize_todo())

"""DELETE: DELETE ONE"""
@app.route('/api/todos/<int:id>', methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify(message="deleted")