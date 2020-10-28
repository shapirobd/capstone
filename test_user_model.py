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

    # def tearDown(self):
    #     db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.decks), 0)
        self.assertEqual(len(u.bookmarked_cards), 0)
        self.assertEqual(len(u.friends), 0)
        self.assertEqual(len(u.posts), 0)

    # **********
    # Does the repr method work as expected?
    # **********

    def test_user_model_repr(self):
        """Does basic model repr work?"""
        # User should have no messages & no followers
        self.assertEqual(
            f'{self.user1}', f'<User {self.user1.username}>')

    def test_user_signup(self):
        self.assertEqual(self.user1.username, 'username_1')
        self.assertTrue(bcrypt.check_password_hash(
            self.user1.password, 'user1password'))
        self.assertEqual(self.user1.email, 'email1@gmail.com')
        self.assertEqual(self.user1.image_url,
                         "/static/images/default_prof_pic.png")

    def test_user_authenticate(self):
        username = self.user1.username
        good_password = 'user1password'
        bad_password = 'user2password'
        self.assertEqual(User.authenticate(
            username=username, password=good_password), self.user1)
        self.assertFalse(User.authenticate(
            username=username, password=bad_password))
