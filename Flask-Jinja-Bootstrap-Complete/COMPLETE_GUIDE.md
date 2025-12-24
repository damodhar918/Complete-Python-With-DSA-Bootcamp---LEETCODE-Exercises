# Flask, Jinja2, and Bootstrap - Complete Guide

## 📖 Introduction

This document provides comprehensive documentation of all Flask, Jinja2, and Bootstrap concepts implemented in this complete application. Each topic includes examples from the codebase.

---

## PART 1: FLASK FRAMEWORK

### 1. Flask Basics

#### 1.1 Application Initialization
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)
```

#### 1.2 Route Definition
```python
@app.route('/')                                    # GET only
@app.route('/posts', methods=['GET', 'POST'])     # Multiple methods
@app.route('/post/<int:post_id>')                 # URL parameters
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)
```

#### 1.3 Request Methods
```python
from flask import request

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        # Process POST data
    else:
        # Handle GET
    return render_template('search.html')
```

---

### 2. Database & ORM (SQLAlchemy)

#### 2.1 Model Definition
```python
class User(UserMixin, db.Model):
    """User model with relationships"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
```

#### 2.2 Relationships
```python
# One-to-Many: User has many Posts
class Post(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # In User: posts = db.relationship('Post', backref='author')

# Access
post = Post.query.get(1)
print(post.author.username)  # Access through backref
user = User.query.get(1)
print(len(user.posts))       # Access through relationship
```

#### 2.3 Query Operations
```python
# Create
user = User(username='john', email='john@example.com')
db.session.add(user)
db.session.commit()

# Read
user = User.query.get(1)                          # By primary key
user = User.query.filter_by(username='john').first()
users = User.query.all()

# Update
user.username = 'jane'
db.session.commit()

# Delete
db.session.delete(user)
db.session.commit()

# Advanced Queries
posts = Post.query.filter_by(category='Tech').order_by(Post.created_at.desc()).limit(5)
featured = Post.query.filter(Post.views > 100).all()
```

#### 2.4 Filtering & Pagination
```python
# Filter
posts = Post.query.filter(Post.title.ilike('%flask%')).all()

# Pagination
page = request.args.get('page', 1, type=int)
paginated = Post.query.paginate(page=page, per_page=10)

# In templates
{% for post in posts.items %}
{% if posts.has_prev %}<a href="...{{ posts.prev_num }}">
{% for page_num in posts.iter_pages() %}
```

---

### 3. Authentication & Authorization

#### 3.1 Flask-Login Setup
```python
from flask_login import LoginManager, UserMixin, login_user, logout_user

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

#### 3.2 User Registration
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Password hashing
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

#### 3.3 User Login
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)
```

#### 3.4 Authorization Decorators
```python
from flask_login import login_required, current_user
from functools import wraps

# Protect routes
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Custom decorator for admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')
```

---

### 4. Forms & Validation

#### 4.1 Flask-WTF & WTForms
```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm',
                                    validators=[DataRequired(), 
                                              EqualTo('password')])
```

#### 4.2 Form Rendering & Validation
```python
# In route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Form is valid
        user = User(username=form.username.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# In template
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.username(class="form-control") }}
    {% if form.username.errors %}
        <div class="invalid-feedback">
            {% for error in form.username.errors %}
                {{ error }}
            {% endfor %}
        </div>
    {% endif %}
</form>
```

#### 4.3 CSRF Protection
```python
# Automatic with Flask-WTF
class MyForm(FlaskForm):
    # Automatically includes CSRF token
    pass

# In template - renders hidden CSRF field
{{ form.hidden_tag() }}
```

---

### 5. Templates & Rendering

#### 5.1 Template Rendering
```python
from flask import render_template

@app.route('/posts')
def posts_list():
    posts = Post.query.all()
    categories = db.session.query(Post.category).distinct()
    return render_template('posts_list.html', 
                         posts=posts,
                         categories=categories)
```

#### 5.2 Static Files
```python
# Access in templates
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}">
```

#### 5.3 URL Building
```python
# In Python
url_for('view_post', post_id=1)           # /post/1
url_for('user_profile', username='john')  # /user/john
url_for('index')                          # /

# In Templates
<a href="{{ url_for('view_post', post_id=post.id) }}">Read More</a>
```

---

### 6. Template Filters & Context Processors

#### 6.1 Custom Template Filters
```python
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    if value is None:
        return ''
    return value.strftime(format)

@app.template_filter('word_count')
def word_count(text):
    return len(text.split()) if text else 0

# Usage in template
{{ post.created_at | datetimeformat('%B %d, %Y') }}
{{ post.content | word_count }}
```

#### 6.2 Context Processors
```python
@app.context_processor
def inject_categories():
    """Make categories available in all templates"""
    categories = db.session.query(Post.category).distinct()
    return {'categories': [c[0] for c in categories]}

@app.context_processor
def inject_user_count():
    """Add user count to all templates"""
    return {'user_count': User.query.count()}

# Access in any template
<p>Total users: {{ user_count }}</p>
{% for cat in categories %}
    <a href="...">{{ cat }}</a>
{% endfor %}
```

---

### 7. Flash Messages

#### 7.1 Flashing Messages
```python
from flask import flash, redirect

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('Permission denied', 'danger')
        return redirect(url_for('view_post', post_id=post.id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('dashboard'))
```

#### 7.2 Displaying Flash Messages
```html
<!-- In base template -->
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

---

### 8. Error Handlers

#### 8.1 Error Handler Routes
```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403
```

#### 8.2 Custom Error Handling
```python
@app.route('/api/post/<int:post_id>')
@json_response
def api_get_post(post_id):
    post = Post.query.get_or_404(post_id)  # 404 automatically
    return {'post': post}
```

---

### 9. API Routes (JSON)

#### 9.1 RESTful JSON API
```python
from flask import jsonify

@app.route('/api/posts', methods=['GET'])
@json_response
def api_get_posts():
    posts = Post.query.all()
    return {
        'posts': [{
            'id': p.id,
            'title': p.title,
            'author': p.author.username,
            'views': p.views
        } for p in posts]
    }

@app.route('/api/stats', methods=['GET'])
@json_response
def api_stats():
    return {
        'users': User.query.count(),
        'posts': Post.query.count(),
        'comments': Comment.query.count()
    }

# Decorator
def json_response(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        return jsonify(result) if isinstance(result, dict) else result
    return decorated
```

---

### 10. Advanced Flask Features

#### 10.1 Custom Decorators
```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def json_response(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        return jsonify(result) if isinstance(result, dict) else result
    return decorated

# Usage
@app.route('/admin')
@login_required
@admin_required
def admin():
    pass

@app.route('/api/data')
@json_response
def get_data():
    return {'data': []}
```

#### 10.2 Hooks & Middleware
```python
@app.before_request
def before_request():
    # Code before every request
    g.user = current_user

@app.after_request
def after_request(response):
    # Code after every request
    return response
```

---

## PART 2: JINJA2 TEMPLATING

### 1. Template Basics

#### 1.1 Variable Interpolation
```jinja2
<!-- Simple variables -->
<h1>{{ post.title }}</h1>
<p>by {{ post.author.username }}</p>

<!-- Expressions -->
<p>{{ 10 + 5 }}</p>
<p>{{ full_name.upper() }}</p>
<p>{{ post.content[:100] }}</p>
```

#### 1.2 Comments
```jinja2
<!-- Jinja2 comment (not rendered) -->
{# This comment won't appear in HTML #}

<!-- HTML comment (rendered) -->
<!-- This will appear in HTML source -->
```

#### 1.3 Tags
```jinja2
{% if condition %}
    {# if tag #}
{% endif %}

{% for item in items %}
    {# for loop #}
{% endfor %}

{% set variable = value %}
    {# variable assignment #}
{% endset %}

{% extends "base.html" %}
    {# template inheritance #}
```

---

### 2. Control Structures

#### 2.1 Conditionals
```jinja2
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% elif user.is_visitor %}
    <p>Welcome, visitor!</p>
{% else %}
    <p>Please log in</p>
{% endif %}

<!-- Inline if (ternary) -->
<p class="{% if post.views > 100 %}popular{% else %}new{% endif %}">

<!-- Conditional filters -->
{% if posts|length > 0 %}
    <p>You have {{ posts|length }} posts</p>
{% endif %}

<!-- Boolean tests -->
{% if post.is_published %}
{% if user in post.viewers %}
{% if 'admin' in user.roles %}
```

#### 2.2 Loops
```jinja2
<!-- Basic loop -->
{% for post in posts %}
    <h3>{{ post.title }}</h3>
{% endfor %}

<!-- Loop with else (if list is empty) -->
{% for post in posts %}
    <p>{{ post.title }}</p>
{% else %}
    <p>No posts found</p>
{% endfor %}

<!-- Loop object properties -->
{% for post in posts %}
    <p>Post #{{ loop.index }} of {{ loop.length }}</p>
    {% if loop.first %}<div class="first">{% endif %}
    {% if loop.last %}</div>{% endif %}
    {% if loop.previtem %}Prev: {{ loop.previtem.title }}{% endif %}
    {% if loop.nextitem %}Next: {{ loop.nextitem.title }}{% endif %}
{% endfor %}

<!-- Nested loops -->
{% for category in categories %}
    <h3>{{ category.name }}</h3>
    {% for post in category.posts %}
        <p>- {{ post.title }}</p>
    {% endfor %}
{% endfor %}

<!-- Loop with filtering -->
{% for post in posts if post.is_published %}
    <p>{{ post.title }}</p>
{% endfor %}

<!-- Unpacking in loops -->
{% for key, value in dict.items() %}
    <p>{{ key }}: {{ value }}</p>
{% endfor %}
```

---

### 3. Template Inheritance

#### 3.1 Base Template
```jinja2
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### 3.2 Child Templates
```jinja2
<!-- templates/home.html -->
{% extends "base.html" %}

{% block title %}Home - My Site{% endblock %}

{% block content %}
    <h1>Welcome Home!</h1>
{% endblock %}

<!-- templates/about.html -->
{% extends "base.html" %}

{% block title %}About - My Site{% endblock %}

{% block content %}
    <h1>About Us</h1>
    <p>This is about page</p>
{% endblock %}
```

#### 3.3 Multi-level Inheritance
```jinja2
<!-- base.html -->
{% block content %}
    <div class="container">
        {% block page_content %}{% endblock %}
    </div>
{% endblock %}

<!-- layout.html -->
{% extends "base.html" %}
{% block content %}
    <div class="wrapper">
        {{ super() }}
    </div>
{% endblock %}

<!-- page.html -->
{% extends "layout.html" %}
{% block page_content %}
    <p>Page content here</p>
{% endblock %}
```

#### 3.4 Super Block
```jinja2
<!-- Child template can include parent block content -->
{% block content %}
    {{ super() }}  <!-- Includes parent block content -->
    <p>Additional content from child</p>
{% endblock %}
```

---

### 4. Filters

#### 4.1 Built-in Filters
```jinja2
<!-- String filters -->
{{ text | upper }}                  <!-- UPPERCASE -->
{{ text | lower }}                  <!-- lowercase -->
{{ text | title }}                  <!-- Title Case -->
{{ text | capitalize }}             <!-- Capitalize -->
{{ text | replace('a', 'b') }}      <!-- Replace -->
{{ text | length }}                 <!-- Length -->
{{ text | wordcount }}              <!-- Word count -->
{{ text | trim }}                   <!-- Trim spaces -->
{{ text | slugify }}                <!-- Slug format -->
{{ text | urlencode }}              <!-- URL encode -->

<!-- Numeric filters -->
{{ 3.14159 | round(2) }}            <!-- 3.14 -->
{{ -10 | abs }}                     <!-- 10 -->
{{ numbers | sum }}                 <!-- Sum of list -->
{{ numbers | min }}                 <!-- Minimum -->
{{ numbers | max }}                 <!-- Maximum -->

<!-- List filters -->
{{ items | length }}                <!-- List length -->
{{ items | first }}                 <!-- First item -->
{{ items | last }}                  <!-- Last item -->
{{ items | join(', ') }}            <!-- Join items -->
{{ items | list }}                  <!-- Convert to list -->
{{ items | reverse }}               <!-- Reverse -->
{{ items | sort }}                  <!-- Sort -->
{{ items | unique }}                <!-- Remove duplicates -->

<!-- Object filters -->
{{ post | tojson }}                 <!-- To JSON -->
{{ post | string }}                 <!-- To string -->

<!-- Date filters -->
{{ date | datetimeformat }}         <!-- Format date -->
{{ date | datetimeformat('%d/%m/%Y') }}
{{ date | default('No date') }}     <!-- Default value -->

<!-- Condition filters -->
{{ value | default('N/A') }}        <!-- Default if empty -->
{{ items | select('attribute', 'public') }}  <!-- Select -->
{{ items | reject('attribute', 'draft') }}   <!-- Reject -->
```

#### 4.2 Custom Filters
```python
# In main.py
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    if value is None:
        return ''
    return value.strftime(format)

@app.template_filter('word_count')
def word_count(text):
    return len(text.split()) if text else 0

@app.template_filter('excerpt')
def excerpt(text, length=100):
    if len(text) > length:
        return text[:length] + '...'
    return text
```

#### 4.3 Filter Chaining
```jinja2
<!-- Filters are applied left to right -->
{{ post.content | lower | title | truncate(50) }}

{{ date | datetimeformat('%Y-%m-%d') | upper }}

{{ users | map(attribute='username') | join(', ') }}

{{ items | select('attribute', 'active') | list | length }}
```

---

### 5. Variables & Scoping

#### 5.1 Variable Assignment
```jinja2
<!-- Set variable -->
{% set my_var = 'Hello' %}
<p>{{ my_var }}</p>

<!-- Set from expression -->
{% set total_posts = posts | length %}
<p>Total: {{ total_posts }}</p>

<!-- Set block content -->
{% set result %}
    <div>Content</div>
{% endset %}

<!-- Set with condition -->
{% set status = 'admin' if user.is_admin else 'user' %}
```

#### 5.2 Variable Scope
```jinja2
<!-- Variables are globally scoped in templates -->
{% for item in items %}
    {% set counter = loop.index %}
{% endfor %}
<!-- counter still exists here -->

<!-- Macro variables are local -->
{% macro greet(name) %}
    {% set greeting = 'Hello ' + name %}
    {{ greeting }}
{% endmacro %}
<!-- greeting doesn't exist here -->
```

#### 5.3 Global Context Variables
```jinja2
<!-- Flask provides these automatically -->
{{ current_user }}                  <!-- Current logged-in user -->
{{ request.args.get('q') }}         <!-- Query parameters -->
{{ url_for('index') }}              <!-- URL building -->
{{ get_flashed_messages() }}        <!-- Flash messages -->
{{ g }}                             <!-- Application context -->
```

---

### 6. Tests

#### 6.1 Built-in Tests
```jinja2
<!-- Type tests -->
{% if variable is string %}
{% if variable is number %}
{% if variable is iterable %}
{% if variable is mapping %}
{% if variable is boolean %}

<!-- Value tests -->
{% if value is none %}
{% if value is undefined %}
{% if value is defined %}
{% if value is empty %}

<!-- Comparison tests -->
{% if post.id is divisibleby(5) %}
{% if text is escaped %}
{% if num is even %}
{% if num is odd %}

<!-- Membership tests -->
{% if user in admin_users %}
{% if 'admin' in user.roles %}
```

#### 6.2 Custom Tests
```python
@app.template_test('admin')
def is_admin(user):
    return user.is_admin

@app.template_test('published')
def is_published(post):
    return post.status == 'published'
```

Usage:
```jinja2
{% if user is admin %}
    Admin panel
{% endif %}

{% if post is published %}
    Visible to public
{% endif %}
```

---

### 7. Macros

#### 7.1 Basic Macros
```jinja2
<!-- Define macro -->
{% macro render_post(post) %}
    <div class="post">
        <h3>{{ post.title }}</h3>
        <p>by {{ post.author }}</p>
    </div>
{% endmacro %}

<!-- Use macro -->
{{ render_post(post) }}
```

#### 7.2 Macros with Parameters
```jinja2
{% macro button(text, class='btn-primary', href='#') %}
    <a href="{{ href }}" class="btn {{ class }}">
        {{ text }}
    </a>
{% endmacro %}

<!-- Usage -->
{{ button('Click Me') }}
{{ button('Delete', class='btn-danger', href='/delete/1') }}
```

#### 7.3 Macros with Loops
```jinja2
{% macro list_items(items, type='ul') %}
    <{{ type }}>
        {% for item in items %}
            <li>{{ item }}</li>
        {% endfor %}
    </{{ type }}>
{% endmacro %}

{{ list_items(posts, type='ol') }}
```

#### 7.4 Macro Caller
```jinja2
{% macro render_card(title) %}
    <div class="card">
        <h3>{{ title }}</h3>
        {{ caller() }}
    </div>
{% endmacro %}

<!-- Usage with content -->
{% call render_card('My Card') %}
    <p>Card content here</p>
{% endcall %}
```

---

### 8. Advanced Jinja2

#### 8.1 Include
```jinja2
<!-- Include another template -->
{% include 'header.html' %}

<!-- Include with variables -->
{% include 'post_card.html' with context %}
{% include 'post_card.html' without context %}
```

#### 8.2 Import
```jinja2
<!-- Import macro from another template -->
{% import 'macros.html' as macros %}
{{ macros.render_post(post) }}

<!-- Import specific macro -->
{% from 'macros.html' import render_post %}
{{ render_post(post) }}
```

#### 8.3 Block Assignment
```jinja2
{% set navigation %}
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
{% endset %}
{{ navigation }}
```

#### 8.4 Whitespace Control
```jinja2
<!-- Preserve whitespace -->
{%+ for item in items %}

<!-- Strip whitespace -->
{%- for item in items %}

{{- value }}  <!-- Strip before -->
{{ value -}}  <!-- Strip after -->
```

---

## PART 3: BOOTSTRAP 5

### 1. Getting Started

#### 1.1 Bootstrap CDN
```html
<!-- CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- JS Bundle (includes Popper) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

#### 1.2 Container Classes
```html
<!-- Fixed width container -->
<div class="container">
    <!-- Content -->
</div>

<!-- Full width container -->
<div class="container-fluid">
    <!-- Content -->
</div>

<!-- Responsive containers -->
<div class="container-sm">  <!-- 540px and up -->
<div class="container-md">  <!-- 720px and up -->
<div class="container-lg">  <!-- 960px and up -->
<div class="container-xl">  <!-- 1140px and up -->
<div class="container-xxl"> <!-- 1320px and up -->
```

---

### 2. Grid System

#### 2.1 Rows and Columns
```html
<!-- 12-column grid -->
<div class="container">
    <div class="row">
        <div class="col">Auto</div>
        <div class="col-6">Half</div>
        <div class="col-3">Quarter</div>
    </div>
</div>
```

#### 2.2 Responsive Columns
```html
<!-- Responsive design -->
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">
        <!-- Full on mobile, half on tablet, third on desktop -->
    </div>
</div>

<!-- Breakpoints -->
col-xs (< 576px)      <!-- Default, no prefix -->
col-sm (≥ 576px)
col-md (≥ 768px)
col-lg (≥ 992px)
col-xl (≥ 1200px)
col-xxl (≥ 1400px)
```

#### 2.3 Gutters
```html
<div class="row g-0">        <!-- No gutters -->
<div class="row g-1">        <!-- 0.25rem -->
<div class="row g-2">        <!-- 0.5rem -->
<div class="row g-3">        <!-- 1rem -->
<div class="row g-4">        <!-- 1.5rem -->
<div class="row g-5">        <!-- 3rem -->
```

#### 2.4 Column Alignment
```html
<!-- Vertical alignment -->
<div class="row align-items-start">     <!-- Top -->
<div class="row align-items-center">    <!-- Middle -->
<div class="row align-items-end">       <!-- Bottom -->

<!-- Horizontal alignment -->
<div class="row justify-content-start">     <!-- Left -->
<div class="row justify-content-center">    <!-- Center -->
<div class="row justify-content-end">       <!-- Right -->
<div class="row justify-content-between">   <!-- Space between -->
<div class="row justify-content-around">    <!-- Space around -->
<div class="row justify-content-evenly">    <!-- Equal space -->

<!-- Individual column alignment -->
<div class="col align-self-start">
<div class="col align-self-center">
<div class="col align-self-end">
```

---

### 3. Typography

#### 3.1 Headings
```html
<h1>Heading 1</h1>      <!-- 2.5rem -->
<h2>Heading 2</h2>      <!-- 2rem -->
<h3>Heading 3</h3>      <!-- 1.75rem -->
<h4>Heading 4</h4>      <!-- 1.5rem -->
<h5>Heading 5</h5>      <!-- 1.25rem -->
<h6>Heading 6</h6>      <!-- 1rem -->

<!-- Display headings -->
<h1 class="display-1">Display 1</h1>    <!-- 5.5rem -->
<h1 class="display-2">Display 2</h1>    <!-- 4.5rem -->
<h1 class="display-3">Display 3</h1>    <!-- 3.5rem -->
<h1 class="display-4">Display 4</h1>    <!-- 2.5rem -->
<h1 class="display-5">Display 5</h1>    <!-- 2rem -->
<h1 class="display-6">Display 6</h1>    <!-- 1.5rem -->
```

#### 3.2 Text Styles
```html
<p class="lead">Lead text - larger font</p>
<p><mark>Highlighted text</mark></p>
<p><del>Deleted text</del></p>
<p><ins>Inserted text</ins></p>
<p><strong>Bold text</strong></p>
<p><em>Italicized text</em></p>
<p><small>Small text</small></p>

<!-- Text alignment -->
<p class="text-start">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-end">Right aligned</p>
```

#### 3.3 Lists
```html
<!-- Ordered list -->
<ol>
    <li>Item</li>
</ol>

<!-- Unordered list -->
<ul>
    <li>Item</li>
</ul>

<!-- Unstyled list -->
<ul class="list-unstyled">
    <li>Item (no bullets)</li>
</ul>

<!-- Inline list -->
<ul class="list-inline">
    <li class="list-inline-item">Item 1</li>
    <li class="list-inline-item">Item 2</li>
</ul>
```

---

### 4. Colors & Backgrounds

#### 4.1 Text Colors
```html
<p class="text-primary">Primary</p>
<p class="text-secondary">Secondary</p>
<p class="text-success">Success</p>
<p class="text-danger">Danger</p>
<p class="text-warning">Warning</p>
<p class="text-info">Info</p>
<p class="text-light">Light</p>
<p class="text-dark">Dark</p>
<p class="text-muted">Muted</p>
<p class="text-white">White</p>
```

#### 4.2 Background Colors
```html
<div class="bg-primary">Primary background</div>
<div class="bg-secondary">Secondary background</div>
<div class="bg-success">Success background</div>
<div class="bg-danger">Danger background</div>
<div class="bg-warning">Warning background</div>
<div class="bg-info">Info background</div>
<div class="bg-light">Light background</div>
<div class="bg-dark">Dark background</div>
```

#### 4.3 Opacity
```html
<div class="bg-primary opacity-100">100%</div>
<div class="bg-primary opacity-75">75%</div>
<div class="bg-primary opacity-50">50%</div>
<div class="bg-primary opacity-25">25%</div>
<div class="bg-primary opacity-0">0%</div>
```

---

### 5. Components

#### 5.1 Buttons
```html
<!-- Solid buttons -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-warning">Warning</button>
<button class="btn btn-info">Info</button>
<button class="btn btn-light">Light</button>
<button class="btn btn-dark">Dark</button>

<!-- Outline buttons -->
<button class="btn btn-outline-primary">Primary</button>
<button class="btn btn-outline-secondary">Secondary</button>

<!-- Button sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Regular</button>
<button class="btn btn-primary btn-lg">Large</button>

<!-- Disabled button -->
<button class="btn btn-primary" disabled>Disabled</button>

<!-- Button as link -->
<a href="#" class="btn btn-primary">Link button</a>
```

#### 5.2 Cards
```html
<div class="card">
    <img src="image.jpg" class="card-img-top" alt="...">
    <div class="card-body">
        <h5 class="card-title">Card Title</h5>
        <p class="card-text">Card content here</p>
        <a href="#" class="btn btn-primary">Go</a>
    </div>
    <div class="card-footer">
        Footer content
    </div>
</div>

<!-- Card with multiple sections -->
<div class="card">
    <div class="card-header">Header</div>
    <div class="card-body">Body</div>
    <div class="card-footer">Footer</div>
</div>
```

#### 5.3 Navigation Bar
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Brand</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link active" href="#">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">About</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="dropdown">
                        Dropdown
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#">Item</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

#### 5.4 Badges & Alerts
```html
<!-- Badges -->
<span class="badge bg-primary">Primary</span>
<span class="badge bg-secondary">Secondary</span>
<span class="badge rounded-pill bg-primary">Pill</span>

<!-- Alerts -->
<div class="alert alert-primary">Primary alert</div>
<div class="alert alert-danger alert-dismissible fade show">
    Dismissible alert
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

#### 5.5 Pagination
```html
<nav>
    <ul class="pagination">
        <li class="page-item"><a class="page-link" href="#">Previous</a></li>
        <li class="page-item active"><span class="page-link">1</span></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">Next</a></li>
    </ul>
</nav>
```

#### 5.6 Breadcrumbs
```html
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="#">Home</a></li>
        <li class="breadcrumb-item"><a href="#">Library</a></li>
        <li class="breadcrumb-item active">Data</li>
    </ol>
</nav>
```

#### 5.7 Tables
```html
<table class="table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Email</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>John</td>
            <td>john@example.com</td>
        </tr>
    </tbody>
</table>

<!-- Table styles -->
<table class="table table-striped">       <!-- Alternating rows -->
<table class="table table-hover">         <!-- Hover effect -->
<table class="table table-dark">          <!-- Dark table -->
<table class="table table-responsive">    <!-- Scrollable on small screens -->
<table class="table table-bordered">      <!-- Borders -->
<table class="table table-sm">            <!-- Compact -->
```

---

### 6. Forms

#### 6.1 Form Controls
```html
<!-- Text input -->
<input type="text" class="form-control" placeholder="Text input">

<!-- Email input -->
<input type="email" class="form-control" placeholder="Email">

<!-- Password input -->
<input type="password" class="form-control" placeholder="Password">

<!-- Textarea -->
<textarea class="form-control" rows="3"></textarea>

<!-- Select dropdown -->
<select class="form-select">
    <option>Choose...</option>
    <option>Option 1</option>
</select>

<!-- Disabled state -->
<input type="text" class="form-control" disabled>

<!-- Readonly state -->
<input type="text" class="form-control" readonly value="Readonly">

<!-- Form validation -->
<input type="text" class="form-control is-valid">
<input type="text" class="form-control is-invalid">
```

#### 6.2 Form Layout
```html
<!-- Form groups -->
<div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control" id="email">
    <small class="form-text text-muted">Help text</small>
</div>

<!-- Inline forms -->
<form class="row g-3">
    <div class="col-auto">
        <input type="text" class="form-control">
    </div>
    <div class="col-auto">
        <button class="btn btn-primary">Submit</button>
    </div>
</form>

<!-- Floating labels -->
<div class="form-floating mb-3">
    <input type="email" class="form-control" id="floatEmail" placeholder="Email">
    <label for="floatEmail">Email address</label>
</div>
```

#### 6.3 Checkboxes & Radios
```html
<!-- Checkbox -->
<div class="form-check">
    <input class="form-check-input" type="checkbox" id="check1">
    <label class="form-check-label" for="check1">
        Checkbox
    </label>
</div>

<!-- Radio button -->
<div class="form-check">
    <input class="form-check-input" type="radio" name="radio" id="radio1">
    <label class="form-check-label" for="radio1">
        Radio 1
    </label>
</div>

<!-- Checkbox inline -->
<div class="form-check form-check-inline">
    <input class="form-check-input" type="checkbox" id="inline1">
    <label class="form-check-label" for="inline1">Inline</label>
</div>
```

#### 6.4 Input Groups
```html
<div class="input-group mb-3">
    <span class="input-group-text">$</span>
    <input type="number" class="form-control">
</div>

<div class="input-group mb-3">
    <input type="text" class="form-control" placeholder="Username">
    <span class="input-group-text">@example.com</span>
</div>

<div class="input-group mb-3">
    <button class="btn btn-outline-secondary">Search</button>
    <input type="text" class="form-control">
</div>
```

---

### 7. Spacing Utilities

#### 7.1 Margins & Padding
```html
<!-- Margins -->
<div class="m-3">Margin all</div>
<div class="mt-3">Margin top</div>
<div class="mb-3">Margin bottom</div>
<div class="ms-3">Margin start (left)</div>
<div class="me-3">Margin end (right)</div>
<div class="mx-3">Margin horizontal</div>
<div class="my-3">Margin vertical</div>

<!-- Padding -->
<div class="p-3">Padding all</div>
<div class="pt-3">Padding top</div>
<div class="pb-3">Padding bottom</div>
<div class="ps-3">Padding start</div>
<div class="pe-3">Padding end</div>
<div class="px-3">Padding horizontal</div>
<div class="py-3">Padding vertical</div>

<!-- Sizes: 0, 1, 2, 3, 4, 5 -->
<!-- Larger: 1rem, 1.5rem, 3rem, etc. -->
```

#### 7.2 Gap (Flexbox)
```html
<div class="d-flex gap-1">  <!-- 0.25rem -->
<div class="d-flex gap-2">  <!-- 0.5rem -->
<div class="d-flex gap-3">  <!-- 1rem -->
<div class="d-flex gap-4">  <!-- 1.5rem -->
<div class="d-flex gap-5">  <!-- 3rem -->
```

---

### 8. Display & Flexbox

#### 8.1 Display Classes
```html
<div class="d-none">Hidden</div>              <!-- display: none -->
<div class="d-block">Block</div>              <!-- display: block -->
<div class="d-inline">Inline</div>            <!-- display: inline -->
<div class="d-inline-block">Inline-block</div>

<!-- Responsive display -->
<div class="d-none d-md-block">Hidden on mobile, visible on tablet+</div>
<div class="d-md-none">Visible on mobile, hidden on tablet+</div>

<!-- Print display -->
<div class="d-print-none">Hidden when printing</div>
<div class="d-print-block">Visible when printing</div>
```

#### 8.2 Flexbox
```html
<div class="d-flex">                           <!-- flex container -->
    <div class="flex-grow-1">Grow</div>        <!-- flex-grow: 1 -->
    <div class="flex-shrink-0">No shrink</div> <!-- flex-shrink: 0 -->
</div>

<div class="d-flex flex-column">               <!-- Column layout -->
    <div>Item 1</div>
    <div>Item 2</div>
</div>

<div class="d-flex flex-row-reverse">          <!-- Reverse -->
    <div>Item 1</div>
</div>

<div class="d-flex flex-wrap">                 <!-- Wrap -->
    <div class="flex-fill">Item</div>
    <div class="flex-fill">Item</div>
</div>
```

#### 8.3 Alignment
```html
<!-- Justify content (horizontal) -->
<div class="d-flex justify-content-start">
<div class="d-flex justify-content-center">
<div class="d-flex justify-content-end">
<div class="d-flex justify-content-between">
<div class="d-flex justify-content-around">
<div class="d-flex justify-content-evenly">

<!-- Align items (vertical) -->
<div class="d-flex align-items-start">
<div class="d-flex align-items-center">
<div class="d-flex align-items-end">
<div class="d-flex align-items-stretch">
<div class="d-flex align-items-baseline">
```

---

### 9. Responsive Design

#### 9.1 Breakpoints
```html
<!-- Bootstrap breakpoints -->
xs: < 576px      (no prefix)
sm: ≥ 576px
md: ≥ 768px
lg: ≥ 992px
xl: ≥ 1200px
xxl: ≥ 1400px
```

#### 9.2 Responsive Utilities
```html
<!-- Responsive display -->
<div class="d-none d-md-block">Tablet and up</div>
<div class="d-lg-none">Below large</div>

<!-- Responsive columns -->
<div class="col-12 col-sm-6 col-md-4 col-lg-3">
    <!-- Full on mobile, half on tablet, 1/3 on desktop, 1/4 on large -->
</div>

<!-- Responsive text alignment -->
<p class="text-start text-md-center text-lg-end">

<!-- Responsive width/height -->
<div class="w-100 h-100">     <!-- 100% width/height -->
<div class="w-75 h-50">       <!-- 75% width, 50% height -->
<div class="mw-100">          <!-- max-width: 100% -->
<div class="mh-100">          <!-- max-height: 100% -->

<!-- Responsive padding/margin -->
<div class="p-2 p-md-4 p-lg-5">
```

---

### 10. Utilities

#### 10.1 Common Utilities
```html
<!-- Borders -->
<div class="border">All borders</div>
<div class="border-top">Top border only</div>
<div class="border-primary">Primary border</div>
<div class="border-1">Thin border</div>
<div class="border-5">Thick border</div>
<div class="rounded">Rounded corners</div>
<div class="rounded-circle">Circle</div>
<div class="rounded-3">Extra rounded</div>

<!-- Shadows -->
<div class="shadow">Box shadow</div>
<div class="shadow-sm">Small shadow</div>
<div class="shadow-lg">Large shadow</div>

<!-- Position -->
<div class="position-relative">Relative</div>
<div class="position-absolute">Absolute</div>
<div class="position-fixed">Fixed</div>

<!-- Overflow -->
<div class="overflow-auto">Auto overflow</div>
<div class="overflow-hidden">Hide overflow</div>

<!-- Float -->
<div class="float-start">Float left</div>
<div class="float-end">Float right</div>
```

#### 10.2 Aspect Ratio
```html
<div class="ratio ratio-16x9">
    <iframe src="..."></iframe>
</div>

<!-- Predefined ratios -->
<div class="ratio ratio-1x1">        <!-- Square -->
<div class="ratio ratio-4x3">        <!-- 4:3 -->
<div class="ratio ratio-16x9">       <!-- 16:9 -->
<div class="ratio ratio-21x9">       <!-- 21:9 -->
```

---

## Quick Reference

### Flask Decorators Summary
```python
@app.route('/')
@app.route('/path/<int:id>')
@login_required
@admin_required
@json_response
@app.errorhandler(404)
@app.before_request
@app.after_request
@app.context_processor
@app.template_filter()
```

### Jinja2 Syntax Summary
```jinja2
{{ variable }}              # Variable interpolation
{% tag %}...{% endtag %}    # Tags
{# comment #}               # Comments
{{ value | filter }}        # Filters
{{ value | filter(arg) }}   # Filter with arguments
{% if condition %}          # Conditionals
{% for item in items %}     # Loops
{% extends "base.html" %}   # Inheritance
{% block name %}{% endblock %} # Blocks
```

### Bootstrap Classes Summary
```
Grid: .container, .row, .col-*, .col-md-6
Spacing: .m-3, .p-3, .mt-4, .mb-2
Display: .d-flex, .d-none, .d-block
Flex: .justify-content-center, .align-items-center
Text: .text-center, .text-primary, .lead
Components: .btn, .card, .table, .form-control
Colors: .bg-primary, .text-danger, .border-info
Utilities: .rounded, .shadow, .border, .position-relative
```

---

## Conclusion

This comprehensive guide covers all major Flask, Jinja2, and Bootstrap 5 concepts used in the application. Use this document as a reference while exploring and extending the application.

Happy coding!
