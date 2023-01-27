"""Seed file to make sample data for blogly db."""

from models import User, db, Post, Tag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
Tom = User(first_name='Tom', last_name='Miller')
Tom1 = User(first_name='Tom', last_name='Richard')
Molly = User(first_name='Molly', last_name="Freeman")
Richa = User(first_name='Richa', last_name='Khanna')
Angel = User(first_name='Angel', last_name='McDowell')

#Add Tags
# meditate = Tag(name = 'meditate')
# self_help = Tag(name ='self-help')
# mindfulness = Tag(name = 'mindfulness')

# Add new objects to session, so they'll persist
db.session.add_all([Tom,Tom1,Molly,Richa,Angel])

# Commit--otherwise, this never gets saved!
db.session.commit()
