from models import db, connect_db, Todo
from app import app

db.drop_all()
db.create_all()

todos = {
    Todo(title="Feed the kids"),
    Todo(title="Rinse and dry dishes"),
    Todo(title="Water the tomato garden", done=True),
    Todo(title="Workout"),
    Todo(title="Wash and dry dirty laundry", done=True),
    Todo(title="Make bed")
}

db.session.add_all(todos)
db.session.commit()