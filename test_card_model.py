from app import app
import os
from unittest import TestCase
import requests

from models import db, User, Card, Bookmark
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


class CardModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        Bookmark.query.delete()
        Card.query.delete()
        db.create_all()

        self.client = app.test_client()

        self.resp = requests.get('http://api.magicthegathering.io/v1/cards', {
            'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6",
            'page': 1
        }).json()

        self.cards = self.resp['cards']

        Card.create_all_cards(self.cards)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_card_model(self):
        """Test that basic card model works"""
        card = Card.query.filter(Card.name == 'Abundance').first()
        self.assertEqual(card.name, 'Abundance')
        print(card.name)

    def test_create_all_cards(self):
        for page in range(2, 11):
            """Test that create_all_cards method works correctly"""
            resp = requests.get('http://api.magicthegathering.io/v1/cards', {
                'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6",
                'page': page
            }).json()
            cards = resp['cards']
            Card.create_all_cards(cards)

        self.assertEqual(len(Card.query.all()), 1000)
