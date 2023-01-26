"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app) 
db.create_all()

@app.route('/')
def root():
    return redirect('/users')
    

######################################
#Users routes >>>>>>>

@app.route('/users')
def list_users(): 

    """List all the users on homepage"""
    
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show user details"""

    user = User.query.get_or_404(user_id)
    return render_template("user_info.html", user=user)

@app.route('/users/new')
def add_user():
    """Show form to create new user"""
    
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_user_submit():
    """Create new user once form is submitted"""
    
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    flash('New User added!')
    return redirect(f"{new_user.id}")

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit user page once clicked on edit"""
    
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_submit(user_id):
    """Update user details once form is submitted"""
    
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url'] or None
        
    db.session.add(user)
    db.session.commit()
    flash('User Details Updated!')
    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Show delete user page once clicked on edit"""
    user = User.query.get_or_404(user_id)
    return render_template('confirm_delete.html', user=user)

@app.route('/users/<int:user_id>/delete/confirm')
def confirm_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted!')
    return redirect('/users')

######################################
#Post routes >>>>>>>

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    '''Show form to create post for a specific user'''
    
    user = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post_submit(user_id):
    '''Handle form submit on create new post page'''
    
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    flash('New Post added!')
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def list_posts(post_id):
    '''Show post'''
    post = Post.query.get_or_404(post_id)
    return render_template('post_list.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show edit post page once clicked on edit"""
    
    post = Post.query.get_or_404(post_id)
    return render_template("post_edit.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_submit(post_id):
    """Update post once form is submitted"""
    
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'],
    post.content = request.form['content'],
        
    db.session.add(post)
    db.session.commit()
    flash(f'Post {post.title} Updated!')
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Show delete post page once clicked on edit"""
    post = Post.query.get_or_404(post_id)
    return render_template('confirm_post_delete.html', post=post)

@app.route('/posts/<int:post_id>/delete/confirm')
def confirm_post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!')
    return redirect('/')