from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """
    The class we'll use to model our user data.
    Users must have a first name and ID.
    Last name is optional.
    Image has a default setting if the user doesn't provide one.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.Text,
                            nullable = False)

    last_name = db.Column(db.Text)

    image = db.Column(db.Text,
                        default= 'https://images.unsplash.com/photo-1601027847350-0285867c31f7?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80')

    def edit(self, first, last, image):
        """
        Update the user's information in the database.
        Any attribute passed with a none value will not be updated.
        """
        if first:
            self.first_name = first
        if last:
            self.last_name = last
        if image:
            self.image = image
        
        db.session.commit()


    @classmethod
    def commit_new_user(cls, first, last, image):
        """Creates a new User instance and commits it to the database"""
        new_user = cls(first_name=first, last_name=last, image=image)
        db.session.add(new_user)
        db.session.commit()

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(
        db.Integer, 
        primary_key = True,
        autoincrement = True
    )

    title = db.Column(
        db.Text,
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.today()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )

    user = db.relationship('User', backref='posts')

    @classmethod
    def commit_new_post(cls, user_id, title, content, tags):
        new_post = Post(user_id=user_id, title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        #Add tags afterwards so that we can use the id returned from SQLA
        if tags:
            for tag in tags:
                tag_int = int(tag)
                post_tag = PostTag(post_id = new_post.id, tag_id = tag_int)
                db.session.add(post_tag)
            db.session.commit()

    def edit(self, title, content, tags):
        self.title = title
        self.content = content

        # loop through all tags to see if we need to add or remove relationships
        all_tags = Tag.query.all()
        for tag in all_tags:
            #Check if a tag was checked in the form that was sent, and if it isn't already in this posts tag add it
            if str(tag.id) in tags:
                if tag not in self.tags:
                    self.tags.append(tag)
            #If the tag is not checked, delete any relationships between the tag and the post
            else:
                PostTag.query.filter_by(post_id = self.id, tag_id = tag.id).delete()

        db.session.commit()

class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    name = db.Column(
        db.Text,
        unique = True,
        nullable = False
    )

    attachments = db.relationship(
        'PostTag',
        backref = 'tag'
    )

    posts = db.relationship(
        'Post',
        secondary = 'posts_tags',
        backref = 'tags'
    )

    @classmethod
    def commit_new_tag(cls, name):
        new_tag = Tag(name=name.lower())
        db.session.add(new_tag)
        db.session.commit()

    def edit(self, name):
        name_lower = name.lower()
        self.name = name_lower
        db.session.commit()


class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key = True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key = True
    )