from unittest import TestCase
from app import app
from models import db, User

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class TestRoutes(TestCase):

    def setUp(self):
        """Delete existing users, add a new test user to the db, and save the ID to this instance for easy reference"""
        User.query.delete()

        new_user = User(first_name="Test", last_name="Case")
        db.session.add(new_user)
        db.session.commit()

        self.user_id = new_user.id

    def tearDown(self):
        """Rollback any transaction that didn't get committed"""
        db.session.rollback()

    #Test creating new user
    def test_add_user(self):
        """
        Test that we can successfully add a user with all data.
        Then, test that we can add a user with just a first name.
        In both cases, test that the name appears on the user list after redirect.
        """
        user1 = {
            "first": "Daft",
            "last": "Punk",
            "image": "https://upload.wikimedia.org/wikipedia/commons/9/91/DaftAlive.jpeg"
        }
        user2 = {"first": "Banksy", 
                "last": "",
                "image": ""}

        with app.test_client() as client:
            response1 = client.post('/users/new', data=user1, follow_redirects=True)
            html1 = response1.get_data(as_text=True)

            self.assertEqual(response1.status_code, 200)
            self.assertIn("Daft Punk", html1)

            response2 = client.post('/users/new', data=user2, follow_redirects=True)
            html2 = response2.get_data(as_text=True)

            self.assertEqual(response2.status_code, 200)
            self.assertIn("Banksy", html2)

    def test_edit_form(self):
        """Test that the form to edit a user appears as expected when we pass a valid user. When we pass a user that doesn't exist, expect a 404."""
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}/edit')
            html = response.get_data(as_text=True)

            expected_input='<input class="form-control" type="text" name="first" placeholder="Test">'

            self.assertEqual(response.status_code, 200)
            self.assertIn(expected_input, html)

            bad_resp = client.get('users/100')
            self.assertEqual(bad_resp.status_code, 404)



    def test_delete_user(self):
        """Test that when we delete a user and follow the redirect, that user's name no longer appears in the user list!"""
        with app.test_client() as client:
            response = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Test Case", html)
            
    def test_user_details(self):
        """
        Test that we see the image and name we expect to when we look at a user's details page that exists.
        When the page does not exist, expect a 404.
        """
        with app.test_client() as client:
            response1 = client.get(f'/users/{self.user_id}')
            html1 = response1.get_data(as_text=True)
            default_img = '<img class="img-fluid" src="https://images.unsplash.com/photo-1601027847350-0285867c31f7?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=668&amp;q=80">'

            self.assertEqual(response1.status_code, 200)
            self.assertIn(default_img, html1)
            self.assertIn('<h1>Test Case</h1>', html1)

            response2 = client.get('/users/100')
            self.assertEqual(response2.status_code, 404)



