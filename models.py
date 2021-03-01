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
        nullable = False,
        db.ForeignKey('users.id')
    )

    user = db.relationship('User', backref='posts')

    @classmethod
    def commit_new_post(cls, user_id, title, content):
        new_post = Post(user_id=user_id, title=title, content=content)
        db.session.add(new_post)
        db.session.commit()