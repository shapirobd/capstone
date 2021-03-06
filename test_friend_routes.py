from app import app, CURR_USER_KEY
import os
from unittest import TestCase
from users import do_logout
from models import db, User, Friendship


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


class FriendRoutesTestCase(TestCase):
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

    def test_add_friend(self):
        """Test that route for adding a friend works"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username
            resp = c.post('/add_friend/username_2', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            # self.assertIn(self.user2, self.user1.friends)
            self.assertEqual(len(Friendship.query.all()), 1)
            self.assertEqual(len(Friendship.query.filter(
                Friendship.user1_username == 'username_2' or Friendship.user2_username == 'username_2').all()), 1)

    def test_show_friends(self):
        """Test that route for showing your friends works"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username
            c.post('/add_friend/username_1', follow_redirects=True)
            resp = c.get('/users/username_1/friends', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

    def test_remove_friend(self):
        """Test that route for removing a friend works"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username
            c.post('/add_friend/username_2')
            resp = c.post('/remove_friend/username_2', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
