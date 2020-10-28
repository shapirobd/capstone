from app import app
import os
from unittest import TestCase
import requests

from models import db, User, Card, Bookmark, Deck, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


class DeckModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.create_all()

        self.client = app.test_client()

        self.user = User.signup(email='email@gmail.com', password='userpassword', username='username',
                                image_url=None)

        self.deck = Deck(deck_name='Sample Deck',
                         deck_type='Standard', username=self.user.username)

        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_deck_model(self):
        self.assertEqual(self.deck.deck_name, 'Sample Deck')
        self.assertEqual(self.deck.deck_type, 'Standard')
        self.assertEqual(self.deck.username, 'username')
