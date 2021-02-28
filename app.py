from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'blogly4567'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def redirect_to_users():
    "Redirect user from the root directory to the users list"
    return redirect('/users')

@app.route('/users')
def show_users():
    "Show a full list of all users"
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    "Show the form for submitting a new user"
    return render_template('new-user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Collect the inputs from the form sent to this route, and then commit a new user from those inputs"""
    first = request.form['first']
    last = request.form['last']
    image = request.form['image']

    User.commit_new_user(first=first, last=last, image=image)
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show the details page for the given user. 404 if that user is not found."""
    user = User.query.get_or_404(user_id)
    return render_template('user-details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_user_edit_form(user_id):
    """Show the form to edit a given user's details. 404 if that user is not found."""
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """
    Collect the inputs to the form that were passed, and pass them to the edit method on the user being edited. 
    Redirect to that user's details page.
    """
    user = User.query.get(user_id)

    first = request.form['first']
    last = request.form['last']
    image = request.form['image']

    user.edit(first=first, last=last, image=image)
    
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """
    Delete a user from the database from the ID passed.
    Redirect to the user list.
    """
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')
