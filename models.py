"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

default_image = 'Images/profile_pic_generic.jpg'

class User(db.Model):
    """ User."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True
                   )
    first_name = db.Column(db.String(50),
                           nullable = False
                           )
    last_name = db.Column(db.String(50), 
                          nullable = False)
    
    image_url = db.Column(db.String(100),
                          nullable = False,
                          default = default_image
                          )
    posts = db.relationship('Post', backref ='user')
    
class Post(db.Model):
    """Post."""
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True
                   )
    title = db.Column( db.Text,
                      nullable=False, unique=True)
    content = db.Column(db.Text,
                        nullable=False, unique=True)
    created_at = db.Column(db.DateTime, 
                           nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)