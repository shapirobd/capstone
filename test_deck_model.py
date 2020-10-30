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
        # Deck.query.delete()
        # Bookmark.query.delete()
        User.query.delete()

        db.create_all()

        self.client = app.test_client()

        self.user = User.signup(email='email@gmail.com', password='userpassword', username='username',
                                image_url=None)

        self.deck = Deck(deck_name='Sample Deck',
                         deck_type='Standard', username=self.user.username)
        self.user.decks.append(self.deck)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_deck_model(self):
        """Test that basic deck model works"""
        print(self.deck.deck_name)
        self.assertEqual(self.deck.deck_name, 'Sample Deck')
        self.assertEqual(self.deck.deck_type, 'Standard')
        self.assertEqual(self.deck.username, 'username')
        self.assertIn(self.deck, self.user.decks)
