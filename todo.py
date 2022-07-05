from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ardab/Desktop/ToDoApp/todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False)


@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route("/complete/<string:id>")
def complete(id):
    todo = Todo.query.filter(Todo.id == id).first()
    if todo.complete == False:
        todo.complete = True
    else:
        todo.complete = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<string:id>")
def delete(id):
    todo = Todo.query.filter(Todo.id == id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/details/<string:id>")
def details(id):
    todo = Todo.query.filter(Todo.id == id).first()
    if todo == None:
        return redirect(url_for("index"))
    else:
        return render_template('details.html', todo=todo)

@app.route("/add", methods=['POST'])
def addTodo():
    title = request.form.get('title')
    content = request.form.get('content')
    newTodo = Todo(title=title, content=content, complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
