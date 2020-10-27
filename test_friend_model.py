from app import app
import os
from unittest import TestCase
import requests

from models import db, User, Friendship, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

os.environ['DATABASE_URL'] = "postgresql:///mtg_db_test"


class FriendModelTestCase(TestCase):
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
        self.friendship = Friendship(
            user1_username='username_1', user2_username='username_2')
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_friend_model(self):
        self.assertEqual(self.friendship.user1_username, 'username_1')
        self.assertEqual(self.friendship.user2_username, 'username_2')
