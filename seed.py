from models import User, Post, db, Tag, PostTag
from app import app

# Drop tables if they already exist, and then create them again
db.drop_all()
db.create_all()

# Delete all entries if there are any
User.query.delete()
PostTag.query.delete()
Post.query.delete()
Tag.query.delete()


# Seed some users
matty = User(first_name='Matthew', last_name='Yglesias', image='https://static01.nyt.com/images/2020/07/30/books/review/Salmon1/Salmon1-superJumbo.jpg?quality=90&auto=webp')
cher = User(first_name='Cher', image='https://i.guim.co.uk/img/media/34deec3b589c8b2d4e3aeb135d6be1f36393ccf6/0_4_2118_1270/master/2118.jpg?width=1300&quality=45&auto=format&fit=max&dpr=2&s=f43d40b80eb2611f61c8be5af24d7c44')
dev = User(first_name='Devlin', last_name='Brush')

# Commit users first 
db.session.add_all([matty, cher, dev])
db.session.commit()

#Seed posts
post1 = Post(title="1 Billion Americans", content="There should be a lot of Americans. Slow boring is the name of my blog. It's ya boi Matt.", user_id=1)
post2 = Post(title="Do you Believe?", content="In life after love. I can feel something inside myself.", user_id=2)
post3 = Post(title="I'm back.", content="It's me, Matt, and I'm back again. Legend in the blog game. Vox is weak.", user_id=1)

#Commit posts
db.session.add_all([post1, post2, post3])
db.session.commit()

#Seed some tags and append posts
politics = Tag(name="politics")
politics.posts.append(post1)
politics.posts.append(post3)

music = Tag(name="music")
music.posts.append(post2)

#Commit tags
db.session.add_all([politics, music])
db.session.commit()