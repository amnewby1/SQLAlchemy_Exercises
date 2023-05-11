"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User (db.Model): 
    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
  
    first_name = db.Column(db.String(15),
                     nullable = False) 
    
    last_name = db.Column(db.String(15),
                     nullable = False) 
    
    image_url = db.Column(db.String,
                          nullable=False)
    
    
class Post (db.Model): 
    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
  
    title = db.Column(db.String(50),
                     nullable = False) 
    
    content = db.Column(db.String,
                     nullable = False) 
    
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user=db.relationship('User', backref='post')

    tags=db.relationship('Tag', secondary='posts_tags', backref='posts')

    
class Tag(db.Model):

    __tablename__='tags'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    name=db.Column(db.String(20), nullable=False, unique=True)

class PostTag(db.Model):

    __tablename__='posts_tags'

    post_id=db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id=db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
