from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_app_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Disable Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    '''Test for views for users'''
    
    def setUp(self):
        '''Add sample user'''
        
        user= User(first_name='Mohan', last_name='Chand', img_url='https://www.freeiconspng.com/img/896')
        db.session.add(user)
        db.session.commit()
        
        self.user.id=user.id
        
    
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        
    def test_list_users(self):
        with app.test_client() as client:
            resp: client.get('/')
            html=resp.get_data(as_Text=True)
            
            self.assertEqual(resp.status.code, 200)
            self.assertIn('<h1>Mohan</h1>', html)
            
    def test_show_user(self):
        with app.test_client() as client:
            resp: client.get(f'/users/{self.user.id}')
            html=resp.get_data(as_Text=True)
            
            self.assertEqual(resp.status.code, 200)
            self.assertIn('<h1>Mohan</h1>', html)
            
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUser", "last_name": "test"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestUser</h1>", html)
            
    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name": "test"}
            resp = client.post(f"/users/{self.user.id}/edit", data=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestUser2</h1>", html)