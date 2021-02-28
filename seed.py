from models import User, db
from app import app

# Drop tables if they already exist, and then create them again
db.drop_all()
db.create_all()

# Delete all entries if there are any
User.query.delete()

# Seed some users
matty = User(first_name='Matthew', last_name='Yglesias', image='https://static01.nyt.com/images/2020/07/30/books/review/Salmon1/Salmon1-superJumbo.jpg?quality=90&auto=webp')
cher = User(first_name='Cher', image='https://i.guim.co.uk/img/media/34deec3b589c8b2d4e3aeb135d6be1f36393ccf6/0_4_2118_1270/master/2118.jpg?width=1300&quality=45&auto=format&fit=max&dpr=2&s=f43d40b80eb2611f61c8be5af24d7c44')
dev = User(first_name='Devlin', last_name='Brush')

# Add them to the session and commmit
db.session.add_all([matty, cher, dev])
db.session.commit()