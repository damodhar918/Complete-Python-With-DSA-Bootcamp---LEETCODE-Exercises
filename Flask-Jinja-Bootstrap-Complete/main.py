"""
Complete Flask, Jinja2, and Bootstrap Application
Covers: Routing, Templates, Forms, Database, Authentication, API, and more
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps
from io import BytesIO
import json

# ==================== FLASK APP INITIALIZATION ====================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# ==================== DATABASE MODELS ====================
class User(UserMixin, db.Model):
    """User model with authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, default='')
    avatar_url = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """Blog post model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'


class Comment(db.Model):
    """Comment model"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment by {self.author.username}>'


class Newsletter(db.Model):
    """Newsletter subscription model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


# ==================== LOGIN MANAGER ====================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== FLASK FORMS ====================
class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')


class PostForm(FlaskForm):
    """Create/edit post form"""
    title = StringField('Post Title', 
                       validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', 
                           validators=[DataRequired(), Length(min=10)])
    category = SelectField('Category', 
                          choices=[('General', 'General'), 
                                 ('Technology', 'Technology'),
                                 ('Travel', 'Travel'),
                                 ('Food', 'Food'),
                                 ('Other', 'Other')])


class CommentForm(FlaskForm):
    """Add comment form"""
    text = TextAreaField('Comment', 
                        validators=[DataRequired(), Length(min=1, max=500)])


class NewsletterForm(FlaskForm):
    """Newsletter subscription form"""
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])


# ==================== DECORATORS ====================
def admin_required(f):
    """Decorator to require admin status"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def json_response(f):
    """Decorator to return JSON response"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = f(*args, **kwargs)
        return jsonify(result) if isinstance(result, dict) else result
    return decorated_function


# ==================== ROUTES - HOME & BASIC ====================
@app.route('/')
def index():
    """Home page"""
    featured_posts = Post.query.order_by(Post.views.desc()).limit(5).all()
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.count(),
        'total_comments': Comment.query.count(),
        'subscribers': Newsletter.query.filter_by(is_active=True).count()
    }
    return render_template('index.html', featured_posts=featured_posts, stats=stats)


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Here you would send email
        flash(f'Thank you {name}! Your message has been received.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')


# ==================== ROUTES - AUTHENTICATION ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ==================== ROUTES - USER PROFILE ====================
@app.route('/user/<username>')
def user_profile(username):
    """View user profile"""
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    return render_template('profile.html', user=user, posts=posts)


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_posts = current_user.posts
    recent_comments = Comment.query.filter_by(user_id=current_user.id).order_by(Comment.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', posts=user_posts, comments=recent_comments)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        current_user.bio = request.form.get('bio', '')
        current_user.avatar_url = request.form.get('avatar_url', '')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user_profile', username=current_user.username))
    
    return render_template('edit_profile.html', user=current_user)


# ==================== ROUTES - BLOG POSTS ====================
@app.route('/posts')
def posts_list():
    """List all blog posts with pagination"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Post.query
    
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Post.title.ilike(f'%{search}%') | Post.content.ilike(f'%{search}%'))
    
    posts = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    categories = db.session.query(Post.category).distinct().all()
    
    return render_template('posts_list.html', posts=posts, categories=categories, search=search, category=category)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """View single blog post"""
    post = Post.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()
    
    form = CommentForm()
    comments = post.comments
    
    return render_template('post_detail.html', post=post, form=form, comments=comments)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create new blog post"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, 
                   content=form.content.data,
                   category=form.category.data,
                   user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('view_post', post_id=post.id))
    
    return render_template('create_post.html', form=form)


@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit blog post"""
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        flash('You do not have permission to edit this post.', 'danger')
        return redirect(url_for('view_post', post_id=post.id))
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('view_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
    
    return render_template('edit_post.html', form=form, post=post)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete blog post"""
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        return jsonify({'error': 'Permission denied'}), 403
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


# ==================== ROUTES - COMMENTS ====================
@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add comment to post"""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, 
                         user_id=current_user.id,
                         post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    
    return redirect(url_for('view_post', post_id=post.id))


@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Delete comment"""
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.author != current_user:
        return jsonify({'error': 'Permission denied'}), 403
    
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!', 'success')
    return redirect(url_for('view_post', post_id=post_id))


# ==================== ROUTES - NEWSLETTER ====================
@app.route('/subscribe', methods=['POST'])
@json_response
def subscribe_newsletter():
    """Subscribe to newsletter"""
    email = request.form.get('email') or request.json.get('email')
    
    if not email:
        return {'success': False, 'message': 'Email is required'}
    
    existing = Newsletter.query.filter_by(email=email).first()
    if existing:
        return {'success': False, 'message': 'Already subscribed'}
    
    subscriber = Newsletter(email=email)
    db.session.add(subscriber)
    db.session.commit()
    
    return {'success': True, 'message': 'Subscribed successfully!'}


@app.route('/unsubscribe/<email>')
def unsubscribe(email):
    """Unsubscribe from newsletter"""
    subscriber = Newsletter.query.filter_by(email=email).first_or_404()
    subscriber.is_active = False
    db.session.commit()
    flash('You have been unsubscribed.', 'info')
    return redirect(url_for('index'))


# ==================== ROUTES - ADMIN ====================
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    stats = {
        'users': User.query.count(),
        'posts': Post.query.count(),
        'comments': Comment.query.count(),
        'subscribers': Newsletter.query.filter_by(is_active=True).count(),
        'recent_users': User.query.order_by(User.created_at.desc()).limit(5).all(),
        'recent_posts': Post.query.order_by(Post.created_at.desc()).limit(5).all()
    }
    return render_template('admin_dashboard.html', stats=stats)


@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin_users.html', users=users)


@app.route('/admin/posts')
@login_required
@admin_required
def admin_posts():
    """Manage posts"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=20)
    return render_template('admin_posts.html', posts=posts)


# ==================== API ROUTES ====================
@app.route('/api/posts', methods=['GET'])
@json_response
def api_get_posts():
    """API: Get all posts"""
    posts = Post.query.all()
    return {
        'posts': [{
            'id': p.id,
            'title': p.title,
            'author': p.author.username,
            'created_at': p.created_at.isoformat(),
            'views': p.views
        } for p in posts]
    }


@app.route('/api/post/<int:post_id>', methods=['GET'])
@json_response
def api_get_post(post_id):
    """API: Get single post"""
    post = Post.query.get_or_404(post_id)
    return {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'created_at': post.created_at.isoformat(),
        'views': post.views,
        'comments_count': len(post.comments)
    }


@app.route('/api/stats', methods=['GET'])
@json_response
def api_stats():
    """API: Get site statistics"""
    return {
        'users': User.query.count(),
        'posts': Post.query.count(),
        'comments': Comment.query.count(),
        'subscribers': Newsletter.query.filter_by(is_active=True).count()
    }


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return render_template('403.html'), 403


# ==================== CONTEXT PROCESSORS ====================
@app.context_processor
def inject_categories():
    """Make categories available in all templates"""
    categories = db.session.query(Post.category).distinct().all()
    return {'categories': [c[0] for c in categories]}


@app.context_processor
def inject_newsletter_form():
    """Make newsletter form available in all templates"""
    return {'newsletter_form': NewsletterForm()}


# ==================== TEMPLATE FILTERS ====================
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    """Format datetime in templates"""
    if value is None:
        return ''
    return value.strftime(format)


@app.template_filter('word_count')
def word_count(text):
    """Count words in text"""
    return len(text.split()) if text else 0


# ==================== RUN APP ====================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create sample data if database is empty
        if User.query.count() == 0:
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            
            user1 = User(username='john', email='john@example.com', bio='Developer & Blogger')
            user1.set_password('password123')
            db.session.add(user1)
            
            db.session.commit()
            
            # Create sample posts
            post1 = Post(title='Getting Started with Flask',
                        content='Flask is a lightweight web framework for Python...',
                        category='Technology',
                        user_id=user1.id)
            db.session.add(post1)
            db.session.commit()
    
    app.run(debug=True, port=5000)
