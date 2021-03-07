from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SECRET_KEY'] = 'blogly4567'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

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
    If they have any posts, delete those first to not violate fK restraints.
    Redirect to the user list.
    """
    user = User.query.get(user_id)
    for post in user.posts:
        Post.query.filter_by(id=post.id).delete()

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """
    Show the form to add a new post for a given user.
    """
    user = User.query.get(user_id)
    all_tags = Tag.query.all()
    return render_template('new-post.html', user=user, all_tags=all_tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """
    Take the data from the submission of a new post form and make a new record of a Post in the database.
    Redirect to the details page of the user who posted.
    """
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')

    Post.commit_new_post(user_id=user_id, title=title, content=content, tags=tags)
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """
    Show all of the contents of a post.
    """
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = post.tags
    timestamp = post.created_at.strftime("%a %b %d %Y, %I:%M %p")

    return render_template('post.html', post=post, user=user, tags=tags, timestamp=timestamp)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """
    Show the form to edit a post.
    Pass the post's tags so that they will be pre-checked when the user sees the form.
    """
    post = Post.query.get_or_404(post_id)
    all_tags = Tag.query.all()
    post_tags = post.tags

    return render_template('post-edit.html', post=post, all_tags=all_tags, post_tags=post_tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """
    Take the data from the form for editing a post, and pass it to the method to edit the post.
    Redirect back to the post details.
    """
    post = Post.query.get(post_id)
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')

    post.edit(title=title, content=content, tags=tags)
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """
    First, delete any tag relationships to this post so that there are no FK violations.
    Then, delete the post and redirect to the user's page.
    """
    post = Post.query.get(post_id)
    user_id = post.user.id 

    PostTag.query.filter_by(post_id=post_id).delete()
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/tags')
def show_tags():
    """
    Show the list of all tags.
    Tags have links to the tag details pages.
    """
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/new')
def add_tag_form():
    """
    Show the form for adding a new tag.
    """
    return render_template('new-tag.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    """
    Process a new tag submitted from the form and commit it to the database.
    Redirect to the list of tags.
    """
    name = request.form['name']
    Tag.commit_new_tag(name)
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """
    Show the posts associated with a given tag, if there are any.
    This route also allows the user to edit or delete a tag.
    """
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag-details.html', tag = tag, posts = posts)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """
    Show the form for editing the name of a tag, if the tag exists.
    """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """
    Handle the submission of the form for editing a tag, and commit changes to the db.
    Redirect to the tag details page.
    """
    tag = Tag.query.get(tag_id)
    name = request.form['name']

    tag.edit(name)
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """
    Delete the tag with the ID in the URL.
    First delete any tag/post relationships so you don't violate FK restraints.
    """
    PostTag.query.filter_by(tag_id=tag_id).delete()
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect('/tags')