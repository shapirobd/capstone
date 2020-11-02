from app import app
import os
from unittest import TestCase
import requests

from models import db, User, Post, Deck, Bookmark

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


class PostModelTestCase(TestCase):
    """Test Post model"""

    def setUp(self):
        """Create test client, add sample data."""
        Deck.query.delete()
        Bookmark.query.delete()
        User.query.delete()

        db.create_all()

        self.client = app.test_client()

        self.user = User.signup(email='email@gmail.com', password='userpassword', username='username',
                                image_url=None)

        self.post = Post(username="username", title="Test Title",
                         content="This is test content for a post!")
        self.user.posts.append(self.post)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_post_model(self):
        """Test that basic post model works"""
        self.assertEqual(self.post.username, 'username')
        self.assertEqual(self.post.title, 'Test Title')
        self.assertEqual(self.post.content, 'This is test content for a post!')
        self.assertIn(self.post, self.user.posts)
