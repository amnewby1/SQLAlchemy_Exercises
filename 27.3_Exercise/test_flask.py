from unittest import TestCase
from app import app

from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_tests'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING']=True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

image_url='https://images.unsplash.com/photo-1681502413474-1bf318cccf22?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80'


class BloglyTestCase(TestCase):
    
    def setUp(self):
        PostTag.query.delete() 
        Post.query.delete() 
        User.query.delete()
        Tag.query.delete()
        

        user=User(first_name='minnie', last_name='mouse', image_url=image_url)
        db.session.add(user)
        db.session.commit()

        post=Post(title="testing", content='testing my model', user_id=user.id)
        tag=Tag(name='testing')
        db.session.add_all([post, tag])
        db.session.commit()

        posttag=PostTag(post_id=post.id, tag_id=tag.id)
        db.session.add(posttag)
        db.session.commit()
        

        self.user_id=user.id
        self.user=user

        self.post_id=post.id
        self.post=post

        self.tag_id=tag.id
        self.tag=tag

        self.post_tag=posttag.tag_id
        self.posttag=posttag

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp=client.get("/users")
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('minnie', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp=client.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>minnie mouse</h1>', html)
            self.assertIn(self.user.first_name, html)
    
    def test_add_user(self):
        with app.test_client() as client:
            d={"first_name": "drew", "last_name": "barrymore", "image_url": image_url}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn("drew", html)