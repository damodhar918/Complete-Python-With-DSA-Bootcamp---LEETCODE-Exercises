# Flask, Jinja2, and Bootstrap Complete Application

A comprehensive, production-ready blog application demonstrating all Flask, Jinja2, and Bootstrap 5 concepts with clean architecture and best practices.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Flask Topics Covered](#flask-topics-covered)
- [Jinja2 Topics Covered](#jinja2-topics-covered)
- [Bootstrap Topics Covered](#bootstrap-topics-covered)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## ✨ Features

### Core Features
- ✅ User Authentication (Register, Login, Logout)
- ✅ User Profiles with Bio and Avatar
- ✅ Blog Post Creation, Editing, and Deletion
- ✅ Comments System with Delete
- ✅ Post Categories and Search
- ✅ Pagination
- ✅ Admin Dashboard
- ✅ Newsletter Subscription
- ✅ RESTful JSON API
- ✅ Responsive Design (Mobile-First)

### Advanced Features
- ✅ Database Models with Relationships
- ✅ Custom Decorators
- ✅ Template Filters and Context Processors
- ✅ Flash Messages
- ✅ Form Validation
- ✅ Error Handling (404, 500)
- ✅ Admin Only Routes
- ✅ View Tracking
- ✅ Dynamic Statistics

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF & WTForms
- **Database**: SQLite (easily switchable)

### Frontend
- **CSS Framework**: Bootstrap 5.3
- **JavaScript**: Vanilla JS (ES6+)
- **Icons**: Font Awesome 6.4
- **Templating**: Jinja2

### Dependencies
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
WTForms==3.0.1
Werkzeug==2.3.7
```

## 📦 Installation

### Prerequisites
- Python 3.7+
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. **Clone or Navigate to Project**
```bash
cd Flask-Jinja-Bootstrap-Complete
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Application**
```bash
python main.py
```

5. **Access Application**
```
Open browser: http://localhost:5000
```

### Demo Credentials
- **Email**: admin@example.com
- **Password**: admin123

## ⚙️ Configuration

Edit `main.py` to customize:

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

## 📁 Project Structure

```
Flask-Jinja-Bootstrap-Complete/
├── main.py                          # Main Flask application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── templates/
│   ├── base.html                   # Base template with navbar/footer
│   ├── index.html                  # Home page
│   ├── register.html               # User registration
│   ├── login.html                  # User login
│   ├── dashboard.html              # User dashboard
│   ├── posts_list.html             # Blog posts listing
│   ├── post_detail.html            # Single post view
│   ├── create_post.html            # Create post form
│   ├── edit_post.html              # Edit post form
│   ├── profile.html                # User profile
│   ├── edit_profile.html           # Edit profile
│   ├── about.html                  # About page
│   ├── contact.html                # Contact form
│   ├── admin_dashboard.html        # Admin dashboard
│   ├── admin_users.html            # User management
│   ├── admin_posts.html            # Post management
│   ├── 404.html                    # 404 error page
│   ├── 403.html                    # 403 error page
│   └── 500.html                    # 500 error page
└── static/
    ├── css/
    │   └── (Bootstrap via CDN)
    └── js/
        └── (Custom JavaScript)
```

## 🔥 Flask Topics Covered

### 1. **Core Flask Concepts**
- Application Factory Pattern
- Route Definition (`@app.route()`)
- HTTP Methods (GET, POST, PUT, DELETE)
- Request/Response Handling
- URL Building with `url_for()`

### 2. **Database**
- SQLAlchemy ORM
- Model Definition
- Relationships (One-to-Many, Foreign Keys)
- Database Migrations
- Query Operations

### 3. **Authentication & Authorization**
- Flask-Login Extension
- User Authentication
- Password Hashing (Werkzeug)
- Session Management
- Login Required Decorator
- Admin Role System

### 4. **Forms**
- Flask-WTF Forms
- Form Validation
- CSRF Protection
- Field Types and Validators
- Error Display

### 5. **Templates & Rendering**
- Template Inheritance
- Block Override
- Static Files
- Flash Messages
- Template Context

### 6. **Advanced Features**
- Custom Decorators
- Context Processors
- Template Filters
- Error Handlers
- API Routes (JSON)

### 7. **Middleware & Hooks**
- Before/After Request Handlers
- Error Handlers
- Login Manager Callbacks

## 🎨 Jinja2 Topics Covered

### 1. **Template Basics**
- Variable Interpolation: `{{ variable }}`
- Tag Syntax: `{% tag %}`
- Comments: `{# comment #}`
- Template Inheritance: `{% extends %}`

### 2. **Control Structures**
- Conditional: `{% if %} {% elif %} {% else %}`
- Loops: `{% for item in list %}`
- Loop Filters: `loop.first`, `loop.last`, `loop.index`

### 3. **Template Inheritance**
```html
{% extends "base.html" %}
{% block content %}...{% endblock %}
```

### 4. **Filters**
- Built-in: `upper`, `lower`, `length`, `date`, `default`
- Custom Filters: `datetimeformat`, `word_count`
- Filter Chaining: `{{ text | upper | length }}`

### 5. **Tests**
```jinja2
{% if user.is_authenticated %}
{% if posts|length > 0 %}
{% if post.id == current_post.id %}
```

### 6. **Macros**
- Reusable template code
- Parameters and defaults
- Macro calls

### 7. **Set & Assignment**
```jinja2
{% set total = posts|length %}
{% set active = 'active' if page == 1 %}
```

### 8. **Context & Scope**
- Global variables
- Context processors
- Template globals
- Local scope

## 🎯 Bootstrap Topics Covered

### 1. **Grid System**
- Containers (`.container`, `.container-fluid`)
- Rows and Columns (`.row`, `.col-*`)
- Responsive Breakpoints (xs, sm, md, lg, xl, xxl)
- Gutters and Spacing

### 2. **Components**
- Navigation Bar (`.navbar`)
- Cards (`.card`)
- Buttons (`.btn`, `.btn-*`)
- Forms (`.form-control`, `.form-label`)
- Alerts (`.alert`)
- Badges (`.badge`)
- Pagination (`.pagination`)
- Breadcrumbs (`.breadcrumb`)
- Tables (`.table`)
- Modals (`.modal`)

### 3. **Typography**
- Headings (h1-h6)
- Paragraphs and Text
- Emphasis (`<strong>`, `<em>`)
- Lists (ordered, unordered)
- Blockquotes

### 4. **Spacing & Layout**
- Margins (`.m-*`, `.ms-*`, `.mt-*`)
- Padding (`.p-*`, `.ps-*`, `.pt-*`)
- Display Classes (`.d-flex`, `.d-block`, `.d-none`)
- Text Alignment (`.text-center`, `.text-start`)

### 5. **Colors & Utilities**
- Text Colors (`.text-primary`, `.text-danger`)
- Background Colors (`.bg-primary`, `.bg-light`)
- Opacity (`.opacity-*`)
- Shadows (`.shadow`, `.shadow-sm`)
- Borders (`.border`, `.border-*`)

### 6. **Forms**
- Input Groups (`.input-group`)
- Select Dropdowns (`.form-select`)
- Checkboxes and Radios
- Form Validation (`.is-invalid`, `.is-valid`)
- Floating Labels

### 7. **Responsive Design**
- Mobile-First Approach
- Breakpoint-Specific Classes (`.d-none`, `.d-md-block`)
- Responsive Images (`.img-fluid`)
- Responsive Navigation

### 8. **Flexbox Utilities**
- Flex Direction (`.flex-row`, `.flex-column`)
- Justify Content (`.justify-content-*`)
- Align Items (`.align-items-*`)
- Gap (`.gap-*`)

### 9. **JavaScript Components**
- Dropdowns
- Modals
- Tooltips
- Popovers
- Scrollspy

### 10. **Customization**
- CSS Variables (`:root`)
- Utility Classes
- Custom Styling
- Theme Colors

## 🚀 Usage

### Create Account
1. Click "Register" in navigation
2. Enter username, email, password
3. Submit form

### Create a Post
1. Login to your account
2. Click "Write a Post" or go to Dashboard
3. Fill in title, select category, write content
4. Click "Publish Post"

### Comment on Posts
1. View a post
2. Scroll to comments section
3. Login (if required)
4. Write and submit comment

### Subscribe to Newsletter
1. Scroll to footer
2. Enter email in newsletter form
3. Click Subscribe

### Access Admin Panel
1. Login with admin account
2. Click admin icon in navbar
3. Manage users and posts

## 🔌 API Endpoints

### Posts
- `GET /api/posts` - Get all posts
- `GET /api/post/<id>` - Get single post

### Statistics
- `GET /api/stats` - Get site statistics

### Example API Call
```bash
curl http://localhost:5000/api/posts
```

Response:
```json
{
  "posts": [
    {
      "id": 1,
      "title": "Post Title",
      "author": "username",
      "created_at": "2024-01-01T10:00:00",
      "views": 42
    }
  ]
}
```

## 📝 Database Models

### User Model
```python
- id (Primary Key)
- username (Unique, String)
- email (Unique, String)
- password_hash (String)
- bio (Text)
- avatar_url (String)
- created_at (DateTime)
- is_admin (Boolean)
- Relationships: posts, comments
```

### Post Model
```python
- id (Primary Key)
- title (String)
- content (Text)
- category (String)
- created_at (DateTime)
- updated_at (DateTime)
- views (Integer)
- user_id (Foreign Key)
- Relationships: comments, author
```

### Comment Model
```python
- id (Primary Key)
- text (Text)
- created_at (DateTime)
- user_id (Foreign Key)
- post_id (Foreign Key)
- Relationships: author, post
```

### Newsletter Model
```python
- id (Primary Key)
- email (Unique, String)
- subscribed_at (DateTime)
- is_active (Boolean)
```

## 🎓 Learning Paths

### Beginner
1. Understand Flask basics with `index` and `about` routes
2. Learn templates with `base.html`
3. Study Bootstrap grid with responsive layouts

### Intermediate
1. Implement authentication with login/register
2. Create database models and relationships
3. Use forms with validation

### Advanced
1. Build admin features
2. Create API endpoints
3. Implement decorators and middleware
4. Custom filters and context processors

## 🔒 Security Features

- ✅ CSRF Protection (Flask-WTF)
- ✅ Password Hashing (Werkzeug)
- ✅ Session Management
- ✅ SQL Injection Prevention (SQLAlchemy)
- ✅ XSS Prevention (Jinja2 Auto-escaping)
- ✅ Authorization Checks

## 📱 Responsive Breakpoints

- **xs**: < 576px (Mobile)
- **sm**: ≥ 576px (Tablet)
- **md**: ≥ 768px (Small Laptop)
- **lg**: ≥ 992px (Laptop)
- **xl**: ≥ 1200px (Desktop)
- **xxl**: ≥ 1400px (Large Desktop)

## 🚨 Error Handling

- 404: Page Not Found
- 403: Forbidden (Permission Denied)
- 500: Internal Server Error

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)

## 💡 Tips & Best Practices

1. **Use Template Inheritance** - Avoid code duplication
2. **Leverage Jinja2 Filters** - Keep templates clean
3. **Custom Decorators** - Reuse authorization logic
4. **Context Processors** - Make data available globally
5. **Bootstrap Utilities** - Reduce custom CSS
6. **Error Handlers** - Provide user-friendly error pages
7. **Pagination** - Handle large datasets efficiently
8. **Flash Messages** - Provide user feedback
9. **Form Validation** - Validate both client and server side
10. **Database Indexes** - Optimize queries

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Database Issues
```bash
# Remove existing database and recreate
rm app.db
python main.py
```

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a comprehensive learning resource for Flask, Jinja2, and Bootstrap.

---

**Happy Coding!** 🎉 Feel free to modify and extend this project to learn more about web development with Flask.
