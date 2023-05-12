from unittest import TestCase
from app import app

from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_tests'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

image_url='https://images.unsplash.com/photo-1681502413474-1bf318cccf22?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80'


class UserModelTestCase(TestCase):
    """Tests model for Users."""

    def setUp(self):
        """Clean up any existing users."""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_User(self):

        user=User(first_name='minnie', last_name='mouse', image_url=image_url)
        
        self.assertEquals(user.first_name, 'minnie')

class PostModelTestCase(TestCase):
    """Tests model for Users."""

    def setUp(self):
        """Clean up any existing users."""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_Post(self):

        post=Post(title="testing", content='testing my model', user_id=1)
        
        self.assertEquals(post.content, 'testing my model')


