"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag
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
def homepage():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)
    

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
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post_submit(user_id):
    '''Handle form submit on create new post page'''
    
    user = User.query.get_or_404(user_id)
    tag_ids = [int(n) for n in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user,  tags=tags)
    db.session.add(new_post)
    db.session.commit()
    flash('New Post added!')
    return redirect(f'/users/{user_id}', user=user, tags=tags)

@app.route('/posts/<int:post_id>')
def list_posts(post_id):
    '''Show post'''
    post = Post.query.get_or_404(post_id)
    return render_template('post_list.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show edit post page once clicked on edit"""
    
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("post_edit.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_submit(post_id):
    """Update post once form is submitted"""
    
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'],
    post.content = request.form['content'],
        
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")

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
    flash(f'Post {post.title} deleted!')
    return redirect('/')


######################################
#Tags routes >>>>>>>

@app.route('/tags')
def list_tags():
    '''List of all the tags'''
    tags = Tag.query.all()
    return render_template('tags/list_tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    '''Show tag details'''
    
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag_detail.html', tag=tag)


@app.route('/tags/new')
def new_tag():
    '''Show page to add a new tag'''
    posts = Post.query.all()
    return render_template('tags/add_tag.html', posts=posts)


@app.route('/tags/new', methods=['POST'])
def new_tag_submit():
    '''Handle form submit on create new tag page'''
    
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name = request.form['tag'], posts = posts)
    
    db.session.add(new_tag)
    db.session.commit()
    flash(f'{new_tag.name} added!')
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show edit tag page once clicked on edit"""
    
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("tags/tag_edit.html", tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_submit(tag_id):
    '''Handle form submit on edit tag page'''

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Show delete tag page once clicked on edit"""
    
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/confirm_tag_delete.html', tag=tag)

@app.route('/tags/<int:tag_id>/delete/confirm')
def confirm_tag_delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    
    flash(f'Tag: {tag.name} deleted!')
    return redirect('/tags')