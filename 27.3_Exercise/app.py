"""Blogly application."""
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config ['SECRET_KEY'] = "amanda1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension

connect_db(app)
db.create_all()

@app.route("/")
def redirect_to_users():
    """redirects to list of users"""
    return redirect("/users")

@app.route("/users")
def show_all_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route("/users/new")
def show_add_form():
    """show add user form"""
    return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Handle form submission"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show info on a single user."""
    user=User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Show Edit Form"""
    user=User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def handle_user_form(user_id):
    """Handle Edited Information"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a User"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    "Show The Post Entry Form"
    user=User.query.get_or_404(user_id)
    tags=Tag.query.all()
    return render_template('post_form.html', user=user, tags=tags)
    
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_post_form(user_id):
    user=User.query.get_or_404(user_id)

    title=request.form['title']
    content=request.form['content']
    
    post_tags=[int(tag) for tag in request.form.getlist('tags')]
    tags=Tag.query.filter(Tag.id.in_(post_tags)).all()

    post = Post(title=title, content=content, user=user, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show user's post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_editpost_form(post_id):
    """Show Edit Form"""
    post=Post.query.get_or_404(post_id)
    tags=Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_editpost_form(post_id):
    """Handle Edited Information"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    post_tags=[int(tag) for tag in request.form.getlist('tags')]
    post.tags=Tag.query.filter(Tag.id.in_(post_tags)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user.id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete Post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()

    return render_template('list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show info on a single tag."""
    tag=Tag.query.get_or_404(tag_id)
    return render_template("tag_details.html", tag=tag)

@app.route("/tags/new")
def show_add_tag_form():
    """show add tag form"""
    return render_template('tag_form.html')

@app.route('/tags/new', methods=["POST"])
def create_tag():
    """Handle form submission"""
    tag_name = request.form["tag_name"]

    tag=Tag(name=tag_name)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_form(tag_id):
    """Show Edit Form"""
    tag=Tag.query.get_or_404(tag_id)
    return render_template('tag_edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_tag_edit_form(tag_id):
    """Handle Edited Information"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a User"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")