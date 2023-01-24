"""Blogly application."""

from flask import Flask, render_template, redirect
from models import db, connect_db, User
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
    
    
@app.route('/users')
def list_users(): 

    """List all the users on homepage"""
    
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route("/users/<int:user_id>")
def show_pet(user_id):
    """Show user details"""

    user = User.query.get_or_404(user_id)
    return render_template("user_info.html", user=user)

