from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'demo12323'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def redirect_to_users():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    return render_template('new-user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    first = request.form['first']
    last = request.form['last'] if request.form['last'] else None
    image = request.form['image'] if request.form['image'] else None

    User.commit_new_user(first=first, last=last, image=image)
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_user_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get(user_id)

    first = request.form['first'] if request.form['last'] else None
    last = request.form['last'] if request.form['last'] else None
    image = request.form['image'] if request.form['image'] else None

    user.edit(first=first, last=last, image=image)
    
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    
    return redirect('/users')
