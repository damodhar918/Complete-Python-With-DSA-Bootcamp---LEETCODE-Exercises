from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Todo {self.title}>'

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    """Display all todos"""
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['GET', 'POST'])
def add_todo():
    """Add a new todo"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            return redirect(url_for('add_todo'))
        
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_todo.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    """Edit an existing todo"""
    todo = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        todo.title = request.form.get('title', todo.title)
        todo.description = request.form.get('description', todo.description)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_todo.html', todo=todo)

@app.route('/delete/<int:id>')
def delete_todo(id):
    """Delete a todo"""
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle_todo(id):
    """Toggle todo completion status"""
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/todos')
def get_todos_api():
    """API endpoint to get todos as JSON"""
    todos = Todo.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'completed': t.completed,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for t in todos])

if __name__ == '__main__':
    app.run(debug=True)
