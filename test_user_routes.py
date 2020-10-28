from app import app, CURR_USER_KEY
import os
from unittest import TestCase
from users import check_confirmed_pwd

from models import db, User, Bookmark, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


class UserRoutesTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user1 = User.signup(email='email1@gmail.com', password='user1password', username='username_1',
                                 image_url=None)
        self.user2 = User.signup(email='email2@gmail.com', password='user2password', username='username_2',
                                 image_url=None)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_register(self):
        with self.client as c:
            resp = c.get('/register')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username', str(resp.data))
            self.assertIn('Password', str(resp.data))
            self.assertIn(
                '<button class="btn btn-success" type="submit">Register</button>', str(resp.data))

    def test_login(self):
        with self.client as c:
            resp = c.get('/login')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username', str(resp.data))
            self.assertIn('Password', str(resp.data))
            self.assertIn(
                '<button class="btn btn-success" type="submit">Login</button>', str(resp.data))

    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            resp = c.get('/logout', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username', str(resp.data))
            self.assertIn('Password', str(resp.data))
            self.assertIn(
                '<button class="btn btn-success" type="submit">Login</button>', str(resp.data))

    def test_user_profile(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            resp = c.get(f'/users/{self.user1.username}')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>username_1</h3>', str(resp.data))
            self.assertIn('<h5>Decks: 0</h5>', str(resp.data))

    def test_edit_profile(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            resp = c.get(f'/users/{{self.user1.username}}/edit')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Email', str(resp.data))
            self.assertIn('Password', str(resp.data))
            self.assertIn('Confirm Password', str(resp.data))
            self.assertIn('Profile Picture', str(resp.data))
