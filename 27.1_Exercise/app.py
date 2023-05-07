"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy import text

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

@app.route('/<int:user_id>')
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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")