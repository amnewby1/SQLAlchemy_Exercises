"""Seed file to make sample data for db."""
from models import db, User, Post, PostTag, Tag
from app import app

"""Drop and create all tables"""
db.drop_all()
db.create_all()


"""Emptied out the tables"""
PostTag.query.delete()
Post.query.delete()
Tag.query.delete()
User.query.delete

"""Add sample users and posts"""
image_url='https://images.unsplash.com/photo-1681502413474-1bf318cccf22?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80'

daffy=User(first_name='daffy', last_name='duck', image_url=image_url)
mickey=User(first_name='mickey', last_name='mouse', image_url=image_url)
chuck=User(first_name='chuck', last_name='norris', image_url=image_url)
lucy=User(first_name='lucy', last_name='liu', image_url=image_url)

"""Add and commit users"""

db.session.add_all([daffy, mickey, chuck, lucy])
db.session.commit()

"""Make sample posts"""

daffy_post=Post(title="Water", content='I love water!', user_id=daffy.id)
mickey_post=Post(title='Cats', content='I hate cats!', user_id=mickey.id)
chuck_post=Post(title="Jokes", content="I love Chuck Norris jokes!", user_id=chuck.id)
lucy_post=Post(title="Angel", content="I am an angel!", user_id=lucy.id)

"""Add and commit posts"""
db.session.add_all([daffy_post, mickey_post, chuck_post, lucy_post])
db.session.commit()

"""Made example tags"""

fun_tag = Tag(name='fun')
lame_tag=Tag(name='lame')
yolo_tag=Tag(name='yolo')
winning_tag=Tag(name='winning')

"""add and commit tags"""
db.session.add_all([fun_tag, lame_tag, yolo_tag, winning_tag])
db.session.commit()