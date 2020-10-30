from app import app
import os
from unittest import TestCase

from models import db, User, Bookmark, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


def test(username, password, email, image_url):
    user = User.signup(email=email, password=password, username=username,
                       image_url=image_url)
    db.session.commit()


class UserModelTestCase(TestCase):
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

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.user1.decks), 0)
        self.assertEqual(len(self.user1.bookmarked_cards), 0)
        self.assertEqual(len(self.user1.friends), 0)
        self.assertEqual(len(self.user1.posts), 0)

    def test_user_model_repr(self):
        """Does basic model repr work?"""
        # User should have no messages & no followers
        self.assertEqual(
            f'{self.user1}', f'<User {self.user1.username}>')

    def test_user_signup(self):
        """Test that signup class method works"""
        self.assertEqual(self.user1.username, 'username_1')
        self.assertTrue(bcrypt.check_password_hash(
            self.user1.password, 'user1password'))
        self.assertEqual(self.user1.email, 'email1@gmail.com')
        self.assertEqual(self.user1.image_url,
                         "/static/images/default_prof_pic.png")

    def test_user_authenticate(self):
        """Test that authenticate class method works"""
        self.assertEqual(User.authenticate(
            username=self.user1.username, password='user1password'), self.user1)
        self.assertFalse(User.authenticate(
            username=self.user1.username, password='user2password'))
        self.assertFalse(User.authenticate(
            username=self.user2.username, password='user1password'))
        self.assertFalse(User.authenticate(
            username='someotherusername', password='someotherpassword'))
