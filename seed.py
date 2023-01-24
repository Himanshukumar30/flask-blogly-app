"""Seed file to make sample data for blogly db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
Tom = User(first_name='Tom', last_name='Miller')
Molly = User(first_name='Molly', last_name="Freeman")

# Add new objects to session, so they'll persist
db.session.add(Tom)
db.session.add(Molly)

# Commit--otherwise, this never gets saved!
db.session.commit()
