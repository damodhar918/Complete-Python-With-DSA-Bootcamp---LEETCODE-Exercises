# Flask Todo App

A modern todo application built with Flask, Jinja2 templates, and Bootstrap 5.

## Features

- ✅ Create, read, update, and delete todos
- ✅ Mark todos as completed/uncompleted
- ✅ Beautiful responsive UI with Bootstrap 5
- ✅ SQLite database for persistent storage
- ✅ RESTful API endpoint for todos
- ✅ Clean Jinja2 template structure
- ✅ Modern CSS styling with animations

## Project Structure

```
flask-todo-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── todos.db              # SQLite database (created on first run)
├── templates/            # Jinja2 templates
│   ├── base.html        # Base template with navbar
│   ├── index.html       # Homepage showing all todos
│   ├── add_todo.html    # Form to add new todo
│   └── edit_todo.html   # Form to edit existing todo
└── static/              # Static files
    └── css/
        └── style.css    # Custom styling
```

## Installation

### 1. Clone or download the project
```bash
cd flask-todo-app
```

### 2. Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Home Page
- View all your todos
- Check off completed todos
- Delete todos
- Edit todos

### Add Todo
- Click "Add Todo" button
- Enter a title (required)
- Add a description (optional)
- Click "Add Todo" to create

### Edit Todo
- Click the "Edit" button on any todo
- Update title and description
- Click "Update Todo" to save changes

### Delete Todo
- Click the "Delete" button on any todo
- Confirm deletion

### Toggle Completion
- Check the checkbox next to a todo to mark it complete/incomplete

## API Endpoints

### Get All Todos (JSON)
```
GET /api/todos
```

Returns a JSON array of all todos with their details.

## Dependencies

- **Flask** (2.3.3): Web framework
- **Flask-SQLAlchemy** (3.0.5): ORM for database management
- **Bootstrap 5**: CSS framework (CDN)

## Database

The app uses SQLite for data persistence. The database is automatically created on first run.

### Todo Model
```python
- id: Integer (Primary Key)
- title: String (Required)
- description: Text (Optional)
- completed: Boolean (Default: False)
- created_at: DateTime (Auto-populated)
- due_date: DateTime (Optional)
```

## Customization

### Change the port
Edit `app.py` and change:
```python
app.run(debug=True, port=8000)  # Change to your desired port
```

### Modify styling
Edit `static/css/style.css` to customize colors and layout.

### Add new features
- Add due dates functionality
- Add priority levels
- Add categories/tags
- Add user authentication

## Development

To enable debug mode (auto-reload on code changes):
- Already enabled in `app.py` with `debug=True`

## Production Deployment

For production, disable debug mode:
```python
app.run(debug=False)
```

Use a production WSGI server like:
- Gunicorn
- uWSGI
- Waitress

## License

This project is open source and available for personal and educational use.

## Author

Created as a learning project for Flask and web development.
