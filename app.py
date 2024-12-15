from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(100), nullable=False)

    def __init__(self, task):
        self.task = task

    def to_dict(self):
        return {self.task_id: self.task}


api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task', type=str, required=True, help="Task cannot be blank!")

class TodoList(Resource):
    def get(self):
        todos = Todo.query.all()
        return jsonify([todo.to_dict() for todo in todos])

    def post(self):
        args = parser.parse_args()
        new_task = Todo(task=args['task'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task added successfully!", "task": new_task.to_dict()})

class Todo_specific(Resource):
    # GET: Retrieve a specific task
    def get(self, task_id):
        todo = Todo.query.get(task_id)
        if not todo:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(todo.to_dict())

    # DELETE: Delete a specific task
    def delete(self, task_id):
        todo = Todo.query.get(task_id)
        if not todo:
            return jsonify({"error": "Task not found"}), 404
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": f"Task {task_id} deleted successfully!"})

    # PUT: Update a specific task
    def put(self, task_id):
        args = parser.parse_args()
        todo = Todo.query.get(task_id)
        if not todo:
            return jsonify({"error": "Task not found"}), 404
        todo.task = args['task']
        db.session.commit()
        return jsonify({"message": f"Task {task_id} updated successfully!", "task": todo.to_dict()})

api.add_resource(TodoList, '/todos')
api.add_resource(Todo_specific,'/todos/<int:task_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

#Add todo from postman like this

#   {
#    "task": "you have perfected flask"
#   }